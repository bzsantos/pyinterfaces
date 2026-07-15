from pyinterfaces.compilador import traduzir_sintaxe_java

def test_deve_traduzir_interface_com_def_e_tipos_pythonicos():
    # Testa a nova sintaxe limpa, usando 'def' e tipos nativos
    codigo_entrada = """
    Interface Conta:
        def abrir(self, titular: str, saldo_inicial: float) -> bool
    """
    
    codigo_traduzido = traduzir_sintaxe_java(codigo_entrada)
    
    # Valida se o compilador inseriu a classe abstrata e o decorador corretamente
    assert "class Conta(ABC):" in codigo_traduzido
    assert "@abstractmethod" in codigo_traduzido
    assert "def abrir(self, titular: str, saldo_inicial: float) -> bool:" in codigo_traduzido


def test_deve_injetar_self_e_dois_pontos_automaticamente():
    # Testa se o motor injeta 'self' e os ':' no final se o desenvolvedor esquecer
    codigo_entrada = """
    Interface Banco:
        def conectar(servidor: str, porta: int)
    """
    
    codigo_traduzido = traduzir_sintaxe_java(codigo_entrada)
    
    # Garante que o método foi mapeado corrigindo a falta de 'self' e ':'
    assert "class Banco(ABC):" in codigo_traduzido
    assert "@abstractmethod" in codigo_traduzido
    assert "def conectar(self, servidor: str, porta: int):" in codigo_traduzido
