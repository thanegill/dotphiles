# Use neovim instead of vim if installed or vi if all else fails
if hash nvim >/dev/null 2>&1; then
    export EDITOR=nvim
elif hash vim >/dev/null 2>&1; then
    export EDITOR=vim
else
    export EDITOR=vi
fi
