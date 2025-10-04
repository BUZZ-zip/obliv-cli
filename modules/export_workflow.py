import requests
import hashlib
from pathlib import Path
import json
import shutil
import os

from modules.utils import get_uid_and_variables
from modules.get_template import get_workflow


config_dir = Path.home() / ".obliv"
config_file = config_dir / "config.json"


def load_config(config_path):
    if Path(config_path).exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

def save_config(config_path, data):
    with open(config_path, 'w') as f:
        json.dump(data, f, indent=2)
    

def copy_files_with_structure(file_map, dest_root):
    for src, rel_dest in file_map:
        dest_path = Path(dest_root) / rel_dest
        os.makedirs(dest_path.parent, exist_ok=True)
        shutil.copy2(src, dest_path)




def export(*args):
    print()
    if len(args) < 4:
        return "Usage: export -name <name> -binary_name <binary_name> \n       export -uid <uid> -binary_name <binary_name> \n       export -number <num> -binary_name <binary_name>"
    mode = args[0]
    value = args[1]
    mode_binary = args[2]
    binary_name = args[3]

    from modules.list_workflow import get_saved_api_key, list_workflow
    workflows = list_workflow() or []
    if not workflows:
        return "Aucun workflow disponible."
    if mode in ["-n", "-name"]:
        uid, variables, doublons = get_uid_and_variables(name=value)
    elif mode == "-uid":
        uid, variables, doublons = get_uid_and_variables(uid=value)
    elif mode in ["-number", "-num"] and value.isdigit():
        idx = int(value) - 1
        if idx < 0 or idx >= len(workflows):
            return "Numéro de workflow invalide."
        wf = workflows[idx]
        wf_name = wf.get("name") if isinstance(wf, dict) else wf
        uid, variables, doublons = get_uid_and_variables(name=wf_name)
    else:
        return "Usage: export -name <name> -binary_name <binary_name> \n       export -uid <uid> -binary_name <binary_name> \n       export -number <num> -binary_name <binary_name>"
    if not uid and doublons:
        return ""
    if not uid and not doublons:
        return "Workflow introuvable."

    
    


        


    



    api_key = get_saved_api_key()
    if not api_key:
        return

    # Ask user for visibility in English
    while True:
        visibility = input("Do you want to make this workflow public or private? (public/private): ").strip().lower()
        if visibility in ["public", "private"]:
            break
        print("Invalid response. Please answer 'public' or 'private'.")
    if visibility == "public":
        confirm = input("Are you sure you want to make this workflow public? (Y/n): ").strip()
        if confirm == "" or confirm.lower() in ["y", "yes"]:
            pass  # Proceed as public
        elif confirm.lower() in ["n", "no"]:
            print("Export cancelled or set to private.")
            visibility = "private"
        else:
            print("Invalid response. Export cancelled or set to private.")
            visibility = "private"

    payload = {}
    payload["workflow_uid"] = uid
    payload["visibility"] = visibility

    try: 
        response = requests.post("http://192.168.0.132/api/external/v1/workflows/export",
                headers={
                    'X-Obliv-Auth': hashlib.sha256(api_key.encode()).hexdigest(),
                    'Content-Type': 'application/json'
                },
                json=payload
         )
        
        if response.status_code == 200:
            result = response.json()
            export_uid = result.get("export_uid", "")
            if not export_uid or export_uid == None:
                return
            

            
    except Exception as e:
        print(f"Erreur lors de l'exportation du workflow: {e}")
        pass

    try :
        template = get_workflow(name=None, id=uid)
        

        user_dir_main = Path.home() / ".obliv/export"
        user_dir_main.mkdir(parents=True, exist_ok=True)
        user_dir = Path.home() / f".obliv/export/{binary_name}_data"
        user_dir.mkdir(parents=True, exist_ok=True)

        # Save template as text in user_dir
        template_path = user_dir / "template.txt"
        with open(template_path, "w") as f:
            if isinstance(template, (dict, list)):
                f.write(json.dumps(template, indent=2, ensure_ascii=False))
            else:
                f.write(str(template))

        config_path = user_dir / "conf.json"
        config = load_config(config_path)
        config["binary_name"] = binary_name
        config["export_uid"] = export_uid
        config["inputs"] = variables
        save_config(config_path, config)

       



        # Copier main_export.py sous le nom du binary_name à la racine du user_dir
        src_main = "modules/main_export.py"
        dest_main = user_dir_main / binary_name
        shutil.copy2(src_main, dest_main)

        # Ajouter le shebang si absent et rendre exécutable
        with open(dest_main, "r+") as f:
            content = f.read()
            if not content.startswith("#!"):
                f.seek(0)
                f.write("#!/usr/bin/env python3\n" + content)
        import stat
        dest_main.chmod(dest_main.stat().st_mode | stat.S_IEXEC)

        # Copier les autres fichiers nécessaires
        file_map = [
            ("modules/engine.py", "modules/engine.py"),
            ("modules/utils.py", "modules/utils.py"),
            ("modules/node/command.py", "modules/node/command.py"),
            ("modules/node/condition.py", "modules/node/condition.py"),
            ("modules/node/data_action.py", "modules/node/data_action.py"),
            ("modules/node/execution.py", "modules/node/execution.py"),
            ("modules/node/flow_control.py", "modules/node/flow_control.py"),
            ("modules/node/network.py", "modules/node/network.py"),
        ]
        dest_root = user_dir
        copy_files_with_structure(file_map, dest_root)



    except Exception as e:
        print(f"Erreur lors de la préparation de l'exportation: {e}")
        input()
        pass

    # Vérifier et ajouter ~/.obliv/export au PATH dans ~/.bashrc si nécessaire
    bashrc_path = Path.home() / ".bashrc"
    export_line = 'export PATH="$HOME/.obliv/export:$PATH"\n'
    already_set = False
    if bashrc_path.exists():
        with open(bashrc_path, "r") as f:
            for line in f:
                if ".obliv/export" in line and "PATH" in line:
                    already_set = True
                    break
    if not already_set:
        with open(bashrc_path, "a") as f:
            f.write("\n# Add obliv export binaries to PATH\n")
            f.write(export_line)
        if mode=='debug':
            print("[INFO] ~/.obliv/export has been added to your PATH in ~/.bashrc. Please run: source ~/.bashrc")
    else:
        if mode=='debug':
            print("[INFO] ~/.obliv/export is already in your PATH.")

    
    return f"Workflow exported successfully! You can run it using {binary_name} from your shell."