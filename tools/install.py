#!/usr/bin/env python

import os
import sys
import platform
import fnmatch
import shutil
import subprocess
import fileinput
import argparse


e_arrow   = "\033[1;33m{0}\033[0m"
e_success = "\033[1;32m{0}\033[0m"
e_error   = "\033[1;31m{0}\033[0m"



def cmdExists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def queryyesno(question, default="yes"):
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
        sys.stdin = open('/dev/tty')

        # try:
        choice = raw_input().lower()
        # except EOFError:
            # if default is not None:
                # return valid[default]
        # else:
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
        print e_error.format("The XCode Command Line Tools must be installed first.")
        exit(1)

    if not cmdExists("git"):
        # OSX
        if "darwin" in platform.platform().lower():
            # It's easiest to get Git via Homebrew, so get that first.
            if not cmdExists("brew"):
                print e_arrow.format("Installing Homebrew")
                os.system("ruby -e \"$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)\"")
            # If Homebrew was installed, install Git.
            if cmdExists("brew"):
                print e_arrow.format("Updating Brew")
                os.system("brew update")
                print e_arrow.format("Installing Git")
                os.system("brew installed git")
        # Ubuntu
        elif "ubuntu" in platform.platform().lower() or "debian" in platform.platform().lower():
            print e_arrow.format("Installing Git")
            os.system("sudo apt-get -qy install git-core")

        # CentOS or Fedora
        elif "centos" in platform.platform().lower() or "fedora" in platform.platform().lower():
            print e_arrow.format("Installing Git")
            os.system("sudo yum -qy install git")

    # If Git isn't installed by now, something exploded. We gots to quit!
    if not cmdExists("git"):
        print e_error.format("Git should be installed. It isn't. Aborting.")
        exit(1)


def initialize(update=False):
    if not os.path.isdir(flags.dotphilesdir):
        print e_arrow.format("Downloading dotphiles...")
        os.system("git clone --recursive https://github.com/psophis/dotphiles ~/.dotphiles")
    elif update:
        shutil.rmtree(flags.dotphilesdir)
        print e_success.format("Old dotphiles removed")
        print e_arrow.format("Downloading dotphiles...")
        os.system("git clone --recursive https://github.com/psophis/dotphiles ~/.dotphiles")
    else:
        print e_error.format("Dotfile directory aleady exists")
        if queryyesno("Do you want to back it up and continue?", "yes"):
            os.rename(flags.dotphilesdir, os.path.join(flags.homedir, ".dotphiles.backup"))
            print "Backup created at \"~/.dotphiles.backup\""
            initialize()
        else:
            if queryyesno("Delete old dotphiles instead?", "no"):
                shutil.rmtree(flags.dotphilesdir)
                print e_success.format("Old dotphiles removed")
                initialize()
            else:
                exit(0)

def installtheme(themedest="oh-my-zsh/custom/themes/"):
    if os.path.isdir(os.path.join(flags.dotphilesdir, themedest)):
        # ~/.dotphiles/oh-my-zsh/custom/themes exists
        if os.path.isfile(os.path.join(flags.dotphilesdir, themedest, flags.theme)):
            # theme already there, remove it
            os.remove(os.path.join(flags.dotphilesdir, themedest, flags.theme))

        os.symlink(os.path.join(flags.dotphilesdir, flags.themepath), os.path.join(flags.dotphilesdir, themedest, flags.theme))

        print e_success.format("Installed ZSH theme")
    else:
        os.mkdir(os.path.join(flags.dotphilesdir, themedest))
        installtheme()


def chsh():
    if "zsh" not in os.environ["SHELL"]:
        if cmdExists("zsh"):
            print ("Enter password to change shell to ZSH.")
            sys.stdin = open('/dev/tty')
            if os.system("chsh -s `which zsh`") is not 0:
                print e_error.format("Shell not changed to ZSH. Try manually")
            else:
                print e_success.format("Changed shell to \"" + os.environ["SHELL"] + "\"" )
        else:
            print e_error.format("ZSH not installed, please install.")
    else:
        print e_arrow.format("Shell is aleady ZSH.")

def getignored():

    filestoignore = []

    if os.path.isfile(flags.dotphilesignore):
        for line in fileinput.input(flags.dotphilesignore):
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
    for file in os.listdir(flags.dotphilesdir):
        if goodfiletolink(file):
            if os.path.islink(os.path.join(flags.homedir, "." + file)):
                os.remove(os.path.join(flags.homedir, "." + file))
            elif (os.path.isfile(os.path.join(flags.homedir, "." + file))
              and not os.path.islink(os.path.join(flags.homedir, "." + file)) or
              (os.path.isdir(os.path.join(flags.homedir, "." + file)))):
                # Backup file if not symlink or directory
                os.rename(os.path.join(flags.homedir, "." + file), os.path.join(flags.homedir, "." + file, ".backup"))
                print e_arrow.format("File \"%s\" has been backed up to \"%s\"." %
                  (os.path.join(flags.homedir, "." + file), os.path.join(flags.homedir, "." + file, ".backup")))

            os.symlink(os.path.join(flags.dotphilesdir, file), os.path.join(flags.homedir, "." + file))
            print e_success.format("Symlinked \"%s\" to \"%s\"." %
              (os.path.join(flags.dotphilesdir, file), os.path.join(flags.homedir, "." + file)))
        else:
            print "Ignoring \"%s\"" % file

def install(toinstall):
    """Install binary based on OS"""

    # Ensure that we can actually, like, compile anything.
    if "darwin" in platform.platform().lower() and not cmdExists("gcc"):
        if os.system("xcode-select --install") is not 0:
            print e_error.format("Xcode command line tools failed to insall please insall\n manually with \"xcode-select --install\"")
            exit(1)

    if not cmdExists(toinstall):
        # OSX
        if "darwin" in platform.platform().lower():
            # Install homebrew.
            if not cmdExists("brew"):
                print e_arrow.format("Installing Homebrew")
                os.system("ruby -e \"$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)\"")
            # If Homebrew was installed, install.
            if cmdExists("brew"):
                print e_arrow.format("Updating Brew")
                os.system("brew update")
                print e_arrow.format("Installing %s" % toinstall)
                os.system("brew install %s" % toinstall)

        # Ubuntu or Debian
        elif "ubuntu" in platform.platform().lower() or "debian" in platform.platform().lower():
            print e_arrow.format("Installing %s" % toinstall)
            os.system("sudo apt-get -qy install %s" % toinstall)

        # CentOS or Fedora
        elif "centos" in platform.platform().lower() or "fedora" in platform.platform().lower():
            print e_arrow.format("Installing %s" % toinstall)
            os.system("sudo yum -q -y install %s" % toinstall)
    else:
        print e_arrow.format("%s was already installed" % toinstall)



def updatedotphiles():

    install("git")
    initialize()
    installtheme()
    linkfiles()
    # http://qntm.org/bash
    # http://stackoverflow.com/questions/5997029/escape-double-quotes-for-json-in-python
    os.system('vim -c "execute \\"BundleInstall\!\\" | q | q"')

    print e_success.format("All done! Your dotphiles are now updated!")

def installdotphiles():

    install("git")
    initialize()
    installtheme()
    linkfiles()
    install("zsh")
    chsh()

    if queryyesno("Install Vim plugins now?", "yes"):
        # http://qntm.org/bash
        # http://stackoverflow.com/questions/5997029/escape-double-quotes-for-json-in-python
        os.system('vim -c "execute \\"BundleInstall\\" | q | q"')

    os.system("`which env` zsh")
    os.system("source " + os.path.join(flags.homedir, ".zshrc"))

    print e_success.format("All done! Your dotphiles are now installed!")


if __name__ == '__main__':


    class Flags(object):
        installflag = True
        updateflag = False
        homedir = os.path.expanduser("~")
        dotphilesdir = os.path.join(homedir, ".dotphiles")
        dotphilesignore = os.path.join(dotphilesdir, ".dotphilesignore")

        theme = "psophis.zsh-theme"
        themepath = os.path.join(dotphilesdir, "lib", theme)


    flags = Flags()

    parser = argparse.ArgumentParser()
    parser.add_argument('--install', '-i', dest='installflag', action='store_true',
            help='New instalation of dotphiles (Default)')
    parser.add_argument('--update', '-u', dest='updateflag', action='store_true',
            help='Upgrate current instalation (will overwite files!)')
    parser.add_argument('--home', dest='homedir', action='store', metavar='PATH',
            type=os.path.join, help='Home directory to install dotphiles to. Can be any directory. (Default "~/")')
    parser.add_argument('--name', dest='dotphilesdir', action='store', metavar='name',
            type=os.path.join, help='Directory name for dotphiles. (Default ".dotphiles")')
    parser.add_argument('--ignore', dest='dotphilesignore', action='store', metavar='PATH',
            type=file, help='File to use as ingore list. Like a .gitignore. (Default ".dotphilesignore")')
    parser.add_argument('--theme', dest='theme', action='store', metavar='PATH',
            type=file, help='Theme file path. (Default .dotphilespsophis.zsh-theme')

    args = parser.parse_args(namespace=flags)

    print vars(flags)

    if flags.updateflag:
        updatedotphiles()
    else:
        installdotphiles()
