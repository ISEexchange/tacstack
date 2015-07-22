# vi aliases
alias vbrc='vi ~/.bashrc'
alias vi='vim'

# Find file aliases
alias fip='find . -name \*.py | xargs grep -i'
alias fia='find . -name \* | xargs grep -i'

# Linux command aliases
alias ltr='ls -ltr'
alias hg='history | grep -i '
alias lts='ls -ltr | grep -i '
alias psf='ps -ef | grep -i '
alias g='grep'
alias gi='grep -i'
alias sbrc='source ~/.bashrc'

# Aliases for controlling MAP
alias stopmap='supervisorctl stop map'
alias startmap='supervisorctl start map'
alias restartmap='supervisorctl restart map'
alias rml='rm -fv /var/log/MAPServer.log'
alias tml='tail -f /var/log/MAPServer.log'
alias cleanmap="stopmap; rml; echo 'use map_db; DELETE FROM task_queue; UPDATE template_instance SET status=2; UPDATE template SET template_status=2' | mysql"
alias launchmap='startmap; tml'

export TERM=xterm
cd /home

