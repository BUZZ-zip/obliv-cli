import json
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich.layout import Layout

from datetime import datetime


DASHBOARD_DIR = Path("dashboard")
DASHBOARD_FILE = DASHBOARD_DIR / "dashboard_state.json"
DASHBOARD_DIR.mkdir(exist_ok=True)

console = Console()

def load_dashboard():
    """Charge le JSON depuis le fichier."""
    if DASHBOARD_FILE.exists():
        try:
            with open(DASHBOARD_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def render_dashboard():
    """Rendu du dashboard selon l'action."""
    data = load_dashboard()

    client_info = data.get("client_info", {})

    if "Username" not in client_info:
        username = data.get("username", "-")
        client_info["Username"] = username

    if "API Key" not in client_info:
        api_key = data.get("api_key", "-")
        client_info["API Key"] = api_key

    if "Workflows" not in client_info:
        workflows_nb = data.get("workflows_nb", "-")
        client_info["Workflows"] = workflows_nb

    if "Cli version" not in client_info:
        cli_version = data.get("cli_version", "-")
        client_info["Cli version"] = cli_version


    keys = ["Username", "API Key", "Workflows", "Cli version"]
    panels = []
    
    for k in keys:
        val = client_info.get(k, "-")
        panels.append(Panel(Align.center(f"[bold]{val}"), title=f"[magenta]{k}[/magenta]", expand=False,))
    
    client_boxes = Align.center(Columns(panels, expand=True, equal=False))


    workflows = data.get("workflows", [])
    last_workflows = workflows[-16:] if len(workflows) > 16 else workflows[-16:]
    wf_table = Table(title="", expand=True)
    wf_table.add_column("Index", style="cyan", no_wrap=True)
    wf_table.add_column("Workflow Name", style="magenta")
    for idx, wf in enumerate(last_workflows, 1):
        wf_table.add_row(str(idx), str(wf))


    # 3. Last Execution Panel (all info from JSON)
    workflow = data.get("current_workflow", "Inconnu")
    mode = data.get("mode", "N/A")
    variables = data.get("variables", {})
    status = data.get("status", "En attente")
    start_time = data.get("start_time")  # datetime au format ISO
    number_node = data.get("number_node", 0)
    current_node = data.get("current_node", 0)
    elapsed = data.get("elapsed", "-")

    # Calcul du pourcentage
    progress_percent = (
        f"{int((current_node / number_node) * 100)}%"
        if number_node else "0%"
    )


    elapsed = "-"
    if start_time:
        if status == "Completed":
            # On affiche uniquement la valeur sauvegardée dans le JSON
            elapsed = data.get("elapsed", "-")
        else:
            # Workflow en cours → on calcule en live
            try:
                start_dt = datetime.fromisoformat(start_time)
                elapsed = str(datetime.now() - start_dt).split(".")[0]
            except Exception:
                elapsed = "-"


    last_exec_info = (
        f"[magenta]Mode:[/magenta] [white]{data.get('mode', '-')}\n"
        f"[magenta]Variables:[/magenta] [white]{data.get('variables', '-')}\n"
        f"[magenta]Status:[/magenta] [white]{data.get('status', '-')}\n"
        f"[magenta]Nodes:[/magenta] [white]{data.get('current_node', '-')}/{data.get('number_node', '-')}[/white]\n"
        f"[magenta]Progress:[/magenta] [white]100%[/white]\n"
        f"[magenta]Time:[/magenta] [white]{data.get('elapsed', '-')}\n"
    )


    panel = Panel(
        last_exec_info,
        title=f'Workflow: {data.get("current_workflow", "-")}',
        expand=True,
        padding=(1, 2)
    )
       


    
    layout = Layout()

    layout.split_column(
        Layout(Panel(client_boxes, title="Client Info", expand=False, height=5), name="client", size=5),
        Layout(Panel(wf_table, title="Recent Workflows", expand=True), name="workflows"),
        Layout(Panel(panel, title="Last Execution", expand=True, padding=(2, 2)), name="execution" ),
    )
    return layout

if __name__ == "__main__":
    with Live(render_dashboard(), refresh_per_second=1, screen=True) as live:
        while True:
            time.sleep(1)
            live.update(render_dashboard())
