#!/usr/bin/env python

import time

def currentEpoch():
  return int(time.time() / 60 / 60 / 24)

# function _current_epoch() {
#   # echo $(($(date +%s) / 60 / 60 / 24))
#   echo $(($(date +%s))) 
# }

def updateDotfilesUpdate():
  

# function _update_dotfiles_update() {
#   echo "LAST_EPOCH=$(_current_epoch)" > ~/.dotfiles/tmp/dotfiles-update
# }

# function _upgrade_dotfiles() {
#   # /usr/bin/env ZSH=$ZSH /bin/sh $ZSH/tools/upgrade.sh
#   # update the zsh file
#   echo "Updated"
#   _update_dotfiles_update
# }

# epoch_target=$UPDATE_DOTFILES_DAYS
# if [[ -z "$epoch_target" ]]; then
#   # Default to old behavior
#   epoch_target=7
# fi

# if [ -f ~/.dotfiles/tmp/dotfiles-update ]
# then
#   . ~/.dotfiles/tmp/dotfiles-update

#   if [[ -z "$LAST_EPOCH" ]]; then
#     _update_dotfiles_update && return 0;
#   fi

#   epoch_diff=$(($(_current_epoch) - $LAST_EPOCH))
#   if [ $epoch_diff -gt $epoch_target ]
#   then
#     if [ "$DISABLE_UPDATE_PROMPT" = "true" ]
#     then
#       _upgrade_dotfiles
#     else
#       echo "[Dotfiles] Would you like to check for updates?"
#       echo "Type Y to update dotfiles: \c"
#       read line
#       if [ "$line" = Y ] || [ "$line" = y ]; then
#         _upgrade_dotfiles
#       else
#         _update_dotfiles_update
#       fi
#     fi
#   fi
# else
#   # create the ditfile file
#   _update_dotfiles_update
# fi

if __name__ == '__main__':

  print currentEpoch()