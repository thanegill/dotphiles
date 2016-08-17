#!/usr/bin/env zsh

is_plugin() {
    local base_dir=$1
    local name=$2
    test -f $base_dir/plugins/$name/$name.plugin.zsh \
        || test -f $base_dir/plugins/$name/_$name
}

# Add a function path
fpath=($ZDOTDIR/functions $ZDOTDIR/completions $fpath)

# Load all of the config files in $ZDOTDIR/lib that end in .zsh
# TIP: Add files you don't want in git to .gitignore
for config_file ($ZDOTDIR/lib/*.zsh); do
    source $config_file
done

# Add all defined plugins to fpath. This must be done
# before running compinit.
for plugin ($plugins); do
    if is_plugin $ZDOTDIR $plugin; then
        fpath=($ZDOTDIR/plugins/$plugin $fpath)
    fi
done

# Save the location of the current completion dump file.
ZSH_COMPDUMP="${ZDOTDIR:-${HOME}}/.zcompdump"

# Load and run compinit
autoload -U compinit
compinit -i -d "${ZSH_COMPDUMP}"

# Load all of the plugins that were defined in .zshrc
for plugin ($plugins); do
    if [ -f $ZDOTDIR/plugins/$plugin/$plugin.plugin.zsh ]; then
        source $ZDOTDIR/plugins/$plugin/$plugin.plugin.zsh
    fi
done

unset config_file
unset -f is_plugin

