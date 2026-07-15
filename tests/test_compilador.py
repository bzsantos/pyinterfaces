from pyinterfaces.compilador import traduzir_sintaxe_java

def test_deve_traduzir_interface_simples_para_classe_abc():
    # Código simulado que o usuário escreveria
    codigo_entrada = """
    Interface Conta {
        abrir(self)
    }
    """
    
    codigo_traduzido = traduzir_sintaxe_java(codigo_entrada)
    
    # Valida se o compilador inseriu as tags do Python corretamente
    assert "class Conta(ABC):" in codigo_traduzido
    assert "@abstractmethod" in codigo_traduzido
    assert "def abrir(self):" in codigo_traduzido


def test_deve_remover_pontos_e_virgulas_estilo_java():
    codigo_entrada = """
    Interface Banco {
        conectar(self);
        desconectar(self);
    }
    """
    
    codigo_traduzido = traduzir_sintaxe_java(codigo_entrada)
    
    # Garante que o ponto e vírgula sumiu para o Python não quebrar
    assert ";" not in codigo_traduzido
    assert "def conectar(self):" in codigo_traduzido
