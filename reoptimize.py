"""
重新优化策略：
- 截图/UI/流程图类 → resize 到 2x 展示尺寸 + WebP lossless（无损保清晰度）
- 照片类 → resize + WebP quality=92（高质量）

手机截图展示宽 146px → 2x = 292px（Retina 足够清晰，无损体积可控）
全宽大图展示约 800px → 2x = 1600px，但截图类用 lossless 体积会大，改为 1x=800px lossless
"""
from PIL import Image
import os, glob

base = "/Users/ailin/Documents/美团工作/portfolio"

def save(src_path, dst_path, max_width, lossless=False, quality=92):
    img = Image.open(src_path)
    # 保留透明通道
    if lossless:
        img = img.convert("RGBA") if img.mode in ("RGBA", "LA", "P") else img.convert("RGB")
    else:
        img = img.convert("RGB")
    old_kb = os.path.getsize(src_path) / 1024
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
    if lossless:
        img.save(dst_path, "WEBP", lossless=True, method=6)
    else:
        img.save(dst_path, "WEBP", quality=quality, method=4)
    new_kb = os.path.getsize(dst_path) / 1024
    tag = "lossless" if lossless else f"q{quality}"
    print(f"  [{tag}] {os.path.relpath(src_path, base)} → {os.path.relpath(dst_path, base)}  {old_kb:.0f}KB → {new_kb:.0f}KB")
    return new_kb

# ══════════════════════════════════════════════
# 1. 手机截图（UI界面）：2x=292px + lossless
# ══════════════════════════════════════════════
print("=== 手机截图 UI 类：292px lossless ===")
mobile_ui = [
    # 方案1
    ("广场改版/方案1-大牌好价1.png", "广场改版/方案1-大牌好价1.webp"),
    ("广场改版/方案1-大牌好价2.png", "广场改版/方案1-大牌好价2.webp"),
    ("广场改版/方案1-整点抢.png",    "广场改版/方案1-整点抢.webp"),
    ("广场改版/方案1-福利中心.png",  "广场改版/方案1-福利中心.webp"),
    ("广场改版/方案1-精选1.png",     "广场改版/方案1-精选1.webp"),
    ("广场改版/方案1-精选2.png",     "广场改版/方案1-精选2.webp"),
    # 方案2
    ("广场改版/日常页面.webp",       "广场改版/日常页面.webp"),
    ("广场改版/有明星场时.webp",     "广场改版/有明星场时.webp"),
    ("广场改版/新人页面.webp",       "广场改版/新人页面.webp"),
    # 其他广场截图
    ("广场改版/最初样式.webp",       "广场改版/最初样式.webp"),
    ("广场改版/改版1.webp",          "广场改版/改版1.webp"),
    ("广场改版/改版2.webp",          "广场改版/改版2.webp"),
    ("广场改版/框架图.webp",         "广场改版/框架图.webp"),
    ("广场改版/广场-框架b.webp",     "广场改版/广场-框架b.webp"),
]
for src_rel, dst_rel in mobile_ui:
    src = os.path.join(base, src_rel)
    dst = os.path.join(base, dst_rel)
    if os.path.exists(src):
        save(src, dst, max_width=292, lossless=True)

# ══════════════════════════════════════════════
# 2. 直播间截图（ls-*.jpg）：展示约 200px 宽 → 2x=400px lossless
# ══════════════════════════════════════════════
print("\n=== 直播间截图：400px lossless ===")
for f in sorted(glob.glob(os.path.join(base, "images/livestream/*.jpg"))):
    dst = os.path.splitext(f)[0] + ".webp"
    save(f, dst, max_width=400, lossless=True)

# ══════════════════════════════════════════════
# 3. ai-search / search2 截图：展示约 200px → 2x=400px lossless
# ══════════════════════════════════════════════
print("\n=== ai-search / search2 截图：400px lossless ===")
for d in ["images/ai-search", "images/search2"]:
    for ext in ["*.jpg", "*.png"]:
        for f in sorted(glob.glob(os.path.join(base, d, ext))):
            dst = os.path.splitext(f)[0] + ".webp"
            save(f, dst, max_width=400, lossless=True)

# ══════════════════════════════════════════════
# 4. 全宽截图/流程图（非照片）：1600px lossless
# ══════════════════════════════════════════════
print("\n=== 全宽截图/流程图：1600px lossless ===")
wide_ui = [
    ("images/competitor-2.png",        "images/competitor-2.webp"),
    ("images/ai-cover-workflow.png",   "images/ai-cover-workflow.webp"),
    ("images/ai-cover-result.png",     "images/ai-cover-result.webp"),
    ("images/competitor-compare.png",  "images/competitor-compare.webp"),
    ("assets/solution-overview.png",   "assets/solution-overview.webp"),
    ("广场改版/广场框架1.webp",         "广场改版/广场框架1.webp"),
    ("广场改版/广场框架2.webp",         "广场改版/广场框架2.webp"),
    ("广场改版/广场-美食tab.png",       "广场改版/广场-美食tab.webp"),
]
for src_rel, dst_rel in wide_ui:
    src = os.path.join(base, src_rel)
    dst = os.path.join(base, dst_rel)
    if os.path.exists(src):
        save(src, dst, max_width=1600, lossless=True)

# ══════════════════════════════════════════════
# 5. 开播工具 AI 生图系列（截图/效果图）：1200px lossless
# ══════════════════════════════════════════════
print("\n=== 开播工具 AI 生图：1200px lossless ===")
ai_imgs = [
    ("开播工具ai生图/生成后@1.5x.png",  "开播工具ai生图/生成后@1.5x.webp"),
    ("开播工具ai生图/方案.png",          "开播工具ai生图/方案.webp"),
    ("开播工具ai生图/生成中@1.5x.png",  "开播工具ai生图/生成中@1.5x.webp"),
    ("开播工具ai生图/flowchart.png",     "开播工具ai生图/flowchart.webp"),
    ("开播工具ai生图/配图2.png",         "开播工具ai生图/配图2.webp"),
    ("开播工具ai生图/配图.png",          "开播工具ai生图/配图.webp"),
    ("images/生成中.png",               "images/生成中.webp"),
    ("images/生成后.png",               "images/生成后.webp"),
]
for src_rel, dst_rel in ai_imgs:
    src = os.path.join(base, src_rel)
    dst = os.path.join(base, dst_rel)
    if os.path.exists(src):
        save(src, dst, max_width=1200, lossless=True)

# ══════════════════════════════════════════════
# 6. 竞品截图（assets/competitor/）：1200px lossless
# ══════════════════════════════════════════════
print("\n=== 竞品截图：1200px lossless ===")
for ext in ["*.jpg", "*.jpeg", "*.png"]:
    for f in sorted(glob.glob(os.path.join(base, "assets/competitor", ext))):
        dst = os.path.splitext(f)[0] + ".webp"
        try:
            save(f, dst, max_width=1200, lossless=True)
        except Exception as e:
            print(f"  [ERROR] {f}: {e}")

# ══════════════════════════════════════════════
# 7. images/ 根目录截图（13-21.jpg/png）：1200px lossless
# ══════════════════════════════════════════════
print("\n=== images/ 根目录截图：1200px lossless ===")
for ext in ["*.jpg", "*.jpeg", "*.png"]:
    for f in sorted(glob.glob(os.path.join(base, "images", ext))):
        # 跳过已处理的 webp
        if f.endswith(".webp"):
            continue
        dst = os.path.splitext(f)[0] + ".webp"
        try:
            save(f, dst, max_width=1200, lossless=True)
        except Exception as e:
            print(f"  [ERROR] {f}: {e}")

# ══════════════════════════════════════════════
# 8. avatar（真实照片）：400px quality=92
# ══════════════════════════════════════════════
print("\n=== avatar（照片）：400px q92 ===")
avatar_src = os.path.join(base, "avatar.webp")  # 已是 webp，从原 png 重新生成
avatar_png = os.path.join(base, "avatar.png")
avatar_dst = os.path.join(base, "avatar.webp")
if os.path.exists(avatar_png):
    save(avatar_png, avatar_dst, max_width=400, lossless=False, quality=92)
else:
    # 从现有 webp 重新以 q92 保存（已经是 400px）
    img = Image.open(avatar_src).convert("RGB")
    old_kb = os.path.getsize(avatar_src) / 1024
    img.save(avatar_dst, "WEBP", quality=92, method=4)
    new_kb = os.path.getsize(avatar_dst) / 1024
    print(f"  [q92] avatar.webp  {old_kb:.0f}KB → {new_kb:.0f}KB")

print("\n✅ 全部完成！")
