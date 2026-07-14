"""
Module 6 : Préparation du diagnostic pour le LLM

Rôle :
Construire un diagnostic technique structuré qui sera transmis
au modèle Gemini. Aucun texte destiné au développeur n'est
généré ici.
"""


def build_resolution_context(comparison_report: dict, explanation: str) -> dict:
    """
    Construit le contexte technique qui sera envoyé à Gemini.
    """

    context = {
        "conflict_type": comparison_report.get("conflict_type"),

        "analysis": explanation,

        "modified_functions": comparison_report.get(
            "modified_functions", []
        ),

        "removed_functions": comparison_report.get(
            "removed_functions", []
        ),

        "added_functions": comparison_report.get(
            "added_functions", []
        ),

        "parameter_changes": comparison_report.get(
            "param_changes", {}
        ),

        "calls_at_risk": comparison_report.get(
            "calls_at_risk", []
        ),

        "details": _build_details(comparison_report)
    }

    return context


def _build_details(report: dict) -> dict:
    """
    Extrait uniquement les informations utiles au LLM.
    """

    return {
        "removed_functions": report.get("removed_functions", []),
        "added_functions": report.get("added_functions", []),
        "parameter_changes": report.get("param_changes", {}),
        "calls_at_risk": report.get("calls_at_risk", [])
    }