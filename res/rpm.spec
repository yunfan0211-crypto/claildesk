Name:       claildesk
Version:    1.1.0
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://claildesk.com
Vendor:     claildesk <info@claildesk.com>
Requires:   gtk3 libxcb libXfixes alsa-lib libva2 pam gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/claildesk/
mkdir -p %{buildroot}/usr/share/claildesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/claildesk %{buildroot}/usr/bin/claildesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/claildesk/libsciter-gtk.so
install $HBB/res/claildesk.service %{buildroot}/usr/share/claildesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/claildesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/claildesk.svg
install $HBB/res/claildesk.desktop %{buildroot}/usr/share/claildesk/files/
install $HBB/res/claildesk-link.desktop %{buildroot}/usr/share/claildesk/files/

%files
/usr/bin/claildesk
/usr/share/claildesk/libsciter-gtk.so
/usr/share/claildesk/files/claildesk.service
/usr/share/icons/hicolor/256x256/apps/claildesk.png
/usr/share/icons/hicolor/scalable/apps/claildesk.svg
/usr/share/claildesk/files/claildesk.desktop
/usr/share/claildesk/files/claildesk-link.desktop
/usr/share/claildesk/files/__pycache__/*

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop claildesk || true
    systemctl stop claildesk || true
  ;;
esac

%post
systemctl stop claildesk || true
systemctl disable claildesk || true
rm -f /etc/systemd/system/claildesk.service
cp /usr/share/claildesk/files/claildesk.service /etc/systemd/system/claildesk.service
cp /usr/share/claildesk/files/claildesk.desktop /usr/share/applications/
cp /usr/share/claildesk/files/claildesk-link.desktop /usr/share/applications/
systemctl daemon-reload
systemctl enable claildesk
systemctl start claildesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop claildesk || true
    systemctl disable claildesk || true
    systemctl stop claildesk || true
    systemctl disable claildesk || true
    rm /etc/systemd/system/claildesk.service || true
    rm /etc/systemd/system/claildesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/share/applications/claildesk.desktop || true
    rm /usr/share/applications/claildesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
