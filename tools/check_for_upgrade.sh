#!/bin/sh

function _current_epoch() {
  echo $(($(date +%s) / 60 / 60 / 24))
}

function _update_dotphiles_update() {
  echo "LAST_EPOCH=$(_current_epoch)" > ~/.dotphiles/dotphiles-update
}

function _upgrade_dotphiles() {
  /usr/bin/python $HOME/.dotphiles/tools/dotphiles.py update
  # update the dotphiles file
  _update_dotphiles_update
}

epoch_target=$UPDATE_DOTPHILES_DAYS
if [[ -z "$epoch_target" ]]; then
  # Default to old behavior
  epoch_target=13
fi

if [ -f ~/.dotphiles/dotphiles-update ]
then
  . ~/.dotphiles/dotphiles-update

  if [[ -z "$LAST_EPOCH" ]]; then
    _update_dotphiles_update && return 0;
  fi

  epoch_diff=$(($(_current_epoch) - $LAST_EPOCH))
  if [ $epoch_diff -gt $epoch_target ]
  then
    if [ "$DISABLE_UPDATE_PROMPT" = "true" ]
    then
      _upgrade_dotphiles
    else
      echo "[Dotphiles] Would you like to check for updates?"
      echo "Type Y to update dotphiles: \c"
      read line
      if [ "$line" = Y ] || [ "$line" = y ]; then
        _upgrade_dotphiles
      else
        _update_dotphiles_update
      fi
    fi
  fi
else
  # create the dotfiles file
  _update_dotphiles_update
fi

