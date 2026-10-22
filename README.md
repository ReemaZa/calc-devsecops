# Calculatrice scientifique DevSecOps (TP2)
## Intégration de la Sécurité dans un Pipeline CI/CD
- Local : `pip install -r requirements.txt -r requirements-dev.txt`, `pytest`, puis `python app.py` -> http://127.0.0.1:5000
- `calculator.py` : moteur de calcul sécurisé (parseur `ast`, liste blanche, sans eval).
- `demo/` : version volontairement vulnérable (eval, injection de commande, debug, pas d'en-têtes) pour la PR de démonstration.
