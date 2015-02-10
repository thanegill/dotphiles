#!env python2

import os
import sys
import platform
import subprocess
import fileinput
import argparse


e_success = '\033[1;32m{0}\033[0m' # Green
e_arrow   = '\033[1;34m{0}\033[0m' # White
e_warning = '\033[1;33m{0}\033[0m' # Orange
e_error   = '\033[1;31m{0}\033[0m' # Red


def _cmd_exists(cmd):
    """Checks to see if ``cmd`` is in the current ``$PATH``.
    """
    return subprocess.call(('hash %s' % cmd), shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE) is 0


def install_binary(to_install):
    """Installs binary if ``to_install`` exist, if not installs using correct
    package manager. Supported OS's:

    OS       Package Manager
    ------------------------
    OSX      brew
    Ubuntu   apt-get
    Debian   apt-get
    CentOS   yum
    Fedora   yum
    """

    if not _cmd_exists(to_install):
        # OSX (brew)
        if 'darwin' in platform.platform().lower():
            # Ensure that we can actually compile anything on OSX.
            if os.system('xcode-select --install') is not 0:
                print e_error.format('Xcode command line tools failed to insall please insall manually with "xcode-select --install".')
                # Exit if xcode command line tools are not installed.
                sys.exit(1)

            # Install homebrew.
            if not _cmd_exists('brew'):
                print e_arrow.format('Installing Homebrew')
                os.system('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"')

            # If Homebrew was installed install ``to_install``.
            if _cmd_exists('brew'):
                print e_arrow.format('Updating Brew')
                os.system('brew update')
                print e_arrow.format('Installing %s' % to_install)
                os.system('brew install %s' % to_install)

        # Ubuntu or Debian (apt-get)
        elif ('ubuntu' or 'debian') in platform.platform().lower():
            print e_arrow.format('Installing %s' % to_install)
            os.system('sudo apt-get -qy install %s' % to_install)

        # CentOS or Fedora (yum)
        elif ('centos' or 'fedora') in platform.platform().lower():
            print e_arrow.format('Installing %s' % to_install)
            os.system('sudo yum -q -y install %s' % to_install)
    else:
        print e_arrow.format('%s was already installed' % to_install)


def _get_link_philes(link_philes_file):
    """Using ``link_philes_file`` get's the files that need to be linked and
    returns a dictionry of the sorce and destination to be linked

    format for link_philes_file is as follows:

    ::
        # Files to be linked
        # <source> <destination>
        # destination defaults to ~/.<basename>
        ~/.dotphiles/zsh/zshrc
        ~/.dotphiles/vim/
        ~/.dotphiles/vim/ ~/.nvim
        ~/.dotphiles/tmux/tmux.conf
        ~/.dotphiles/git/gitconfig

    """
    # Normalize path and expand $HOME and ~
    link_philes_file = os.path.normpath(os.path.expanduser(link_philes_file))

    if os.path.exists(link_philes_file) and not os.path.isdir(link_philes_file):
        philes = []
        for line in fileinput.input(link_philes_file):
            line = line.strip()
            if line.startswith('#') or not line:
                # Skip comments and blank lines
                continue
            if '#' in line:
                # Remove inline comments
                line = line.split('#')[0].strip()
            if ' ' in line:
                # Split on space if exist
                line = line.strip().split(' ')
                philes.append([os.path.normpath(os.path.expanduser(line[0])),
                    os.path.normpath(os.path.expanduser(line[1]))])
            else:
                # Default to ~./basename
                philes.append([os.path.normpath(os.path.expanduser(line.strip())),
                    os.path.normpath(os.path.expanduser("~/.%s" %
                        os.path.basename(os.path.normpath(line))))])

        return philes
    else:
        raise IOError


def unlink_philes(link_philes_file):
    """Unlink files from ``link_philes_file``.
    """
    philes = _get_link_philes(link_philes_file)
    for phile in philes:
        if os.path.islink(phile[1]):
            os.remove(phile[1])
    print e_warning.format('Removed old links')


def link_philes(link_philes_file):
    """Symbolically link files listed in ``link_philes_file`` where ``[0]`` is
    the source and ``[1]`` is the destination.
    """
    philes = _get_link_philes(link_philes_file)

    for phile in philes:
        # Skip nonexistent sources
        if not os.path.exists(phile[0]):
            print e_error.format('Link %s -> %s was not created, as the source does not exist.'
                    % (phile[1], phile[0]))
            continue

        # Remove conflicting link
        if os.path.islink(phile[1]):
            print e_warning.format('Removing link %s -> %s, as it conflicts with a link that is being created.' %
                    (phile[1], os.path.normpath(os.readlink(os.path.expanduser(phile[1])))))
            os.remove(phile[1])

        # Backup file or directory if not symlink
        if ((os.path.isfile(phile[1])
            or os.path.isdir(phile[1]))
            and not os.path.islink(phile[1])):
            os.rename(phile[1], ('%s.backup' % phile[1]))
            print e_warning.format('File "%s" has been backed up to "%s".' %
                    (phile[1], ('%s.backup' % phile[1])))

        print e_arrow.format('Creating link %s -> %s' % (phile[1], phile[0]))

        os.symlink(phile[0], phile[1])

    print e_success.format('All files have been linked.')


def _is_git_repo(directory):
    """Checks to see if there is a ``.git`` directory in the ``directory``
    given.
    """
    return (os.path.exists(os.path.join(directory, '.git'))
        and os.path.isdir(os.path.join(directory, '.git')))


def _git_submodual_update(repo_directory):
    """Recursively updates all submodule for the git repository for the given
    ``repo_directory``.
    """
    # Normalize repo_directory and expand $HOME and ~
    repo_directory = os.path.normpath(os.path.expanduser(repo_directory))

    if _is_git_repo(repo_directory):
        os.chdir(repo_directory)
        print e_arrow.format('Updating submoduals...')

        if os.system('git submodule update --recursive --init') is not 0:
            raise OSError
    else:
        raise IOError


def git_clone(repo_directory, repo_url, branch):
    """Recursively clones the given ``repo_url`` with branch ``branch`` into
    repo_directory ``repo_directory``.
    """
    # Normalize repo_directory and expand $HOME and ~
    repo_directory = os.path.normpath(os.path.expanduser(repo_directory))

    if not os.path.exists(repo_directory):
        print e_arrow.format('Downloading dotphiles...')
        if os.system('git clone --branch %s --recursive %s %s' %
            (branch, repo_url, repo_directory)) is not 0:
            raise OSError
        _git_submodual_update(repo_directory)
    else:
        raise IOError


def git_pull(repo_directory, branch):
    """Git pulls the given ``branch`` from the git repository in the given
    ``repo_directory``.
    """
    # Normalize repo_directory and expand $HOME and ~
    repo_directory = os.path.normpath(os.path.expanduser(repo_directory))

    if _is_git_repo(repo_directory):
        os.chdir(repo_directory)
        print e_arrow.format('Updating dotphiles...')
        if os.system('git pull origin %s' % branch) is not 0:
            raise OSError
        _git_submodual_update(repo_directory)
    else:
        raise IOError


def vim_update_plugins(dotphiles_directory):
    """Update/install plugins vim plugins using NeoBundle's neoinstall.
    """
    if os.system(os.path.join(dotphiles_directory,
        'vim/bundle/neobundle.vim/bin/neoinstall')) is not 0:
        raise OSError
    print e_success.format('Vim plugins installed.')


def vim_clean_plugins():
    """Clean up unused plugins in Vim.
    """
    if os.system('vim +NeoBundleClean\! +qall') is not 0:
        raise OSError
    print e_success.format('Unused Vim plugins removed.')


def change_shell(shell, etc_shells):
    """Change shell of current user to shell ``shell`` should be the full path
    of the shell executable.
    """
    if not os.path.exists(etc_shells):
        raise IOError

    shell_avalible = False

    for line in open(etc_shells).readlines():
        if shell in line:
            shell_avalible = True

    if not shell_avalible:
        raise OSError

    if os.environ['SHELL'] in shell:
        print e_success.format('Shell is already %s.' % shell)
    else:
        print ('Enter password to change shell to %s.' % shell)
        sys.stdin = open('/dev/tty')
        if os.system('chsh -s %s' % shell) is not 0:
            print e_error.format('Shell not changed to %s. Try manually' % shell)
        else:
            print e_success.format('Changed shell to "%s"' %
                    os.environ['SHELL'])

if __name__ == '__main__':

    def install(args):
        install_binary('git')

        try:
            git_clone(args.dotphilesdir, args.repo_url, args.branch)
        except IOError:
            print e_error.format('Directory %s alrady exists. Try `dotphiles update` instead?' %
                    args.dotphilesdir)
            sys.exit(1)
        except OSError:
            print e_error.format('Something went wrong with git. Try cloning manually.')
            sys.exit(1)

        try:
            link_philes(args.linkphile)
        except IOError:
            print e_error.format('linkphile "%s" does not exist.' %
                    args.linkphile)
            sys.exit(1)

        install_binary('vim')

        if args.novim:
            print e_arrow.format('Skipping Vim plugin install.')
        else:
            try:
                vim_update_plugins(args.dotphilesdir)
            except OSError:
                print e_error.format('Something went wrong while installing Vim plugings. Try manually.')

        install_binary('zsh')

        chsh(args)

        print e_success.format('All done! Your dotphiles are now installed!')

    def update(args):

        # Unlink old files first, incase one was changed or deleted
        try:
            unlink_philes(args.linkphile)
        except IOError:
            print e_error.format('linkphile "%s" does not exist.' %
                    args.linkphile)
            sys.exit(1)

        # Pull new dotphiles repo
        try:
            git_pull(args.dotphilesdir, args.branch)
        except OSError:
            print e_error.format('Something went wrong with git. Try pulling manually.')
            print e_arrow.format('Relinking files...')

            # Relink files if update failed
            try:
                link_philes(args.linkphile)
            except IOError:
                print e_error.format('linkphile "%s" does not exist. Try linking with dotphiles link.' %
                        args.linkphile)
            sys.exit(1)

        # Link new dotphiles
        try:
            link_philes(args.linkphile)
        except IOError:
            print e_error.format('linkphile "%s" does not exist. Try linking with dotphiles link.' %
                    args.linkphile)
            sys.exit(1)

        # Update vim plugins
        if args.novim:
            # Skip vim plugins
            print e_arrow.format('Skipping Vim plugin updates')
        else:
            # Install and update plugins
            try:
                vim_update_plugins(args.dotphilesdir)
            except OSError:
                print e_error.format('Something went wrong while installing Vim plugings. Try manually.')
            # Cleanup old plugins
            try:
                vim_clean_plugins()
            except OSError:
                print e_error.format('Something went wrong while removing Vim plugings. Try manually.')

        print e_success.format('All done! Your dotphiles are now updated!')



    def link(args):
        try:
            if args.relink:
                unlink_philes(args.linkphile)
                link_philes(args.linkphile)
            elif args.unlink:
                unlink_philes(args.linkphile)
            else:
                link_philes(args.linkphile)
        except IOError:
            print e_error.format('linkphile "%s" does not exist.' %
                    args.linkphile)
            sys.exit(1)

    def chsh(args):
        try:
            change_shell(args.shell, args.etcshells)
            os.system(args.shell)
        except IOError:
            print e_error.format('"%s" does not exist.' % args.etcshells)
            sys.exit(1)
        except OSError:
            print e_error.format('"%s" is not in "%s".' %
                    (args.shell, args.etcshells))
            sys.exit(1)

    parser = argparse.ArgumentParser(prog='dotphiles')
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
            help='Do not install Vim plugins. NeoBundle will still be installed. Useful for faster install.')

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

