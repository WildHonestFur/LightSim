import math
import pygame
import matplotlib.path
import numpy as np

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((350, 250), pygame.RESIZABLE)
font = pygame.font.Font('freesansbold.ttf', 50)
bulb = pygame.image.load("lightbulb.png").convert()
bulb = pygame.transform.scale(bulb, (80, 80))
trash2 = pygame.image.load("trash1.png").convert()
trash2 = pygame.transform.scale(trash2, (90, 120))
trash1 = pygame.image.load("trash2.png").convert()
trash1 = pygame.transform.scale(trash1, (90, 120))
las = pygame.image.load("laser_new3.png").convert()
las = pygame.transform.scale(las, (100, 60))
trash1 = pygame.transform.scale(trash1, (90, 120))
poly = pygame.image.load("poly.png").convert()
poly = pygame.transform.scale(poly, (150, 85))
mouse = pygame.image.load("m.png").convert()
mouse = pygame.transform.scale(mouse, (25, 30))
a1 = pygame.image.load("arrow1.png").convert()
a2 = pygame.image.load("arrow2.png").convert()
a3 = pygame.image.load("arrow3.png").convert()
a1 = pygame.transform.scale(a1, (700, 400))
a2 = pygame.transform.scale(a2, (700, 400))
a3 = pygame.transform.scale(a3, (700, 400))
run = True
opentrash = False
poly_move = None
onclick = None
mode = 'click'
lasers = []
mirrors = []
polygons = []
poly_temp = []
lights = []
velocity = 1
r_l = [False, False]


def point_in(poly_shape, p):
    poly_new = np.array([[x, y] for x, y in poly_shape])
    path = matplotlib.path.Path(poly_new)
    return path.contains_points([p])[0]


def laser_path(s, laser_vals, width, height):
    x, y, r = laser_vals[:3]
    adder = 0
    steps = 0
    step = 2
    current = (x + 65 / 2 * math.cos(r * math.pi / 180), y - 65 / 2 * math.sin(r * math.pi / 180))
    direction = r
    in_shape = False
    for pol in polygons:
        if point_in(pol[0], current):
            in_shape = True
            break
    while 0 <= current[0] < width and height / 12 <= current[1] < height and steps < 8000:
        if adder:
            step += adder
            adder = 0
        else:
            step = 2
        add = (step * math.cos(direction * math.pi / 180), -step * math.sin(direction * math.pi / 180))
        current = (current[0] + add[0], current[1] + add[1])
        for m_vals in mirrors:
            xm, ym, rm = m_vals[:3]
            endpoints = [(xm - 45 * math.sin(rm * math.pi / 180), ym - 45 * math.cos(rm * math.pi / 180)),
                         (xm + 45 * math.sin(rm * math.pi / 180), ym + 45 * math.cos(rm * math.pi / 180))]
            if math.dist(current, endpoints[0]) + math.dist(current, endpoints[1]) < 0.5 + math.dist(endpoints[0],
                                                                                                     endpoints[1]):
                direction = 180 - direction + 2 * rm
                adder = 1.5
                break
        if not in_shape:
            for polyshape in polygons:
                if point_in(polyshape[0], current):
                    for p in range(len(polyshape[0])):
                        if math.dist(current, polyshape[0][p - 1]) + math.dist(current,
                                                                               polyshape[0][p]) < 0.5 + math.dist(
                            polyshape[0][p], polyshape[0][p - 1]):
                            try:
                                angle = math.atan((- polyshape[0][p][1] + polyshape[0][p - 1][1]) /
                                                  (polyshape[0][p][0] - polyshape[0][p - 1][0]))
                            except ZeroDivisionError:
                                angle = math.pi / 2
                            angle *= 180 / math.pi
                            while direction < 0:
                                direction += 360
                            direction %= 360
                            if angle < 0:
                                angle += 180
                            i = 90 - angle + direction
                            while i > 90:
                                i -= 180
                            r = math.asin(math.sin(i * math.pi / 180) / polyshape[1]) * 180 / math.pi
                            direction = r + angle - 180 * ((direction - angle + 360) % 360 < 180) - 90
                            adder = 1.5
                            in_shape = True
                            break
                    break
        else:
            for polyshape in polygons:
                if not point_in(polyshape[0], current):
                    for p in range(len(polyshape[0])):
                        if math.dist(current, polyshape[0][p - 1]) + math.dist(current,
                                                                               polyshape[0][p]) < 0.5 + math.dist(
                            polyshape[0][p], polyshape[0][p - 1]):
                            try:
                                angle = math.atan((- polyshape[0][p][1] + polyshape[0][p - 1][1]) /
                                                  (polyshape[0][p][0] - polyshape[0][p - 1][0]))
                            except ZeroDivisionError:
                                angle = math.pi / 2
                            angle *= 180 / math.pi
                            while direction < 0:
                                direction += 360
                            direction %= 360
                            if angle < 0:
                                angle += 180
                            i = 90 - angle + direction
                            while i > 90:
                                i -= 180
                            try:
                                r = math.asin(math.sin(i * math.pi / 180) * polyshape[1]) * 180 / math.pi
                                direction = r + angle - 180 * ((direction - angle + 360) % 360 < 180) - 90
                                in_shape = False
                            except ValueError:
                                direction = 2*angle - direction
                            adder = 1.5
                            break
                    break
        pygame.draw.circle(s, (175, 25, 25), current, 2)
        steps += 1


def draw_poly(s, p, color):
    pygame.draw.polygon(s, color, p)
    for pp in range(len(p)):
        pygame.draw.line(s, (0, 0, 0), p[pp - 1], p[pp], width=3)


def draw_rectangle(s, x, y, width, height, color, rotation=0):
    points = []
    radius = math.sqrt((height / 2) ** 2 + (width / 2) ** 2)
    angle = math.atan2(height / 2, width / 2)
    angles = [angle, -angle + math.pi, angle + math.pi, -angle]
    rot_radians = (math.pi / 180) * rotation
    for angle in angles:
        y_offset = -1 * radius * math.sin(angle + rot_radians)
        x_offset = radius * math.cos(angle + rot_radians)
        points.append((x + x_offset, y + y_offset))
    pygame.draw.polygon(s, color, points)


def mirror(s, x, y, r=0, c=False):
    if c:
        draw_rectangle(s, x, y, 5, 90, (71, 175, 209), r)
    else:
        draw_rectangle(s, x, y, 5, 90, (192,) * 3, r)


def laser(s, x, y, r=0, c=False):
    if c:
        draw_rectangle(s, x, y, 65, 15, (71, 175, 209), r)
    else:
        draw_rectangle(s, x, y, 65, 15, (0,) * 3, r)


while run:
    screen.fill((50,) * 3)
    w, h = pygame.display.get_surface().get_size()
    mx, my = pygame.mouse.get_pos()
    for l in range(len(lasers)):
        if lasers[l][3]:
            screen.blit(a1, (0, h-400))
    for m in range(len(mirrors)):
        if mirrors[m][3]:
            screen.blit(a2, (0, h-400))
    for p in range(len(polygons)):
        if polygons[p][2]:
            screen.blit(a3, (0, h-400))
    if opentrash:
        screen.blit(trash2, (w - 110, h - 140))
    else:
        screen.blit(trash1, (w - 110, h - 140))
    if mx > w - 110 and my > h - 140:
        opentrash = True
    else:
        opentrash = False
    if onclick is not None:
        if onclick[0] == 'm' and my < h / 6 + 45:
            opentrash = True
        elif onclick[0] == 'l' and my < h / 6 + 20:
            opentrash = True
    if poly_move is not None:
        if my < h / 6 + 20:
            opentrash = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                r_l[0] = True
            elif event.key == pygame.K_LEFT:
                r_l[1] = True
            elif event.key == pygame.K_UP:
                for l in range(len(lasers)):
                    if lasers[l][3]:
                        lasers[l][4] = True
                        break
            elif event.key == pygame.K_DOWN:
                for l in range(len(lasers)):
                    if lasers[l][3]:
                        lasers[l][4] = False
                        break
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                r_l[0] = False
            elif event.key == pygame.K_LEFT:
                r_l[1] = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if onclick is not None and opentrash:
                if onclick[0] == 'l':
                    lasers.pop(onclick[1])
                elif onclick[0] == 'm':
                    mirrors.pop(onclick[1])
            if poly_move is not None and opentrash:
                polygons.pop(poly_move[0])
            onclick = None
            poly_move = None
        elif event.type == pygame.MOUSEMOTION:
            if onclick is not None:
                onclick = onclick[:2] + (True,)
            if poly_move is not None:
                poly_move = poly_move[:2] + (True,)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if my < h / 6:
                if 8.3 * w / 12 - 65 / 2 < mx < 8.3 * w / 12 + 60:
                    mode = 'laser'
                elif 9.8 * w / 12 - 30 < mx < 9.8 * w / 12 + 30:
                    mode = 'mirror'
                elif 10.2 * w / 12 - 75 < mx < 10.2 * w / 12 + 130:
                    mode = 'poly'
            for l in range(len(lasers)):
                lasers[l][3] = False
            for m in range(len(mirrors)):
                mirrors[m][3] = False
            for p in range(len(polygons)):
                polygons[p][2] = False
            if mode == 'laser':
                if opentrash:
                    mode = 'click'
                elif my > h / 6 + 20:
                    lasers.append([mx, my, 0, False, False])
                    lights.append([])
                    mode = 'click'
            elif mode == 'mirror':
                if opentrash:
                    mode = 'click'
                elif my > h / 6 + 45:
                    mirrors.append([mx, my, 0, False])
                    mode = 'click'
            elif mode == 'poly':
                if opentrash:
                    mode = 'click'
                    poly_temp.clear()
                elif my > h / 6 + 20:
                    if len(poly_temp) > 0:
                        if math.dist((mx, my), poly_temp[0]) < 10:
                            polygons.append([poly_temp[:], 1.33, False])
                            poly_temp.clear()
                            mode = 'click'
                        else:
                            poly_temp.append((mx, my))
                    else:
                        poly_temp.append((mx, my))
            elif mode == 'click':
                for l in range(len(lasers)):
                    endpts = [(lasers[l][0] + 65 / 2 * math.cos(lasers[l][2] * math.pi / 180),
                               lasers[l][1] - 65 / 2 * math.sin(lasers[l][2] * math.pi / 180)),
                              (lasers[l][0] - 65 / 2 * math.cos(lasers[l][2] * math.pi / 180),
                               lasers[l][1] + 65 / 2 * math.sin(lasers[l][2] * math.pi / 180))]
                    if math.dist((mx, my), endpts[0]) + math.dist((mx, my), endpts[1]) < 2 + math.dist(endpts[0],
                                                                                                       endpts[1]):
                        lasers[l][3] = True
                        onclick = ('l', l, False)
                for m in range(len(mirrors)):
                    endpts = [(mirrors[m][0] - 45 * math.sin(mirrors[m][2] * math.pi / 180),
                               mirrors[m][1] - 45 * math.cos(mirrors[m][2] * math.pi / 180)),

                              (mirrors[m][0] + 45 * math.sin(mirrors[m][2] * math.pi / 180),
                               mirrors[m][1] + 45 * math.cos(mirrors[m][2] * math.pi / 180))]
                    if math.dist((mx, my), endpts[0]) + math.dist((mx, my), endpts[1]) < 1.5 + math.dist(endpts[0],
                                                                                                          endpts[1]):
                        mirrors[m][3] = True
                        onclick = ('m', m, False)

                for p in range(len(polygons)-1, -1, -1):
                    if point_in(polygons[p][0], (mx, my)):
                        poly_move = (p, (mx, my), False)
                        polygons[p][2] = True

    for polygon in polygons[::-1]:
        draw_poly(screen, polygon[0], (40, 114, 138))

    for l in lasers:
        if l[4]:
            laser_path(screen, l, w, h)

    if r_l[1]:
        for l in range(len(lasers)):
            if lasers[l][3]:
                lasers[l][2] += 1
                break
        for m in range(len(mirrors)):
            if mirrors[m][3]:
                mirrors[m][2] += 1
                break
        for p in range(len(polygons)):
            if polygons[p][2]:
                polygons[p][1] -= 0.03*(polygons[p][1]>=1.03)
                break

    elif r_l[0]:
        for l in range(len(lasers)):
            if lasers[l][3]:
                lasers[l][2] -= 1
                break
        for m in range(len(mirrors)):
            if mirrors[m][3]:
                mirrors[m][2] -= 1
                break
        for p in range(len(polygons)):
            if polygons[p][2]:
                polygons[p][1] += 0.03
                break

    if mode == 'mirror' and my > h / 6 + 45:
        mirror(screen, mx, my)
    for mirrordata in mirrors:
        xl, yl, rl, click = mirrordata
        mirror(screen, xl, yl, rl, click)

    if mode == 'laser' and my > h / 6 + 20:
        laser(screen, mx, my)
    for laserdata in lasers:
        xl, yl, rl, click, on = laserdata
        laser(screen, xl, yl, rl, click)

    if onclick is not None:
        if onclick[0] == 'l' and onclick[2]:
            lasers[onclick[1]][:2] = [mx, my]
        elif onclick[0] == 'm' and onclick[2]:
            mirrors[onclick[1]][:2] = [mx, my]
    if poly_move is not None and poly_move[2]:
        for i in range(len(polygons[poly_move[0]][0])):
            x, y = polygons[poly_move[0]][0][i]
            ax, ay = (mx - poly_move[1][0], my - poly_move[1][1])
            polygons[poly_move[0]][0][i] = (x + ax, y + ay)
        poly_move = (poly_move[0], (mx, my), True)

    surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for point in range(1, len(poly_temp)):
        pygame.draw.line(surface, (40, 114, 138), poly_temp[point - 1], poly_temp[point], width=6)

    if mode == 'poly' and len(poly_temp) > 0:
        pygame.draw.line(surface, (40, 114, 138, 125), poly_temp[-1], (mx, my), width=6)

    for point in range(len(poly_temp)):
        pygame.draw.circle(surface, (71, 175, 209), poly_temp[point], 7)

    if mode == 'poly':
        pygame.draw.circle(surface, (71, 175, 209, 125), (mx, my), 7)
    screen.blit(surface, (0, 0))

    # Header
    screen.fill((75,) * 3, pygame.Rect(0, 0, w, h / 6))

    text = font.render('Light Simulator', True, (40, 114, 138))
    textRect = text.get_rect()
    textRect.center = (300, h / 12)
    screen.blit(text, textRect)

    screen.blit(bulb, (10, h / 12 - 45))

    screen.blit(las, (8.3 * w / 12 + 10, h / 12 - 30))
    laser(screen, 8.3 * w / 12, h / 12)

    mirror(screen, 9.8 * w / 12, h / 12)

    screen.blit(poly, (10.2 * w / 12, h / 12 - 85 / 2))
    screen.blit(mouse, (10.2 * w / 12 + 116, h / 12 - 85 / 2 + 53))

    pygame.display.flip()
    clock.tick(60)
print("Thank You!")