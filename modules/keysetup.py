import json
import hashlib
import requests
from pathlib import Path
# Fichiers de configuration
config_dir = Path.home() / ".obliv"
config_file = config_dir / "config.json"





def save_api_key(api_key, username=None):
    """Crée le dossier config et enregistre la clé API et le nom d'utilisateur dans config.json."""
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Charger la configuration existante s'il y en a une
    config_data = {}
    if config_file.exists():
        with open(config_file, 'r') as file:
            config_data = json.load(file)
    
    # Mettre à jour avec la nouvelle clé API et le nom d'utilisateur
    config_data["apiKey"] = api_key
    if username:
        config_data["username"] = username
    
    with open(config_file, 'w') as file:
        json.dump(config_data, file, indent=4)
    




def authenticate(api_key=None):
    """Vérifie la clé API. Si valide, la sauvegarde dans config.json."""
    result = auth_request(api_key)
    if result and result.get("success"):
        username = result.get("username")  # Récupérer le nom d'utilisateur depuis la réponse
        save_api_key(api_key, username)
        return True
    else:
        return False

def auth_request(api_key):
    """Envoie une requête avec la clé API pour vérification."""
        
    hashed_key = hashlib.sha256(api_key.encode()).hexdigest()

    headers = {
        'X-Obliv-Auth': hashed_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get("http://machwix.com/api/external/v1/auth/auth", headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success") == True:
                return response_data  # Retourner toute la réponse pour récupérer le nom d'utilisateur
            elif response_data.get("success") == False:
                return None
        return None
        
    except Exception as e:
        print("Erreur lors de la vérification de la clé API :", e)
        return None


def get_saved_username():
    """Lit le nom d'utilisateur depuis le fichier de configuration s'il existe."""
    if config_file.exists():
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config.get("username")
    return None

