import codecs
import io
import re

def converter_tipos_java_para_python(argumentos_str: str) -> str:
    """
    Transforma 'String titular, int idade' em 'titular: str, idade: int'.
    Também garante que o 'self' seja mantido corretamente se o usuário colocar.
    """
    mapa_tipos = {
        'String': 'str',
        'int': 'int',
        'double': 'float',
        'float': 'float',
        'boolean': 'bool',
        'void': 'None',
        'List': 'list',
        'Map': 'dict'
    }
    
    argumentos_limpos = argumentos_str.strip()
    if not argumentos_limpos:
        return "self"
        
    partes = [p.strip() for p in argumentos_limpos.split(',')]
    novos_args = []
    
    # CORREÇÃO AQUI: Verificamos se 'self' está contido na lista de partes
    if len(partes) > 0 and partes[0] == 'self':
        novos_args.append('self')
        partes = partes[1:]
    else:
        # Injeta o 'self' automaticamente (padrão Java puro)
        novos_args.append('self')
        
    for parte in partes:
        if not parte:
            continue
        componentes = re.split(r'\s+', parte)
        if len(componentes) == 2:
            tipo_java, nome_var = componentes
            tipo_python = mapa_tipos.get(tipo_java, tipo_java)
            novos_args.append(f"{nome_var}: {tipo_python}")
        else:
            novos_args.append(parte)
            
    return ", ".join(novos_args)

def traduzir_sintaxe_java(texto: str) -> str:
    """
    Varre o arquivo de texto substituindo a sintaxe 'Interface Nome { ... }'
    por classes Python puras usando abc.ABC, tipagem estrita e @abstractmethod.
    """
    linhas = texto.split('\n')
    resultado = ["from abc import ABC, abstractmethod\n"]
    dentro_da_interface = False
    
    for linha in linhas:
        # 1. Detecta o início da declaração: 'Interface Nome {'
        inicio_match = re.match(r'\s*Interface\s+(\w+)\s*\{', linha)
        if inicio_match:
            nome_interface = inicio_match.group(1)
            resultado.append(f"class {nome_interface}(ABC):")
            dentro_da_interface = True
            continue
            
        if dentro_da_interface:
            # 2. Detecta o fechamento da interface com a chave '}'
            if '}' in linha:
                dentro_da_interface = False
                continue
            
            # 3. Captura o método com padrão Java: TipoRetorno nomeMetodo(Argumentos)
            linha_limpa = linha.strip().replace(';', '')
            if linha_limpa:
                metodo_match = re.match(r'(?:\w+\s+)?(\w+)\s*\((.*?)\)', linha_limpa)
                if metodo_match:
                    nome_metodo = metodo_match.group(1)
                    args_brutos = metodo_match.group(2)
                    
                    args_traduzidos = converter_tipos_java_para_python(args_brutos)
                    
                    resultado.append(f"    @abstractmethod")
                    resultado.append(f"    def {nome_metodo}({args_traduzidos}):")
                    resultado.append(f"        pass")
        else:
            resultado.append(linha)
            
    return '\n'.join(resultado)

# --- INFRAESTRUTURA DE CODEC DO PYTHON ---

class JavaInterfaceDecoder(codecs.BufferedIncrementalDecoder):
    def _buffer_decode(self, input, errors, final):
        if final:
            dados_em_bytes = bytes(input)
            texto_traduzido = traduzir_sintaxe_java(dados_em_bytes.decode('utf-8'))
            return (texto_traduzido, len(input))
        return ('', 0)

def buscar_codec(nome_codec):
    if nome_codec == 'py_interface':
        return codecs.CodecInfo(
            name='py_interface',
            encode=codecs.utf_8_encode,
            decode=lambda input, errors='strict': (traduzir_sintaxe_java(bytes(input).decode('utf-8')), len(input)),
            incrementalencoder=codecs.utf_8_encode,
            incrementaldecoder=JavaInterfaceDecoder,
            streamreader=lambda stream, errors='strict': io.StringIO(traduzir_sintaxe_java(stream.read().decode('utf-8'))),
            streamwriter=codecs.utf_8_encode
        )
    return None

def registrar_syntax():
    """Registra o tradutor de código dentro do núcleo de encodings do Python"""
    codecs.register(buscar_codec)
