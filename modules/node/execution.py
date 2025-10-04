from datetime import datetime

"""Module"""
from modules.utils import get_variable_value,save_output, replace_all_variables_in_command
from modules.node.command import execute_command

def run_print_execution(node,variables,mode,system_vars):
    if mode=='debug':
        print("[+] Running Print")
    flag_value = node['print_text']
    if not isinstance(flag_value, list):
        flag_value = [flag_value]
    
    for flag in flag_value:
        resolved_value  = replace_all_variables_in_command(flag, variables,system_vars)
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        print(f"{timestamp} {resolved_value}")

def run_command_execution(node,variables,mode,system_vars):
    if mode=='debug':
        print("[+] Running Command")

    output=[]
    flag_value = node['command']
    if mode=='debug':
        print(system_vars)
    command  = replace_all_variables_in_command(flag_value, variables,system_vars)
    if mode=='debug':
        print(command)

    execute_command(command, output, mode)

    if node.get('output_file'):
        save_output(node, output, system_vars,mode)


def run_tool_execution(node,variables,mode,system_vars):
    tool = node.get('tool')
    if mode=='debug':
        print(f"[+] Running {tool}")
    try :
        output=[]
        
        command = node.get('command')
        basic_cmd = node.get('basic_args')
        advanced_cmd = node.get('advanced_args')

        if advanced_cmd:
            command = f"{command} {advanced_cmd}"
        else:
            command = f"{command} {basic_cmd}"

        command  = replace_all_variables_in_command(command, variables,system_vars)

        if mode=='debug':
            print(command)

        execute_command(command, output, mode)

        if node.get('output_file'):
            save_output(node, output, system_vars,mode)
    except Exception as e:
        print(f"[!] Error during executing tool {tool} : {e}")



    