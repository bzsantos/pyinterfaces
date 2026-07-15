# -*- coding: py_interface -*-

Interface AbrirConta:
    void abrir(String titular, double saldoInicial)
    boolean fechar()

class ContaCorrente(AbrirConta):
    def abrir(self, titular: str, saldoInicial: float):
        print(f"Sucesso! Conta do {titular} aberta com R${saldoInicial}.")
        
    def fechar(self) -> bool:
        print("Conta fechada.")
        return True

conta = ContaCorrente()
conta.abrir("Bruno", 1000.0)
conta.fechar()
