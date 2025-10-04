from modules.utils import get_uid_and_variables
from modules.get_template import get_workflow
from modules.engine import main_engine






def run_workflow(*args):

    try:
        if len(args) < 2:
            return "Usage: run -name <nom> | run -uid <uid> | run -number <num> [params...]"
        mode = args[0]
        value = args[1]
        params = args[2:] if len(args) > 2 else []
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
            return "Usage: run -name <nom> | run -uid <uid> | run -number <num> [params...]"
        if not uid and doublons:
            return ""  # Ne rien afficher si doublons
        if not uid and not doublons:
            return "Workflow introuvable."
        if not uid:  # Vérification supplémentaire
            return "UID du workflow non trouvé."

        if variables and not params:
            def clean_var(v):
                return v.replace("{{","").replace("}}","").strip()
            cleaned_vars = [clean_var(v) for v in variables]
            var_str = " ".join(f"-{v} <valeur>" for v in cleaned_vars)
            return f"Ce workflow attend des variables : {', '.join(cleaned_vars)}\nExemple : run {mode} {value} {var_str}"
        # Adapter les params pour enlever le tiret devant le nom de variable
        param_dict = {}
        for i in range(0, len(params), 2):
            if i+1 < len(params):
                key = params[i].lstrip('-')
                value = params[i+1]
                param_dict[key] = value
        
        
        template = get_workflow(name=None, id=uid)
        
        if not template:
            return "Impossible de récupérer le template du workflow. Vérifiez votre authentification et que le workflow existe."
        
        main_engine(template, param_dict)

    except Exception as e:
        return f"Erreur lors de l'exécution du workflow : {e}"
