#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""在 `npx cap add android` 之后运行：覆盖图标、启动屏、主题，生成深色沉浸式原生壳。"""
import os, math, shutil
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "android", "app", "src", "main", "res")

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def gradient(img, c_top, c_bot):
    w, h = img.size
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = 0.5 * x / w + 0.5 * y / h
            px[x, y] = lerp(c_top, c_bot, t)

def arrow(draw, p1, p2, width, color):
    draw.line([p1, p2], fill=color, width=width)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    L = 46
    h1 = (p2[0] + math.cos(ang + math.radians(150)) * L,
          p2[1] + math.sin(ang + math.radians(150)) * L)
    h2 = (p2[0] + math.cos(ang - math.radians(150)) * L,
          p2[1] + math.sin(ang - math.radians(150)) * L)
    draw.polygon([p2, h1, h2], fill=color)

def make_mark(size, with_bg):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    if with_bg:
        bg = Image.new("RGB", (size, size))
        gradient(bg, (11, 17, 32), (30, 41, 59))
        img.paste(bg, (0, 0))
    d = ImageDraw.Draw(img)
    s = size / 512.0
    sc = lambda v: int(v * s)
    bw, gap, base_y = 62, 30, 408
    heights = [120, 196, 272]
    x0 = (512 - (3 * bw + 2 * gap)) / 2
    colors = [(234, 88, 12, 255), (249, 115, 22, 255), (251, 146, 60, 255)]
    for i, hgt in enumerate(heights):
        x = x0 + i * (bw + gap)
        d.rounded_rectangle([sc(x), sc(base_y - hgt), sc(x + bw), sc(base_y)],
                            radius=sc(14), fill=colors[i])
    d.rounded_rectangle([sc(108), sc(base_y + 10), sc(404), sc(base_y + 22)],
                        radius=sc(6), fill=(148, 163, 184, 255))
    arrow(d, (sc(150), sc(252)), (sc(372), sc(108)), sc(20), (250, 204, 21, 255))
    return img

logo_full = make_mark(512, True)
logo_trans = make_mark(1024, False)
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
logo_full.convert("RGB").save(os.path.join(ROOT, "assets", "icon-512.png"))

# 启动器图标（整图，删除自适应）
for dens, px in {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}.items():
    folder = os.path.join(RES, "mipmap-" + dens)
    os.makedirs(folder, exist_ok=True)
    ic = logo_full.resize((px, px), Image.LANCZOS)
    ic.save(os.path.join(folder, "ic_launcher.png"))
    ic.save(os.path.join(folder, "ic_launcher_round.png"))
    ic.save(os.path.join(folder, "ic_launcher_foreground.png"))
ad = os.path.join(RES, "mipmap-anydpi-v26")
if os.path.isdir(ad):
    shutil.rmtree(ad, ignore_errors=True)

# 启动屏
def splash(w, h):
    bg = Image.new("RGB", (w, h), (15, 23, 42))
    m = int(min(w, h) * 0.34)
    mark = logo_trans.resize((m, m), Image.LANCZOS)
    bg.paste(mark, ((w - m) // 2, (h - m) // 2), mark)
    return bg

dims = {"drawable-port-mdpi": (320, 480), "drawable-port-hdpi": (480, 800),
        "drawable-port-xhdpi": (720, 1280), "drawable-port-xxhdpi": (960, 1600),
        "drawable-port-xxxhdpi": (1280, 1920), "drawable-land-mdpi": (480, 320),
        "drawable-land-hdpi": (800, 480), "drawable-land-xhdpi": (1280, 720),
        "drawable-land-xxhdpi": (1600, 960), "drawable-land-xxxhdpi": (1920, 1280)}
for dens, (w, h) in dims.items():
    folder = os.path.join(RES, dens)
    os.makedirs(folder, exist_ok=True)
    splash(w, h).save(os.path.join(folder, "splash.png"))
splash(1080, 1920).save(os.path.join(RES, "drawable", "splash.png"))

# 深色主题
with open(os.path.join(RES, "values", "styles.xml"), "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.Light.DarkActionBar">
        <item name="colorPrimary">@color/colorPrimary</item>
        <item name="colorPrimaryDark">@color/colorPrimaryDark</item>
        <item name="colorAccent">@color/colorAccent</item>
    </style>
    <style name="AppTheme.NoActionBar" parent="Theme.AppCompat.DayNight.NoActionBar">
        <item name="windowActionBar">false</item>
        <item name="windowNoTitle">true</item>
        <item name="android:background">@null</item>
        <item name="android:windowBackground">#0F172A</item>
        <item name="android:statusBarColor">#0F172A</item>
        <item name="android:navigationBarColor">#0F172A</item>
    </style>
    <style name="AppTheme.NoActionBarLaunch" parent="Theme.SplashScreen">
        <item name="android:background">@drawable/splash</item>
    </style>
</resources>
""")
print("native assets prepared OK")
