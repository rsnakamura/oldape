NEWLINE = '\n'

PSE_LINUX = """
  PID TTY          TIME CMD
    1 ?        00:00:01 init
    2 ?        00:00:00 kthreadd
    3 ?        00:00:05 ksoftirqd/0
    6 ?        00:00:00 migration/0
    7 ?        00:00:00 watchdog/0
    8 ?        00:00:00 migration/1
   10 ?        00:00:04 ksoftirqd/1
   11 ?        00:00:14 kworker/0:1
   12 ?        00:00:00 watchdog/1
   13 ?        00:00:00 migration/2
   15 ?        00:00:04 ksoftirqd/2
   16 ?        00:00:00 watchdog/2
   17 ?        00:00:00 migration/3
   19 ?        00:00:04 ksoftirqd/3
   20 ?        00:00:00 watchdog/3
   21 ?        00:00:00 cpuset
   22 ?        00:00:00 khelper
   23 ?        00:00:00 kdevtmpfs
   24 ?        00:00:00 netns
   26 ?        00:00:00 sync_supers
   27 ?        00:00:00 bdi-default
   28 ?        00:00:00 kintegrityd
   29 ?        00:00:00 kblockd
   30 ?        00:00:00 ata_sff
   31 ?        00:00:00 khubd
   32 ?        00:00:00 md
   34 ?        00:00:00 khungtaskd
   35 ?        00:00:00 kswapd0
   36 ?        00:00:00 ksmd
   37 ?        00:00:00 khugepaged
   38 ?        00:00:00 fsnotify_mark
   39 ?        00:00:00 ecryptfs-kthrea
   40 ?        00:00:00 crypto
   48 ?        00:00:00 kthrotld
   49 ?        00:00:00 scsi_eh_0
   50 ?        00:00:00 scsi_eh_1
   51 ?        00:00:00 kworker/u:2
   52 ?        00:00:00 scsi_eh_2
   53 ?        00:00:00 scsi_eh_3
   54 ?        00:00:04 kworker/u:3
   75 ?        00:00:00 devfreq_wq
   76 ?        00:00:38 kworker/1:1
  209 ?        00:00:29 firefox
  211 ?        00:00:03 jbd2/sda3-8
  212 ?        00:00:00 ext4-dio-unwrit
  300 ?        00:00:00 upstart-udev-br
  302 ?        00:00:00 udevd
  409 ?        00:00:00 udevd
  419 ?        00:00:00 kpsmoused
  704 ?        00:00:00 upstart-socket-
  723 ?        00:00:00 irq/48-mei
  737 ?        00:00:00 hd-audio0
  767 ?        00:00:00 sshd
  779 ?        00:00:00 dbus-daemon
  798 ?        00:00:00 modem-manager
  800 ?        00:00:00 bluetoothd
  801 ?        00:00:10 rsyslogd
  805 ?        00:00:01 NetworkManager
  813 ?        00:00:00 krfcommd
  816 ?        00:00:06 avahi-daemon
  817 ?        00:00:00 avahi-daemon
  819 ?        00:00:00 polkitd
  879 ?        00:00:00 cupsd
  902 tty4     00:00:00 getty
  912 tty5     00:00:00 getty
  919 tty2     00:00:00 getty
  920 tty3     00:00:00 getty
  922 tty6     00:00:00 getty
  939 ?        00:00:07 whoopsie
  941 ?        00:00:00 acpid
  942 ?        00:00:33 irqbalance
  945 ?        00:00:00 cron
  946 ?        00:00:00 atd
  956 ?        00:00:00 iprt
  958 ?        00:00:00 udevd
  975 ?        00:00:00 lightdm
 1049 tty7     00:13:17 Xorg
 1132 ?        00:00:00 lightdm
 1155 ?        00:00:03 accounts-daemon
 1182 ?        00:00:00 kworker/3:2
 1196 ?        00:00:00 gnome-keyring-d
 1202 tty1     00:00:00 getty
 1205 ?        00:00:00 console-kit-dae
 1273 ?        00:00:00 gnome-session
 1311 ?        00:00:00 ssh-agent
 1314 ?        00:00:00 dbus-launch
 1315 ?        00:00:04 dbus-daemon
 1319 ?        00:00:00 gvfsd
 1321 ?        00:00:00 gvfs-fuse-daemo
 1330 ?        00:00:09 gnome-settings-
 1341 ?        00:12:43 compiz
 1344 ?        00:00:00 gconfd-2
 1351 ?        00:00:00 upowerd
 1354 ?        00:00:09 pulseaudio
 1356 ?        00:00:00 gnome-fallback-
 1357 ?        00:00:21 nautilus
 1358 ?        00:00:00 nm-applet
 1363 ?        00:00:00 gconf-helper
 1364 ?        00:00:00 bluetooth-apple
 1366 ?        00:00:00 polkit-gnome-au
 1375 ?        00:03:03 dropbox
 1381 ?        00:00:00 gvfs-gdu-volume
 1383 ?        00:00:02 gvfs-afc-volume
 1386 ?        00:00:00 gvfs-gphoto2-vo
 1392 ?        00:00:00 gvfsd-trash
 1402 ?        00:00:00 colord
 1423 ?        00:00:03 bamfdaemon
 1428 ?        00:00:00 gvfsd-burn
 1457 ?        00:00:00 sh
 1458 ?        00:00:06 gtk-window-deco
 1476 ?        00:00:00 gvfsd-metadata
 1483 ?        00:00:01 rtkit-daemon
 1493 ?        00:00:11 unity-panel-ser
 1495 ?        00:00:02 hud-service
 1510 ?        00:00:04 udisks-daemon
 1511 ?        00:00:00 udisks-daemon
 1516 ?        00:00:00 indicator-sound
 1519 ?        00:00:00 indicator-messa
 1523 ?        00:00:00 indicator-print
 1526 ?        00:00:00 indicator-sessi
 1527 ?        00:00:00 indicator-appli
 1529 ?        00:00:00 indicator-datet
 1556 ?        00:00:00 geoclue-master
 1570 ?        00:00:00 ubuntu-geoip-pr
 1587 ?        00:00:01 notify-osd
 1617 ?        00:00:00 sh
 1618 ?        00:02:51 gnome-terminal
 1622 ?        00:00:00 gnome-pty-helpe
 1623 pts/4    00:00:00 bash
 1719 ?        00:00:00 dnsmasq
 1816 ?        00:00:00 gdu-notificatio
 1819 pts/4    00:00:00 screen
 1890 ?        00:00:00 telepathy-indic
 1896 ?        00:00:00 mission-control
 1901 ?        00:00:00 goa-daemon
 1922 ?        00:00:00 zeitgeist-datah
 1923 ?        00:00:04 gnome-screensav
 1930 ?        00:00:00 zeitgeist-daemo
 1932 ?        00:00:00 system-service-
 1938 ?        00:00:00 zeitgeist-fts
 1946 ?        00:00:00 cat
 1968 ?        00:00:30 kworker/3:1
 2020 ?        00:00:03 ubuntuone-syncd
 2179 ?        00:00:00 ssh-agent
 2203 ?        00:00:01 update-notifier
 2226 ?        00:00:10 update-manager
 2242 ?        00:00:00 dconf-service
 2262 ?        00:00:00 unity-files-dae
 2264 ?        00:00:01 unity-applicati
 2266 ?        00:00:00 unity-lens-vide
 2267 ?        00:00:01 unity-music-dae
 2286 ?        00:02:39 screen
 2339 ?        00:00:00 unity-musicstor
 2341 ?        00:00:00 unity-scope-vid
 2342 pts/2    00:00:00 bash
 2587 pts/3    00:00:00 bash
 2627 ?        00:00:02 deja-dup-monito
 2689 pts/3    00:00:09 adb
 2796 ?        00:00:00 sshd
 2798 ?        00:00:08 sshd
 2799 pts/1    00:00:00 bash
 7660 ?        00:34:29 firefox
 9179 pts/7    00:00:00 bash
10107 ?        00:00:00 kworker/1:2
11721 ?        00:00:00 at-spi-bus-laun
11797 ?        00:00:07 kworker/0:0
12079 ?        00:00:02 kworker/2:1
14551 pts/8    00:00:00 bash
15110 ?        00:52:33 plugin-containe
16339 ?        00:00:00 kworker/2:0
17389 ?        00:00:00 kworker/1:0
17521 pts/8    00:00:00 iperf
17574 ?        00:00:00 kworker/2:2
17724 pts/3    00:00:00 ps
17725 pts/3    00:00:00 tee
19870 ?        00:00:00 flush-8:0
22488 pts/5    00:00:00 bash
23676 ?        00:00:00 dbus
30829 ?        00:04:15 emacs
31212 pts/1    00:00:08 ssh
32567 pts/6    00:00:00 python
""".split(NEWLINE)

PSE_LINUX_NO_FIREFOX = """
  PID TTY          TIME CMD
    1 ?        00:00:01 init
    2 ?        00:00:00 kthreadd
    3 ?        00:00:05 ksoftirqd/0
    6 ?        00:00:00 migration/0
    7 ?        00:00:00 watchdog/0
    8 ?        00:00:00 migration/1
   10 ?        00:00:04 ksoftirqd/1
   11 ?        00:00:14 kworker/0:1
   12 ?        00:00:00 watchdog/1
   13 ?        00:00:00 migration/2
   15 ?        00:00:04 ksoftirqd/2
   16 ?        00:00:00 watchdog/2
   17 ?        00:00:00 migration/3
   19 ?        00:00:04 ksoftirqd/3
   20 ?        00:00:00 watchdog/3
   21 ?        00:00:00 cpuset
   22 ?        00:00:00 khelper
   23 ?        00:00:00 kdevtmpfs
   24 ?        00:00:00 netns
   26 ?        00:00:00 sync_supers
   27 ?        00:00:00 bdi-default
   28 ?        00:00:00 kintegrityd
   29 ?        00:00:00 kblockd
   30 ?        00:00:00 ata_sff
   31 ?        00:00:00 khubd
   32 ?        00:00:00 md
   34 ?        00:00:00 khungtaskd
   35 ?        00:00:00 kswapd0
   36 ?        00:00:00 ksmd
   37 ?        00:00:00 khugepaged
   38 ?        00:00:00 fsnotify_mark
   39 ?        00:00:00 ecryptfs-kthrea
   40 ?        00:00:00 crypto
   48 ?        00:00:00 kthrotld
   49 ?        00:00:00 scsi_eh_0
   50 ?        00:00:00 scsi_eh_1
   51 ?        00:00:00 kworker/u:2
   52 ?        00:00:00 scsi_eh_2
   53 ?        00:00:00 scsi_eh_3
   54 ?        00:00:04 kworker/u:3
   75 ?        00:00:00 devfreq_wq
   76 ?        00:00:38 kworker/1:1
  211 ?        00:00:03 jbd2/sda3-8
  212 ?        00:00:00 ext4-dio-unwrit
  300 ?        00:00:00 upstart-udev-br
  302 ?        00:00:00 udevd
  409 ?        00:00:00 udevd
  419 ?        00:00:00 kpsmoused
  704 ?        00:00:00 upstart-socket-
  723 ?        00:00:00 irq/48-mei
  737 ?        00:00:00 hd-audio0
  767 ?        00:00:00 sshd
  779 ?        00:00:00 dbus-daemon
  798 ?        00:00:00 modem-manager
  800 ?        00:00:00 bluetoothd
  801 ?        00:00:10 rsyslogd
  805 ?        00:00:01 NetworkManager
  813 ?        00:00:00 krfcommd
  816 ?        00:00:06 avahi-daemon
  817 ?        00:00:00 avahi-daemon
  819 ?        00:00:00 polkitd
  879 ?        00:00:00 cupsd
  902 tty4     00:00:00 getty
  912 tty5     00:00:00 getty
  919 tty2     00:00:00 getty
  920 tty3     00:00:00 getty
  922 tty6     00:00:00 getty
  939 ?        00:00:07 whoopsie
  941 ?        00:00:00 acpid
  942 ?        00:00:33 irqbalance
  945 ?        00:00:00 cron
  946 ?        00:00:00 atd
  956 ?        00:00:00 iprt
  958 ?        00:00:00 udevd
  975 ?        00:00:00 lightdm
 1049 tty7     00:13:17 Xorg
 1132 ?        00:00:00 lightdm
 1155 ?        00:00:03 accounts-daemon
 1182 ?        00:00:00 kworker/3:2
 1196 ?        00:00:00 gnome-keyring-d
 1202 tty1     00:00:00 getty
 1205 ?        00:00:00 console-kit-dae
 1273 ?        00:00:00 gnome-session
 1311 ?        00:00:00 ssh-agent
 1314 ?        00:00:00 dbus-launch
 1315 ?        00:00:04 dbus-daemon
 1319 ?        00:00:00 gvfsd
 1321 ?        00:00:00 gvfs-fuse-daemo
 1330 ?        00:00:09 gnome-settings-
 1341 ?        00:12:43 compiz
 1344 ?        00:00:00 gconfd-2
 1351 ?        00:00:00 upowerd
 1354 ?        00:00:09 pulseaudio
 1356 ?        00:00:00 gnome-fallback-
 1357 ?        00:00:21 nautilus
 1358 ?        00:00:00 nm-applet
 1363 ?        00:00:00 gconf-helper
 1364 ?        00:00:00 bluetooth-apple
 1366 ?        00:00:00 polkit-gnome-au
 1375 ?        00:03:03 dropbox
 1381 ?        00:00:00 gvfs-gdu-volume
 1383 ?        00:00:02 gvfs-afc-volume
 1386 ?        00:00:00 gvfs-gphoto2-vo
 1392 ?        00:00:00 gvfsd-trash
 1402 ?        00:00:00 colord
 1423 ?        00:00:03 bamfdaemon
 1428 ?        00:00:00 gvfsd-burn
 1457 ?        00:00:00 sh
 1458 ?        00:00:06 gtk-window-deco
 1476 ?        00:00:00 gvfsd-metadata
 1483 ?        00:00:01 rtkit-daemon
 1493 ?        00:00:11 unity-panel-ser
 1495 ?        00:00:02 hud-service
 1510 ?        00:00:04 udisks-daemon
 1511 ?        00:00:00 udisks-daemon
 1516 ?        00:00:00 indicator-sound
 1519 ?        00:00:00 indicator-messa
 1523 ?        00:00:00 indicator-print
 1526 ?        00:00:00 indicator-sessi
 1527 ?        00:00:00 indicator-appli
 1529 ?        00:00:00 indicator-datet
 1556 ?        00:00:00 geoclue-master
 1570 ?        00:00:00 ubuntu-geoip-pr
 1587 ?        00:00:01 notify-osd
 1617 ?        00:00:00 sh
 1618 ?        00:02:51 gnome-terminal
 1622 ?        00:00:00 gnome-pty-helpe
 1623 pts/4    00:00:00 bash
 1719 ?        00:00:00 dnsmasq
 1816 ?        00:00:00 gdu-notificatio
 1819 pts/4    00:00:00 screen
 1890 ?        00:00:00 telepathy-indic
 1896 ?        00:00:00 mission-control
 1901 ?        00:00:00 goa-daemon
 1922 ?        00:00:00 zeitgeist-datah
 1923 ?        00:00:04 gnome-screensav
 1930 ?        00:00:00 zeitgeist-daemo
 1932 ?        00:00:00 system-service-
 1938 ?        00:00:00 zeitgeist-fts
 1946 ?        00:00:00 cat
 1968 ?        00:00:30 kworker/3:1
 2020 ?        00:00:03 ubuntuone-syncd
 2179 ?        00:00:00 ssh-agent
 2203 ?        00:00:01 update-notifier
 2226 ?        00:00:10 update-manager
 2242 ?        00:00:00 dconf-service
 2262 ?        00:00:00 unity-files-dae
 2264 ?        00:00:01 unity-applicati
 2266 ?        00:00:00 unity-lens-vide
 2267 ?        00:00:01 unity-music-dae
 2286 ?        00:02:39 screen
 2339 ?        00:00:00 unity-musicstor
 2341 ?        00:00:00 unity-scope-vid
 2342 pts/2    00:00:00 bash
 2587 pts/3    00:00:00 bash
 2627 ?        00:00:02 deja-dup-monito
 2689 pts/3    00:00:09 adb
 2796 ?        00:00:00 sshd
 2798 ?        00:00:08 sshd
 2799 pts/1    00:00:00 bash
 9179 pts/7    00:00:00 bash
10107 ?        00:00:00 kworker/1:2
11721 ?        00:00:00 at-spi-bus-laun
11797 ?        00:00:07 kworker/0:0
12079 ?        00:00:02 kworker/2:1
14551 pts/8    00:00:00 bash
15110 ?        00:52:33 plugin-containe
16339 ?        00:00:00 kworker/2:0
17389 ?        00:00:00 kworker/1:0
17521 pts/8    00:00:00 iperf
17574 ?        00:00:00 kworker/2:2
17724 pts/3    00:00:00 ps
17725 pts/3    00:00:00 tee
19870 ?        00:00:00 flush-8:0
22488 pts/5    00:00:00 bash
23676 ?        00:00:00 dbus
30829 ?        00:04:15 emacs
31212 pts/1    00:00:08 ssh
32567 pts/6    00:00:00 python
""".split(NEWLINE)
