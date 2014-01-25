# -------------------- #
#   OH-MY-ZSH Config   #
# -------------------- #

# Path to your oh-my-zsh configuration.
ZSH=$HOME/.dotfiles/oh-my-zsh

# Set name of the theme to load.
# Look in ~/.dotfiles/oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="psophis"
THEME_RUBY=false

MY_ZSH_THEME=$ZSH_THEME; ZSH_THEME=''

# ZSH_CUSTOM=~/.dotfiles/oh-my-zsh/custom/themes

export EDITOR=vim

# Set to this to use case-sensitive completion
# CASE_SENSITIVE="true"

# Comment this out to disable weekly auto-update checks
# DISABLE_AUTO_UPDATE="true"

# Uncomment following line if you want to disable colors in ls
# DISABLE_LS_COLORS="true"

# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment following line if you want red dots to
# be displayed while waiting for completion
COMPLETION_WAITING_DOTS="true"

# Which plugins would you like to load?
# (plugins can be found in ~/.dotfiles/oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.dotfiles/oh-my-zsh/custom/plugins/
plugins=(\
brew \
cloudapp \
colored-man \
cp \
django \
gem \
git \
postgres \
python \
pip \
ruby \
rsync \
osx \
rvm \
rake \
sublime \
screen \
vagrant \
web-search \
)

# Source oh-my-zsh
source $ZSH/oh-my-zsh.sh

# Source custom theme
source "$ZSH_CUSTOM/themes/$MY_ZSH_THEME.zsh-theme"


# -------------- #
#      PATH      #
# -------------- #


if [[ "$OSTYPE" == "darwin"* ]]; then
    export PATH="$HOME/.dotfiles/bin:$(brew --prefix coreutils)/libexec/gnubin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    export PYTHONPATH=$(brew --prefix)/lib/python2.7/site-packages:$PYTHONPATH
    export MANPATH=$(brew --prefix coreutils)/libexec/gnuman:$MANPATH
else
    export PATH="$HOME/.dotfiles/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    export PYTHONPATH=$(python -c 'from distutils.sysconfig import get_python_lib; print(get_python_lib())'):$PYTHONPATH
fi



# -------------- #
#   Ruby Stuff   #
# -------------- #

# Load RVM if it exists
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"


# --------------------- #
#   virtualenvwrapper   #
# --------------------- #

export WORKON_HOME=~/.virtualenvs

# http://hmarr.com/2010/jan/19/making-virtualenv-play-nice-with-git/

# Load virtualenvwrapper is it and virtualenv exists otherwise try and install
if [ $(whence virtualenv) ] && [  $(whence virtualenvwrapper.sh) ]; then
    source `whence virtualenvwrapper_lazy.sh`
else
    if [ $(whence pip) ]; then
        echo "virtualenv and or virtuallenvwarpper not installed"
    else
        echo "pip not installed"
    fi
fi

## Tying to pip’s virtualenv support
# Via http://becomingguru.com/:
# Add this to your shell login script to make pip use the same
# directory for virtualenvs as virtualenvwrapper:
export PIP_VIRTUALENV_BASE=$WORKON_HOME

# and Via Nat:
# in addition to what becomingguru said, this line is key:
export PIP_RESPECT_VIRTUALENV=true

# That makes pip detect an active virtualenv and install to it,
# without having to pass it the -E parameter.


# ------------------ #
#   Custom Aliases   #
# ------------------ #

# http://brettterpstra.com/2013/03/31/a-few-more-of-my-favorite-shell-aliases/
# http://brettterpstra.com/2013/03/14/more-command-line-handiness/

# Shortcuts
alias vi='vim'

# OSX Specific alises
if [[ "$OSTYPE" == "darwin"* ]]; then

    function trash() {
        local trash_dir="${HOME}/.Trash"
        local temp_ifs=$IFS
        IFS=$'\n'
        for item in "$@"; do
            if [[ -e "$item" ]]; then
                item_name="$(basename $item)"
                if [[ -e "${trash_dir}/${item_name}" ]]; then
                    mv -f "$item" "${trash_dir}/${item_name} $(date "+%H-%M-%S")"
                else
                    mv -f "$item" "${trash_dir}/"
                fi
            fi
        done
        IFS=$temp_ifs
    }

    # Open Apps
    alias byword='open -a "/Applications/Byword.app"'
    alias ql="qlmanage -p &>/dev/null"
    alias finder="open ."

    # Recursively delete `.DS_Store` files
    alias clean-ds_store="find . -name '*.DS_Store' -type f -ls -delete"

    # cd to the path of the front Finder window
    cdf() {
        target=`osascript -e 'tell application "Finder" to if (count of Finder windows) > 0 then get POSIX path of (target of front Finder window as text)'`
        if [ "$target" != "" ]; then
            cd "$target"; unset target
        else
            echo 'No Finder window found' >&2
        fi
    }

fi

# List direcory contents - ls
if [[ $(whence -cp ls) = "/bin/ls" ]]; then
    alias l='ls -Alh'
    alias lt='echo "--Newest--" && ls -Alht && echo "--Oldest--"'
    alias ltr='echo "--Oldest--" && ls -Alhrt && echo "--Newest--"'
else
    alias ls='ls --color=always --classify'
    alias l='ls --color=always --almost-all --format=long --human-readable --sort=none'
fi

# Make executable
alias ax="chmod a+x"

# Get your current public IP
alias ip="curl icanhazip.com"

# list TODO/FIX lines from the current project
alias todos="ack --recurse --group '(TODO|XXX|BUG|HACK|FIX(ME)?):'"
