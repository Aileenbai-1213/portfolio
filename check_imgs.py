from PIL import Image
import os

base = "/Users/ailin/Documents/美团工作/portfolio"
imgs = [
    "广场改版/方案1-大牌好价1.webp",
    "广场改版/方案1-精选1.webp",
    "广场改版/日常页面.webp",
    "images/livestream/ls-3.webp",
    "images/livestream/ls-1-1.webp",
    "images/competitor-2.webp",
    "images/ai-cover-workflow.webp",
    "images/21.webp",
    "avatar.webp",
    "assets/solution-overview.webp",
    "images/search2/s2-3.webp",
    "images/ai-search/ai-2.webp",
]
for p in imgs:
    fp = os.path.join(base, p)
    if os.path.exists(fp):
        img = Image.open(fp)
        kb = os.path.getsize(fp) / 1024
        print(f"{p}: {img.width}x{img.height}  {kb:.0f}KB")
