#!/bin/bash

# Clone all to local
cd ~ 
git clone --recursive https://github.com/psophis/dotfiles .dotfiles


# #Install theme
mkdir -p ~/.dotfiles/oh-my-zsh/custom/themes/
cd $_
curl -O https://gist.github.com/psophis/5297937/raw/psophis.zsh-theme



#Link files
cd ~
ln -s .dotfiles/gitconfig .gitconfig
ln -s .dotfiles/gitignore_global .gitignore_global
ln -s .dotfiles/oh-my-zsh .oh-my-zsh
ln -s .dotfiles/vimrc .vimrc
ln -s .dotfiles/zshrc .zshrc

# Source zshrc
source .zshrc
