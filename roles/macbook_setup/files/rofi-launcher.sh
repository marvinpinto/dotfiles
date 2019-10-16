#!/usr/bin/env bash

DND_FILE="${HOME}/.irssi/do_not_disturb.txt"
I3LOCK='/usr/bin/i3lock --color 333333'

if [ -z $@ ]; then
  function gen_options()
  {
    option_list=("Lock Screen","Logout","Suspend Computer","Hibernate Computer","Reboot Computer","Shutdown Computer","Enable Screensaver","Disable Screensaver","Toggle Do Not Disturb (DND)","Initiate Backup","Check Email","Create Development Workspace","2FA Tokens","Emoji Picker","Switch Bluetooth Device")
    echo ${option_list[@]} | tr ',' '\n' | sort
  }

  echo "Choose an option from the list below:"; gen_options
else
  OPTION=$@

  case "$OPTION" in
    'Choose an option from the list below:')
      exit 0
      ;;
    'Lock Screen')
      coproc (/usr/local/bin/rofi-i3-locker)
      ;;
    'Logout')
      /usr/bin/i3-msg exit
      ;;
    'Suspend Computer')
      ${I3LOCK} && /usr/bin/dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.Suspend" boolean:true
      ;;
    'Hibernate Computer')
      ${I3LOCK} && /usr/bin/dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.Hibernate" boolean:true
      ;;
    'Reboot Computer')
      /usr/bin/dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.Reboot" boolean:true
      ;;
    'Shutdown Computer')
      /usr/bin/dbus-send --system --print-reply --dest=org.freedesktop.login1 /org/freedesktop/login1 "org.freedesktop.login1.Manager.PowerOff" boolean:true
      ;;
    'Enable Screensaver')
      /usr/bin/xautolock -exit
      /usr/bin/xautolock -resetsaver -detectsleep -time 3 -locker '/usr/local/bin/rofi-i3-locker' -notify 30 -notifier "notify-send -i info -u normal -t 3000 -- 'Locking screen in 30 seconds'" &
      ;;
    'Disable Screensaver')
      /usr/bin/xautolock -exit
      ;;
    'Toggle Do Not Disturb (DND)')
      [ -e ${DND_FILE} ] && rm ${DND_FILE} || touch ${DND_FILE}
      ;;
    'Initiate Backup')
      coproc (PINENTRY_USER_DATA=gui /usr/local/bin/acd-backup "up")
      ;;
    'Check Email')
      coproc (PINENTRY_USER_DATA=gui ${HOME}/.i3/fastmail_unread_count.py --force)
      ;;
    'Create Development Workspace')
      coproc (${HOME}/.i3/dev-layout.sh)
      ;;
    '2FA Tokens')
      coproc (/usr/local/bin/rofi-2fa)
      ;;
    'Emoji Picker')
      coproc (PINENTRY_USER_DATA=gui /usr/local/bin/rofi-emoji)
      ;;
    'Switch Bluetooth Device')
      coproc (/usr/local/bin/switch-bluetooth-device)
      ;;
    *)
      echo "Invalid option \"$OPTION\""
      exit 2
  esac
fi
