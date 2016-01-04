# .dotphiles
[![Build Status](https://travis-ci.org/thanegill/dotphiles.svg?branch=master)](https://travis-ci.org/thanegill/dotphiles)

My personal dot files.

## Installation

```sh
curl -L https://raw.github.com/psophis/dotphiles/master/tools/dotphiles.py | python - install
```
or
```sh
wget -q -O - https://raw.github.com/psophis/dotphiles/master/tools/dotphiles.py | python - install
```

## Usage

```sh
dotphiles [--help]
dotphiles {install, update, link, chsh} [--help]

dotphiles install [-h] [--repourl URL] [--branch BRANCH] [--home PATH]
                  [--dotphilesdir PATH] [--linkphile PATH] [--force] [--novim]
    -h, --help           show this help message and exit
    --repourl URL        URL for the dotphile repo (default:
                           "https://github.com/psophis/dotphiles.git")
    --branch BRANCH      Branch to use for cloning (default: "master")
    --home PATH          Home directory to install dotphiles to. Can be any
                           directory. (default: "~/")
    --dotphilesdir PATH  Directory name for dotphiles. (default: "~/.dotphiles")
    --linkphile PATH     File with to link dotphiles. (default:
                           "~/.dotphiles/linkphiles")
    --force              Force removal of old dotphiles and installation of vim
                           plugins.
    --novim              Do not install Vim plugins. Vundle will still be
                           install. Useful for faster install.]

dotphiles update [-h] [--branch BRANCH] [--dotphilesdir PATH] [--linkphile PATH]
                 [--novim]
    -h, --help           show this help message and exit
    --branch BRANCH      Branch to use for cloning (default: "master")
    --dotphilesdir PATH  Directory name for dotphiles. (default: "~/.dotphiles")
    --linkphile PATH     File with to link dotphiles. (default:
                           "~/.dotphiles/linkphiles")
    --novim              Do not update Vim plugins. Useful for faster update.

dotphiles link [-h] [--linkphile path] [--relink | --unlink]
    -h, --help           show this help message and exit
    --linkphile path     linkphile. (default: "~/.dotphiles/linkphiles")
    --relink             relink all links listed in linkphile.
    --unlink             delete all links in linkphile.

dotphiles chsh [-h] [--shell path] [--etcshells path]
    -h, --help           show this help message and exit
    --shell path         Path to shell exicutable. (default: "/bin/zsh"))
    --etcshells path     Path to /etc/shells if diffrent. (default: "/etc/shells"))
```
