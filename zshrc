# Path to your oh-my-zsh configuration.
ZSH=$HOME/.oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="psophis"
THEME_RUBY=false

MY_ZSH_THEME=$ZSH_THEME; ZSH_THEME=''

# ZSH_CUSTOM=~/.oh-my-zsh/custom/themes

# export EDITOR="$HOME/.scripts/editor.sh" #TODO

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
export PATH="~/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/share/python:/usr/local/git/bin:/usr/local/gnat/bin"


# -------------- #
#   Ruby Stuff   #
# -------------- #

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM


# --------------------- #
#   Directory Aliases   #
# --------------------- #



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
alias todos="ack -n --nogroup '(TODO|FIX(ME)?):'"

# Open config files
alias zshconfig='subl -w ~/.zshrc'
alias ohmyzsh='subl -w ~/.oh-my-zsh'

# ZSH Fixes
alias rake='noglob rake'
