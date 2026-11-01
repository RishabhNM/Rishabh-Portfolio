"""Makes lighter copies of the project media so the site opens panels without lag.

Run from the project folder after adding or replacing images or clips:

    python tools/make-web-assets.py

- Screenshots in site.yaml get a small preview in images/thumbs/ (the full image is still used when you enlarge it).
- Page backgrounds (images/backgrounds/) get a greyscale 1920px copy and a blurred copy in images/web/ (point `page_background:` and `page_background_blur:` at them).
- Clips that are bigger than 1280px or run above 30 fps get a lighter copy in images/web/ (originals are never touched).
  Point `src:` in site.yaml at the images/web/ copy for those clips.
"""
import os, re, subprocess, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
yaml_text = open("site.yaml", encoding="utf-8").read()
files = sorted(set(re.findall(r"images/[\w\-./ ]+?\.(?:png|jpe?g|webp|mp4)", yaml_text)))
import glob
files += sorted(g.replace(os.sep, "/") for g in glob.glob("images/backgrounds/*") if g.lower().endswith((".png", ".jpg", ".jpeg")))

os.makedirs("images/thumbs", exist_ok=True)
os.makedirs("images/web", exist_ok=True)

for f in files:
    if not os.path.exists(f) or "/thumbs/" in f or "/web/" in f:
        continue
    name, ext = os.path.splitext(os.path.basename(f))
    if "/backgrounds/" in f and ext.lower() in (".png", ".jpg", ".jpeg"):
        out = f"images/web/{name}.webp"
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(f):
            continue
        im = Image.open(f).convert("L").convert("RGB")   # greyscale, so the site keeps a gray theme
        w = min(1920, im.width)
        im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).save(out, "WEBP", quality=80, method=6)
        print("page background", out, os.path.getsize(out) // 1024, "KB")
        # a small, very blurry copy: the panels show this one, which looks like frosted glass without any GPU effect
        from PIL import ImageFilter
        small = im.resize((960, round(im.height * 960 / im.width)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(16))
        blur_out = f"images/web/{name}-blur.webp"
        small.save(blur_out, "WEBP", quality=72, method=6)
        print("blurred copy   ", blur_out, os.path.getsize(blur_out) // 1024, "KB")
        continue
    if ext.lower() in (".png", ".jpg", ".jpeg"):
        out = f"images/thumbs/{name}.webp"
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(f):
            continue
        im = Image.open(f).convert("RGBA" if ext.lower() == ".png" else "RGB")
        w = 420
        h = round(im.height * w / im.width)
        im.resize((w, h), Image.LANCZOS).save(out, "WEBP", quality=84, method=6)
        print("thumb", out, os.path.getsize(out) // 1024, "KB")
    elif ext.lower() == ".mp4":
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate", "-of", "csv=p=0", f],
            capture_output=True, text=True).stdout.strip().split(",")
        w, h, rate = int(probe[0]), int(probe[1]), probe[2]
        num, den = (rate.split("/") + ["1"])[:2]
        fps = float(num) / float(den or 1)
        if max(w, h) <= 1280 and fps <= 31:
            continue
        out = f"images/web/{name}.mp4"
        if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(f):
            continue
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", f,
             "-vf", "scale='min(1280,iw)':'min(1280,ih)':force_original_aspect_ratio=decrease:force_divisible_by=2,fps=30",
             "-c:v", "libx264", "-crf", "23", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", out],
            check=True)
        print("clip ", out, round(os.path.getsize(out) / 1e6, 2), "MB")
print("done")
