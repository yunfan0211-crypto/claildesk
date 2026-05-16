#!/bin/bash
set -e
cd "$(dirname "$0")/.."

echo "=== 品牌替换开始 ==="

# 1. 替换目录名
echo "[1/8] 替换目录名..."
find . -type d -name "*claildesk*" -o -type d -name "*ClailDesk*" -o -type d -name "*CLAILDESK*" 2>/dev/null | while read d; do
    newd=$(echo "$d" | sed -e 's/claildesk/claildesk/g' -e 's/ClailDesk/ClailDesk/g' -e 's/CLAILDESK/CLAILDESK/g')
    if [ "$d" != "$newd" ]; then
        mv "$d" "$newd"
        echo "  目录: $d -> $newd"
    fi
done

# 2. 替换文件名
echo "[2/8] 替换文件名..."
find . -type f \( -name "*claildesk*" -o -name "*ClailDesk*" -o -name "*CLAILDESK*" \) 2>/dev/null | while read f; do
    newf=$(echo "$f" | sed -e 's/claildesk/claildesk/g' -e 's/ClailDesk/ClailDesk/g' -e 's/CLAILDESK/CLAILDESK/g')
    if [ "$f" != "$newf" ]; then
        mv "$f" "$newf"
        echo "  文件: $f -> $newf"
    fi
done

# 3. 替换文件内容 - claildesk -> claildesk
echo "[3/8] 替换文件内容 (claildesk -> claildesk)..."
find . -type f \( -name "*.rs" -o -name "*.toml" -o -name "*.yml" -o -name "*.yaml" -o -name "*.md" -o -name "*.nsi" -o -name "*.html" -o -name "*.css" -o -name "*.tis" -o -name "*.json" -o -name "*.py" -o -name "*.sh" -o -name "*.txt" -o -name "*.proto" -o -name "*.service" -o -name "*.plist" -o -name "*.desktop" -o -name "Dockerfile" \) 2>/dev/null | while read f; do
    if grep -qi "claildesk" "$f" 2>/dev/null; then
        sed -i -e 's/claildesk/claildesk/g' -e 's/ClailDesk/ClailDesk/g' -e 's/CLAILDESK/CLAILDESK/g' "$f"
        echo "  修改: $f"
    fi
done

# 4. 替换 hbb_common -> claildesk_common
echo "[4/8] 替换 hbb_common -> claildesk_common..."
find . -type f \( -name "*.rs" -o -name "*.toml" \) 2>/dev/null | while read f; do
    if grep -qi "hbb_common\|hbb_common\|HBB_COMMON" "$f" 2>/dev/null; then
        sed -i -e 's/hbb_common/claildesk_common/g' -e 's/hbb_common/ClailDesk_Common/g' "$f"
        echo "  修改: $f"
    fi
done

# 5. 替换服务器相关
echo "[5/8] 删除官方服务器配置..."
find . -type f \( -name "*.rs" -o -name "*.toml" -o -name "*.md" \) 2>/dev/null | while read f; do
    if grep -qi "claildesk.com\|api.claildesk\|relay.claildesk\|hbbs\|hbbr" "$f" 2>/dev/null; then
        sed -i -e 's/api\.claildesk\.com//g' -e 's/relay\.claildesk\.com//g' -e 's/hbbs//g' -e 's/hbbr//g' -e 's/claildesk\.com//g' "$f"
        echo "  修改: $f"
    fi
done

# 6. 替换关于页面文案
echo "[6/8] 替换关于页面文案..."
find . -type f 2>/dev/null | while read f; do
    if grep -qi "Made with heart in this chaotic world\|在这个混乱的世界中" "$f" 2>/dev/null; then
        sed -i "s/长风破浪会有时，直挂云帆济沧海/长风破浪会有时，直挂云帆济沧海/g" "$f"
        sed -i "s/长风破浪会有时，直挂云帆济沧海/长风破浪会有时，直挂云帆济沧海/g" "$f"
        echo "  修改: $f"
    fi
done

# 7. 删除 macOS 相关
echo "[7/8] 删除 macOS 相关文件..."
rm -f src/platform/macos.rs src/ui/macos.rs mac-tray.png 2>/dev/null
find . -type f -name "*.plist" -path "*/privileges_scripts/*" -delete 2>/dev/null
find . -type f -name "*mac*" -delete 2>/dev/null
echo "  macOS 文件已删除"

# 8. 删除多语言文件
echo "[8/8] 删除多语言文件..."
rm -f src/lang/de.rs src/lang/en.rs src/lang/eo.rs src/lang/fr.rs src/lang/it.rs src/lang/ptbr.rs src/lang/ru.rs src/lang/tw.rs src/lang/template.rs 2>/dev/null
rm -f README-DE.md README-EO.md README-ES.md README-FI.md README-FR.md README-IT.md README-JP.md README-ML.md README-NL.md README-PL.md README-PTBR.md README-RU.md README.md 2>/dev/null
echo "  多语言文件已删除"

echo "=== 品牌替换完成 ==="
