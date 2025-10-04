import subprocess


"""Modules"""
from modules.utils import found_variable, save_output,replace_all_variables_in_command


def execute_command(cmd,output_list,mode):
    """Exécute une commande shell et stocke la sortie dans output_list (thread-safe)."""
    try:
        if mode == "silent":
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            lines = result.stdout.strip().splitlines()
            output_list.extend(lines)
        else:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, text=True, bufsize=1)
            
            for line in process.stdout:
                line = line.rstrip()
                print(line)
                output_list.append(line)
            
            process.wait()
    except Exception as e:

        print(f"[!] Error running command: {cmd}")
        print(str(e))


def build_command(node, variables,system_vars):
    
    tool_name=node['tool']
    
    command=tool_name
    print(command)
    
    try:
        flag_value = node['arguments']
            
        command+=' '
        print(flag_value)
    
        variable_name = found_variable(flag_value)
        
        
        
        if variable_name:
            # Remplacer la variable par sa valeur
            if variable_name in variables:
                replaced_command = replace_all_variables_in_command(flag_value, variables,system_vars)
                
                command+= replaced_command
            else:
                replaced_command=system_vars[variable_name]
                print(replaced_command)
                command+=replaced_command
                print(command)
        else:
            command+= flag_value
                

        
        return command
    except:
        print(f'[!] Error during command {tool_name}')





def run_command(node,variables,mode,system_vars):
    """Run command node"""

    if mode=='debug':
        print("[+] Running Command")

    command=build_command(node,variables,system_vars)
    print(command)
    output=[]
    
    execute_command(command,output,mode)
   
    save_output(node, output, system_vars,mode)
            
   


