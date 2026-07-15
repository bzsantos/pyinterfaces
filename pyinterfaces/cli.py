import os
import json
import sys

def inicializar_projeto():
    print("\n🚀 Initializing pyinterfaces corporate environment...")
    
    pasta_vscode = ".vscode"
    arquivo_settings = os.path.join(pasta_vscode, "settings.json")
    
    configuracoes = {
        "python.analysis.diagnosticSeverityOverrides": {
            "reportUndefinedVariable": "none",
            "reportGeneralTypeIssues": "none",
            "reportMissingImports": "none"
        },
        "python.analysis.ignore": [
            "**/modules/**/*.py",
            "*.py"
        ]
    }
    
    try:
        if not os.path.exists(pasta_vscode):
            os.makedirs(pasta_vscode)
            print("📁 Folder '.vscode' created successfully.")
            
        with open(arquivo_settings, "w", encoding="utf-8") as f:
            json.dump(configuracoes, f, indent=4, ensure_ascii=False)
            
        # Cria as pastas estruturais de arquitetura do projeto
        for pasta in ["modules"]:
            if not os.path.exists(pasta):
                os.makedirs(pasta)
                print(f"📁 Folder '{pasta}' structured automatically.")
                
            arquivo_init = os.path.join(pasta, "__init__.py")
            if not os.path.exists(arquivo_init):
                with open(arquivo_init, "w", encoding="utf-8") as f:
                    f.write("# Global Modules Package\n")
                print(f"📄 File '{pasta}/__init__.py' generated to activate Import Hooks.")
                
        print("\n✨ Environment configured successfully! No yellow or red lines will bother you.")
        print("💡 Use 'python -m poetry run pyinterfaces-generate <name>' to create Spring MVC modules.\n")
        
    except Exception as e:
        print(f"❌ Error configuring environment: {e}")


def gerar_modulo():
    """
    Lê o argumento do terminal (ex: produto) e gera a estrutura Spring MVC.
    """
    # Garante que o usuário digitou o nome do módulo (ex: pyinterfaces-generate produto)
    if len(sys.argv) < 2:
        print("\n❌ Error: Missing module name!")
        print("💡 Usage: python -m poetry run pyinterfaces-generate <module_name>\n")
        return

    nome_cru = sys.argv[1].lower().strip()
    nome_capitalizado = nome_cru.capitalize()
    
    base_dir = os.path.join("modules", nome_cru)
    views_dir = os.path.join(base_dir, "views")
    
    print(f"\n🍃 Generating Spring MVC Module: '{nome_cru}'...")
    
    # 1. Cria a árvore de diretórios
    try:
        os.makedirs(views_dir, exist_ok=True)
        print(f"📁 Structured folders for 'modules/{nome_cru}/views/'")
    except Exception as e:
        print(f"❌ Error creating folders: {e}")
        return

    # 2. Definição dos templates de código
    templates = {
        "__init__.py": f"# Module {nome_capitalizado}\n",
        
        "interfaces.py": f"""# -*- coding: py_interface -*-

Interface {nome_capitalizado}Repository:
    def buscar_por_id(id_registro: str) -> dict
    def salvar(dados: dict) -> bool
""",

        "repository.py": f"""from modules.{nome_cru}.interfaces import {nome_capitalizado}Repository

class {nome_capitalizado}RepositoryImpl({nome_capitalizado}Repository):
    def buscar_por_id(self, id_registro: str) -> dict:
        print(f"💾 [Repository] Fetching {nome_cru} data (ID: {{id_registro}}) from DB...")
        return {{"id": id_registro, "status": "active_loaded"}}

    def salvar(self, dados: dict) -> bool:
        print(f"💾 [Repository] Changes for {nome_cru} saved to DB successfully.")
        return True
""",

        "service.py": f"""from modules.{nome_cru}.interfaces import {nome_capitalizado}Repository

class {nome_capitalizado}Service:
    def __init__(self, repository: {nome_capitalizado}Repository):
        self.repository = repository

    def process_flow(self, id_registro: str) -> dict:
        print(f"⚙️ [Service] Executing business logic for {nome_cru}...")
        data = self.repository.buscar_por_id(id_registro)
        
        # Add your business validations here
        
        self.repository.salvar(data)
        return data
""",

        "controller.py": f"""import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from modules.{nome_cru}.service import {nome_capitalizado}Service

router = APIRouter(prefix="/{nome_cru}s")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "views"))

class {nome_capitalizado}Controller:
    def __init__(self, service: {nome_capitalizado}Service):
        self.service = service

    @router.get("/dashboard", response_class=HTMLResponse)
    def render_page(self, request: Request):
        print(f"📥 [Web/MVC] User accessed web dashboard for {nome_cru}")
        result_data = self.service.process_flow("AUTO-GENERATED-ID")
        
        return templates.TemplateResponse(
            "index.html", 
            {{"request": request, "data": result_data}}
        )
"""
    }

    # Template especial para a View (HTML / Thymeleaf style)
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Management of {nome_capitalizado}</title>
</head>
<body style="font-family: sans-serif; background-color: #f4f4f9; padding: 40px;">
    <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h1 style="color: #4caf50;">🍃 Spring MVC System: {nome_capitalizado}</h1>
        <hr>
        <p><strong>Current Status:</strong> <span style="background: #e8f5e9; color: #2e7d32; padding: 4px 8px; border-radius: 4px;">{{{{ data.status }}}}</span></p>
        <p><strong>Generated Record ID:</strong> {{{{ data.id }}}}</p>
    </div>
</body>
</html>
"""

    # 3. Escreve as camadas do servidor (.py)
    for arquivo, conteudo in templates.items():
        caminho_final = os.path.join(base_dir, arquivo)
        with open(caminho_final, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"📄 Generated layer: {caminho_final}")

    # 4. Escreve a camada visual (index.html)
    caminho_html = os.path.join(views_dir, "index.html")
    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"🌐 Generated web view: {caminho_html}")
    
    print(f"\n✨ Module '{nome_cru}' successfully generated in 5 layers! Spring MVC style inside Python. 🚀\n")
