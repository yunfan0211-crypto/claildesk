Name:       claildesk
Version:    1.1.0
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://claildesk.com
Vendor:     claildesk <info@claildesk.com>
Requires:   gtk3 libxcb1 libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1 xdotool
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/claildesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/claildesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/claildesk.service -t "%{buildroot}/usr/share/claildesk/files"
install -Dm 644 $HBB/res/claildesk.desktop -t "%{buildroot}/usr/share/claildesk/files"
install -Dm 644 $HBB/res/claildesk-link.desktop -t "%{buildroot}/usr/share/claildesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/claildesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/claildesk.svg"

%files
/usr/share/claildesk/*
/usr/share/claildesk/files/claildesk.service
/usr/share/icons/hicolor/256x256/apps/claildesk.png
/usr/share/icons/hicolor/scalable/apps/claildesk.svg
/usr/share/claildesk/files/claildesk.desktop
/usr/share/claildesk/files/claildesk-link.desktop

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
ln -sf /usr/share/claildesk/claildesk /usr/bin/claildesk
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
    rm /usr/bin/claildesk || true
    rmdir /usr/lib/claildesk || true
    rmdir /usr/local/claildesk || true
    rmdir /usr/share/claildesk || true
    rm /usr/share/applications/claildesk.desktop || true
    rm /usr/share/applications/claildesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/claildesk || true
    rmdir /usr/local/claildesk || true
  ;;
esac
