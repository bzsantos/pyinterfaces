import os
import json

def inicializar_projeto():
    print("\n🚀 Inicializando ambiente pyinterfaces...")
    
    pasta_vscode = ".vscode"
    arquivo_settings = os.path.join(pasta_vscode, "settings.json")
    
    configuracoes = {
        "python.analysis.diagnosticSeverityOverrides": {
            "reportUndefinedVariable": "none",
            "reportGeneralTypeIssues": "none",
            "reportMissingImports": "none"
        },
        "python.analysis.ignore": [
            "**/models/*.py",
            "**/interfaces/*.py",
            "*.py"
        ]
    }
    
    try:
        if not os.path.exists(pasta_vscode):
            os.makedirs(pasta_vscode)
            print("📁 Pasta '.vscode' criada com sucesso.")
            
        with open(arquivo_settings, "w", encoding="utf-8") as f:
            json.dump(configuracoes, f, indent=4, ensure_ascii=False)
            
        # Cria as pastas padrões e injeta o __init__.py automaticamente!
        for pasta in ["models", "interfaces"]:
            if not os.path.exists(pasta):
                os.makedirs(pasta)
                print(f"📁 Pasta '{pasta}' estruturada automaticamente.")
            
            # CRIAÇÃO DO __INIT__.PY AUTOMÁTICO
            arquivo_init = os.path.join(pasta, "__init__.py")
            if not os.path.exists(arquivo_init):
                with open(arquivo_init, "w", encoding="utf-8") as f:
                    f.write(f"# Pacote de {pasta.capitalize()} do pyinterfaces\n")
                print(f"📄 Arquivo '{pasta}/__init__.py' gerado para ativar o Import Hook.")
                
        print("\n✨ Ambiente configurado com 100% de sucesso! Nenhuma linha amarela ou vermelha vai te incomodar.")
        print("💡 Lembre-se de colocar '# -*- coding: py_interface -*-' no topo das suas interfaces.\n")
        
    except Exception as e:
        print(f"❌ Erro ao configurar o ambiente: {e}")
