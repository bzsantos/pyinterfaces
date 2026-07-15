# -*- coding: py_interface -*-

Interface AbrirConta {
    void abrir(String titular, double saldoInicial);
    boolean fechar();
}

class ContaCorrente(AbrirConta):
    def abrir(self, titular: str, saldoInicial: float):
        print(f"Conta Java aberta para {titular} com saldo de R${saldoInicial}")
        
    def fechar(self) -> bool:
        print("Conta encerrada.")
        return True

# Execução que gera o texto no terminal
conta = ContaCorrente()
conta.abrir("Leandro Reginaldo", 5000.0)
conta.fechar()
