#! /bin/zsh/
ZSH_THEME_GIT_PROMPT_PREFIX="[git:"
ZSH_THEME_GIT_PROMPT_SUFFIX="]%{$reset_color%}"
ZSH_THEME_GIT_PROMPT_DIRTY="%{$fg[red]%}✘"
ZSH_THEME_GIT_PROMPT_CLEAN="%{$fg[green]%}✔"

# Checks if working tree is dirty (From git plugin)
function parse_git_dirty() {
  local SUBMODULE_SYNTAX=''
  local GIT_STATUS=''
  local CLEAN_MESSAGE='nothing to commit (working directory clean)'
  if [[ "$(command git config --get oh-my-zsh.hide-status)" != "1" ]]; then
    if [[ $POST_1_7_2_GIT -gt 0 ]]; then
          SUBMODULE_SYNTAX="--ignore-submodules=dirty"
    fi
    if [[ "$DISABLE_UNTRACKED_FILES_DIRTY" == "true" ]]; then
        GIT_STATUS=$(command git status -s ${SUBMODULE_SYNTAX} -uno 2> /dev/null | tail -n1)
    else
        GIT_STATUS=$(command git status -s ${SUBMODULE_SYNTAX} 2> /dev/null | tail -n1)
    fi
    if [[ -n $GIT_STATUS ]]; then
      echo "$ZSH_THEME_GIT_PROMPT_DIRTY"
    else
      echo "$ZSH_THEME_GIT_PROMPT_CLEAN"
    fi
  else
    echo "$ZSH_THEME_GIT_PROMPT_CLEAN"
  fi
}

# From git plugin
function current_branch() {
  ref=$(git symbolic-ref HEAD 2> /dev/null) || \
  ref=$(git rev-parse --short HEAD 2> /dev/null) || return
  echo ${ref#refs/heads/}
}

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
