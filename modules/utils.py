from platform import node
import json
from pathlib import Path
import re
import os



def parse_dollar_vars(text):
    pattern = r"\$\$(\w+):([^\n]+)"
    matches = re.findall(pattern, text)
    result = {}
    for key, value in matches:
        result[key] = value.strip()
    return result

def load_config():
    """Charge le fichier YAML et retourne les données."""

    config_dir = Path.home() / ".obliv"
    config_file = config_dir / "config.json"

    with open(config_file, 'r') as file:
            config = json.load(file)
            return config
    
    return None

def extract_nodes_from_template(template_text):
    """
    Prend le texte du template, retire le header ($$...) et retourne la partie nodes.
    """
    lines = template_text.splitlines()
    node_lines = [line for line in lines if not line.strip().startswith('$$') and line.strip()]
    
    return "\n".join(node_lines)





def extract_data(template):
    vars_dict = parse_dollar_vars(template)
    flowx_version = vars_dict.get("flowx_version")
    sig = vars_dict.get("sig")
    name = vars_dict.get("name")
    mode = vars_dict.get("mode")
    return flowx_version, sig, name, mode

   

def found_variable(flag):
    variable_input = r'\{\{(\w+)\}\}'
    variable_systeme = r'\[\[(\w+)\]\]'
    
    match_input = re.search(variable_input, flag)
    if match_input:
        return match_input.group(1)
    
    match_sys = re.search(variable_systeme, flag)
    if match_sys:
        return match_sys.group(1)

    
    return None


def replace_all_variables_in_command(command, variables, system_vars):
    """
    Remplace toutes les variables dans la commande.
    Les variables d'entrée sont entourées de {{}}
    Les variables système sont entourées de [[]]."""
    def repl_input(match):
        var = match.group(1)
        return str(variables.get(var, match.group(0)))
    def repl_sys(match):
        var = match.group(1)
        return str(system_vars.get(var, match.group(0)))
    command = re.sub(r'\{\{(\w+)\}\}', repl_input, command)
    command = re.sub(r'\[\[(\w+)\]\]', repl_sys, command)
    return command


def get_variable_value(node, variables, system_vars):
    for flag in node['arguments']:
        flag_value=flag['value']
        variable_name = found_variable(flag_value)

        resolved_value  = replace_all_variables_in_command(flag_value, variables,system_vars)

        return resolved_value
    return None

def save_output(node, output, system_vars, mode):
    """
    Enregistre la sortie dans un fichier si le nom de fichier est spécifié.
    """
    if mode=='debug':
        print("[+] Saving output")
        print(node)
    destination = node.get('destination')
    output_file = node.get('output_file')
    if destination or output_file:
        # Cherche une variable système dans destination ou output_file
        output_var = None
        if destination:
            output_var = found_variable(destination)
        if output_var is None and output_file:
            output_var = found_variable(output_file)

        if output_var is not None:
            # On stocke dans la variable système, pas de création de fichier
            if output_var not in system_vars:
                system_vars[output_var] = []
            system_vars[output_var].append(output)
            if mode=='debug':
                print(system_vars)
        else:
            # On écrit dans le fichier destination ou output_file
            file_path = destination if destination else output_file
            with open(file_path, 'a', encoding='utf-8') as f:
                for line in output:
                    f.write(line)
                    f.write('\n')
                f.write('\n')



def flatten_workflow(workflow):
    flat = []
    for node in workflow:
        if isinstance(node, dict) and 'branch' in node:
            for branch in node['branch']:
                flat.extend(flatten_workflow(branch))
        else:
            flat.append(node)
    return flat



def get_uid_and_variables(name=None, uid=None):
    """
    Recherche un workflow par nom ou par UID et retourne (uid, variables).
    Si plusieurs workflows ont le même nom, demande à l'utilisateur de choisir.
    Affiche les messages dans history_field si fourni.
    """
    doublons = False
            
    config_file = Path.home() / ".obliv" / "config.json"
    if config_file.exists():
        with open(config_file, "r") as file:
            config = json.load(file)
            workflows = config.get("workflows", [])
            # Recherche par UID direct
            if uid:
                for wf in workflows:
                    if wf.get("workflow_uid") == uid:
                        return wf.get("workflow_uid"), wf.get("variables", []), False
                return None, [], False
            # Sinon, recherche par nom
            if name:
                matches = [wf for wf in workflows if wf.get("name") == name]
                if not matches:
                    return None, [], False
                if len(matches) == 1:
                    wf = matches[0]
                    return wf.get("workflow_uid"), wf.get("variables", []), False
                doublons = True
                print("Plusieurs workflows trouvés :")
                config_file = Path.home() / ".obliv" / "config.json"
                with open(config_file, "r") as file:
                    config = json.load(file)
                    all_workflows = config.get("workflows", [])
                lines = []
                header = f"{'N°':<3} | {'Nom':<15} | {'UID':<12} | {'Créé':<10} | {'Variables':<20} | {'Desc':<30}"
                lines.append(header)
                lines.append("-" * len(header))
                for wf in matches:
                    try:
                        global_idx = all_workflows.index(wf) + 1
                    except ValueError:
                        global_idx = "?"
                    nom = wf.get('name', '')
                    uid = wf.get('workflow_uid', '')
                    created = wf.get('created_at', '')[:10]
                    desc = wf.get('description', '')
                    variables = wf.get('variables', [])
                    variables_uniques = list(dict.fromkeys(variables))
                    var_str = ", ".join(variables_uniques) if variables_uniques else "-"
                    line = f"{global_idx:<3} | {nom:<15} | {uid[:12]:<12} | {created:<10} | {var_str:<20} | {desc[:30]}"
                    lines.append(line)
                for l in lines:
                    print(l)
                print("Veuillez relancer la commande avec l'UID (ex: run -uid <UID>) ou le numéro (ex: run -number <N°>) du workflow souhaité.")
                return None, [], doublons
    return None, [], doublons






DASHBOARD_DIR = "dashboard"
os.makedirs(DASHBOARD_DIR, exist_ok=True)

DASHBOARD_FILE = os.path.join(DASHBOARD_DIR, "dashboard_state.json")

def save_dashboard_info(info: dict):
    """
    Écrit les infos dans dashboard/dashboard_state.json.
    info: dictionnaire avec ce que tu veux sauvegarder.
    """
    # Si le fichier existe, on charge les données existantes
    if os.path.exists(DASHBOARD_FILE):
        try:
            with open(DASHBOARD_FILE, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {}
    else:
        data = {}

    # On met à jour avec les nouvelles infos
    data.update(info)

    # On sauvegarde
    with open(DASHBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)


def mask_api_key(api_key):
    if not api_key or len(api_key) < 12:
        return api_key or "-"
    # Garde les 8 premiers et 4 derniers caractères, masque le reste
    return api_key[:8] + '•' * (len(api_key) - 32) + api_key[-4:]

def count_nodes(node):
    """Compte le nombre total de nodes dans un workflow récursivement."""
    nodes = node['children']
    number_node = len(nodes)
    return number_node


