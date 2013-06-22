# -------------------- #
#   OH-MY-ZSH Config   #
# -------------------- #

# Path to your oh-my-zsh configuration.
ZSH=$HOME/.dotfiles/oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="psophis"
THEME_RUBY=false

MY_ZSH_THEME=$ZSH_THEME; ZSH_THEME=''

# ZSH_CUSTOM=~/.oh-my-zsh/custom/themes



# export EDITOR="$HOME/.scripts/editor.sh" #TODO
export EDITOR=vim

# Set to this to use case-sensitive completion
# CASE_SENSITIVE="true"

# Comment this out to disable weekly auto-update checks
# DISABLE_AUTO_UPDATE="true"

# Uncomment following line if you want to disable colors in ls
# DISABLE_LS_COLORS="true"

# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment following line if you want red dots to be displayed while waiting for completion
COMPLETION_WAITING_DOTS="true"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
plugins=(git pip brew django ruby sublime ruby osx rvm rake)

source $ZSH/oh-my-zsh.sh

source "$ZSH_CUSTOM/themes/$MY_ZSH_THEME.zsh-theme"
# Customize to your needs...
export PATH="$HOME/.dotfiles/bin:$HOME/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/share/python:/usr/local/git/bin:/usr/local/gnat/bin"


# -------------- #
#   Ruby Stuff   #
# -------------- #

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM


# ---------------------------- #
#   python virtualenvwrapper   #
# ---------------------------- #

WORKON_HOME=~/.virtualenv/

# http://hmarr.com/2010/jan/19/making-virtualenv-play-nice-with-git/

# Automatically activate Git projects' virtual environments based on the
# directory name of the project. Virtual environment name can be overridden
# by placing a .venv file in the project root with a virtualenv name in it

function workon_cwd {
    # Check that this is a Git repo
    GIT_DIR=`git rev-parse --git-dir 2> /dev/null`
    if [ $? == 0 ]; then
        # Find the repo root and check for virtualenv name override
        GIT_DIR=`\cd $GIT_DIR; pwd`
        PROJECT_ROOT=`dirname "$GIT_DIR"`
        ENV_NAME=`basename "$PROJECT_ROOT"`
        if [ -f "$PROJECT_ROOT/.venv" ]; then
            ENV_NAME=`cat "$PROJECT_ROOT/.venv"`
        fi
        # Activate the environment only if it is not already active
        if [ "$VIRTUAL_ENV" != "$WORKON_HOME/$ENV_NAME" ]; then
            if [ -e "$WORKON_HOME/$ENV_NAME/bin/activate" ]; then
                workon "$ENV_NAME" && export CD_VIRTUAL_ENV="$ENV_NAME"
            fi
        fi
    elif [ $CD_VIRTUAL_ENV ]; then
        # We've just left the repo, deactivate the environment
        # Note: this only happens if the virtualenv was activated automatically
        deactivate && unset CD_VIRTUAL_ENV
    fi
}

# New cd function that does the virtualenv magic
function venv_cd {
    cd "$@" && workon_cwd
}

alias cd="venv_cd"

# ------------------ #
#   Custom Aliases   #
# ------------------ #

# http://brettterpstra.com/2013/03/31/a-few-more-of-my-favorite-shell-aliases/
# http://brettterpstra.com/2013/03/14/more-command-line-handiness/

# Open Apps
alias byword='open -a "/Applications/Byword.app"'
alias ql="qlmanage -p &>/dev/null"
alias finder="open ."

# List direcory contents - ls
alias l='ls -Alh'
alias lt='ls -At1 && echo "------Oldest--"'
alias ltr='ls -Art1 && echo "------Newest--"'

# cd to the path of the front Finder window
cdf() {
    target=`osascript -e 'tell application "Finder" to if (count of Finder windows) > 0 then get POSIX path of (target of front Finder window as text)'`
    if [ "$target" != "" ]; then
        cd "$target"; unset target
    else
        echo 'No Finder window found' >&2
    fi
}

# Make executable
alias ax="chmod a+x"

# Get your current public IP
alias ip="curl icanhazip.com"

# list TODO/FIX lines from the current project
alias todos="ack --recurse --group '(TODO|XXX|BUG|HACK|FIX(ME)?):'"

# Open config files
alias zshconfig='subl -w ~/.zshrc'
alias ohmyzsh='subl -w ~/.oh-my-zsh'

# ZSH Fixes
alias rake='noglob rake'
