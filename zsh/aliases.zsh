# No arguments: `git status`
# With arguments: acts like `git`
function g() {
    if [[ $# > 0 ]]; then
        git $@
    else
        git st
    fi
}

# Complete g like git
compdef g=git

# Alias vi to $EDITOR
alias vi=$EDITOR

# Edit zshrc
alias zshrc="$EDITOR $ZDOTDIR/.zshrc"

# Alias xdg-open to open if xdg-open exist
hash xdg-open >/dev/null 2>&1 && alias open='xdg-open'

# Recursively delete `.DS_Store` files
alias clean_DS_Store="find . -name '*.DS_Store' -type f -ls -delete"

# OSX Specific aliases
if [[ "$OSTYPE" == "darwin"* ]]; then
    # Open Apps
    alias quicklook="qlmanage -p &>/dev/null"
    alias ql="quicklook"
    alias finder="open ."

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

    # cd to the path of the front Finder window
    cdf() {
        local target=`osascript -e 'tell application "Finder" to if (count of Finder windows) > 0 then get POSIX path of (target of front Finder window as text)'`
        if [ "$target" != "" ]; then
            cd "$target"; unset target
        else
            echo 'No Finder window found' >&2
        fi
    }
fi

# Set <Caps Lock> to <Ctrl> and single press <Ctrl> to <Esc>
if [[ "$OSTYPE" != "darwin"* ]]; then
    if hash xcape >/dev/null 2>&1; then
        setxkbmap -option 'caps:ctrl_modifier'
        xcape -e 'Caps_Lock=Escape;Control_L=Escape;Control_R=Escape'
    fi
fi

# List directory contents - ls
if $(ls --version >/dev/null 2>&1) && [[ "$(ls --version)" = *"GNU"* ]]; then
    # GNU ls
    alias ls='ls --color=always'
    alias ll='ls --color=always --format=long --human-readable'
    alias l='ls --color=always --almost-all --format=long --human-readable'
else
    # Not GNU ls
    alias ll='ls -lh'
    alias l='ls -Alh'
fi

# Make executable
alias ax="chmod a+x"

# Get current public IP
alias externalip="curl icanhazip.com"

# list TODO lines from the current project
alias todos="ack --recurse --group '(TODO|todo|Todo|XXX|BUG|HACK|FIX(ME)?):'"

function rdp() {
    if hash xfreerdp >/dev/null 2>&1; then
        if [[ $# -eq  0 || $# > 2 ]]; then
            echo "Usage: rdp user host"
        else
            xfreerdp /u:$1 /v:$2 /cert-ignore /clipboard /fonts /auto-reconnect /smart-sizing:1836x1377 /size:1224x918 /home-drive -grab-keyboard
        fi
    else
        echo "xfreerdp not installed"
    fi
}
