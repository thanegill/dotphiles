#!/bin/bash

if [ -d ~/.dotfiles ]
then
  echo "\033[0;33mYou already have a .dotfiles directory.\033[0m You'll need to remove ~/.dotfile if you want to install"
  exit
fi


echo "\033[0;34mCloning your dotfiles...\033[0m"
hash git >/dev/null && /usr/bin/env git clone --recursive https://github.com/psophis/dotfiles ~/.dotfiles || {
  echo "git not installed"
  exit
}


#Install theme
echo "\033[0;34mInstalling theme...\033[0m"
mkdir -p ~/.dotfiles/oh-my-zsh/custom/themes/
cd ~/.dotfiles/oh-my-zsh/custom/themes/
curl -O https://gist.github.com/psophis/5297937/raw/psophis.zsh-theme



#Link files
echo "\033[0;34mSymlinking your dotfiles...\033[0m"
cd ~
ln -s ~/.dotfiles/gitconfig .gitconfig
ln -s ~/.dotfiles/gitignore_global .gitignore_global
ln -s ~/.dotfiles/oh-my-zsh .oh-my-zsh
ln -s ~/.dotfiles/vimrc .vimrc
ln -s ~/.dotfiles/zshrc .zshrc

chsh -s `which zsh`

echo "\n\n \033[0;32mYour dotfiles are now installed.\033[0m"

/usr/bin/env zsh

# Source zshrc
source ~/.zshrc
