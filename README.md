# Application Web d'analyse des sentiments
## Installation
### Environnement dockerisé
Le projet peut être lancé depuis un container. Pour cela il faut d'abord copier le fichier d'environnement exemple comme suit :   
```bash
cp .env.example .env
```
Il faudra ensuite compléter les variables d'environnement manquantes.  

Il faut ensuite monter le container et le lancer :
```bash
docker compose build
docker compose up -d 
docker compose exec api bash
```

### Lancer le projet sans Docker

#### Mettre en place l'environnement virtuel 
```bash
python -m venv .venv
```

#### Lancer l'environnement virtuel
- Windows 
```bash
.venv/Scripts/Ativate.ps1
```
- Unix 
```bash
source .venv/bin/activate
```
#### Installation des dépendances
```bash
pip install -r requirement.txt
```

Après avoir activé l'environnement virtuel et installé les dépendances, lancez les services suivants dans deux terminaux séparés :

#### 1. Lancer l'API FastAPI avec Uvicorn
```bash
uvicorn api.main:app --reload
```

#### 2. Lancer le serveur MLflow pour le suivi des expériences
```bash
mlflow ui
```
Par défaut, l'interface MLflow sera accessible sur [http://localhost:5000](http://localhost:5000).

---

## Entraînement des modèles

L'entraînement des modèles se fait via le script Python dédié. Voici les étapes et résultats obtenus :

### 1. Modèles sur les anciennes données

Deux types de prétraitement ont été testés :
- **Préprocessing éthique** : respect strict des contraintes éthiques et RGPD.
  - **Score R² obtenu** : 0.24
- **Préprocessing lâche éthiquement** : moins de contraintes, plus de variables sensibles utilisées.
  - **Score R² obtenu** : 0.33

### 2. Modèles sur les nouvelles données

Un nouveau modèle a été entraîné en se basant sur le précédent, mais avec deux nouvelles features ajoutées aux données.  
- **Préprocessing éthique** : respect strict des contraintes éthiques et RGPD.
  - **Score R² obtenu** : 0.38
- **Préprocessing lâche éthiquement** : moins de contraintes, plus de variables sensibles utilisées.
  - **Score R² obtenu** : 0.47

### Conclusion
On note une amélioration des performances pour les 2 types de modèles avec les nouvelles données.

#### Exemple de commande pour entraîner un modèle :
```bash
python api/scripts/training.py
```

Vous pouvez adapter le script pour choisir le type de préprocessing et le jeu de données