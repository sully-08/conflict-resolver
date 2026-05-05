"""
Module 3 : Analyse syntaxique (AST)
Rôle : Transformer chaque version du code en arbre de syntaxe abstraite via Tree-sitter
"""

import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# Initialisation du parseur Python
PY_LANGUAGE = Language(tspython.language())
_parser = Parser(PY_LANGUAGE)


def parse_code(code: str) -> dict:
    """
    Parse le code source et retourne l'AST avec les éléments clés extraits.
    Fonctionne même si le code est incomplet (robustesse Tree-sitter).
    """
    tree = _parser.parse(bytes(code, "utf8"))
    root = tree.root_node

    elements = _extract_elements(root, code)
    has_errors = root.has_error

    return {
        "tree": tree,
        "root": root,
        "elements": elements,
        "has_errors": has_errors,
        "code": code
    }


def _extract_elements(node, code: str) -> dict:
    """
    Parcourt l'AST et extrait les fonctions, paramètres et appels de fonctions.
    """
    elements = {
        "functions": [],      # définitions de fonctions
        "parameters": {},     # paramètres par fonction
        "calls": []           # appels de fonctions
    }
    _walk(node, code, elements, current_function=None)
    return elements


def _walk(node, code: str, elements: dict, current_function: str):
    """Parcours récursif de l'AST."""

    if node.type == "function_definition":
        # Récupère le nom de la fonction
        name_node = node.child_by_field_name("name")
        func_name = _node_text(name_node, code) if name_node else "anonyme"
        elements["functions"].append(func_name)

        # Récupère les paramètres
        params_node = node.child_by_field_name("parameters")
        params = []
        if params_node:
            for child in params_node.children:
                if child.type in ("identifier", "typed_parameter",
                                  "default_parameter", "typed_default_parameter"):
                    params.append(_node_text(child, code))
        elements["parameters"][func_name] = params
        current_function = func_name

    elif node.type == "call":
        func_node = node.child_by_field_name("function")
        if func_node:
            call_name = _node_text(func_node, code)
            # Récupère les arguments
            args_node = node.child_by_field_name("arguments")
            args = []
            if args_node:
                for child in args_node.children:
                    if child.type not in (",", "(", ")"):
                        args.append(_node_text(child, code))
            elements["calls"].append({
                "name": call_name,
                "args": args,
                "in_function": current_function
            })

    for child in node.children:
        _walk(child, code, elements, current_function)


def _node_text(node, code: str) -> str:
    """Extrait le texte brut d'un nœud AST."""
    if node is None:
        return ""
    return code[node.start_byte:node.end_byte]


def analyze_versions(code_a: str, code_b: str) -> tuple:
    """
    Analyse les deux versions et retourne (ast_a, ast_b).
    """
    ast_a = parse_code(code_a)
    ast_b = parse_code(code_b)

    print(f"[AST] Version A — fonctions: {ast_a['elements']['functions']} "
          f"| erreurs: {ast_a['has_errors']}")
    print(f"[AST] Version B — fonctions: {ast_b['elements']['functions']} "
          f"| erreurs: {ast_b['has_errors']}")
    return ast_a, ast_b
