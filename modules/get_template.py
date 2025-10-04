from collections import defaultdict
from pathlib import Path
from unittest import result
import requests
import hashlib
import json

config_dir = Path.home() / ".obliv"
config_file = config_dir / "config.json"



def get_saved_api_key():
    """Lit la clé API depuis le fichier de configuration s'il existe."""
    if config_file.exists():
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config.get("apiKey")
    return None


def get_uid_from_name(name):
    """Retourne l'UID d'un workflow à partir de son nom (demande à l'utilisateur si plusieurs)."""
    if config_file.exists():
        with open(config_file, 'r') as file:
            config = json.load(file)
            workflows = config.get("workflows", [])
            matches = [wf for wf in workflows if wf.get("name") == name]
            if not matches:
                print(f"Aucun workflow trouvé avec le nom : {name}")
                return None
            if len(matches) == 1:
                return matches[0].get("workflow_uid")
            # Plusieurs workflows avec le même nom
            print("Plusieurs workflows trouvés :")
            print("─" * 60)
            for i, wf in enumerate(matches):
                uid = wf.get("workflow_uid", "")
                nom = wf.get("name", "")
                created = wf.get("created_at", "")
                desc = wf.get("description", "")
                print(f"[{i}] UID: {uid} | Nom: {nom:12} | Créé: {created[:10]} | Desc: {desc}")
            choix = input("Entrez le numéro du workflow à utiliser : ")
            try:
                choix = int(choix)
                return matches[choix].get("workflow_uid")
            except Exception:
                print("Choix invalide.")
                return None
    else:
        return None

def get_workflow(name, id):
    """Récupère un workflow spécifique."""


    payload = {}

    api_key = get_saved_api_key()
    if not api_key:
        return


    if not name and not id:
        return
    


    if name:
        uid = get_uid_from_name(name)
            
        payload["workflow_uid"] = uid
        
    if id:
        
        payload["workflow_uid"] = id
        

    
    try: 
        response = requests.post("http://192.168.0.132/api/external/v1/workflows/template",
                headers={
                    'X-Obliv-Auth': hashlib.sha256(api_key.encode()).hexdigest(),
                    'Content-Type': 'application/json'
                },
                json=payload
         )
        
        if response.status_code == 200:
            result = response.json()
            template = result.get("template", "")
            if not template or template == None:
                return
            
            return template
            
            

        
    except Exception as e:
        pass





