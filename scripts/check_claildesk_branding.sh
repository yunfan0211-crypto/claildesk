#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

require_fixed() {
  local file="$1"
  local expected="$2"
  if ! grep -Fq -- "$expected" "$file"; then
    printf 'Missing ClaiDesk branding in %s: %s\n' "$file" "$expected" >&2
    exit 1
  fi
}

require_fixed README.md '# ClaiDesk'
require_fixed Cargo.toml 'description = "ClaiDesk LAN/VPN Remote Desktop"'
require_fixed Cargo.toml 'ProductName = "ClaiDesk"'
require_fixed Cargo.toml 'identifier = "com.zibochen.claildesk"'
require_fixed libs/hbb_common/src/config.rs 'RwLock::new("ClaiDesk".to_owned())'
require_fixed libs/hbb_common/src/config.rs 'RwLock::new("com.zibochen".to_owned())'
require_fixed flutter/android/app/build.gradle 'applicationId "com.zibochen.claildesk"'
require_fixed flutter/android/app/src/main/res/values/strings.xml '<string name="app_name">ClaiDesk</string>'
require_fixed flutter/ios/Runner/Info.plist '<string>com.zibochen.claildesk</string>'
require_fixed flutter/ios/Runner/Info.plist '<string>claildesk</string>'
require_fixed flutter/macos/Runner/Configs/AppInfo.xcconfig 'PRODUCT_NAME = ClaiDesk'
require_fixed flutter/macos/Runner/Configs/AppInfo.xcconfig 'PRODUCT_BUNDLE_IDENTIFIER = com.zibochen.claildesk'
require_fixed flutter/windows/runner/Runner.rc 'VALUE "ProductName", "ClaiDesk"'
require_fixed flutter/linux/CMakeLists.txt 'set(APPLICATION_ID "com.zibochen.claildesk")'
require_fixed flatpak/rustdesk.json '"id": "com.zibochen.ClaiDesk"'
require_fixed flatpak/com.zibochen.ClaiDesk.metainfo.xml '<name>ClaiDesk</name>'
require_fixed res/rustdesk.desktop 'Name=ClaiDesk'
require_fixed res/claildesk.service 'Description=ClaiDesk'
require_fixed .gitmodules 'https://github.com/zibo-chen/hbb_common.git'
require_fixed build.py 'Build/Products/Release/ClaiDesk.app'
require_fixed .github/workflows/flutter-build.yml 'Build/Products/Release/ClaiDesk.app'
require_fixed .github/workflows/flutter-build.yml 'claildesk-${{ env.VERSION }}'

if grep -Fq 'RustDesk.app' .github/workflows/flutter-build.yml; then
  printf 'Release workflow still references RustDesk.app\n' >&2
  exit 1
fi

for stale in \
  flutter/ios/Runner/GoogleService-Info.plist \
  flutter/ios/exportOptions.plist \
  flatpak/com.rustdesk.RustDesk.metainfo.xml \
  .github/workflows/fdroid.yml; do
  if [[ -e "$stale" ]]; then
    printf 'Stale upstream release file is still present: %s\n' "$stale" >&2
    exit 1
  fi
done

python3 scripts/generate_claildesk_icons.py --check
bash scripts/check_linux_service_branding.sh
printf 'ClaiDesk branding and generated icons are consistent.\n'
