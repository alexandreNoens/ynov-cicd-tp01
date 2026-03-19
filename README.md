# ynov-cicd-tp01

## Prérequis

- Python 3.11+
- `uv`

## Étapes

### 1) Installation du projet

```bash
make install
```

Crée l'environnement virtuel si besoin, génère le lock des dépendances avec hashes, puis installe les dépendances.

### 2) Initialiser la base de données (reset)

```bash
make install-db
```

Supprime et recrée la base SQLite, puis charge le schéma et les données de dev.

### 3) Lancer l'application

```bash
make serve
```

Lance l'API FastAPI en local avec rechargement automatique.

Swagger UI : http://127.0.0.1:8000/docs

ReDoc : http://127.0.0.1:8000/redoc

### 4) Lancer les tests

```bash
make check
```

Exécute les tests avec `pytest`.

### 5) Lancer le linter

```bash
make lint
```

Exécute le lint avec `ruff`.