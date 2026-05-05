# Système d'aide à la résolution des conflits de fusion Git

Système automatisé de détection, analyse et résolution des conflits de fusion Git,
basé sur l'analyse syntaxique (AST) et un modèle de langage (Gemini).

## Architecture

```
conflict-resolver/
├── modules/          ← Les 6 modules du pipeline
├── tests/            ← Tests unitaires par module
├── main.py           ← Point d'entrée (local + GitHub Actions)
├── tests_scenarios.py← Tests des 3 scénarios complets
└── requirements.txt  ← Dépendances Python
```

## Pipeline (6 modules)

| Module | Rôle |
|--------|------|
| Module 1 — Détection | Identifie les marqueurs Git `<<<<<<<` |
| Module 2 — Extraction | Isole les versions A et B |
| Module 3 — AST | Génère les arbres syntaxiques via Tree-sitter |
| Module 4 — Comparaison | Détecte les différences structurelles |
| Module 5 — Explication | Génère une explication via Gemini |
| Module 6 — Résolution | Propose un guide de résolution |

## Installation

```bash
git clone https://github.com/ton-user/conflict-resolver.git
cd conflict-resolver
pip install -r requirements.txt
```

## Utilisation locale

```bash
python main.py
```

## Tests unitaires

```bash
# Tester un module spécifique
python tests/test_module1.py

# Tester les 3 scénarios complets
python tests_scenarios.py
```

## Intégration GitHub Actions

Le workflow se déclenche automatiquement sur chaque Pull Request.
Il analyse les fichiers en conflit et publie un commentaire dans la PR
avec l'explication et le guide de résolution.

### Configuration requise

Ajouter la clé API Gemini dans les secrets du dépôt :
1. Aller dans **Settings → Secrets and variables → Actions**
2. Cliquer **New repository secret**
3. Nom : `GEMINI_API_KEY`
4. Valeur : ta clé API Gemini

## Types de conflits détectés

- **INTRA_METHODE** — Deux modifications dans la même fonction
- **STRUCTUREL_RENOMMAGE** — Une fonction renommée avec des appels obsolètes
- **SEMANTIQUE_SIGNATURE** — Changement de paramètres d'une fonction
- **MIXTE** — Combinaison de plusieurs types
