from pyinterfaces.compilador import traduzir_sintaxe_java

def test_deve_traduzir_interface_com_dois_pontos_e_indentacao():
    # Testa a nova sintaxe limpa sem chaves
    codigo_entrada = """
    Interface Conta:
        abrir(self)
    """
    
    codigo_traduzido = traduzir_sintaxe_java(codigo_entrada)
    
    # Valida se o compilador inseriu as estruturas do Python corretamente
    assert "class Conta(ABC):" in codigo_traduzido
    assert "@abstractmethod" in codigo_traduzido
    assert "def abrir(self):" in codigo_traduzido


def test_deve_traduzir_tipos_estritos_do_java_nos_argumentos():
    # Testa se o motor converte 'String titular' para 'titular: str' e ignora o 'void'
    codigo_entrada = """
    Interface Banco:
        void conectar(String servidor, int porta)
    """
    
    codigo_traduzido = traduzir_sintaxe_java(codigo_entrada)
    
    # Garante que o método foi mapeado com a tipagem correta do Python
    assert "class Banco(ABC):" in codigo_traduzido
    assert "@abstractmethod" in codigo_traduzido
    assert "def conectar(self, servidor: str, porta: int):" in codigo_traduzido
