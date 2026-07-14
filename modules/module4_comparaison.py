"""
Module 4 : Comparaison structurelle (Diff AST)

Rôle :
Comparer les deux AST et produire un diagnostic technique
structuré destiné au LLM.

Aucun texte utilisateur n'est généré ici.
"""


def compare_asts(ast_a: dict, ast_b: dict) -> dict:

    elems_a = ast_a["elements"]
    elems_b = ast_b["elements"]

    funcs_a = set(elems_a["functions"])
    funcs_b = set(elems_b["functions"])

    added_functions = sorted(list(funcs_b - funcs_a))
    removed_functions = sorted(list(funcs_a - funcs_b))
    common_functions = sorted(list(funcs_a & funcs_b))

    modified_parameters = {}

    for func in common_functions:

        params_a = elems_a["parameters"].get(func, [])
        params_b = elems_b["parameters"].get(func, [])

        if params_a != params_b:

            modified_parameters[func] = {
                "before": params_a,
                "after": params_b
            }

    broken_calls = []

    all_calls = elems_a["calls"] + elems_b["calls"]

    for call in all_calls:

        called = call["name"].split(".")[0]

        if called in removed_functions:

            broken_calls.append({
                "function": called,
                "location": call.get("location")
            })

    diagnostic = {

        "summary": {

            "added_functions": added_functions,

            "removed_functions": removed_functions,

            "modified_functions": common_functions,

            "parameter_changes": modified_parameters,

            "broken_calls": broken_calls

        },

        "metrics": {

            "added": len(added_functions),

            "removed": len(removed_functions),

            "parameter_changes": len(modified_parameters),

            "broken_calls": len(broken_calls)

        }

    }

    return diagnostic