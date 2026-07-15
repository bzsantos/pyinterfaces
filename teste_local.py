# -*- coding: py_interface -*-

Interface AbrirConta:
    def abrir(titular: str, saldo_inicial: float)
    def fechar() -> bool

class ContaCorrente(AbrirConta):
    def abrir(self, titular: str, saldo_inicial: float):
        print(f"Sucesso! Conta do {titular} aberta com R${saldo_inicial}.")
        
    def fechar(self) -> bool:
        print("Conta fechada.")
        return True

# Execução do teste manual
conta = ContaCorrente()
conta.abrir("Bruno", 1000.0)
conta.fechar()
