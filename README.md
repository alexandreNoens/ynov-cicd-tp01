# ynov-cicd-tp01

## Étapes

### 1) Installation du projet

```bash
make install
```

Crée l'environnement virtuel si besoin, génère le lock des dépendances avec hashes, puis installe les dépendances.

### 2) Lancer l'application

```bash
make serve
```

Lance l'API FastAPI en local avec rechargement automatique.

### 3) Lancer les tests

```bash
make check
```

Exécute les tests avec `pytest`.

### 4) Lancer le linter

```bash
make lint
```

Exécute le lint avec `ruff`.