# -*- coding: py_interface -*-

Interface AbrirConta {
    abrir(self, titular)
    fechar(self)
}

class ContaCorrente(AbrirConta):
    def abrir(self, titular):
        print(f"Sucesso! Conta do {titular} aberta usando a sintaxe com Interface.")
        
    def fechar(self):
        print("Conta fechada.")

# Execução
conta = ContaCorrente()
conta.abrir("Bruno")
