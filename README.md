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

### Mettre en place l'environnement virtuel 
```bash
python -m venv .venv
```

### Lancer l'environnement virtuel
#### Windows 
```bash
.venv/Scripts/Ativate.ps1
```
#### Unix 
```bash
source .venv/bin/activate
```
### Installation des dépendances
```bash
pip install -r requirement.txt
```