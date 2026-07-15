import codecs
import io
import re
import sys
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec

def traduzir_sintaxe_java(texto: str) -> str:
    """
    Substitui 'Interface Nome:' por 'class Nome(ABC):' e adiciona 
    @abstractmethod em todos os métodos que começam com 'def'.
    """
    linhas = texto.split('\n')
    resultado = ["from abc import ABC, abstractmethod\n"]
    dentro_da_interface = False
    
    for linha in linhas:
        inicio_match = re.match(r'\s*Interface\s+(\w+)\s*:', linha)
        if inicio_match:
            nome_interface = inicio_match.group(1)
            resultado.append(f"class {nome_interface}(ABC):")
            dentro_da_interface = True
            continue
            
        if dentro_da_interface and linha.strip() and not linha.startswith(' '):
            dentro_da_interface = False

        if dentro_da_interface:
            linha_limpa = linha.strip()
            if linha_limpa.startswith('def '):
                if not linha_limpa.endswith(':'):
                    linha_limpa += ':'
                if '(self' not in linha_limpa:
                    linha_limpa = linha_limpa.replace('(', '(self, ').replace('(self, )', '(self)')
                
                resultado.append(f"    @abstractmethod")
                resultado.append(f"    {linha_limpa}")
                resultado.append(f"        pass")
        else:
            resultado.append(linha)
            
    return '\n'.join(resultado)

# --- SISTEMA DE IMPORTAÇÃO NATIVA DO PYTHON (GANCHO) ---

class InterfaceLoader(Loader):
    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        return None  # Usa o carregador padrão do Python para criar o módulo

    def exec_module(self, module):
        with open(self.filename, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Passa o código pelo nosso compilador antes de executar
        codigo_traduzido = traduzir_sintaxe_java(conteudo)
        code_obj = compile(codigo_traduzido, self.filename, 'exec')
        exec(code_obj, module.__dict__)

class InterfaceFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        # Transforma o nome do módulo em caminho (ex: interfaces.banco -> interfaces/banco.py)
        mod_name = fullname.split('.')[-1]
        
        # Caminhos possíveis para buscar o arquivo
        search_paths = path if path else sys.path
        import os
        
        for p in search_paths:
            base_path = os.path.join(p, mod_name)
            filename = base_path + ".py"
            
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    primeira_linha = f.readline()
                
                # Se o arquivo tiver o nosso cabeçalho mágico, nós assumimos o controle da compilação!
                if "py_interface" in primeira_linha:
                    return ModuleSpec(fullname, InterfaceLoader(filename), origin=filename)
        return None

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
    """Registra o tradutor de código no núcleo do Python e injeta o Import Hook"""
    codecs.register(buscar_codec)
    # Injeta o nosso buscador de arquivos customizados no topo do sistema do Python
    if not any(isinstance(f, InterfaceFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, InterfaceFinder())
