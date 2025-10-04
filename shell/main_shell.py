import cmd
import subprocess
import os
import json
import shlex
import signal
from datetime import datetime
import urllib.request

from modules.keysetup import authenticate, auth_request, get_saved_username
from modules.get_template import get_saved_api_key
from modules.list_workflow import get_workflow_table, list_workflow
from modules.execute_workflow import run_workflow
from modules.export_workflow import export
from modules.utils import save_dashboard_info,mask_api_key


def signal_handler(sig, frame):
    """Gestionnaire pour Ctrl+C - affiche un message et le prompt au prompt principal"""
    print()
    print(f"\nUse 'exit' to quit the application.")
    print()
    # Affiche le prompt si on a accès à l'instance shell courante
    if hasattr(signal_handler, 'shell') and signal_handler.shell:
        print(signal_handler.shell.prompt, end='', flush=True)
    return


def command_interrupt_handler(sig, frame):
    """Gestionnaire pour Ctrl+C pendant les commandes - lance une exception"""
    raise KeyboardInterrupt


# Ne pas configurer le gestionnaire de signal ici - on le fera dans cmdloop




def get_local_version():
    try:
        with open(os.path.join(os.path.dirname(__file__), '../VERSION'), 'r') as f:
            value = f.read().strip()
            # print(value)  # Remove or comment out debug print
            return value
    except Exception:
        return None

def get_remote_version():
    url = 'https://raw.githubusercontent.com/BUZZ-zip/obliv-cli/refs/heads/main/VERSION'
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            value = response.read().decode('utf-8').strip()
            # print(value)  # Remove or comment out debug print
            return value
    except Exception:
        return None

def check_update_message():
    local = get_local_version()
    remote = get_remote_version()
    if local and remote and local != remote:
        print(f"Update available: Version {remote} (you have version {local})")
        print("Type 'update' to update the client.\n")


class ForSShell(cmd.Cmd):
    # ANSI color codes
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    MAGENTA = '\033[35m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    


    try:
        api_key = get_saved_api_key()
        username = get_saved_username()
        save_dashboard_info({"action": "render_user", "username": username if username else "anonymous"})
        masked_api_key = mask_api_key(api_key) if api_key else "no"
        save_dashboard_info({"action": "render_user", "api_key": masked_api_key})

        save_dashboard_info({"action": "render_user", "cli_version": "1.0.0"})

        signal.signal(signal.SIGINT, command_interrupt_handler)
        if api_key and auth_request(api_key):
            intro = (
                "Welcome to Obliv. Type 'help' to see available commands.\n"
                "To copy text, use Shift + select with your mouse.\n"
            )
            prompt = f"{MAGENTA}{username}@obliv{RESET}:{BLUE}~{RESET}$ "
            workflow_list = list_workflow()
        else:
            intro = (
                "Welcome to Obliv. Type 'help' to see available commands.\n"
                "To copy text, use Shift + select with your mouse.\n"
            )
            prompt = f"{MAGENTA}anonymous@obliv{RESET}:{BLUE}~{RESET}$ "
    except KeyboardInterrupt:
        print(f"\nUse 'exit' to quit the application.")
    except Exception as e:
        print(f"Error during shell initialization: {e}")
        intro = "Welcome to Obliv. Type 'help' to see available commands.\n"
        prompt = f"{MAGENTA}anonymous@obliv{RESET}:{BLUE}~{RESET}$ "
    finally:
        signal.signal(signal.SIGINT, signal_handler)
    

    def emptyline(self):
        """Override emptyline to do nothing instead of repeating last command"""
        pass

    def cmdloop(self, intro=None):
        """Override cmdloop to handle KeyboardInterrupt gracefully and print intro only once at startup."""
        # Attach self to signal_handler so it can print the prompt
        signal_handler.shell = self
        if intro:
            print(intro)
        check_update_message()
            
        while True:
            try:
                signal.signal(signal.SIGINT, signal_handler)
                super().cmdloop(None)
                break
            except KeyboardInterrupt:
                continue

    # ---------- Commands ----------

    def do_help(self, arg):
        """Display the list of commands"""
        print()
        print("Available commands:")
        print("- help: display this help")
        print("- clear: clear the screen")
        print("- exit: quit the application")
        print("- auth <key>: authenticate the user with API key")
        print("- showall: display all workflows")
        print("- refresh: refresh the workflow list")
        print("- run -name <name> | run -uid <uid> | run -number <num> [params...]: execute a workflow")
        print("- export -name <name> -binary_name <binary_name>: export a workflow")
        print("- update: update the client")
        print()
        
        

    def do_exit(self, arg):
        """Exit ForS and close the tmux session"""
        print("Exiting the application...")
        session = os.environ.get("TMUX_SESSION", "fors")
        try:
            subprocess.run(["tmux", "kill-session", "-t", session])
        except Exception as e:
            print(f"Unable to kill tmux: {e}")
        return True

    def do_auth(self, arg):
        """Authenticate the user with an API key"""
        print()
        
        # Vérification si une clé API est fournie
        if not arg.strip():
            print("Usage: auth <key>")
            print()
            return
        
        # Utiliser notre gestionnaire personnalisé pendant l'authentification
        signal.signal(signal.SIGINT, command_interrupt_handler)
        
        try:
            result = authenticate(arg)
            timestamp = datetime.now().strftime("[%H:%M:%S]")
            if result:
                username = get_saved_username() or "user"
                print(f"{timestamp} Authentication successful")
                
                self.prompt = f"{self.MAGENTA}{username}@obliv{self.RESET}:{self.BLUE}~{self.RESET}$ "
            else:
                print(f"{timestamp} Authentication failed")
        except KeyboardInterrupt:
            print(f"\nAuthentication interrupted")
        except Exception as e:
            timestamp = datetime.now().strftime("[%H:%M:%S]")
            print(f"{timestamp} Error during authentication: {e}")
        finally:
            # Remettre notre gestionnaire principal
            signal.signal(signal.SIGINT, signal_handler)

        print()

    def do_showall(self, arg):
        """Display all workflows"""
        print()
        print(get_workflow_table())
        print()


    def do_run(self, arg):
        """Execute a shell command"""
        print()
        if not arg.strip():
            print("Usage: run -name <name> [params...] \n       run -uid <uid> [params...] \n       run -number <num> [params...]")
            print()
            return

        # Utiliser notre gestionnaire personnalisé pendant l'exécution
        signal.signal(signal.SIGINT, command_interrupt_handler)
        
        try:
            args = shlex.split(arg)
            result = run_workflow(*args)
            
            if result is not None:
                print(result)
        except KeyboardInterrupt:
            print(f"\nCommand interrupted")
        finally:
            # Remettre notre gestionnaire principal
            signal.signal(signal.SIGINT, signal_handler)
        
        print()
        workflow_list = list_workflow()
        save_dashboard_info({"action": "render_list", "workflows": workflow_list})
        
    def do_refresh(self, arg):
        """Refresh the workflow list"""
        workflow_list = list_workflow()
        save_dashboard_info({"action": "render_list", "workflows": workflow_list})
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        print()
        print(f"{timestamp} Workflow list refreshed")
        print()


    def do_clear(self, arg):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')


    def do_export(self, arg):
        if not arg.strip():
            print()
            print("Usage: export -name <name> -binary_name <binary_name> \n       export -uid <uid> -binary_name <binary_name> \n       export -number <num> -binary_name <binary_name>")
            print()
            return

        # Utiliser notre gestionnaire personnalisé pendant l'exécution
        signal.signal(signal.SIGINT, command_interrupt_handler)
        try:
            args = shlex.split(arg)
            result = export(*args)
            if result is not None:
                print(result)
                print()
        except KeyboardInterrupt:
            print(f"\nCommand interrupted")
            print()
        finally:
            # Remettre notre gestionnaire principal
            signal.signal(signal.SIGINT, signal_handler)
            


    def do_update(self, arg):
        """Update the client"""
        print("\nUpdating client...")
        try:
            import subprocess
            result = subprocess.run([
                "git", "pull", "origin", "main"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            if 'Already up to date' in result.stdout:
                print("\033[93mClient is already up to date.\033[0m")
            else:
                print("\033[92mClient updated successfully. Restarting...\033[0m")
                import sys, os
                python = sys.executable
                os.execv(python, [python] + sys.argv)
        except subprocess.CalledProcessError as e:
            print("Error during update:", e.stderr)
        except Exception as e:
            print("Error during update:", e)


    # ---------- Handle unknown commands ----------
    def default(self, line):
        print()
        print(f"{line} : command not found")
        print()





ForSShell().cmdloop()


