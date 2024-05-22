import pyxel
import random

# Initialisation des variables
bonhomme_x = 128
bonhomme_y = 128
direction = "right"  # direction du bonhomme (right ou left)
points_de_vie = 10
points_de_victoire = 0

# Création des positions aléatoires des cailloux et des barils avec types
def generate_positions():
    positions = []
    while len(positions) < 10:
        x, y = random.randint(0, 240), random.randint(0, 240)
        overlap = False
        for pos in positions:
            if (abs(x - pos[0]) < 16) and (abs(y - pos[1]) < 16):
                overlap = True
                break
        if not overlap:
            positions.append((x, y))
    return positions[:8], positions[8:10]

positions_cailloux, positions_barils = generate_positions()
position_caillou = [(x, y, random.randint(1, 3)) for x, y in positions_cailloux]
position_barril = [(x, y, random.randint(1, 2)) for x, y in positions_barils]

arthropode_liste = []
projectile_liste = []
ft_liste = []

# Initialisation de Pyxel
pyxel.init(256, 256)
pyxel.cls(5)
pyxel.load("3.pyxres")


def collision_cercle(cx1, cy1, r1, cx2, cy2, r2):
    return ((cx1 - cx2) ** 2) + ((cy1 - cy2) ** 2) <= (r1 + r2) ** 2


def projectile_creation(x, y, direction, projectile_liste):
    if pyxel.btnp(pyxel.KEY_SPACE) and len(projectile_liste) < 10:
        if direction == "right":
            projectile_liste.append([x + 14, y + 3, "right"])
        else:
            projectile_liste.append([x - 2, y + 3, "left"])
    return projectile_liste


def projectile_deplacement(projectile_liste):
    for projectile in projectile_liste[:]:
        if projectile[2] == "right":
            projectile[0] += 5
        else:
            projectile[0] -= 5
        if projectile[0] > 256 or projectile[0] < 0:
            projectile_liste.remove(projectile)
    return projectile_liste


def ft_creation(x, y, direction, ft_liste):
    if pyxel.btnp(pyxel.KEY_F) and len(ft_liste) < 1:
        if direction == "right":
            ft_liste.append([x + 14, y + 3, "right"])
        else:
            ft_liste.append([x - 2, y + 3, "left"])
    return ft_liste


def ft_deplacement(ft_liste):
    for ft in ft_liste[:]:
        if ft[2] == "right":
            ft[0] += 1
        else:
            ft[0] -= 1
        if ft[0] > 256 or ft[0] < 0:
            ft_liste.remove(ft)
    return ft_liste


def bonhomme_deplacement(x, y):
    global direction
    if pyxel.btn(pyxel.KEY_DOWN) and y < 240:
        y += 1.5
    if pyxel.btn(pyxel.KEY_UP) and y > 0:
        y -= 1.5
    if pyxel.btn(pyxel.KEY_LEFT) and x > 0:
        x -= 1.5
        direction = "left"
    if pyxel.btn(pyxel.KEY_RIGHT) and x < 240:
        x += 1.5
        direction = "right"
    return x, y


def arthropode_creation(arthropode_liste):
    if pyxel.frame_count % 50 == 0 and len(arthropode_liste) < 5:
        arthropode_liste.append([random.randint(0, 256), random.randint(0, 256)])
    return arthropode_liste


def arthropode_suppression():
    global bonhomme_x, bonhomme_y, arthropode_liste, points_de_victoire, points_de_vie

    for arthropode in arthropode_liste[:]:
        arthropode_x, arthropode_y = arthropode
        for tir_r in projectile_liste[:]:
            if collision_cercle(arthropode_x, arthropode_y, 7.5, tir_r[0], tir_r[1], 7.5):
                arthropode_liste.remove(arthropode)
                projectile_liste.remove(tir_r)
                points_de_victoire += 1
        if collision_cercle(arthropode_x, arthropode_y, 7.5, bonhomme_x, bonhomme_y, 7.5):
            arthropode_liste.remove(arthropode)
            points_de_vie -= 1


def arthropode_suppressionft():
    global arthropode_liste

    for arthropode in arthropode_liste[:]:
        arthropode_x, arthropode_y = arthropode
        for tirft in ft_liste[:]:
            if collision_cercle(arthropode_x, arthropode_y, 7.5, tirft[0], tirft[1], 7.5):
                arthropode_liste.remove(arthropode)
                ft_liste.remove(tirft)


def arthropode_deplacement(arthropode_liste):
    for arthropode in arthropode_liste[:]:
        arthropode[1] += random.randint(-1, 1)
        arthropode[0] += random.randint(-1, 1)
        if arthropode[1] > 248 or arthropode[1] < 8 or arthropode[0] > 248 or arthropode[0] < 8:
            arthropode_liste.remove(arthropode)
    return arthropode_liste


def update():
    global bonhomme_x, bonhomme_y, arthropode_liste, points_de_vie, projectile_liste, ft_liste

    bonhomme_x, bonhomme_y = bonhomme_deplacement(bonhomme_x, bonhomme_y)
    arthropode_liste = arthropode_creation(arthropode_liste)
    arthropode_liste = arthropode_deplacement(arthropode_liste)
    projectile_liste = projectile_creation(bonhomme_x, bonhomme_y, direction, projectile_liste)
    projectile_liste = projectile_deplacement(projectile_liste)
    ft_liste = ft_creation(bonhomme_x, bonhomme_y, direction, ft_liste)
    ft_liste = ft_deplacement(ft_liste)
    arthropode_suppression()
    arthropode_suppressionft()


def draw():
    global direction, projectile_liste, ft_liste

    pyxel.cls(5)
    if points_de_victoire >= 25:
        pyxel.cls(0)
        pyxel.text(0, 54, 'Vous avez vaincu les Aliens !', 7)
        pyxel.text(0, 64, 'La Democratie a gagne', 7)
        pyxel.text(0, 74, 'Team Campi', 7)
    elif points_de_vie > 0:
        for x, y, t in position_caillou:
            if t == 1:
                pyxel.blt(x, y, 0, 176, 128, 16, 16)
            elif t == 2:
                pyxel.blt(x, y, 0, 192, 128, 16, 16)
            elif t == 3:
                pyxel.blt(x, y, 0, 208, 128, 16, 16)
        for x, y, t in position_barril:
            if t == 1:
                pyxel.blt(x, y, 0, 176, 112, 16, 16)
            elif t == 2:
                pyxel.blt(x, y, 0, 192, 112, 16, 16)
        for arthropode in arthropode_liste:
            pyxel.blt(arthropode[0], arthropode[1], 0, 0, 120, -15, 15)
        if direction == "right":
            pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, 16, 16)
        else:
            pyxel.blt(bonhomme_x, bonhomme_y, 0, 0, 8, -16, 16)
        for projectile in projectile_liste:
            pyxel.blt(projectile[0], projectile[1], 0, 48, 8, 8, 8)
        for tirft in ft_liste:
            pyxel.blt(tirft[0], tirft[1], 0, 128, 32, 16, 16)
    else:
        pyxel.cls(0)
        pyxel.text(0, 54, 'Les Aliens on pris la planète !', 7)
        pyxel.text(0, 64, 'La Democratie a perdu', 7)
    pyxel.text(10, 10, str(points_de_victoire), 6)
    pyxel.text(224, 240, str(points_de_vie), 0)

pyxel.run(update, draw)
