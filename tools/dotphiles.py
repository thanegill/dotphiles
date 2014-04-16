#!/usr/bin/env python

import os
import sys
import platform
import fnmatch
import shutil
import subprocess
import fileinput
import argparse


e_success = "\033[1;32m{0}\033[0m"
e_arrow   = "\033[1;34m{0}\033[0m"
e_warning = "\033[1;33m{0}\033[0m"
e_error   = "\033[1;31m{0}\033[0m"


def cmdExists(cmd):
    return subprocess.call(("type %s" % cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) is 0


def installbin(toinstall):
    """Install binary based on OS"""

    # Ensure that we can actually, like, compile anything.
    if "darwin" in platform.platform().lower() and not cmdExists("gcc"):
        if os.system("xcode-select --install") is not 0:
            print e_error.format("Xcode command line tools failed to insall please insall\nmanually with \"xcode-select --install\".")
            sys.exit(1)

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


def __getlinkphiles(linkphilesfile):
    """Get files to link"""
    linkphilesfile = os.path.normpath(os.path.expanduser(linkphilesfile))

    if os.path.exists(linkphilesfile) and not os.path.isdir(linkphilesfile):
        philes = []
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
                    os.path.normpath(os.path.expanduser("~/.%s" % os.path.basename(os.path.normpath(line))))])

        return philes
    else:
        raise IOError


def unlinkphiles(linkphilesfile):
    philes = __getlinkphiles(linkphilesfile)
    for phile in philes:
        if os.path.islink(phile[1]):
            os.remove(phile[1])
    print e_warning.format("Removed old links")


def linkphiles(linkphilesfile):
    philes = __getlinkphiles(linkphilesfile)

    for phile in philes:
        if not os.path.exists(phile[0]):
            # Skip nonexsistant sources
            print e_error.format("Link %s -> %s was not created,\nas the source does not exist." %
                (phile[1], phile[0]))
            continue

        if os.path.islink(phile[1]):
            # Remove conflitcing link
            print e_warning.format("Removing link %s -> %s,\nas it confilts with a link that is being created." %
                (phile[1], os.path.normpath(os.readlink(os.path.expanduser(phile[1])))))
            os.remove(phile[1])

        if ((os.path.isfile(phile[1])
            or os.path.isdir(phile[1]))
            and not os.path.islink(phile[1])):
            # Backup file or dir if not symlink
            os.rename(phile[1], ("%s.backup" % phile[1]))
            print e_warning.format("File \"%s\" has been backed up to \"%s\"." %
                (phile[1], ("%s.backup" % phile[1])))

        print e_arrow.format("Creating link %s -> %s" %
                (phile[1], phile[0]))
        os.symlink(phile[0], phile[1])

    print e_success.format("All files have been linked.")


def gitclone(dotphilesdir, repourl, branch):
    dotphilesdir = os.path.normpath(os.path.expanduser(dotphilesdir))

    if not os.path.exists(dotphilesdir):
        print e_arrow.format("Downloading dotphiles...")
        if os.system("git clone --branch %s --recursive %s %s" %
            (branch, repourl, dotphilesdir)) is not 0:
            raise OSError
    else:
        raise IOError

def gitpull(dotphilesdir, branch):
    dotphilesdir = os.path.normpath(os.path.expanduser(dotphilesdir))

    if (os.path.exists(os.path.join(dotphilesdir, ".git"))
        and os.path.isdir(os.path.join(dotphilesdir, ".git"))):
        os.chdir(dotphilesdir)
        print e_arrow.format("Updating dotphiles...")

        if os.system("git pull origin %s" % branch) is not 0:
            raise oserror

        if os.system("git submodule foreach git checkout master") is not 0:
            raise oserror

        if os.system("git submodule foreach git pull origin master") is not 0:
            raise oserror
    else:
        raise IOError


def gitsubupdate(dotphilesdir):
    dotphilesdir = os.path.normpath(os.path.expanduser(dotphilesdir))

    if (os.path.exists(os.path.join(dotphilesdir, ".git"))
        and os.path.isdir(os.path.join(dotphilesdir, ".git"))):
        os.chdir(dotphilesdir)
        print e_arrow.format("Updating submoduals...")

        if os.system("git submodule foreach git checkout master") is not 0:
            raise oserror

        if os.system("git submodule foreach git pull origin master") is not 0:
            raise oserror
    else:
        raise IOError


def vundleupdate():
    if os.system('vim -c "execute \\"BundleInstall\!\\" | q | q"') is not 0:
        raise OSError
    print e_success.format("Vim plugins installed.")


def vundleclean():
    if os.system('vim -c "execute \\"BundleClean\!\\" | q | q"') is not 0:
        raise OSError
    print e_success.format("Unused Vim plugins removed.")


def changeshell(shell, etcshells):
    """
    Change shell of current user to shell
    `shell` should be the full path of the shell executable
    """

    if not os.path.exists(etcshells):
        raise IOError

    shellavalible = False

    for line in open(etcshells).readlines():
        if shell in line:
            shellavalible = True

    if not shellavalible:
        raise OSError

    if shell in os.environ["SHELL"]:
        print e_success.format("Shell is aleady %s." % shell)
    else:
        print ("Enter password to change shell to %s." % shell)
        sys.stdin = open('/dev/tty')
        if os.system("chsh -s %s" % shell) is not 0:
            print e_error.format("Shell not changed to %s. Try manually" % shell)
        else:
            print e_success.format("Changed shell to \"%s\"" % os.environ["SHELL"])

if __name__ == '__main__':

    def install(args):
        installbin("git")

        try:
            gitclone(args.dotphilesdir, args.repourl, args.branch)
        except IOError:
            print e_error.format("Directory %s alrady exists.\nTry `dotphiles update` instead?" %
                args.dotphilesdir)
            sys.exit(1)
        except OSError:
            print e_error.format("Something went wrong with git.\nTry cloning manually.")
            sys.exit(1)

        try:
            linkphiles(args.linkphile)
        except IOError:
            print e_error.format("linkphile \"%s\" doesn't exist." % args.linkphile)
            sys.exit(1)

        installbin("zsh")

        if args.novim:
            print e_arrow.format("Skipping Vim plugin install.")
        else:
            try:
                vundleupdate()
            except OSError:
                print e_error.format("Something went wrong while installing Vim plugings.\nTry manually.")

        chsh("zsh", "/etc/shells")

        os.system("`which env` zsh")
        os.system("source %s" % os.path.join(args.home, ".zshrc"))

        print e_success.format("All done! Your dotphiles are now installed!")

    def update(args):
        # Unlink old files first, incase source changed or deleted
        try:
            unlinkphiles(args.linkphile)
        except IOError:
            print e_error.format("linkphile \"%s\" doesn't exist." % args.linkphile)
            sys.exit(1)

        try:
            gitpull(args.dotphilesdir, args.branch)
        except OSError:
            print e_error.format("Something went wrong with git.\nTry pulling manually.")
            print e_arrow.format("Relinking files...")

            # Relink files if update failed
            try:
                linkphiles(args.linkphile)
            except IOError:
                print e_error.format("linkphile \"%s\" doesn't exist.\nTry linking with dotphiles link." % args.linkphile)
            sys.exit(1)

        try:
            linkphiles(args.linkphile)
        except IOError:
            print e_error.format("linkphile \"%s\" doesn't exist.\nTry linking with dotphiles link." % args.linkphile)

        if args.novim:
            print e_arrow.format("Skipping Vim plugin updates")
        else:
            try:
                vundleupdate()
            except OSError:
                print e_error.format("Something went wrong while installing Vim plugings.\nTry manually.")

            try:
                vundleclean()
            except OSError:
                print e_error.format("Something went wrong while removing Vim plugings.\nTry manually.")


        print e_success.format("All done! Your dotphiles are now updated!")

    def link(args):
        try:
            if args.relink:
                unlinkphiles(args.linkphile)
                linkphiles(args.linkphile)
            elif args.unlink:
                unlinkphiles(args.linkphile)
            else:
                linkphiles(args.linkphile)
        except IOError:
            print e_error.format("linkphile \"%s\" doesn't exist." % args.linkphile)
            sys.exit(1)

    def chsh(args):
        try:
            changeshell(args.shell, args.etcshells)
        except IOError:
            print e_error.format("\"%s\" doesn't exist." % args.etcshells)
            sys.exit(1)
        except OSError:
            print e_error.format("\"%s\" is not in \"%s\"." % (args.shell, args.etcshells))
            sys.exit(1)


    parser = argparse.ArgumentParser(prog='dotphiles', description="Change me")
    subparsers = parser.add_subparsers(help='sub-command --help')


    parser_install = subparsers.add_parser('install', help='install --help')
    parser_install.set_defaults(func=install)
    parser_install.add_argument('--repourl', action='store', metavar='URL',
            help='URL for the dotphile repo (default: "%(default)s")',
            default='https://github.com/psophis/dotphiles.git')
    parser_install.add_argument('--branch', action='store', default='master',
            help='Branch to use for cloning (default: "%(default)s")')
    parser_install.add_argument('--home', action='store', metavar='PATH',
            type=os.path.join, default='~/',
            help='Home directory to install dotphiles to. Can be any directory. (default: "%(default)s")')
    parser_install.add_argument('--dotphilesdir', action='store', metavar='PATH',
            type=os.path.join, default='~/.dotphiles',
            help='Directory name for dotphiles. (default: "%(default)s")')
    parser_install.add_argument('--linkphile', action='store', metavar='PATH',
            type=os.path.join, default='~/.dotphiles/linkphiles',
            help='File with to link dotphiles. (default: "%(default)s")')
    parser_install.add_argument('--force', action='store_true',
            help='Force removal of old dotphiles and installation of vim plugins.')
    parser_install.add_argument('--novim', action='store_true',
            help='Do not install Vim plugins. Vundle will still be install. Useful for faster install.')

    parser_update = subparsers.add_parser('update', help='update --help')
    parser_update.set_defaults(func=update)
    parser_update.add_argument('--branch', action='store', default='master',
            help='Branch to use for cloning (default: "%(default)s")')
    parser_update.add_argument('--dotphilesdir', action='store', metavar='PATH',
            type=os.path.join, default='~/.dotphiles',
            help='Directory name for dotphiles. (default: "%(default)s")')
    parser_update.add_argument('--linkphile', action='store', metavar='PATH',
            type=os.path.join, default='~/.dotphiles/linkphiles',
            help='File with to link dotphiles. (default: "%(default)s")')
    parser_update.add_argument('--novim', action='store_true',
            help='Do not update Vim plugins. Useful for faster update.')

    parser_link = subparsers.add_parser('link', help='relink --help')
    parser_link.set_defaults(func=link)
    parser_link.add_argument('--linkphile', action='store', metavar='path',
            type=os.path.join, default='~/.dotphiles/linkphiles',
            help='linkphile. (default: "%(default)s")')
    parser_link_group = parser_link.add_mutually_exclusive_group()
    parser_link_group.add_argument('--relink', action='store_true',
            help='relink all links listed in linkphile.')
    parser_link_group.add_argument('--unlink', action='store_true',
            help='delete all links in linkphile.')

    parser_chsh = subparsers.add_parser('chsh', help='chsh --help')
    parser_chsh.set_defaults(func=chsh)
    parser_chsh.add_argument('--shell', action='store', metavar='path',
            type=os.path.join, default='/bin/zsh',
            help='Path to shell exicutable. (default: "%(default)s"))')
    parser_chsh.add_argument('--etcshells', action='store', metavar='path',
            type=os.path.join, default='/etc/shells',
            help='Path to /etc/shells if diffrent. (default: "%(default)s"))')


    args = parser.parse_args()
    args.func(args)

