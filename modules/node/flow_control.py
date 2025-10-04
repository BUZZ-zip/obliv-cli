import time
import threading
import ast


"""Modules"""
from modules.utils import * 




def start_workflow(mode):
    """Start workflow."""
    if mode=='debug':
        print(f"[+] START Workflow")


def end_workflow(mode):
    """End workflow."""
    if mode=='debug':
        print(f"[+] END Workflow")



def run_wait_mid(node,mode,):
    """
    Run wait mid node.
    input : nombre de secondes à attendre
    output : None
    """
    if mode=='debug':
        print(f"[+] Running Wait")

    flag_value=node['arguments']
    try :
        val = float(flag_value)
        time.sleep(val)
    except ValueError:
        if mode=='debug':
            print(f"[!] Error during Wait")




def read_file_mid(node,variables,mode,system_vars):
    """
    Run file mid node.
    input : nom du ou des fichiers à lire
    output : variable système contenant le contenu du ou des fichiers
    """
    if mode=='debug':
        print(f"[+] Running File")

    flag_value = node['files']
    if isinstance(flag_value, str):
        
        if flag_value.strip().startswith("[") and flag_value.strip().endswith("]"):
            try:
                flag_value = ast.literal_eval(flag_value)
            except Exception:
                flag_value = [f.strip() for f in flag_value.strip("[]").split(",") if f.strip()]
        else:
            flag_value = [f.strip() for f in flag_value.split(",") if f.strip()]


    
    for flag in flag_value:
        
        variable_name = found_variable(flag)
        

        if variable_name:
            
            if variable_name in variables:
                file = replace_all_variables_in_command(flag, variables,system_vars)
                
            elif variable_name in system_vars:
                file = system_vars[variable_name]
                
            else:
                if mode=='debug':
                    print(f'Variable {variable_name} not found in variables')
        else:
            file=flag

        
        try:
            with open(file, 'r') as f:
                output = [line.strip() for line in f if line.strip()]
        except:
            if mode=='debug':
                print(f"[!] Error during opening file {file}")
            output = []


        save_output(node, output, system_vars,mode)
    










def execute_branch(branch, variables,mode,skip_node):
    """ Execute a branch of nodes in parallel."""

    from modules.engine import engine
    
    for node in branch:
        if mode=='debug':
            print(f"Thread {threading.current_thread().name} : Exécution du nœud {node['id']}")
        if skip_node==node['id']:
            if mode=='debug':
                print(f"[DEBUG] Skip node : {skip_node}")
        else:
            engine([node], variables, mode)  


def run_parallel_mid(node,workflow,variables,mode,skip_node):
    """
    Run parallel mid node
    Recup les branches du noeud et les exécute en parallèle.
    execute toutes les nodes meme si les branches n ont pas la meme taille
    """

    if mode=='debug':
        print(f"[+] Running Parallel")

    for node in workflow:
        if 'branch' in node:
            threads = []
            for i, branch in enumerate(node['branch']):
               t = threading.Thread(target=execute_branch, args=(branch, variables, mode, skip_node), name=f"Branche-{i+1}")
               t.start()
               threads.append(t)
            for t in threads:
                t.join()











def run_loop_mid(node,template,variables,mode,system_vars,workflow_global):
    """ 
    Run loop mid node.
    input : variable contenant la liste des éléments à itérer
    output : variable système contenant l'élément courant de la boucle
    """

    from modules.engine import engine

    if mode=='debug':
        print(f"[+] Running Loop")

    loop_id=node['n']
    
    if 'output_file' in node and node['output_file']:
            output_var=node['output_file']
            output_var=found_variable(output_var)

    if mode=='debug':
        print(f"[DEBUG] OUTPUT: {output_var}")



    flag = ast.literal_eval(node['loop_inputs'])
    for flag_value in flag:
        

        

        variable_name = found_variable(flag_value)
        

        if variable_name:
            
            list_for_loop=system_vars[variable_name]   
            
            if mode=='debug':
                print(f"[DEBUG] variable_name = {variable_name}")
                print(f"[DEBUG] list_for_loop = {list_for_loop}")

            for list in list_for_loop:
                for element in list:
                    if mode=='debug':
                        print(f"[DEBUG] element = {element}")


                    system_vars[output_var]=element
                    if mode=='debug':
                        print(f"[DEBUG] {system_vars}")
                    children = template['children']
                    for idx, node2 in enumerate(children):
                        
                        if node2['tool'] == 'loop':
                        
                            # Prendre le node suivant s'il existe
                            if idx + 1 < len(children):
                                next_node_id = children[idx + 1]
                                if mode=='debug':
                                    print(f"[+] Running Loop on {next_node_id['tool']}")
                                node_workflow = {"type": "root", "children": [next_node_id]}

                                engine(template, variables, mode, node_workflow)
                                if output_var in system_vars:
                                    del system_vars[output_var]
                    
                        
            
            skip_node=next_node_id['n']
            if mode=='debug':
                print(f"[DEBUG] skip_node = {skip_node}")

        else:
            if mode=='debug':
                print("pas de varriable trouvé pour le loop")

        return skip_node



