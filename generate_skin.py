"""Generates skin.png — a 64x64 Minecraft skin (classic 4px arms).

Look: curly brown hair, white tank top, maroon sweater tied over the
shoulders (hood draped on the back), black belt, baggy black cargo pants,
white sneakers, black wristband on the left arm.

Run:  python3 generate_skin.py
"""
import random
from PIL import Image

T = None  # transparent

# ---------- palette ----------
SKIN = [(239, 192, 150), (228, 175, 130), (214, 160, 117), (196, 142, 102)]
HAIR = [(38, 23, 15), (56, 35, 22), (76, 49, 31), (96, 64, 40), (118, 80, 51)]
EYE_W = (236, 236, 236)
IRIS = (38, 92, 96)
IRIS_D = (26, 58, 62)
BROW = (60, 38, 24)
MOUTH = (190, 128, 96)
MAR = [(64, 16, 22), (86, 24, 31), (106, 32, 39), (126, 44, 51), (146, 58, 64)]
TANK = [(242, 242, 240), (228, 228, 226), (210, 210, 210)]
PANT = [(20, 18, 18), (29, 26, 25), (38, 34, 32), (50, 45, 42)]
BELT = (30, 29, 30)
BUCKLE = [(150, 150, 156), (104, 104, 110)]
SHOE = [(244, 244, 244), (222, 222, 224), (186, 186, 192)]
BAND = [(28, 28, 30), (58, 58, 64)]

img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
rnd = random.Random(7)


def put(x, y, c):
    if c is not None:
        img.putpixel((x, y), c + (255,) if len(c) == 3 else c)


def face(x0, y0, w, h, fn):
    for j in range(h):
        for i in range(w):
            put(x0 + i, y0 + j, fn(i, j))


def pick(pal, weights):
    return rnd.choices(pal, weights=weights)[0]


def hair(i, j, light=0):
    """Curly hair: clumps of 2x2 with highlights and dark gaps."""
    cell = ((i + (j // 2) % 2) // 2, j // 2)
    h = hash((cell, light)) % 5
    if h == 0:
        base = [0, 1]
    elif h in (1, 2):
        base = [1, 2]
    else:
        base = [2, 3]
    if light:
        base = [min(b + 1, 4) for b in base]
    c = HAIR[rnd.choice(base)]
    if rnd.random() < 0.12:
        c = HAIR[min(base[-1] + 1, 4)]
    if rnd.random() < 0.10:
        c = HAIR[0]
    return c


def skin(i, j, shade=1):
    if shade == 1 and i == 1 and 1 <= j <= 8:
        return SKIN[0]  # soft highlight down the arm
    return SKIN[min(3, shade + (1 if rnd.random() < 0.05 else 0))]


def pant(i, j, w):
    c = PANT[1] if rnd.random() < 0.7 else PANT[2]
    if rnd.random() < 0.08:
        c = PANT[0]
    return c


# =====================================================================
# HEAD  (base at 0,0 ; overlay at 32,0)
# faces: top(8,0) bottom(16,0) right(0,8) front(8,8) left(16,8) back(24,8)
# =====================================================================
face(8, 0, 8, 8, lambda i, j: hair(i, j, 1))                    # top
face(16, 0, 8, 8, lambda i, j: SKIN[2])                         # bottom (chin)

FRONT = [
    "HHHHHHHH",
    "HHHHHHHH",
    "HHHsHHHH",
    "HBBssBBH",
    "HWIssIWH",
    "SssnnssS",
    "sssmmsss",
    "SsssssSS",
]


def head_front(i, j):
    k = FRONT[j][i]
    if k == "H":
        return hair(i, j)
    if k == "B":
        return BROW
    if k == "W":
        return EYE_W
    if k == "I":
        return IRIS if j == 4 else IRIS_D
    if k == "m":
        return MOUTH
    if k == "n":
        return SKIN[2]
    if k == "S":
        return SKIN[2]
    return SKIN[1]


face(8, 8, 8, 8, head_front)


def head_side(front_on_right):
    def fn(i, j):
        f = i if front_on_right else 7 - i  # f: 7 = towards face
        if j <= 3:
            return hair(i, j)
        if j <= 5 and f >= 3:
            if f == 4 and j == 5:
                return SKIN[3]  # ear
            return SKIN[2] if f < 6 else SKIN[1]
        if j >= 6 and f >= 2:
            return SKIN[2]
        return hair(i, j)
    return fn


face(0, 8, 8, 8, head_side(True))    # right: texture right edge = front
face(16, 8, 8, 8, head_side(False))  # left: texture left edge = front
face(24, 8, 8, 8, lambda i, j: hair(i, j) if j < 7 else SKIN[2])  # back

# ---- hat overlay: big curly volume ----
face(40, 0, 8, 8, lambda i, j: hair(i, j, 1))                   # top
# front: ragged bangs, sideburns, eyes stay clear
BANG = [3, 3, 4, 3, 3, 4, 3, 3]  # rows covered per column
SIDE_LOCK = {0: 5, 7: 5}


def hat_front(i, j):
    depth = SIDE_LOCK.get(i, BANG[i])
    if j < depth - 1:
        return hair(i, j, 1 if j == 0 else 0)
    if j == depth - 1 and (i + j) % 2 == 0:
        return hair(i, j)
    if i in (0, 7) and j < depth:
        return hair(i, j)
    return T


face(40, 8, 8, 8, hat_front)


def hat_side(front_on_right):
    def fn(i, j):
        f = i if front_on_right else 7 - i
        limit = 7 if f < 3 else (5 if f < 6 else 4)
        if j < limit:
            return hair(i, j, 1 if j < 2 else 0)
        if j == limit and rnd.random() < 0.5:
            return hair(i, j)
        return T
    return fn


face(32, 8, 8, 8, hat_side(True))
face(48, 8, 8, 8, hat_side(False))
face(56, 8, 8, 8, lambda i, j: hair(i, j, 1 if j < 3 else 0)
     if j < 7 or (i % 3 != 1) else T)                            # back

# =====================================================================
# BODY  (base 16,16 ; overlay 16,32)
# top(20,16 8x4) bottom(28,16) right(16,20 4x12) front(20,20 8x12)
# left(28,20) back(32,20 8x12)
# =====================================================================


def torso_tank(i, j, back=False):
    if j == 9:  # belt
        if not back and i in (3, 4):
            return BUCKLE[0] if i == 3 else BUCKLE[1]
        return BELT
    if j >= 10:
        return pant(i, j, 8)
    if j == 0 and 2 <= i <= 5:
        return SKIN[1] if not back else SKIN[2]
    if j == 1 and 3 <= i <= 4 and not back:
        return SKIN[1]
    if j <= 2 and i in (0, 7):
        return SKIN[2]
    c = TANK[0]
    if j in (7, 8) or i in (0, 7):
        c = TANK[1]
    if rnd.random() < 0.08:
        c = TANK[2]
    return c


face(20, 20, 8, 12, lambda i, j: torso_tank(i, j))
face(32, 20, 8, 12, lambda i, j: torso_tank(i, j, back=True))
face(16, 20, 4, 12, lambda i, j: torso_tank(i + 1, j, back=True))
face(28, 20, 4, 12, lambda i, j: torso_tank(i + 1, j, back=True))
face(20, 16, 8, 4, lambda i, j: SKIN[1] if 2 <= i <= 5 and 1 <= j <= 2 else TANK[1])
face(28, 16, 8, 4, lambda i, j: PANT[1])

# ---- body overlay: sweater over shoulders ----
SWEATER_FRONT = [
    "lmmmmmml",
    "mdmmmmdm",
    "..kKKk..",
    "..kKKk..",
    "..mdlm..",
    "..mdlm..",
    "..mdlm..",
    "..mdlm..",
    "..cccc..",
]
HOOD_BACK = [
    "lmmmmmml",
    "mmlmmlmm",
    ".dmmmmd.",
    ".mlmmlm.",
    "..dmmd..",
    "..mlmm..",
    "...dd...",
]
SW = {"l": MAR[3], "m": MAR[2], "d": MAR[1], "k": MAR[1], "K": MAR[3],
      "c": MAR[0]}


def from_map(m):
    def fn(i, j):
        if j >= len(m):
            return T
        k = m[j][i]
        if k == ".":
            return T
        c = SW[k]
        if rnd.random() < 0.1 and k == "m":
            c = MAR[3]
        return c
    return fn


face(20, 36, 8, 12, from_map(SWEATER_FRONT))
face(32, 36, 8, 12, from_map(HOOD_BACK))
face(16, 36, 4, 12, lambda i, j: SW["m"] if j < 2 else T)       # right side
face(28, 36, 4, 12, lambda i, j: SW["m"] if j < 2 else T)       # left side
face(20, 32, 8, 4, lambda i, j: T if 2 <= i <= 5 and 1 <= j <= 2 else MAR[3])
# pants overlay on the hips (matches baggy legs)
for x0, w in ((20, 8), (32, 8), (16, 4), (28, 4)):
    face(x0, 46, w, 2, lambda i, j, w=w: pant(i, j, w))

# =====================================================================
# ARMS (classic 4px)
# right arm base 40,16 / overlay 40,32 ; left arm base 32,48 / overlay 48,48
# top(+4,+0) bottom(+8,+0) right(+0,+4) front(+4,+4) left(+8,+4) back(+12,+4)
# =====================================================================


def arm_face(band, inner=False):
    def fn(i, j):
        if band and j == 9:
            return BAND[1] if i == 1 else BAND[0]
        shade = 2 if inner else 1
        if j == 0:
            shade = 2
        if j >= 11:
            shade = 2
        return skin(i, j, shade)
    return fn


def build_arm(bx, by, ox, oy, band, outer_is_right):
    face(bx + 4, by, 4, 4, lambda i, j: SKIN[1])
    face(bx + 8, by, 4, 4, lambda i, j: SKIN[2])
    face(bx + 0, by + 4, 4, 12, arm_face(band, inner=not outer_is_right))
    face(bx + 4, by + 4, 4, 12, arm_face(band))
    face(bx + 8, by + 4, 4, 12, arm_face(band, inner=outer_is_right))
    face(bx + 12, by + 4, 4, 12, arm_face(band))
    # sweater draped over the shoulder (overlay)
    face(ox + 4, oy, 4, 4, lambda i, j: MAR[3])

    def drape(outer):
        def fn(i, j):
            if j == 0:
                return MAR[3]
            if j == 1:
                return MAR[2]
            if j == 2 and outer and i in (1, 2):
                return MAR[1]
            return T
        return fn
    face(ox + 0, oy + 4, 4, 12, drape(outer_is_right))
    face(ox + 4, oy + 4, 4, 12, drape(False))
    face(ox + 8, oy + 4, 4, 12, drape(not outer_is_right))
    face(ox + 12, oy + 4, 4, 12, drape(False))


build_arm(40, 16, 40, 32, band=False, outer_is_right=True)
build_arm(32, 48, 48, 48, band=True, outer_is_right=False)

# =====================================================================
# LEGS
# right leg base 0,16 / overlay 0,32 ; left leg base 16,48 / overlay 0,48
# =====================================================================


def leg_face(kind, pocket=False):
    def fn(i, j):
        if j == 11:
            return SHOE[2] if kind != "front" else SHOE[1]
        if j == 10:
            return SHOE[0]
        if pocket and 3 <= j <= 6:
            if j == 3 or i in (0, 3):
                return PANT[3]
            return PANT[2]
        c = pant(i, j, 4)
        if kind == "front" and j in (5, 6) and i in (1, 2):
            c = PANT[0]  # knee fold
        if j == 9:
            c = PANT[0]  # bunched hem
        return c
    return fn


def leg_overlay(kind, pocket=False):
    base = leg_face(kind, pocket)

    def fn(i, j):
        if j >= 11:
            return T
        if j == 10:
            return T
        if j < 7 and not pocket:
            return T
        return base(i, j)
    return fn


def build_leg(bx, by, ox, oy, outer_is_right):
    face(bx + 4, by, 4, 4, lambda i, j: PANT[1])
    face(bx + 8, by, 4, 4, lambda i, j: SHOE[2])
    face(bx + 0, by + 4, 4, 12, leg_face("side", pocket=outer_is_right))
    face(bx + 4, by + 4, 4, 12, leg_face("front"))
    face(bx + 8, by + 4, 4, 12, leg_face("side", pocket=not outer_is_right))
    face(bx + 12, by + 4, 4, 12, leg_face("back"))
    face(ox + 0, oy + 4, 4, 12, leg_overlay("side", pocket=outer_is_right))
    face(ox + 4, oy + 4, 4, 12, leg_overlay("front"))
    face(ox + 8, oy + 4, 4, 12, leg_overlay("side", pocket=not outer_is_right))
    face(ox + 12, oy + 4, 4, 12, leg_overlay("back"))


build_leg(0, 16, 0, 32, outer_is_right=True)
build_leg(16, 48, 0, 48, outer_is_right=False)

img.save("skin.png")
print("saved skin.png")
