#!/bin/bash

SESSION="SHADOW"

# Vérifie si la session existe déjà
tmux has-session -t $SESSION 2>/dev/null
if [ $? != 0 ]; then

    # Crée une nouvelle session détachée avec le shell interactif
    tmux new-session -d -s $SESSION "TMUX_SESSION=$SESSION python3 -m shell.main_shell.py"

    # Configuration tmux pour cette session uniquement
    # Active la status bar
    tmux set -g status on

    # Couleur du bandeau en bas
    tmux set -g status-bg colour93    # violet
    tmux set -g status-fg white       # texte blanc

    # Fenêtres actives
    tmux set-window-option -g window-status-current-style bg=colour93,fg=white

    # Fenêtres inactives
    tmux set-window-option -g window-status-style bg=black,fg=white

    # Bordures de panes (séparateur entre gauche/droite)
    tmux set -g pane-border-style fg=colour93        # bordure inactive = violet
    tmux set -g pane-active-border-style fg=colour93 # bordure active = violet

    # Couleur de l'indicateur de scroll (mode copie) en violet
    tmux set -g mode-style bg=colour93,fg=white

    # Activer le scroll avec la molette
    tmux set -g mouse on

    # Mode de copie plus naturel
    tmux setw -g mode-keys vi

    # Scroll avec la molette sans entrer en mode copie
    tmux bind -n WheelUpPane if-shell -F -t = "#{mouse_any_flag}" "send-keys -M" "if -Ft= '#{pane_in_mode}' 'send-keys -M' 'select-pane -t=; copy-mode -e; send-keys -M'"
    tmux bind -n WheelDownPane select-pane -t= \; send-keys -M

    # Split vertical pour le dashboard (30% largeur) à droite
    tmux split-window -h -p 30 -t $SESSION "python3 dashboard/dashboard.py"

    # Sélectionne le pane gauche (shell) par défaut
    tmux select-pane -t $SESSION:0.0

    # Verrouille le pane du dashboard pour empêcher la saisie clavier
    tmux lock-pane -t $SESSION:0.1

    # Optionnel : désactive Ctrl+b o pour passer d’un pane à l’autre
    # (empêche de naviguer vers le dashboard)
    tmux unbind o

fi

# Attache la session
tmux attach -t $SESSION
