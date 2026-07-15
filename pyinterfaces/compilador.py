import codecs
import io
import re

def traduzir_sintaxe_java(texto: str) -> str:
    """
    Varre o arquivo de texto substituindo a sintaxe 'Interface Nome { ... }'
    por classes Python puras usando abc.ABC e @abstractmethod.
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
            
            # 3. Limpa pontos e vírgulas do estilo Java e captura o método
            metodo_limpo = linha.strip().replace(';', '')
            if metodo_limpo:
                # Transforma a assinatura em um método abstrato Python
                resultado.append(f"    @abstractmethod")
                resultado.append(f"    def {metodo_limpo}:")
                resultado.append(f"        pass")
        else:
            # Mantém qualquer outra linha de código Python normal intacta
            resultado.append(linha)
            
    return '\n'.join(resultado)

# --- INFRAESTRUTURA DE CODEC DO PYTHON (ATUALIZADA) ---

class JavaInterfaceDecoder(codecs.BufferedIncrementalDecoder):
    def _buffer_decode(self, input, errors, final):
        if final:
            # CORREÇÃO: Força a conversão para bytes caso o Python envie um memoryview
            dados_em_bytes = bytes(input)
            texto_traduzido = traduzir_sintaxe_java(dados_em_bytes.decode('utf-8'))
            return (texto_traduzido, len(input))
        return ('', 0)

def buscar_codec(nome_codec):
    if nome_codec == 'py_interface':
        return codecs.CodecInfo(
            name='py_interface',
            encode=codecs.utf_8_encode,
            # CORREÇÃO: Aplicamos o cast de bytes(input) também na leitura direta do decode
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
