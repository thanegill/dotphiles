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


def install(toinstall):
    """Install binary based on OS"""

    # Ensure that we can actually, like, compile anything.
    if "darwin" in platform.platform().lower() and not cmdExists("gcc"):
        if os.system("xcode-select --install") is not 0:
            print e_error.format("Xcode command line tools failed to insall please insall\nmanually with \"xcode-select --install\".")
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


def getlinkphiles(linkphilesfile):
    # Get files to link

    philes = []
    if os.path.isfile(linkphilesfile):
        for line in fileinput.input(linkphilesfile):
            line = line.strip()
            if line.startswith("#") or not line:
                # Skip comments and blank lines
                continue

            if "#" in line:
                # Remove inline comments
                line = line.split("#")[0].strip()

            if " " in line:
                # Split on slace if exist
                line = line.strip().split(" ")
                philes.append([os.path.normpath(os.path.expanduser(line[0])),
                    os.path.normpath(os.path.expanduser(line[1]))])
            else:
                # Default to ~./basename
                philes.append([os.path.normpath(os.path.expanduser(line.strip())),
                    os.path.normpath(os.path.expanduser("~/."+ os.path.basename(os.path.normpath(line))))])

    return philes


def unlinkphiles(linkphilesfile):
    philes = getlinkphiles(linkphilesfile)

    print e_arrow.format("Removing old links first")

    for phile in philes:
        if os.path.islink(phile[1]):
            os.remove(phile[1])

def linkphiles(linkphilesfile):
    philes = getlinkphiles(linkphilesfile)

    for phile in philes:
        if not os.path.exists(phile[0]):
            # Skip nonexsistant sources
            print e_error.format("Link %s -> %s was not created,\nas the source does not exist." %
                    phile[0], phile[1])
            continue

        if os.path.islink(phile[1]):
            # Remove conflitcing link
            print e_arrow.format("Removing link %s -> %s,\nas it confilts with a link that is being created." %
                    phile[1], os.path.normpath(os.readlink(os.path.expanduser(phile[1]))))
            os.remove(phile[1])

        if ((os.path.isfile(phile[1])
            or os.path.isdir(phile[1]))
            and not os.path.islink(phile[1])):
            # Backup file or dir if not symlink
            os.rename(phile[1], phile[1] + ".backup")
            print e_arrow.format("File \"%s\" has been backed up to \"%s\"." %
                    (phile[1], phile[1] + ".backup"))

        print e_success.format("Creating link %s -> %s" %
                (phile[0], phile[1]))
        os.symlink(phile[0], phile[1])


def updatedotphiles():

    # Unlink old files first, incase source changed or deleted
    unlinkphiles(flags.linkphile)
    initialize(flags.updateflag)
    linkphiles(flags.linkphile)
    os.system('vim -c "execute \\"BundleInstall\!\\" | q | q"')

    print e_success.format("All done! Your dotphiles are now updated!")

def installdotphiles():

    install("git")
    initialize()
    linkphiles(flags.linkphile)
    install("zsh")
    chsh()

    if queryyesno("Install Vim plugins now?", "yes"):
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
        linkphile = os.path.join(dotphilesdir, "linkphiles")

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
    parser.add_argument('--link', dest='linkphile', action='store', metavar='PATH',
            type=file, help='File so with to link dotphiles. (Default ~/.dotphiles/linkphiles)')

    args = parser.parse_args(namespace=flags)

    print vars(flags)

    if flags.updateflag:
        updatedotphiles()
    else:
        installdotphiles()
