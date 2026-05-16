#!/usr/bin/env python3

import os
import platform
import zlib
from shutil import copy2
import hashlib

windows = platform.platform().startswith('Windows')
osx = platform.platform().startswith('Darwin') or platform.platform().startswith("macOS")
hbb_name = 'claildesk' + ('.exe' if windows else '')
exe_path = 'target/release/' + hbb_name


def get_version():
    with open("Cargo.toml") as fh:
        for line in fh:
            if line.startswith("version"):
                return line.replace("version", "").replace("=", "").replace('"', '').strip()
    return ''


def main():
    os.system("cp Cargo.toml Cargo.toml.bk")
    os.system("cp src/main.rs src/main.rs.bk")
    if windows:
        txt = open('src/main.rs', encoding='utf8').read()
        with open('src/main.rs', 'wt', encoding='utf8') as fh:
            fh.write(txt.replace(
                '//#![windows_subsystem', '#![windows_subsystem'))
    if os.path.exists(exe_path):
        os.unlink(exe_path)
    os.system('python3 inline-sciter.py')
    if os.path.isfile('/usr/bin/pacman'):
        os.system('git checkout src/ui/common.tis')
    version = get_version()
    if windows:
        os.system('cargo build --release --features inline')
        # os.system('upx.exe target/release/claildesk.exe')
        os.system('mv target/release/claildesk.exe target/release/ClailDesk.exe')
        pa = os.environ.get('P')
        if pa:
          os.system('signtool sign /a /v /p %s /debug /f .\\cert.pfx /t http://timestamp.digicert.com  target\\release\\claildesk.exe'%pa)
        else:
          print('Not signed')
        os.system('cp -rf target/release/ClailDesk.exe claildesk-%s-putes.exe'%version)
    else:
        os.system('cargo bundle --release --features inline')
        if osx:
            os.system(
                'strip target/release/bundle/osx/ClailDesk.app/Contents/MacOS/claildesk')
            os.system(
                'cp libsciter.dylib target/release/bundle/osx/ClailDesk.app/Contents/MacOS/')
            # https://github.com/sindresorhus/create-dmg
            os.system('/bin/rm -rf *.dmg')
            plist = "target/release/bundle/osx/ClailDesk.app/Contents/Info.plist"
            txt = open(plist).read()
            with open(plist, "wt") as fh:
                fh.write(txt.replace("</dict>", """
  <key>LSUIElement</key>    
  <string>1</string>    
</dict>"""))
            pa = os.environ.get('P')
            if pa:
              os.system('''
# buggy: rcodesign sign ... path/*, have to sign one by one
#rcodesign sign --p12-file ~/.p12/claildesk-developer-id.p12 --p12-password-file ~/.p12/.cert-pass --code-signature-flags runtime ./target/release/bundle/osx/ClailDesk.app/Contents/MacOS/claildesk
#rcodesign sign --p12-file ~/.p12/claildesk-developer-id.p12 --p12-password-file ~/.p12/.cert-pass --code-signature-flags runtime ./target/release/bundle/osx/ClailDesk.app/Contents/MacOS/libsciter.dylib
#rcodesign sign --p12-file ~/.p12/claildesk-developer-id.p12 --p12-password-file ~/.p12/.cert-pass --code-signature-flags runtime ./target/release/bundle/osx/ClailDesk.app
# goto "Keychain Access" -> "My Certificates" for below id which starts with "Developer ID Application:"
codesign -s "Developer ID Application: {0}" --force --options runtime  ./target/release/bundle/osx/ClailDesk.app/Contents/MacOS/*
codesign -s "Developer ID Application: {0}" --force --options runtime  ./target/release/bundle/osx/ClailDesk.app
'''.format(pa))
            os.system('create-dmg target/release/bundle/osx/ClailDesk.app')
            os.rename('ClailDesk %s.dmg'%version, 'claildesk-%s.dmg'%version)
            if pa:
              os.system('''
#rcodesign sign --p12-file ~/.p12/claildesk-developer-id.p12 --p12-password-file ~/.p12/.cert-pass --code-signature-flags runtime ./claildesk-{1}.dmg
codesign -s "Developer ID Application: {0}" --force --options runtime ./claildesk-{1}.dmg
# https://pyoxidizer.readthedocs.io/en/latest/apple_codesign_rcodesign.html
rcodesign notarize --api-issuer 69a6de7d-2907-47e3-e053-5b8c7c11a4d1 --api-key 9JBRHG3JHT --staple ./claildesk-{1}.dmg
# verify:  spctl -a -t exec -v /Applications/ClailDesk.app
'''.format(pa, version))
            else:
              print('Not signed')
        else:
            os.system('mv target/release/bundle/deb/claildesk*.deb ./claildesk.deb')
            os.system('dpkg-deb -R claildesk.deb tmpdeb')
            os.system('mkdir -p tmpdeb/usr/share/claildesk/files/systemd/')
            os.system(
                'cp claildesk.service tmpdeb/usr/share/claildesk/files/systemd/')
            os.system('cp pynput_service.py tmpdeb/usr/share/claildesk/files/')
            os.system('cp DEBIAN/* tmpdeb/DEBIAN/')
            os.system('strip tmpdeb/usr/bin/claildesk')
            os.system('mkdir -p tmpdeb/usr/lib/claildesk')
            os.system('cp libsciter-gtk.so tmpdeb/usr/lib/claildesk/')
            md5_file('usr/share/claildesk/files/systemd/claildesk.service')
            md5_file('usr/share/claildesk/files/pynput_service.py')
            md5_file('usr/lib/claildesk/libsciter-gtk.so')
            os.system('dpkg-deb -b tmpdeb claildesk.deb; /bin/rm -rf tmpdeb/')
            os.rename('claildesk.deb', 'claildesk-%s.deb'%version)
    os.system("mv Cargo.toml.bk Cargo.toml")
    os.system("mv src/main.rs.bk src/main.rs")


def md5_file(fn):
    md5 = hashlib.md5(open('tmpdeb/' + fn, 'rb').read()).hexdigest()
    os.system('echo "%s %s" >> tmpdeb/DEBIAN/md5sums' % (md5, fn))


if __name__ == "__main__":
    main()
