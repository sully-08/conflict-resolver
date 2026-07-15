"""
Module 5 : Génération du rapport de résolution avec Gemini

Rôle :
Recevoir le diagnostic technique produit par les modules Python
et demander à Gemini de rédiger le rapport final destiné au
développeur.

Aucun texte utilisateur n'est généré par Python.
"""

import json
import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

_client = genai.Client(api_key=GEMINI_API_KEY)


def build_prompt(code_a: str, code_b: str, comparison_report: dict) -> str:
    """
    Construit le prompt destiné à Gemini.
    Python fournit uniquement un diagnostic structuré.
    """

    diagnostic = {
        "conflict_type": comparison_report.get("conflict_type"),
        "modified_functions": comparison_report.get("modified_functions", []),
        "removed_functions": comparison_report.get("removed_functions", []),
        "added_functions": comparison_report.get("added_functions", []),
        "parameter_changes": comparison_report.get("param_changes", {}),
        "calls_at_risk": comparison_report.get("calls_at_risk", [])
    }

    return f"""
Tu es un expert Git et développement collaboratif.

Tu assistes un développeur confronté à un conflit de fusion.

Voici le diagnostic technique produit automatiquement par le système.

CODE VERSION A
--------------
{code_a}

CODE VERSION B
--------------
{code_b}

DIAGNOSTIC
----------
{json.dumps(diagnostic, indent=2, ensure_ascii=False)}

Ta mission est de rédiger directement le rapport qui sera publié
dans une Pull Request GitHub.

Le rapport doit être entièrement rédigé en langage naturel.

Il doit contenir uniquement les sections suivantes :

------- Rapport d'assistance à la résolution -------

------- Résumé -------

Résume en quelques phrases la nature du conflit.

------- Analyse -------

Explique ce qui différencie les deux versions et pourquoi Git ne
peut pas résoudre automatiquement ce conflit.

------- Risques -------

Présente les conséquences possibles si une mauvaise résolution est
effectuée.

## Recommandations

Donne un guide de résolution clair, concret et adapté au conflit
détecté.

Consignes importantes :

- Ne parle jamais d'AST.
- Ne parle jamais de Tree-sitter.
- Ne parle jamais du pipeline interne.
- Ne parle jamais des modules.
- Ne fais aucune référence au fonctionnement du système.
- Ne reproduis pas le JSON.
- Ne fais aucune formule de politesse.
- Utilise un ton professionnel destiné à un développeur.
"""


def generate_resolution_report(
    code_a: str,
    code_b: str,
    comparison_report: dict
) -> str:
    """
    Génère le rapport final destiné au développeur.
    """

    prompt = build_prompt(
        code_a,
        code_b,
        comparison_report
    )

    response = _client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    return response.text