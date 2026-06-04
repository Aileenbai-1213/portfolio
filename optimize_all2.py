"""
批量将 images/ 下所有 jpg/png 转为 webp，并更新 HTML 引用
"""
from PIL import Image
import os, glob

base = "/Users/ailin/Documents/美团工作/portfolio"
MOBILE_DIRS = ["images/livestream", "images/ai-search", "images/search2"]
MAX_WIDE = 1200
converted = []

def convert(src_path, max_width, quality=85):
    dst_path = os.path.splitext(src_path)[0] + ".webp"
    if os.path.exists(dst_path) and os.path.getmtime(dst_path) >= os.path.getmtime(src_path):
        old_kb = os.path.getsize(src_path) / 1024
        new_kb = os.path.getsize(dst_path) / 1024
        print(f"  [skip] {os.path.relpath(dst_path, base)}  {old_kb:.0f}KB → {new_kb:.0f}KB")
        return os.path.relpath(src_path, base), os.path.relpath(dst_path, base)
    try:
        img = Image.open(src_path).convert("RGB")
    except Exception as e:
        print(f"  [ERROR] {os.path.relpath(src_path, base)}: {e}")
        return None, None
    old_kb = os.path.getsize(src_path) / 1024
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
    img.save(dst_path, "WEBP", quality=quality, method=4)
    new_kb = os.path.getsize(dst_path) / 1024
    print(f"  ✓ {os.path.relpath(src_path, base)}  {old_kb:.0f}KB → {new_kb:.0f}KB  (节省 {(1-new_kb/old_kb)*100:.0f}%)")
    return os.path.relpath(src_path, base), os.path.relpath(dst_path, base)

# 1. 手机截图目录
print("=== 手机截图目录（resize 到 438px）===")
for d in MOBILE_DIRS:
    full_d = os.path.join(base, d)
    if not os.path.isdir(full_d):
        continue
    for ext in ["*.jpg", "*.jpeg", "*.png"]:
        for f in sorted(glob.glob(os.path.join(full_d, ext))):
            old_rel, new_rel = convert(f, max_width=438, quality=85)
            if old_rel:
                converted.append((old_rel, new_rel))

# 2. assets/competitor/
print("\n=== assets/competitor/ ===")
comp_dir = os.path.join(base, "assets/competitor")
if os.path.isdir(comp_dir):
    for ext in ["*.jpg", "*.jpeg", "*.png"]:
        for f in sorted(glob.glob(os.path.join(comp_dir, ext))):
            old_rel, new_rel = convert(f, max_width=MAX_WIDE, quality=82)
            if old_rel:
                converted.append((old_rel, new_rel))

# 3. images/ 根目录
print("\n=== images/ 根目录 ===")
for ext in ["*.jpg", "*.jpeg", "*.png"]:
    for f in sorted(glob.glob(os.path.join(base, "images", ext))):
        old_rel, new_rel = convert(f, max_width=MAX_WIDE, quality=82)
        if old_rel:
            converted.append((old_rel, new_rel))

# 4. avatar_透明.png（带透明通道）
print("\n=== avatar_透明 ===")
avatar_t = os.path.join(base, "avatar_透明.png")
if os.path.exists(avatar_t):
    dst = os.path.join(base, "avatar_透明.webp")
    try:
        img = Image.open(avatar_t).convert("RGBA")
        old_kb = os.path.getsize(avatar_t) / 1024
        if img.width > 400:
            ratio = 400 / img.width
            img = img.resize((400, int(img.height * ratio)), Image.LANCZOS)
        img.save(dst, "WEBP", quality=88, method=4)
        new_kb = os.path.getsize(dst) / 1024
        print(f"  ✓ avatar_透明.png  {old_kb:.0f}KB → {new_kb:.0f}KB  (节省 {(1-new_kb/old_kb)*100:.0f}%)")
        converted.append(("avatar_透明.png", "avatar_透明.webp"))
    except Exception as e:
        print(f"  [ERROR] avatar_透明.png: {e}")

# 5. images/生成中.png
for fname in ["images/生成中.png"]:
    fp = os.path.join(base, fname)
    if os.path.exists(fp):
        old_rel, new_rel = convert(fp, max_width=900, quality=82)
        if old_rel:
            converted.append((old_rel, new_rel))

print(f"\n共转换 {len(converted)} 张图片")

# 更新 HTML 引用
print("\n=== 更新 HTML 引用 ===")
html_files = glob.glob(os.path.join(base, "*.html"))
for html_path in html_files:
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for old_rel, new_rel in converted:
        for old, new in [(old_rel, new_rel), (old_rel.lstrip("./"), new_rel.lstrip("./"))]:
            content = content.replace(f'"{old}"', f'"{new}"')
            content = content.replace(f"'{old}'", f"'{new}'")
    if content != original:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✓ 更新 {os.path.basename(html_path)}")
    else:
        print(f"  - 无变化 {os.path.basename(html_path)}")

print("\n✅ 全部完成！")
