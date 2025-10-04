from modules.utils import found_variable, save_output,replace_all_variables_in_command
import re

def run_extract_data_action(node,variables,mode,system_vars):
    if mode=='debug':
        print("[+] Running Extract")

    data = node.get('input_data', '')
    regex = node.get('regex', '')

    data = replace_all_variables_in_command(data, variables, system_vars)
    regex = replace_all_variables_in_command(regex, variables, system_vars)


    if isinstance(data, list):
        
        if any(isinstance(item, list) for item in data):
            data = "\n".join(line.strip(" ',") for sublist in data for line in sublist)
        else:
            data = "\n".join(line.strip(" ',") for line in data)
    if isinstance(data, str) and data.startswith('[['):
        # C'est une string qui encode une liste de listes, on l'évalue
        import ast
        try:
            data_eval = ast.literal_eval(data)
            if isinstance(data_eval, list):
                # flatten proprement
                data = "\n".join(line for sublist in data_eval for line in sublist)
        except Exception:
            pass
    if mode=='debug':
        print(data)
        print(f"[DEBUG] Regex appliquée : {regex}")
        print('---DATA TO EXTRACT---')
        print(repr(data))
        print('---REGEX---')
        print(regex)
        print('---')

    matches = re.findall(regex, data, re.MULTILINE)
    if mode=='debug':
        print(f"[DEBUG] {len(matches)} valeur(s) extraite(s)")

    clean_matches = []
    for m in matches:
        if isinstance(m, tuple):
            clean = [s.strip(" ',") for s in m]
            clean_matches.append("".join(clean))
        else:
            clean_matches.append(m.strip(" ',"))
    output = clean_matches

    if node.get('output_file'):
        save_output(node, output, system_vars,mode)


def run_validate_data_action(node,variables,mode,system_vars):
    if mode=='debug':
        print("[+] Running Validate")

def run_transform_data_action(node,variables,mode,system_vars):
    if mode=='debug':
        print("[+] Running Transform")
