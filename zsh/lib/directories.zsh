# Basic directory operations
alias -- -='cd -'

setopt auto_name_dirs
setopt auto_cd

alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias cd..='cd ..'
alias cd...='cd ../..'
alias cd....='cd ../../..'
alias cd.....='cd ../../../..'
alias cd/='cd /'

cd () {
  if   [[ "x$*" == "x..." ]]; then
    cd ../..
  elif [[ "x$*" == "x...." ]]; then
    cd ../../..
  elif [[ "x$*" == "x....." ]]; then
    cd ../../../..
  elif [[ "x$*" == "x......" ]]; then
    cd ../../../../..
  else
    builtin cd "$@"
  fi
}
