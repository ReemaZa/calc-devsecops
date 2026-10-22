# Calculatrice scientifique DevSecOps (TP2)
## Intégration de la Sécurité dans un Pipeline CI/CD



[![CI-DevSecOps](https://github.com/ReemaZa/calc-devsecops/actions/workflows/ci.yml/badge.svg)](https://github.com/ReemaZa/calc-devsecops/actions/workflows/ci.yml)

Calculatrice web (Flask) servant à illustrer l'**intégration de la sécurité dans un pipeline CI/CD** (TP2 DevSecOps INSAT). Une faille grave détectée dans le pipeline **bloque la fusion** dans `main`.


## 🔐 Pipeline de sécurité

Le workflow [`ci.yml`](.github/workflows/ci.yml) s'exécute à chaque push sur `main` et à chaque pull request vers `main`.

| Job | Outil | Vérifie | Bloque si |
|---|---|---|---|
| `build-test` | pytest, Docker | Tests unitaires et build de l'image | Un test échoue |
| `sast` | Bandit | Code source (`eval`, injection, `debug=True`…) | Sévérité ≥ Medium |
| `sca` | Trivy | CVE dans les dépendances | HIGH ou CRITICAL |
| `dast` | OWASP ZAP | App lancée dans un conteneur éphémère | Alerte ≥ Medium |

`dast` ne démarre que si les trois autres jobs sont verts.


## 🚀 Démarrage rapide

```bash
git clone https://github.com/ReemaZa/calc-devsecops.git
cd calc-devsecops
pip install -r requirements.txt -r requirements-dev.txt
pytest
python app.py          # http://127.0.0.1:5000
```

Avec Docker :

```bash
docker build -t calc-app .
docker run --rm -p 5000:5000 calc-app
```


## ⚠️ Dossier `demo/`

Contient une version **volontairement vulnérable** (`eval`, route admin non protégée, `debug=True`, dépendances obsolètes), utilisée uniquement pour prouver, via une pull request, que le pipeline bloque ces failles. Elle n'est jamais déployée.


