# [udevil & devmon – mount without password](https://copr.fedoraproject.org/coprs/username/udevil/) #

[![license: GPLv3+](https://img.shields.io/badge/license-GPLv3+-blue.svg)](http://www.gnu.org/licenses/gpl-3.0.html)

udevil mounts and unmounts removable devices and networks without a password (set suid), shows device info, monitors device changes. Emulates mount's and udisks's command line usage and udisks v1's output.

devmon is a configuration-less bash daemon script which automounts optical discs and removable drives. It can also selectively autostart apps or execute commands after mounting, ignore specified devices and volume labels, and manually mount and unmount devices.

## Usage ##

See `udevil --help`.

`devmon` is optional (disabled by default) and not required for `udevil`.

## Security note ##

This package sets SUID bit on `/usr/bin/udevil`. Consider that if you pay close attention to your system's security.

Luckily, udevil is highly configurable. All permissions can be adjusted by editing `/etc/udevil/udevil.conf`.

## Non-systemd distros (RHEL and CentOS 6) ##

Init script for `devmon` is not included. You need to start `/usr/bin/devmon` manually if you want to have automount working.

## Feedback ##

Contact developer: click `Contact` button on the right side of this page.

Contact packager & contribute:
[![Gitter](https://badges.gitter.im/selurvedu/specs.svg)](https://gitter.im/selurvedu/specs)
[![GitLab](https://img.shields.io/badge/Git-Lab-6251B1.svg)](https://gitlab.com/selurvedu/specs/blob/master/udevil)
[![GitHub](https://img.shields.io/badge/Git-Hub-6251B1.svg)](https://github.com/selurvedu/specs/blob/master/udevil)
