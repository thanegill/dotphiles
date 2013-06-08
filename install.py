#!/usr/bin/env python

import os
import sys
import platform
import fnmatch
import subprocess
import fileinput

_homedir = os.path.expanduser("~/")
_dotfilesdir = _homedir + ".dotfiles/"
_dotfilesignore = _dotfilesdir + ".dotfilesignore"

_theme = "psophis.zsh-theme"
_themepath = "init/" + _theme


e_header = "\n\033[1m{0}\033[0m"
e_success = "\033[1;32m{0}\033[0m"
e_error = "\033[1;31m{0}\033[0m"
e_arrow = "\033[1;33m{0}\033[0m"



colorred = "\033[01;31m{0}\033[00m"
colorgrn = "\033[1;36m{0}\033[00m"

def cmdExists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True, "y":True, "ye":True, "no":False, "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")


def installgit():

    # Ensure that we can actually, like, compile anything.
    if "darwin" in platform.platform().lower() and not cmdExists("gcc"):
        print e_header.format("The XCode Command Line Tools must be installed first.")
        exit(1)

    if not cmdExists("git"):
        # OSX
        if "darwin" in platform.platform().lower():
            # It's easiest to get Git via Homebrew, so get that first.
            if not cmdExists("brew"):
                print e_header.format("Installing Homebrew")
                os.system("ruby -e \"$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)\"")      
            # If Homebrew was installed, install Git.
            if cmdExists("brew"):
                print e_header.format("Updating Brew")
                os.system("brew update")
                print e_header.format("Installing Git")
                os.system("brew installed git")
        # Ubuntu
        elif "ubuntu" in platform.platform().lower():
            print e_header("Installing Git")
            os.system("sudo apt-get -qq install git-core")

        # CentOS or Fedora
        elif "centos" in platform.platform().lower() or "fedora" in platform.platform().lower():
            print e_header("Installing Git")
            os.system("sudo yum install git")

    # If Git isn't installed by now, something exploded. We gots to quit!
    if not cmdExists("git"):
        print e_error.format("Git should be installed. It isn't. Aborting.")
        exit(1)


def initialize():
    if not os.path.isdir(_dotfilesdir):
        print e_header.format("Downloading dotfiles")
        os.system("git clone --recursive https://github.com/psophis/dotfiles ~/.dotfiles")
    else:
        print e_error.format("Dotfile directory aleady exists")
        if query_yes_no("Do you want to back it up and continue?"):
            # os.rename(_dotfilesdir, _homedir + ".dotfiles.backup")
            print "Backup created at \"~/.dotfiles.backup\""
            initialize()
        else:
            if query_yes_no("Delete old dotfiles instead", "no"):
                os.removedirs(_dotfilesdir)
                print "Old dotfiles removed"
                initialize()
            else:
                exit(0)

def installtheme(themedest="oh-my-zsh/custom/themes/"):
    if os.path.isdir(_dotfilesdir + themedest):
        if os.path.isfile(_dotfilesdir + themedest + _theme):
            os.remove(_dotfilesdir + themedest + _theme)
        os.symlink(_dotfilesdir + _themepath, _dotfilesdir + themedest + _theme)
        print e_success.format("Installed ZSH theme")
    else:
        os.mkdir(_dotfilesdir + themedest)
        installtheme()


def chsh():
    #TODO ask if want to change
    if "zsh" not in os.environ["SHELL"]:
        if cmdExists("zsh"):
            print ("Enter password to change shell to ZSH.")
            if os.system("chsh -s /bin/zsh") is not 0:
                print e_error.format("Shell not changed to ZSH.")
            else:
                print e_success.format("Changed shell to \"" + os.environ["SHELL"] + "\"" )
        else:
            print e_error.format("ZSH not installed, please install.")
    else:
        print "Shell is aleady ZSH"

def getignored():

    filestoignore = []

    if os.path.isfile(_dotfilesignore):
        for line in fileinput.input(_dotfilesignore):
            if line.startswith('#') or not line:
                continue
            else:
                filestoignore.append(line.strip())
        return filestoignore
    else:
        print "nope"

def goodfiletolink(file):
    filestoignore = getignored()
    if os.path.isdir(file):
        file += "/"

    for l in filestoignore:
        if file.startswith(".") or fnmatch.fnmatch(file, l):
            return False

    return True

def linkfiles():

    filestolink = []
    for file in os.listdir(_dotfilesdir):
        if goodfiletolink(file):
            filestolink.append(file)

    for file in filestolink:
        if os.path.islink(_homedir + "." + file):
            os.remove(_homedir + "." + file)
        elif ((os.path.isfile(_homedir + "." + file) and not os.path.islink(_homedir + "." + file)) or
             (os.path.isdir(_homedir + "." + file))):
             os.rename(_homedir + "." + file, _homedir + "." + file + ".backup")
             print e_error.format("File \"" + _homedir + "." + file + "\" has been backed up to \"" + _homedir + "." + file + ".backup\".")

        os.symlink(_dotfilesdir + file, _homedir + "." + file)
        print e_success.format("Symlinked \"" + _dotfilesdir + file + "\" to \"" + _homedir + "." + file + "\"")


if __name__ == '__main__':
    installgit()
    initialize()
    # sleep(10)
    installtheme()
    linkfiles()
    chsh()
    os.system("source " + _homedir + ".zshrc")

    os.system("vim +BundleInstall +qall")

    # Update existing sudo time stamp if set, otherwise do nothing.
    # while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

    print e_success.format("All done!")
