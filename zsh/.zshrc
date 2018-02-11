# Reset $PATH if path_helper exists, path_helper fucks up the path on macOS,
# which is called in /etc/zprofile
if [ -f /usr/libexec/path_helper ]; then
    source $ZDOTDIR/zshenv
fi

# Set to this to use case-sensitive completion
# CASE_SENSITIVE="true"

# Comment this out to disable weekly dotphiles auto-update checks
# DOTPHILES_AUTO_UPDATE="false"

# Uncomment the following line to change how often to auto-update dotphiles (in days).
# export UPDATE_DOTPHILES_DAYS=13

# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment following line if you want red dots to
# be displayed while waiting for completion
COMPLETION_WAITING_DOTS="true"

# Which plugins would you like to load?
# (plugins can be found in ~/.dotphiles/zsh/plugins/*)
# Custom plugins may be added to ~/.dotphiles/zsh/custom/plugins/
plugins=(\
    solarized-man \
    zsh-completions \
)

# If OSX add these plugins as well.
if [[ "$OSTYPE" == "darwin"* ]]; then
    plugins+=( \
        pod \
    )
fi

# Load plugins
source $ZDOTDIR/load-plugins.zsh
# Load theme
source $ZDOTDIR/prompt.zsh
# Set $EDITOR
source $ZDOTDIR/editor.zsh
# Load Aliases
source $ZDOTDIR/aliases.zsh
# Check for dotphiles update
source $ZDOTDIR/update-dotphiles.zsh

# Load RVM into a shell session as a function
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"

