"""
Module 5 : Explication en langage naturel
Rôle : Envoyer le diagnostic à Gemini et retourner une explication du conflit

Installation :
    pip install google-genai
"""

import json
from google import genai

# ── Configuration ─────────────────────────────────────────────────
GEMINI_API_KEY = "AIzaSyCvU08W2US7-C9GNd3d1yUuY0HouFAPCdo"
#utilisation de la derniere version de Gemini
GEMINI_MODEL   = "gemini-2.5-flash"

_client = genai.Client(api_key=GEMINI_API_KEY)


def build_prompt(code_a: str, code_b: str, comparison_report: dict) -> str:
    """Construit le prompt envoyé à Gemini."""
    conflict_type = comparison_report.get("conflict_type", "INCONNU")
    param_changes = comparison_report.get("param_changes", {})
    removed_funcs = comparison_report.get("removed_functions", [])
    added_funcs   = comparison_report.get("added_functions", [])
    calls_at_risk = [c["name"] for c in comparison_report.get("calls_at_risk", [])]

    return f"""Tu es un assistant expert en développement logiciel collaboratif.
Analyse ce conflit de fusion Git et explique-le de manière claire et concise.

=== VERSION A (branche locale) ===
{code_a}

=== VERSION B (branche distante) ===
{code_b}

=== DIAGNOSTIC STRUCTUREL ===
- Type de conflit détecté : {conflict_type}
- Fonctions supprimées/renommées : {removed_funcs}
- Fonctions ajoutées : {added_funcs}
- Changements de paramètres : {json.dumps(param_changes, ensure_ascii=False)}
- Appels de fonctions à risque : {calls_at_risk}

Génère une explication structurée avec exactement ces trois sections :
1. NATURE DU CONFLIT : En une ou deux phrases, décris ce qui s'est passé.
2. DIFFÉRENCES OBSERVÉES : Liste les différences concrètes entre A et B.
3. RISQUES POTENTIELS : Quels problèmes ce conflit peut-il causer si mal résolu ?

Sois direct et technique. Pas de formules de politesse."""


def explain_conflict(code_a: str, code_b: str, comparison_report: dict) -> str:
    """Envoie le prompt à Gemini et retourne l'explication."""
    prompt = build_prompt(code_a, code_b, comparison_report)

    try:
        response = _client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        explanation = response.text
        print("[EXPLICATION]  Explication générée par Gemini")
        return explanation

    except Exception as e:
        print(f"[EXPLICATION] Erreur Gemini ({e}), fallback utilisé")
        return _fallback_explanation(comparison_report)


def _fallback_explanation(report: dict) -> str:
    """Explication statique si l'API est inaccessible."""
    t = report.get("conflict_type", "INCONNU")
    lines = [
        "1. NATURE DU CONFLIT :",
        f"   Type identifié : {t}",
        "",
        "2. DIFFÉRENCES OBSERVÉES :",
    ]
    if report.get("removed_functions"):
        lines.append(f"   - Fonctions absentes dans B : {report['removed_functions']}")
    if report.get("added_functions"):
        lines.append(f"   - Fonctions ajoutées dans B : {report['added_functions']}")
    if report.get("param_changes"):
        for fn, ch in report["param_changes"].items():
            lines.append(
                f"   - Paramètres de '{fn}' modifiés : "
                f"{ch['version_a']} → {ch['version_b']}"
            )
    lines += [
        "",
        "3. RISQUES POTENTIELS :",
        "   - Erreur de compilation si les appels ne correspondent plus aux signatures.",
        "   - Bug silencieux si Git fusionne sans conflit textuel.",
    ]
    return "\n".join(lines)