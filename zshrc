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
plugins=(git brew pip django ruby sublime osx rvm rake vagrant)

# Source oh-my-zsh
source $ZSH/oh-my-zsh.sh

# Source custom theme
source "$ZSH_CUSTOM/themes/$MY_ZSH_THEME.zsh-theme"


# -------------- #
#      PATH      #
# -------------- #

export PATH="$HOME/.dotfiles/bin:$HOME/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/share/python:/usr/local/git/bin:/usr/local/gnat/bin"


# -------------- #
#   Ruby Stuff   #
# -------------- #

# Load RVM if it exists
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"


# ---------------------- #
#    virtualenvwrapper   #
# ---------------------- #

export WORKON_HOME=~/.virtualenvs

# http://hmarr.com/2010/jan/19/making-virtualenv-play-nice-with-git/

source /usr/local/share/python/virtualenvwrapper_lazy.sh

# source ~/.autoenv/activate.sh

## Tying to pip’s virtualenv support
# Via http://becomingguru.com/:
# Add this to your shell login script to make pip use the same directory for virtualenvs as virtualenvwrapper:

export PIP_VIRTUALENV_BASE=$WORKON_HOME

# and Via Nat:
# in addition to what becomingguru said, this line is key:

export PIP_RESPECT_VIRTUALENV=true

# That makes pip detect an active virtualenv and install to it, without having to pass it the -E parameter.


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
alias lt='echo "--Newest--" && ls -Alht && echo "--Oldest--"'
alias ltr='echo "--Oldest--" && ls -Alhrt && echo "--Newest--"'

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

# ZSH Fixes
alias rake='noglob rake'
