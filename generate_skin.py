"""Generates skin.png — a 64x64 Minecraft skin (classic 4px arms).

Based on reference photos: curly dark-brown hair with a messy
fringe and visible ears, grey-blue eyes, white ribbed tank top with open
shoulders, dark burgundy sweater tied over the shoulders (sleeves knotted on
the chest, hood draped on the back), black leather belt with a steel buckle,
wide black denim jeans with contrast stitching, chunky white/silver
sneakers, steel watch with a brown leather strap on the left wrist.

Run:  python3 generate_skin.py
"""
import random
from PIL import Image

T = None  # transparent

# ---------- palette ----------
SKIN = [(232, 182, 142), (221, 168, 126), (204, 150, 110), (182, 131, 94)]
EAR = (198, 140, 106)
HAIR = [(24, 16, 11), (38, 26, 18), (54, 37, 26), (72, 50, 35), (92, 65, 45)]
EYE_W = (232, 232, 230)
IRIS = (104, 124, 134)
BROW = (40, 28, 21)
LIPS = (186, 124, 100)
MAR = [(46, 14, 22), (62, 20, 30), (78, 27, 38), (94, 36, 47), (110, 47, 57)]
TANK = [(244, 244, 242), (230, 230, 228), (212, 212, 212)]
DEN = [(13, 13, 15), (19, 19, 22), (26, 26, 30), (34, 34, 38)]
STITCH = (52, 49, 45)
BELT = [(24, 22, 22), (40, 37, 36)]
STEEL = [(196, 198, 204), (150, 152, 160), (104, 106, 114)]
DIAL = (20, 22, 26)
STRAP = [(104, 66, 40), (80, 50, 30)]
SHOE = [(246, 246, 246), (226, 226, 230), (190, 192, 200), (70, 70, 76)]

img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
rnd = random.Random(11)


def put(x, y, c):
    if c is not None:
        img.putpixel((x, y), c + (255,))


def face(x0, y0, w, h, fn):
    for j in range(h):
        for i in range(w):
            put(x0 + i, y0 + j, fn(i, j))


def hair(i, j, top=False):
    """Curly hair: staggered 2x2 curls, lit on top-left, shadow bottom-right."""
    shift = ((j // 2) * 3 + (i // 4)) % 2
    lx, ly = (i + shift) % 2, (j + (i // 2) % 2) % 2
    if lx == 0 and ly == 0:
        k = 3
    elif lx == 1 and ly == 1:
        k = 1
    else:
        k = 2
    if top:
        k += 1
    if rnd.random() < 0.25:
        k += rnd.choice((-1, 1))
    return HAIR[max(0, min(4, k))]


def skin(i, j, shade=1):
    return SKIN[min(3, shade + (1 if rnd.random() < 0.05 else 0))]


def denim(i, j):
    r = rnd.random()
    return DEN[1] if r < 0.7 else (DEN[2] if r < 0.88 else DEN[0])


# =====================================================================
# HEAD  base (0,0) / overlay (32,0)
# top(+8,0) bottom(+16,0) right(0,8) front(8,8) left(16,8) back(24,8)
# =====================================================================
face(8, 0, 8, 8, lambda i, j: hair(i, j, top=True))
face(16, 0, 8, 8, lambda i, j: SKIN[2])

FRONT = [
    "HHHHHHHH",
    "HHHHHHHH",
    "HssssssH",
    "sBBssBBs",
    "sWIssIWs",
    "ssssnsss",
    "sssLLsss",
    "Jsssssss",
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
        return IRIS
    if k == "L":
        return LIPS
    if k == "n":
        return SKIN[2]
    if k == "J" or (j == 7 and i == 7):
        return SKIN[2]
    if i in (0, 7):
        return SKIN[2]
    return SKIN[1]


face(8, 8, 8, 8, head_front)


def head_side(front_on_right):
    # f: 0 = back edge, 7 = face edge
    def fn(i, j):
        f = i if front_on_right else 7 - i
        if j <= 2:
            return hair(i, j)
        if j == 3:
            return hair(i, j) if f <= 4 else SKIN[2]
        if j in (4, 5) and f in (3, 4):
            return EAR if f == 4 else SKIN[3]
        if j <= 6 and f <= 2:
            return hair(i, j)
        return SKIN[2] if f < 6 else SKIN[1]
    return fn


face(0, 8, 8, 8, head_side(True))
face(16, 8, 8, 8, head_side(False))
face(24, 8, 8, 8, lambda i, j: hair(i, j) if j <= 5 or (j == 6 and 1 <= i <= 6)
     else SKIN[2])

# ---- hat overlay: modest volume, messy fringe ----
face(40, 0, 8, 8, lambda i, j: hair(i, j, top=True))
FRINGE = [4, 2, 3, 2, 2, 3, 2, 4]  # mirror-symmetric; brows (row 3) stay clear


def hat_front(i, j):
    d = FRINGE[i]
    if j < d and (j < 3 or i in (0, 7)):
        return hair(i, j, top=(j == 0))
    return T


face(40, 8, 8, 8, hat_front)


def hat_side(front_on_right):
    def fn(i, j):
        f = i if front_on_right else 7 - i
        limit = 4 if f >= 5 else (4 if f >= 3 else 7)
        if j == limit and f in (1, 5, 6) :
            return hair(i, j)  # curls poking out below the line
        if j < limit:
            return hair(i, j, top=(j == 0))
        return T
    return fn


face(32, 8, 8, 8, hat_side(True))
face(48, 8, 8, 8, hat_side(False))
face(56, 8, 8, 8, lambda i, j: hair(i, j, top=(j == 0))
     if j <= 5 or (j == 6 and i % 3 != 0) else T)

# =====================================================================
# BODY  base (16,16) / overlay (16,32)
# top(20,16 8x4) bottom(28,16) right(16,20 4x12) front(20,20 8x12)
# left(28,20 4x12) back(32,20 8x12)
# =====================================================================


def tank(i):
    # ribbed knit: alternating columns
    c = TANK[0] if i % 2 == 0 else TANK[1]
    if rnd.random() < 0.05:
        c = TANK[2]
    return c


def torso(i, j, side="front"):
    if j == 9:  # belt
        if side == "front" and i in (2, 3):
            return STEEL[0] if i == 2 else STEEL[1]
        return BELT[1] if (i + j) % 5 == 0 else BELT[0]
    if j >= 10:  # jeans waist
        if side == "front" and j == 10 and i in (0, 7):
            return STITCH  # front pocket corners
        if side == "front" and i == 4:
            return DEN[2]  # fly
        return denim(i, j)
    if side == "front":
        if j == 0 and 2 <= i <= 5:
            return SKIN[1]
        if j == 1 and 3 <= i <= 4:
            return SKIN[1]
        if j <= 3 and i in (0, 7):
            return SKIN[2]  # deep armholes
    if side == "back":
        if j == 0 and 2 <= i <= 5:
            return SKIN[2]
        if j <= 3 and i in (0, 7):
            return SKIN[2]
    return tank(i)


face(20, 20, 8, 12, lambda i, j: torso(i, j, "front"))
face(32, 20, 8, 12, lambda i, j: torso(i, j, "back"))
face(16, 20, 4, 12, lambda i, j: torso(i, j, "side") if j >= 2 else SKIN[2])
face(28, 20, 4, 12, lambda i, j: torso(i, j, "side") if j >= 2 else SKIN[2])
face(20, 16, 8, 4, lambda i, j: SKIN[1] if 2 <= i <= 5 and 1 <= j <= 2 else TANK[1])
face(28, 16, 8, 4, lambda i, j: DEN[1])

# ---- body overlay: sweater over the shoulders ----
SWEATER_FRONT = [
    "lmm..mml",
    ".dmm.mmd",
    "..dkKKd.",
    "...kKk..",
    "...dml..",
    "...dml..",
    "...dml..",
    "...dml..",
    "...ccc..",
]
HOOD_BACK = [
    "lmmmmmml",
    "mmlmmlmm",
    "mmmddmmm",
    "dmlmmlmd",
    ".mmddmm.",
    ".dmmmmd.",
    "..mmmm..",
    "...dd...",
]
SW = {"l": MAR[3], "m": MAR[2], "d": MAR[1], "k": MAR[1], "K": MAR[3],
      "c": MAR[0]}


def from_map(m):
    def fn(i, j):
        if j >= len(m) or m[j][i] == ".":
            return T
        k = m[j][i]
        c = SW[k]
        if k == "m" and rnd.random() < 0.12:
            c = MAR[3]
        return c
    return fn


face(20, 36, 8, 12, from_map(SWEATER_FRONT))
face(32, 36, 8, 12, from_map(HOOD_BACK))
face(16, 36, 4, 12, lambda i, j: MAR[2] if j == 0 else T)
face(28, 36, 4, 12, lambda i, j: MAR[2] if j == 0 else T)
face(20, 32, 8, 4, lambda i, j: T if 2 <= i <= 5 and 1 <= j <= 2 else MAR[3])
# jeans overlay at the hips so they look as baggy as the legs
for x0, w in ((20, 8), (32, 8), (16, 4), (28, 4)):
    face(x0, 46, w, 2, lambda i, j: denim(i, j))

# =====================================================================
# ARMS (classic 4px)
# right arm base (40,16) / overlay (40,32); left arm base (32,48) / overlay (48,48)
# top(+4,0) bottom(+8,0) right(0,+4) front(+4,+4) left(+8,+4) back(+12,+4)
# Texture x runs from the character's right to left on front/top faces and
# from left to right on the back face.
# =====================================================================
WRIST = 9  # watch row


def arm_face(inner=False, watch=None):
    def fn(i, j):
        if watch == "strap" and j == WRIST:
            return STRAP[0] if i % 2 == 0 else STRAP[1]
        if watch == "case" and j == WRIST:
            return (STRAP[1], STEEL[0], DIAL, STRAP[1])[i]
        shade = 2 if inner else 1
        if j == 0 or j >= 11:
            shade = 2
        if not inner and i == 1 and 1 <= j <= 7:
            return SKIN[0]  # highlight along the muscle
        return skin(i, j, shade)
    return fn


def build_arm(bx, by, ox, oy, is_right, watch=False):
    # outer side face: right face for the right arm, left face for the left
    outer = (bx, by + 4) if is_right else (bx + 8, by + 4)
    inner = (bx + 8, by + 4) if is_right else (bx, by + 4)
    w = "strap" if watch else None
    face(bx + 4, by, 4, 4, lambda i, j: SKIN[1])
    face(bx + 8, by, 4, 4, lambda i, j: SKIN[2])
    face(*outer, 4, 12, arm_face(watch="case" if watch else None))
    face(*inner, 4, 12, arm_face(inner=True, watch=w))
    face(bx + 4, by + 4, 4, 12, arm_face(watch=w))
    face(bx + 12, by + 4, 4, 12, arm_face(watch=w))

    # sweater covers only the inner half of the shoulder (overlay)
    front_inner = (2, 3) if is_right else (0, 1)
    back_inner = (0, 1) if is_right else (2, 3)
    face(ox + 4, oy, 4, 4, lambda i, j: MAR[3] if i in front_inner else T)
    face(ox + 4, oy + 4, 4, 12, lambda i, j: MAR[2] if j == 0 and i in front_inner else T)
    face(ox + 12, oy + 4, 4, 12, lambda i, j: MAR[2] if j == 0 and i in back_inner else T)



build_arm(40, 16, 40, 32, is_right=True)
build_arm(32, 48, 48, 48, is_right=False, watch=True)

# =====================================================================
# LEGS — wide black jeans with contrast stitching, chunky white sneakers
# right leg base (0,16) / overlay (0,32); left leg base (16,48) / overlay (0,48)
# =====================================================================


def shoe(kind, i, j):
    if j == 11:
        return SHOE[2] if kind != "front" else SHOE[1]
    if kind == "side" and i in (1, 2):
        return SHOE[2]  # silver panel
    if kind == "front" and i == 1:
        return SHOE[1]
    return SHOE[0]


def leg_face(kind, outer_seam=None, pocket=False):
    def fn(i, j):
        if j >= 10:
            return shoe(kind, i, j)
        if pocket and 1 <= j <= 3:  # back pocket with stitched outline
            if (j == 3 and i in (1, 2)) or (i in (0, 3) and j == 1):
                return STITCH
            return denim(i, j)
        if outer_seam is not None and i == outer_seam and j % 3 == 1:
            return STITCH
        c = denim(i, j)
        if kind == "front" and i in (1, 2) and j in (5, 7):
            c = DEN[0]  # fold lines
        if j == 9:
            c = DEN[0]  # hem pooling on the shoe
        return c
    return fn


def leg_overlay(kind, **kw):
    base = leg_face(kind, **kw)

    def fn(i, j):
        if j >= 11:
            return T
        if j == 10:
            return DEN[0] if kind == "back" else T
        if j <= 5:
            return T
        return base(i, j)
    return fn


def build_leg(bx, by, ox, oy, is_right):
    outer = (0, 4) if is_right else (8, 4)
    inner = (8, 4) if is_right else (0, 4)
    face(bx + 4, by, 4, 4, lambda i, j: DEN[1])
    face(bx + 8, by, 4, 4, lambda i, j: SHOE[3])
    for (dx, dy), seam in ((outer, 1), (inner, None)):
        face(bx + dx, by + dy, 4, 12, leg_face("side", outer_seam=seam))
        face(ox + dx, oy + dy, 4, 12, leg_overlay("side", outer_seam=seam))
    face(bx + 4, by + 4, 4, 12, leg_face("front"))
    face(ox + 4, oy + 4, 4, 12, leg_overlay("front"))
    face(bx + 12, by + 4, 4, 12, leg_face("back", pocket=True))
    face(ox + 12, oy + 4, 4, 12, leg_overlay("back", pocket=True))


build_leg(0, 16, 0, 32, is_right=True)
build_leg(16, 48, 0, 48, is_right=False)

img.save("skin.png")
print("saved skin.png")
