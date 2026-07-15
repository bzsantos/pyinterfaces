"""
pyinterfaces - Java-style interfaces for Python.

Co-conceptualized and inspired by Leandro Reginaldo.
Maintained by Bruno Zolotareff.
"""


from .compilador import registrar_syntax

# Ativa o mecanismo de codec assim que a biblioteca é importada
registrar_syntax()