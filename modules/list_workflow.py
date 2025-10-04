from collections import defaultdict
from pathlib import Path
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

def list_workflow():
    """Liste les workflows disponibles."""
    workflow_name=[]
    api_key = get_saved_api_key()
    if not api_key:
        print("Aucune clé API définie. Veuillez d'abord vous authentifier.")
        return
    try: 
        response = requests.get("http://192.168.0.132/api/external/v1/workflows/list", headers={
            'X-Obliv-Auth': hashlib.sha256(api_key.encode()).hexdigest(),
            'Content-Type': 'application/json'
        })
        if response.status_code == 200:
            data = response.json().get("data", {})
            workflows = data.get("workflows", [])
            
            if workflows:
                
                for i, wf in enumerate(workflows):
                    uid = wf.get("workflow_uid", "")
                    nom = wf.get("name", "")
                    created = wf.get("created_at", "")
                    desc = wf.get("description", "")
                   
                    variables = wf.get("variables", [])
                    variables_uniques = list(dict.fromkeys(variables))
                    var_str = ", ".join(variables_uniques) if variables_uniques else "-"
                    
                    workflow_name.append(nom)

                
                config = {}
                if config_file.exists():
                    with open(config_file, 'r') as file:
                        config = json.load(file)
                config["workflows"] = workflows
                with open(config_file, 'w') as file:
                    json.dump(config, file, indent=2)
                
                return workflow_name
            else:
                print("Aucun workflow disponible.")
        else:
            print(f"Erreur lors de la récupération des workflows: {response.status_code}")
    except Exception as e:
        print(f"Erreur lors de la requête: {e}")

def get_workflow_table():
    api_key = get_saved_api_key()
    if not api_key:
        return "Aucune clé API définie. Veuillez d'abord vous authentifier."
    try:
        response = requests.get("http://192.168.0.132/api/external/v1/workflows/list", headers={
            'X-Obliv-Auth': hashlib.sha256(api_key.encode()).hexdigest(),
            'Content-Type': 'application/json'
        })
        if response.status_code == 200:
            data = response.json().get("data", {})
            workflows = data.get("workflows", [])
            if not workflows:
                return "Aucun workflow disponible."
            lines = []
            header = f"{'N°':<3} | {'Nom':<15} | {'UID':<12} | {'Créé':<10} | {'Variables':<20} | {'Desc':<15}"
            lines.append(header)
            lines.append("-" * len(header))
            for i, wf in enumerate(workflows):
                uid = wf.get("workflow_uid", "")
                nom = wf.get("name", "")
                created = wf.get("created_at", "")[:10]
                desc = wf.get("description", "")
                variables = wf.get("variables", [])
                variables_uniques = list(dict.fromkeys(variables))
                var_str = ", ".join(variables_uniques) if variables_uniques else "-"
                line = f"{i+1:<3} | {nom:<15} | {uid[:12]:<12} | {created:<10} | {var_str:<20} | {desc[:15]}"
                lines.append(line)
            return "\n".join(lines)
        else:
            return f"Erreur lors de la récupération des workflows: {response.status_code}"
    except Exception as e:
        return f"Erreur lors de la requête: {e}"





