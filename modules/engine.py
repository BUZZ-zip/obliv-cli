import re
import subprocess
import time
import threading
import requests
from datetime import datetime




"""Modules"""
from modules.utils import save_dashboard_info, count_nodes
from modules.node.flow_control import *
from modules.node.command import *
from modules.node.condition import *
from modules.node.execution import *
from modules.node.network import *
from modules.node.data_action import *

""""Variables globales"""
system_vars={}
skip_node=''
next_node_id=''


def stack_push(template):
    """
    Ajoute un nœud à la pile.
    """
    stack = [{"type": "root", "children": []}]

    for line in template:
        line = line.strip()
        if line.endswith("{"):
            block_type = line.split()[0].replace(":", "")
            new_block = {"type": block_type, "children": []}
            stack[-1]["children"].append(new_block)
            stack.append(new_block)

        elif line == "}":
            stack.pop()

        elif line.startswith("n="):
            node = {}
            for item in line.split("|"):
                if "=" in item:
                    key, val = item.split("=", 1)
                    node[key] = val
            stack[-1]["children"].append(node)
    
    return stack[0]





def engine(template,variables,mode,stack):
    global skip_node , actual_number_node
    actual_number_node=0
    try : 
        
        
        if mode=='debug':
                print(f"Stack initial : {stack}")

        for node in stack["children"]:

                actual_number_node+=1
                if not node.get("type", "")== "if-else":
                        save_dashboard_info({
                        "current_node": actual_number_node,
                        "current_node_name": node['n']
                        })
                if 'n' in node and node['n'] == skip_node:
                        if mode=='debug':
                                print(f"[!] Skip node : {node['n']}")

                else : 
                        node_type = node.get("t", "")
                        node_tool = node.get("tool", "")
                        

                        if 'start' in node_type:
                                start_workflow(mode)
                        elif 'end' in node_type:
                                end_workflow(mode)
                                end_time = datetime.now()
                                elapsed_final = str(end_time - datetime.fromisoformat(start_time)).split(".")[0]
                                save_dashboard_info({
                                        "status": "Completed",
                                        "elapsed": elapsed_final
                                })

                        elif 'if-else' == node.get("type", ""):
                                run_condition(template,variables, mode, node)

                        
                        elif 'wait' == node_tool:
                                run_wait_mid(node,mode)
                        elif 'file' == node_tool:
                                read_file_mid(node,variables,mode,system_vars)
                        elif 'loop' == node_tool:
                                skip_node=run_loop_mid(node,stack,variables,mode,system_vars,workflow_global)
                        elif 'parallel' == node_tool:
                                run_parallel_mid(node,template,variables,mode,skip_node)

                        elif 'print' == node_tool:
                                run_print_execution(node,variables,mode,system_vars)
                        elif 'command' == node_tool:
                                run_command_execution(node,variables,mode,system_vars)

                        elif 'http' == node_tool:
                                run_http_network(node,variables,mode,system_vars)
                        elif 'api-call' == node_tool:
                                run_api_call_network(node,variables,mode, system_vars)
                        elif 'webhook' == node_tool:
                                run_webhook_network(node,variables,mode,system_vars)

                        elif 'extract' == node_tool:
                                run_extract_data_action(node,variables,mode,system_vars)
                        elif 'validate' == node_tool:
                                run_validate_data_action(node,variables,mode,system_vars)
                        elif 'transform' == node_tool:
                                run_transform_data_action(node,variables,mode,system_vars)


                        elif 'execution' == node_type:
                                run_tool_execution(node,variables,mode,system_vars)

    except Exception as e:
        print(f"Erreur lors de l'exécution du workflow : {e}")


def main_engine(template,variables):
    global workflow_global,total_nodes, start_time
    

    flowx_version, sig, name, mode = extract_data(template)
    

    

    template = extract_nodes_from_template(template)
    if mode == 'debug':
        print(template)
    template = template.splitlines()
    stack = stack_push(template)
    workflow_global= template
    
    total_nodes = count_nodes(stack)
    start_time = datetime.now().isoformat()
    save_dashboard_info({"action": "render_run", "current_workflow": name, "mode": mode, "variables": variables, "status": "Running", "start_time": start_time,"number_node": total_nodes })
    
    stack=engine(template,variables,mode,stack,)
    

    system_vars.clear()



