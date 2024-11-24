import math
import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((350, 250), pygame.RESIZABLE)
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 22)
run = True
start = False
trying = 0
best = (-1, float('inf'))
v1 = 1
v2 = 2
p1 = (-100, -100)
p2 = (-100, -100)
stage = 0


def dashed_line(s, c, p, q, t, d):
    x = (q[0] - p[0]) / (2 * d - 1)
    y = (q[1] - p[1]) / (2 * d - 1)
    for i in range(0, 2 * d, 2):
        pygame.draw.line(s, c, (p[0] + i * x, p[1] + i * y), (p[0] + i * x + x, p[1] + i * y + y), t)


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and stage > 1:
                start = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if stage == 0:
                p1 = pygame.mouse.get_pos()
                best = (-1, float('inf'))
            elif stage == 1:
                p2 = pygame.mouse.get_pos()
            stage += 1

    screen.fill((100, 100, 100))
    w, h = pygame.display.get_surface().get_size()
    screen.fill((0, 51, 153), pygame.Rect(0, h / 2, w, h / 2))
    pygame.draw.line(screen, (0, 0, 0), (0, h / 2), (w, h / 2), 3)

    text = font.render('A', True, (200, 0, 0))
    textRect = text.get_rect()
    textRect.center = (p1[0] - 25, p1[1] - 25)
    screen.blit(text, textRect)

    text = font.render('B', True, (0, 200, 0))
    textRect = text.get_rect()
    textRect.center = (p2[0] + 25, p2[1] + 25)
    screen.blit(text, textRect)

    if start:
        time = math.sqrt((trying - p1[0]) ** 2 + (h / 2 - p1[1]) ** 2) / v1
        time += math.sqrt((trying - p2[0]) ** 2 + (h / 2 - p2[1]) ** 2) / v2
        if time < best[1]:
            best = trying, time
        pygame.draw.line(screen, (0, 0, 0), p1, (trying, h / 2), 2)
        pygame.draw.line(screen, (0, 0, 0), p2, (trying, h / 2), 2)
        dashed_line(screen, (0, 0, 0), (trying, h / 4), (trying, 3 * h / 4), 2, 10)
        text = font2.render('Normal', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (trying + 45 - 90 * (trying < p1[0]), h / 4 - 10)
        screen.blit(text, textRect)
        pygame.draw.circle(screen, (0, 0, 0), (trying, h / 2), 5)
        if trying < p1[0]:
            pygame.draw.rect(screen, (0, 0, 0), [trying - 15, h / 2 - 15, 15, 15], 1)
        else:
            pygame.draw.rect(screen, (0, 0, 0), [trying, h / 2 - 15, 15, 15], 1)
        trying += 0.5

    elif best[0] >= 0 and stage == 0:
        pygame.draw.line(screen, (0, 0, 0), p1, (best[0], h / 2), 2)
        pygame.draw.line(screen, (0, 0, 0), p2, (best[0], h / 2), 2)
        text = font2.render('Normal', True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (best[0] + 45 - 90 * (best[0] < p1[0]), h / 4 - 10)
        screen.blit(text, textRect)
        dashed_line(screen, (0, 0, 0), (best[0], h / 4), (best[0], 3 * h / 4), 2, 10)
        pygame.draw.circle(screen, (0, 0, 0), (best[0], h / 2), 5)
        if best[0] < p1[0]:
            pygame.draw.rect(screen, (0, 0, 0), [best[0] - 15, h / 2 - 15, 15, 15], 1)
        else:
            pygame.draw.rect(screen, (0, 0, 0), [best[0], h / 2 - 15, 15, 15], 1)

    if trying == w:
        start = False
        trying = 0
        stage = 0
        sin_i = abs((best[0] - p1[0]) / math.sqrt((best[0] - p1[0]) ** 2 + (h / 2 - p1[1]) ** 2))
        sin_r = abs((best[0] - p2[0]) / math.sqrt((best[0] - p2[0]) ** 2 + (h / 2 - p2[1]) ** 2))
        print(round(sin_i / sin_r, 2), v1 / v2)

    pygame.draw.circle(screen, (200, 0, 0), p1, 5)
    pygame.draw.circle(screen, (0, 200, 0), p2, 5)

    pygame.display.flip()
    clock.tick(200)

pygame.quit()
