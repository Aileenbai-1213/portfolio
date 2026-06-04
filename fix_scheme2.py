"""
从 git 历史恢复的原始图重新生成方案2截图（292px lossless）
同时修正几个体积过大的图片
"""
from PIL import Image
import os

base = "/Users/ailin/Documents/美团工作/portfolio"

def save_lossless(src_path, dst_path, max_width):
    img = Image.open(src_path).convert("RGB")
    old_kb = os.path.getsize(src_path) / 1024
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
    img.save(dst_path, "WEBP", lossless=True, method=6)
    new_kb = os.path.getsize(dst_path) / 1024
    print(f"  ✓ {os.path.basename(dst_path)}  {old_kb:.0f}KB → {new_kb:.0f}KB  ({img.width}x{img.height})")

# 方案2：从 git 恢复的原始图 → 292px lossless
print("=== 方案2截图（从原始恢复）===")
save_lossless("/tmp/daily_orig.webp",   os.path.join(base, "广场改版/日常页面.webp"),   292)
save_lossless("/tmp/star_orig.webp",    os.path.join(base, "广场改版/有明星场时.webp"), 292)
save_lossless("/tmp/newuser_orig.webp", os.path.join(base, "广场改版/新人页面.webp"),   292)

# 广场-美食tab.png 太大（1.7MB），降到 800px lossless
print("\n=== 广场-美食tab：800px lossless ===")
save_lossless(
    os.path.join(base, "广场改版/广场-美食tab.png"),
    os.path.join(base, "广场改版/广场-美食tab.webp"),
    800
)

# competitor-2 用 1200px 版本（比 1600px 小很多，视觉差异不大）
print("\n=== competitor-2：1200px lossless ===")
save_lossless(
    os.path.join(base, "images/competitor-2.png"),
    os.path.join(base, "images/competitor-2.webp"),
    1200
)

# avatar：从原始 png 重新生成，quality=92
print("\n=== avatar：400px q92 ===")
avatar_png = os.path.join(base, "avatar.png")
avatar_dst = os.path.join(base, "avatar.webp")
img = Image.open(avatar_png).convert("RGB")
old_kb = os.path.getsize(avatar_png) / 1024
if img.width > 400:
    ratio = 400 / img.width
    img = img.resize((400, int(img.height * ratio)), Image.LANCZOS)
img.save(avatar_dst, "WEBP", quality=92, method=4)
new_kb = os.path.getsize(avatar_dst) / 1024
print(f"  ✓ avatar.webp  {old_kb:.0f}KB → {new_kb:.0f}KB  ({img.width}x{img.height})")

print("\n✅ 完成！")
