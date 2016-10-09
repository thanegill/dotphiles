#!/usr/bin/env zsh

# Theme options
THEME_RUBY="false"

PROMPT_GIT_PREFIX="[git:"
PROMPT_GIT_SUFFIX="]%{$reset_color%}"
PROMPT_GIT_DIRTY="%{$fg[red]%}✘"
PROMPT_GIT_CLEAN="%{$fg[green]%}✔"

# Setup the prompt with pretty colors
setopt prompt_subst

# Checks if working tree is dirty
function parse_git_dirty() {
  local STATUS=''
  local FLAGS
  FLAGS=('--porcelain')
  if [[ "$(command git config --get oh-my-zsh.hide-dirty)" != "1" ]]; then
    if [[ $POST_1_7_2_GIT -gt 0 ]]; then
      FLAGS+='--ignore-submodules=dirty'
    fi
    if [[ "$DISABLE_UNTRACKED_FILES_DIRTY" == "true" ]]; then
      FLAGS+='--untracked-files=no'
    fi
    STATUS=$(command git status ${FLAGS} 2> /dev/null | tail -n1)
  fi
  if [[ -n $STATUS ]]; then
    echo "$PROMPT_GIT_DIRTY"
  else
    echo "$PROMPT_GIT_CLEAN"
  fi
}

# Outputs the name of the current branch
# Usage example: git pull origin $(git_current_branch)
# Using '--quiet' with 'symbolic-ref' will not cause a fatal error (128) if
# it's not a symbolic ref, but in a Git repo.
function git_current_branch() {
  local ref
  ref=$(command git symbolic-ref --quiet HEAD 2> /dev/null)
  local ret=$?
  if [[ $ret != 0 ]]; then
    [[ $ret == 128 ]] && return  # no git repo.
    ref=$(command git rev-parse --short HEAD 2> /dev/null) || return
  fi
  echo ${ref#refs/heads/}
}

# Customized git status, oh-my-zsh currently does not allow render dirty status before branch
function git_custom_status() {
    local cb=$(git_current_branch)
    if [ -n "$cb" ]; then
        echo " $(parse_git_dirty)$PROMPT_GIT_PREFIX${cb}$PROMPT_GIT_SUFFIX"
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
        print "%{${fg[blue]}%}[venv:$virtualenv_name]"
    fi
}

function is_ssh() {
    if [[ -n $SSH_TTY || -n $SSH_CONNECTION || -n $SSH_CLIENT ]]; then
        echo "$fg[red]ssh %{$reset_color%}"
    fi

}

export VIRTUAL_ENV_DISABLE_PROMPT=1

ASYNC_PROC=0
function precmd() {
    function async() {
        # save to temp file
        printf "%s" "$(is_ssh)$(user_host)$(git_custom_status)$(virtualenv_promt_info)$(rvm_promt_version)$(get_pwd)" > "${ZDOTDIR}/.zsh_tmp_prompt"

        # signal parent
        kill -s USR1 $$
    }

    # kill child if necessary
    if [[ "${ASYNC_PROC}" != 0 ]]; then
        kill -s HUP $ASYNC_PROC >/dev/null 2>&1 || :
    fi

    # start background computation
    async &!
    ASYNC_PROC=$!
}

function TRAPUSR1() {
    # read from temp file
    # Clear entire line and go to begging of line
    print -P "\033[2K\r$(cat ${ZDOTDIR}/.zsh_tmp_prompt)"
    rm "${ZDOTDIR}/.zsh_tmp_prompt"
    # reset proc number
    ASYNC_PROC=0

    # redisplay
    zle && zle reset-prompt
}

PROMPT='%(?.%{$fg[green]%}.%{$fg[red]%})➜%{$reset_color%} '
