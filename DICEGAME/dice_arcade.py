# NOTE THIS WAS GENERATED USING LLMS

# dice_arcade.py
import pygame as pg
import random, time, sys

W, H = 560, 360
FPS = 120
BG = (20, 25, 24)          # dark night
NEON = (0, 255, 170)       # minty neon
TEXT = (240, 246, 255)
DIE_COLOR = (250, 250, 252)
DIE_EDGE = (220, 224, 235)
SHADOW = (0, 0, 0, 70)

pg.init()
pg.display.set_caption("Dice Arcade — press SPACE to roll")
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()
font = pg.font.SysFont(None, 28)
big  = pg.font.SysFont(None, 44, bold=True)

def draw_glow_text(surf, msg, pos, color=NEON):
    x, y = pos
    for r in (6, 3, 1):
        glow = pg.Surface(big.size(msg), pg.SRCALPHA)
        t = big.render(msg, True, color)
        glow.blit(t, (0, 0))
        pg.draw.rect(glow, (0, 0, 0, 0), glow.get_rect(), 0, r)
        glow.set_alpha(60 if r==6 else 120 if r==3 else 255)
    surf.blit(big.render(msg, True, color), (x, y))

def draw_rounded_rect(surf, rect, color, radius=14, border=0, border_color=None):
    pg.draw.rect(surf, color, rect, border, border_radius=radius)
    if border and border_color:
        pg.draw.rect(surf, border_color, rect, border, border_radius=radius)

def draw_die(surf, center, size, value, jitter=(0, 0)):
    cx, cy = center
    jx, jy = jitter
    x = int(cx - size//2 + jx)
    y = int(cy - size//2 + jy)
    rect = pg.Rect(x, y, size, size)

    # soft drop shadow
    shadow = pg.Surface((size+10, size+10), pg.SRCALPHA)
    pg.draw.rect(shadow, SHADOW, shadow.get_rect(), border_radius=16)
    surf.blit(shadow, (x-5, y+6))

    draw_rounded_rect(surf, rect, DIE_COLOR, radius=16)
    pg.draw.rect(surf, DIE_EDGE, rect, 2, border_radius=16)

    # pip drawing
    pip_r = max(4, size//12)
    def pip(px, py):
        pg.draw.circle(surf, (30, 30, 40), (x+px, y+py), pip_r)

    # pip grid positions (3x3)
    m = size//6
    spots = {
        1: [(3*m, 3*m)],
        2: [(2*m, 2*m), (4*m, 4*m)],
        3: [(2*m, 2*m), (3*m, 3*m), (4*m, 4*m)],
        4: [(2*m, 2*m), (2*m, 4*m), (4*m, 2*m), (4*m, 4*m)],
        5: [(2*m, 2*m), (2*m, 4*m), (3*m, 3*m), (4*m, 2*m), (4*m, 4*m)],
        6: [(2*m, 2*m), (2*m, 3*m), (2*m, 4*m),
            (4*m, 2*m), (4*m, 3*m), (4*m, 4*m)],
    }
    for px, py in spots[value]:
        pip(px, py)

def animate_roll(num_dice, sides=6, duration=0.6):
    t0 = time.time()
    last_vals = [random.randint(1, sides) for _ in range(num_dice)]
    while True:
        t = time.time() - t0
        if t >= duration: break
        # Ease-out jitter amplitude
        k = 1 - (t / duration)
        jitter = [(random.randint(-5, 5)*k, random.randint(-5, 5)*k) for _ in range(num_dice)]
        # keep numbers flickering
        last_vals = [random.randint(1, sides) for _ in range(num_dice)]
        draw_scene(last_vals, jitter=jitter, hint="Rolling…")
        clock.tick(FPS)
    # final stable result
    final = [random.randint(1, sides) for _ in range(num_dice)]
    for _ in range(10):  # quick settle frames
        draw_scene(final, jitter=[(0,0)]*num_dice, hint="Result")
        clock.tick(FPS)
    return tuple(final)

def draw_background():
    # subtle vertical gradient
    for i in range(H):
        c = int(14 + 10*(i/H))
        pg.draw.line(screen, (c, c+2, c+8), (0, i), (W, i))
    # neon frame
    pg.draw.rect(screen, NEON, pg.Rect(10, 10, W-20, H-20), 2, border_radius=18)

def draw_scene(dice_vals, jitter=None, rolls=0, total=None, hint="Press SPACE to roll"):
    screen.fill(BG)
    draw_background()

    title = big.render("Dice Arcade", True, NEON)
    screen.blit(title, (20, 16))
    msg = font.render(hint, True, TEXT)
    screen.blit(msg, (22, 60))

    # layout dice centered
    n = len(dice_vals)
    size = 96 if n <= 3 else max(64, 220//n)
    gap = 22
    total_w = n*size + (n-1)*gap
    start_x = W//2 - total_w//2 + size//2
    y = H//2 + 8

    for i, v in enumerate(dice_vals):
        j = (0,0) if not jitter else jitter[i]
        draw_die(screen, (start_x + i*(size+gap), y), size, v, jitter=j)

    # HUD
    if total is not None:
        hud = font.render(f"Sum: {total}   Rolls: {rolls}", True, TEXT)
        screen.blit(hud, (22, H-40))

    pg.display.flip()

def main():
    num_dice = 2
    sides = 6
    rolls = 0
    current = [random.randint(1, sides) for _ in range(num_dice)]

    draw_scene(current, rolls=rolls, total=sum(current))
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit(); sys.exit(0)
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    pg.quit(); sys.exit(0)
                if e.key == pg.K_SPACE:
                    current = list(animate_roll(num_dice, sides))
                    rolls += 1
                    draw_scene(current, rolls=rolls, total=sum(current))
                if e.key in (pg.K_MINUS, pg.K_KP_MINUS):
                    num_dice = max(1, num_dice-1)
                    current = [random.randint(1, sides) for _ in range(num_dice)]
                    draw_scene(current, rolls=rolls, total=sum(current))
                if e.key in (pg.K_EQUALS, pg.K_PLUS, pg.K_KP_PLUS):
                    num_dice = min(8, num_dice+1)
                    current = [random.randint(1, sides) for _ in range(num_dice)]
                    draw_scene(current, rolls=rolls, total=sum(current))
                if e.key == pg.K_TAB:
                    sides = 6 if sides != 6 else 20  # quick toggle 6↔20
                    current = [random.randint(1, sides) for _ in range(num_dice)]
                    draw_scene(current, rolls=rolls, total=sum(current))
            if e.type == pg.MOUSEBUTTONDOWN:
                current = list(animate_roll(num_dice, sides))
                rolls += 1
                draw_scene(current, rolls=rolls, total=sum(current))

        clock.tick(FPS)

if __name__ == "__main__":
    main()
