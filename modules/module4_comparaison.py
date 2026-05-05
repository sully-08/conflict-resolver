"""
Module 4 : Comparaison structurelle
Rôle : Identifier les différences entre les deux AST (fonctions, paramètres, appels)
"""


def compare_asts(ast_a: dict, ast_b: dict) -> dict:
    """
    Compare les éléments extraits des deux AST.
    Retourne un rapport structuré des différences.
    """
    elems_a = ast_a["elements"]
    elems_b = ast_b["elements"]

    funcs_a = set(elems_a["functions"])
    funcs_b = set(elems_b["functions"])

    # 1. Fonctions modifiées / renommées
    added_functions   = list(funcs_b - funcs_a)   # nouvelles dans B
    removed_functions = list(funcs_a - funcs_b)   # absentes dans B
    common_functions  = list(funcs_a & funcs_b)

    # 2. Changements de paramètres sur les fonctions communes
    param_changes = {}
    for func in common_functions:
        params_a = elems_a["parameters"].get(func, [])
        params_b = elems_b["parameters"].get(func, [])
        if params_a != params_b:
            param_changes[func] = {
                "version_a": params_a,
                "version_b": params_b
            }

    # 3. Appels de fonctions potentiellement invalides
    # Un appel est "à risque" si le nom appelé a été supprimé dans B
    calls_at_risk = []
    all_calls = elems_a["calls"] + elems_b["calls"]
    for call in all_calls:
        called = call["name"].split(".")[0]  # ignore les méthodes chaînées
        if called in removed_functions or called in added_functions:
            calls_at_risk.append(call)

    # 4. Classification du type de conflit
    conflict_type = _classify_conflict(
        added_functions, removed_functions, param_changes, calls_at_risk
    )

    report = {
        "conflict_type": conflict_type,
        "added_functions": added_functions,
        "removed_functions": removed_functions,
        "common_functions": common_functions,
        "param_changes": param_changes,
        "calls_at_risk": calls_at_risk,
    }

    _print_report(report)
    return report


def _classify_conflict(added, removed, param_changes, calls_at_risk) -> str:
    """Détermine le type de conflit dominant."""
    if removed and calls_at_risk:
        return "STRUCTUREL_RENOMMAGE"
    if param_changes:
        return "SEMANTIQUE_SIGNATURE"
    if not added and not removed and not param_changes:
        return "INTRA_METHODE"
    return "MIXTE"


def _print_report(report: dict):
    print(f"[COMPARAISON] Type de conflit : {report['conflict_type']}")
    if report["added_functions"]:
        print(f"  + Fonctions ajoutées dans B  : {report['added_functions']}")
    if report["removed_functions"]:
        print(f"  - Fonctions absentes dans B  : {report['removed_functions']}")
    if report["param_changes"]:
        for fn, ch in report["param_changes"].items():
            print(f"  ~ Paramètres modifiés [{fn}] : A={ch['version_a']} → B={ch['version_b']}")
    if report["calls_at_risk"]:
        risky = [c["name"] for c in report["calls_at_risk"]]
        print(f"  ! Appels à risque            : {risky}")
