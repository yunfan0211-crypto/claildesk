## How to build and run with Snap

Begin by cloning the repository and make sure snapcraft is installed in your Linux.

```sh
git clone https://github.com/claildesk/claildesk
# if snapcraft is installed, please skip this
sudo snap install snapcraft --classic
# build claildesk snap package
snapcraft --use-lxd
# install claildesk snap package, `--dangerous` flag must exists if u manually build and install claildesk
sudo snap install claildesk_xxx.snap --dangerous
```

Note: Some of interfaces needed by ClailDesk cannot automatically connected by Snap. Please **manually** connect them by executing:
```sh
# record system audio
snap connect claildesk:audio-record
snap connect claildesk:pulseaudio
# observe loginctl session
snap connect claildesk:login-session-observe
```

After steps above, ClailDesk can be found in System App Menu.

