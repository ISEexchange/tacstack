# http_proxy
proxy_url="http://proxy.inf.ise.com:3128"

# ftp_proxy (but you should prefer to use hftp:// for ftp-over-http)
ftp_proxy_url="http://proxy.inf.ise.com:8021"

# Some things should not be proxied.
#   http://www.w3.org/Daemon/User/Proxies/ProxyClients.html
# CAUTION: some client don't support no_proxy
export no_proxy="localhost.localdomain,localhost,127.0.0.1"

export http_proxy="$proxy_url"
export HTTP_PROXY="$proxy_url"
export https_proxy="$proxy_url"
export HTTPS_PROXY="$proxy_url"
export ftp_proxy="$ftp_proxy_url"
export FTP_PROXY="$ftp_proxy_url"
export ALL_PROXY="$proxy_url"

# vi aliases
alias vbrc='vi ~/.bashrc'

# svn aliases
alias svs='svn status'
alias svd='svn diff'
alias svc='svn commit '
alias svu='svn update'
alias sva='svn add'

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
