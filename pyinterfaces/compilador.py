import codecs
import io
import re

def traduzir_sintaxe_java(texto: str) -> str:
    """
    Substitui 'Interface Nome:' por 'class Nome(ABC):' e adiciona 
    @abstractmethod em todos os métodos que começam com 'def'.
    """
    linhas = texto.split('\n')
    resultado = ["from abc import ABC, abstractmethod\n"]
    dentro_da_interface = False
    
    for linha in linhas:
        # 1. Detecta o início da declaração: 'Interface Nome:' (com ou sem espaços)
        inicio_match = re.match(r'\s*Interface\s+(\w+)\s*:', linha)
        if inicio_match:
            nome_interface = inicio_match.group(1)
            resultado.append(f"class {nome_interface}(ABC):")
            dentro_da_interface = True
            continue
            
        # Detecta se o bloco da interface acabou (linha sem espaços na esquerda)
        if dentro_da_interface and linha.strip() and not linha.startswith(' '):
            dentro_da_interface = False

        if dentro_da_interface:
            linha_limpa = linha.strip()
            # 2. Captura métodos que começam com 'def' dentro da interface
            if linha_limpa.startswith('def '):
                # Garante que o método termine com ':' esperado pelo Python
                if not linha_limpa.endswith(':'):
                    linha_limpa += ':'
                
                # Injeta o 'self' automaticamente caso o usuário não tenha colocado
                if '(self' not in linha_limpa:
                    linha_limpa = linha_limpa.replace('(', '(self, ').replace('(self, )', '(self)')
                
                resultado.append(f"    @abstractmethod")
                resultado.append(f"    {linha_limpa}")
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
