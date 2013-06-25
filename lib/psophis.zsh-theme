ZSH_THEME_GIT_PROMPT_PREFIX="[git:"
ZSH_THEME_GIT_PROMPT_SUFFIX="]%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[red]%}✘"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[green]%}✔"

#Customized git status, oh-my-zsh currently does not allow render dirty status before branch
function git_custom_status() {
  local cb=$(current_branch)
  if [ -n "$cb" ]; then
    echo " $(parse_git_dirty)$ZSH_THEME_GIT_PROMPT_PREFIX$(current_branch)$ZSH_THEME_GIT_PROMPT_SUFFIX"
  fi
}

function rvm_promt_version {
  if $THEME_RUBY; then
    echo " %{$fg[red]%}\[$(~/.rvm/bin/rvm-prompt)\]%{$reset_color%}"
  fi
}

function user_host() {
  echo "$fg[cyan]%n@%m%{$reset_color%}"
}

function get_pwd() {
  echo " $fg[yellow]%~%{$reset_color%}"
}

function virtualenv_promt_info(){
  local virtualenv_path="$VIRTUAL_ENV"
  if [[ -n $virtualenv_path ]]; then
    local virtualenv_name=`basename $virtualenv_path`
    print " %{${fg[blue]}%}[$virtualenv_name]"
  fi
}

export VIRTUAL_ENV_DISABLE_PROMPT=1

function precmd() {
  print -rP "$(user_host)$(git_custom_status)$(virtualenv_promt_info)$(rvm_promt_version)$(get_pwd)"
}

PROMPT='%(?.%{$fg[green]%}.%{$fg[red]%})➜%{$reset_color%} '
