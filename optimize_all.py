"""
全站图片优化：
1. 手机截图类（展示 146px 宽）→ resize 到 438px 宽 + 有损 WebP quality=85
2. 大图（全宽展示）→ resize 到最大 1200px 宽 + 有损 WebP quality=82
3. avatar → resize 到 400px + 有损 WebP quality=85
"""
from PIL import Image
import os

base = "/Users/ailin/Documents/美团工作/portfolio"

def save_webp(img, out_path, quality=85):
    img.save(out_path, "WEBP", quality=quality, method=4)
    return os.path.getsize(out_path) / 1024

def resize_and_save(src_path, out_path, max_width, quality=85):
    img = Image.open(src_path).convert("RGB")
    old_kb = os.path.getsize(src_path) / 1024
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
    new_kb = save_webp(img, out_path, quality)
    print(f"  {os.path.relpath(src_path, base)}  {old_kb:.0f}KB → {new_kb:.0f}KB  (节省 {(1-new_kb/old_kb)*100:.0f}%)")

# ── 1. 手机截图：方案2（日常/明星/新人）还没 resize ──
mobile_438 = [
    "广场改版/日常页面.webp",
    "广场改版/有明星场时.webp",
    "广场改版/新人页面.webp",
]
print("=== 方案2手机截图 resize 到 438px ===")
for rel in mobile_438:
    path = os.path.join(base, rel)
    img = Image.open(path).convert("RGB")
    old_kb = os.path.getsize(path) / 1024
    if img.width > 438:
        ratio = 438 / img.width
        img = img.resize((438, int(img.height * ratio)), Image.LANCZOS)
    new_kb = save_webp(img, path, quality=85)
    print(f"  {rel}  {old_kb:.0f}KB → {new_kb:.0f}KB  (节省 {(1-new_kb/old_kb)*100:.0f}%)")

# ── 2. 方案1手机截图：已 resize 但用了无损，改为有损 quality=85 ──
mobile_scheme1 = [
    "广场改版/方案1-大牌好价1.webp",
    "广场改版/方案1-大牌好价2.webp",
    "广场改版/方案1-整点抢.webp",
    "广场改版/方案1-福利中心.webp",
    "广场改版/方案1-精选1.webp",
    "广场改版/方案1-精选2.webp",
]
print("\n=== 方案1手机截图 改为有损 quality=85 ===")
for rel in mobile_scheme1:
    path = os.path.join(base, rel)
    img = Image.open(path).convert("RGB")
    old_kb = os.path.getsize(path) / 1024
    new_kb = save_webp(img, path, quality=85)
    print(f"  {rel}  {old_kb:.0f}KB → {new_kb:.0f}KB  (节省 {(1-new_kb/old_kb)*100:.0f}%)")

# ── 3. 大图转 WebP ──
print("\n=== 大图压缩 ===")

# avatar.webp 7.5MB → 400px
avatar_path = os.path.join(base, "avatar.webp")
resize_and_save(avatar_path, avatar_path, max_width=400, quality=88)

# solution-overview.png → webp
sol_src = os.path.join(base, "assets/solution-overview.png")
sol_dst = os.path.join(base, "assets/solution-overview.webp")
resize_and_save(sol_src, sol_dst, max_width=1200, quality=82)

# competitor-2.png → webp（已有 webp 版本，重新生成更小的）
comp2_src = os.path.join(base, "images/competitor-2.png")
comp2_dst = os.path.join(base, "images/competitor-2.webp")
resize_and_save(comp2_src, comp2_dst, max_width=1200, quality=82)

# images/21.png
img21_src = os.path.join(base, "images/21.png")
img21_dst = os.path.join(base, "images/21.webp")
if os.path.exists(img21_src):
    resize_and_save(img21_src, img21_dst, max_width=1200, quality=82)

# images/18.png
img18_src = os.path.join(base, "images/18.png")
img18_dst = os.path.join(base, "images/18.webp")
if os.path.exists(img18_src):
    resize_and_save(img18_src, img18_dst, max_width=1200, quality=82)

# images/19.png
img19_src = os.path.join(base, "images/19.png")
img19_dst = os.path.join(base, "images/19.webp")
if os.path.exists(img19_src):
    resize_and_save(img19_src, img19_dst, max_width=1200, quality=82)

# images/20.png
img20_src = os.path.join(base, "images/20.png")
img20_dst = os.path.join(base, "images/20.webp")
if os.path.exists(img20_src):
    resize_and_save(img20_src, img20_dst, max_width=1200, quality=82)

# ai-cover-workflow.png
wf_src = os.path.join(base, "images/ai-cover-workflow.png")
wf_dst = os.path.join(base, "images/ai-cover-workflow.webp")
if os.path.exists(wf_src):
    resize_and_save(wf_src, wf_dst, max_width=1200, quality=82)

# ai-cover-result.png
res_src = os.path.join(base, "images/ai-cover-result.png")
res_dst = os.path.join(base, "images/ai-cover-result.webp")
if os.path.exists(res_src):
    resize_and_save(res_src, res_dst, max_width=1200, quality=82)

# competitor-compare.png
cc_src = os.path.join(base, "images/competitor-compare.png")
cc_dst = os.path.join(base, "images/competitor-compare.webp")
if os.path.exists(cc_src):
    resize_and_save(cc_src, cc_dst, max_width=1200, quality=82)

# 开播工具ai生图 系列
ai_imgs = [
    ("开播工具ai生图/生成后@1.5x.png", "开播工具ai生图/生成后@1.5x.webp", 900),
    ("开播工具ai生图/方案.png", "开播工具ai生图/方案.webp", 1200),
    ("开播工具ai生图/生成中@1.5x.png", "开播工具ai生图/生成中@1.5x.webp", 900),
    ("开播工具ai生图/flowchart.png", "开播工具ai生图/flowchart.webp", 1200),
    ("开播工具ai生图/配图2.png", "开播工具ai生图/配图2.webp", 1200),
    ("开播工具ai生图/配图.png", "开播工具ai生图/配图.webp", 1200),
]
for src_rel, dst_rel, mw in ai_imgs:
    src = os.path.join(base, src_rel)
    dst = os.path.join(base, dst_rel)
    if os.path.exists(src):
        resize_and_save(src, dst, max_width=mw, quality=82)

# images/生成后.png
gen_src = os.path.join(base, "images/生成后.png")
gen_dst = os.path.join(base, "images/生成后.webp")
if os.path.exists(gen_src):
    resize_and_save(gen_src, gen_dst, max_width=900, quality=82)

# assets/competitor/jimeng-multimodal.jpg
jm_src = os.path.join(base, "assets/competitor/jimeng-multimodal.jpg")
jm_dst = os.path.join(base, "assets/competitor/jimeng-multimodal.webp")
if os.path.exists(jm_src):
    resize_and_save(jm_src, jm_dst, max_width=1200, quality=82)

# 广场改版/广场-美食tab.png
mt_src = os.path.join(base, "广场改版/广场-美食tab.png")
mt_dst = os.path.join(base, "广场改版/广场-美食tab.webp")
if os.path.exists(mt_src):
    resize_and_save(mt_src, mt_dst, max_width=438, quality=85)

print("\n✅ 全部完成！")
