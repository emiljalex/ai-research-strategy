"""Recreate the original, non-quantitative handoff illustration. Requires Pillow."""
from math import cos, exp, pi, sin
from pathlib import Path
from PIL import Image, ImageDraw

W, H, SCALE = 960, 540, 2
image = Image.new("RGB", (W * SCALE, H * SCALE), "#101d37")
draw = ImageDraw.Draw(image)


def line(points, color, width=1):
    draw.line([(round(x * SCALE), round(y * SCALE)) for x, y in points],
              fill=color, width=max(1, round(width * SCALE)), joint="curve")


def circle(x, y, radius, color, outline=False):
    box = tuple(round(v * SCALE) for v in (x - radius, y - radius, x + radius, y + radius))
    if outline:
        draw.ellipse(box, outline=color, width=SCALE)
    else:
        draw.ellipse(box, fill=color)


def trace(x, layer):
    # The fan narrows at the decision boundary, then opens into possible readings.
    mid = 276 + 51 * sin((x / W * 1.9 - .29) * pi) - 28 * x / W
    width = 13 + 182 * (1 - exp(-((x - 493) / 235) ** 2))
    curled = 29 * sin(x / W * 2.75 * pi + .5) * (1 - layer ** 2)
    return mid + layer * width * .70 + curled


for x in range(0, W + 1, 32):
    line([(x, 0), (x, H)], "#1a2942", .5)
for y in range(0, H + 1, 32):
    line([(0, y), (W, y)], "#1a2942", .5)
for x in range(32, W, 96):
    for y in range(32, H, 96):
        line([(x - 2, y), (x + 2, y)], "#33415c", .6)
        line([(x, y - 2), (x, y + 2)], "#33415c", .6)

for i in range(51):
    layer = (i - 25) / 25
    brightness = (1 + cos(i * pi / 18)) / 2
    tone = (round(99 + 72 * brightness), round(138 + 54 * brightness), round(202 + 40 * brightness))
    line([(x, trace(x, layer)) for x in range(-2, W + 4, 3)], tone, .9)

# The copper intervention departs from the upper trace and rejoins at the gate.
x0, x1 = 263, 503
branch = []
for x in range(x0, x1 + 1):
    t = (x - x0) / (x1 - x0)
    lift = 102 * sin(pi * t) ** 2
    branch.append((x, trace(x, -1 + t) - lift))
line(branch, "#f1ab73", 2.6)
exit_path = [(x, trace(x, 0.22 * sin((x - x1) / 400 * pi))) for x in range(x1, W + 1, 2)]
line(exit_path, "#f1ab73", 2)
for x, y in [branch[0], branch[-1]]:
    circle(x, y, 7, "#121d37")
    circle(x, y, 6, "#f2af80", True)
    circle(x, y, 2.4, "#f2af80")
xg, yg = branch[-1]
for y in range(100, H - 65, 8):
    if abs(y - yg) > 12:
        line([(xg, y), (xg, y + 3)], "#74839d", .8)
image.resize((W * 3 // 2, H * 3 // 2), Image.Resampling.LANCZOS).save(
    Path(__file__).resolve().parents[1] / "assets" / "handoff.webp",
    quality=91, method=6)

icon = Image.new("RGB", (64, 64), "#fafaf6")
pen = ImageDraw.Draw(icon)
for x, y, depth in [(8, 29, 25), (20, 29, 17), (32, 21, 23), (44, 12, 29)]:
    pen.polygon([(x, y), (x + 8, y - 3), (x + 8, y + depth - 3), (x, y + depth)], fill="#28439c")
icon.save(Path(__file__).resolve().parents[1] / "assets" / "mark.png")
