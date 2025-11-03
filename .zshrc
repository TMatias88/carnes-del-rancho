# -----------------------------
# Configuración básica de la terminal (ZSH)
# -----------------------------

# Activar colores en la terminal
export CLICOLOR=1
export LSCOLORS=GxFxCxDxBxegedabagaced

# Alias útiles (opcional)
alias ll='ls -lah'
alias gs='git status'
alias py='python3'

# -----------------------------
# PATH para Postgres.app
# -----------------------------
# ⚠️ Ajusta el número de versión si tu Postgres.app usa 17 o 18
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/18/bin

# -----------------------------
# Python virtual environments
# -----------------------------
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source /usr/local/bin/virtualenvwrapper.sh 2>/dev/null || true

# -----------------------------
# Fin del archivo
# -----------------------------

