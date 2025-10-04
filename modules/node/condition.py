"""Module"""
from modules.utils import get_variable_value



def run_condition(template,variables, mode, node):
    """
    Exécute une condition.
    Si la condition est vraie, exécute les noeuds
    sinon execute les noeuds du bloc else.
    """

    from modules.engine import engine


    if_block = node["children"][0]
    if mode=='debug':
        print(f"[+] Running If-Else on {if_block['type']}")
    else_block = node["children"][1]
    if mode=='debug':
        print(f"[+] Running Else on {else_block['type']}")

    # Récupère la condition depuis le type du bloc if
    cond_str = if_block["type"]
    # Extrait la condition (après 'condition=')
    cond_expr = ""
    if "condition=" in cond_str:
            cond_expr = cond_str.split("condition=", 1)[1].split("{")[0].strip()
    try:
            result = eval(cond_expr)
            if mode=='debug':
                print(f"[DEBUG] Condition '{cond_expr}' évaluée à {result}")
    except Exception as e:
            print(f"[!] Erreur dans la condition: {e}")
            result = False
    # Exécute la bonne branche
    branch = if_block if result else else_block
    for child in branch["children"]:
            engine(template, variables, mode, {"type": "root", "children": [child]})
        