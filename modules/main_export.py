import argparse
import json
from pathlib import Path
import sys
from pyfiglet import Figlet

current_bin = Path(__file__).resolve()
data_dir = current_bin.parent / f"{current_bin.name}_data"
if data_dir.exists():
    sys.path.insert(0, str(data_dir))




from modules.engine import main_engine

def print_ascii_banner(tool_name):
    if Figlet:
        f = Figlet(font='slant')
        print(f.renderText(tool_name))
    else:
        print(f"*** {tool_name} ***")
    print("      powered by Buzz\n")



def clean_var(v):
    return v.replace("{{", "").replace("}}", "").strip()

def main():

    

    # Charger la conf
    config_path = data_dir / "conf.json"
    with open(config_path, "r") as f:
        conf = json.load(f)

    # Charger la template en texte brut
    template_path = data_dir / "template.txt"
    with open(template_path, "r") as f:
        template = f.read()

    parser = argparse.ArgumentParser(description="Dynamic workflow runner")
    # Ajouter dynamiquement les arguments si présents
    

    for var in conf.get("inputs", []):
        clean = clean_var(var)
        parser.add_argument(f"-{clean}" , f"--{clean}", required=True, help=f"Input variable: {clean}")

    args = parser.parse_args()
    
    variables = {clean_var(var): getattr(args, clean_var(var)) for var in conf.get("inputs", [])}

    
    return template, variables

if __name__ == "__main__":
    print_ascii_banner(current_bin.name)
    template, variables = main()
    main_engine(template, variables)