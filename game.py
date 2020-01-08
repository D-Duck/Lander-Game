import pygame as pg
import pyautogui, time, random
from keyboard import get_hotkey_name
from math import pi, sin, cos, atan2, sqrt
from random import randint as rand

# Loading all fonts / font settings
pg.font.init()
button_font = pg.font.SysFont('Arial', 45)
main_font = pg.font.SysFont('Arial', 100)
title_font = pg.font.SysFont('Arial', 50)
text_font = pg.font.SysFont('Arial', 25)

# Creating window
pg.init()
width, height = pyautogui.size()
window = pg.display.set_mode((width,height), pg.FULLSCREEN)

# draw function only draws menus, game is rendered in game function
creative = False
end = 0
draw_var = (0, 0)
anim_on = True
anim_count = 1000
pause_drop = height
def draw(dv):
    global anim_count, pause_drop
    if dv[0] == 0: # DRAW MAIN-SCREEN
        if dv[1] == 0: # DRAW FIRST-MENU
            window.fill((50, 50, 50))
            textsurface = main_font.render("Lander Lander", False, (255, 255, 255))
            window.blit(textsurface, (150, 100))

            button((1300, 600), 250, 60, "draw_var", (1, 0), "Start", Anim=True)
            button((1320, 670), 250, 60, "draw_var", (0, 1), "How To Play", Anim=True)
            button((1340, 740), 250, 60, "draw_var", (0, 2), "Options", Anim=True)
            button((1360, 810), 250, 60, "end", 1, "Quit", Anim=True)

            an, x, y, angle, r = 2.5, 500, 600, pi+pi/2, 100
            for n in range(random.randint(5, 10)):
                pg.draw.circle(window, (255, 165, 0), (
                int(x + cos(angle + pi) * random.randint(r+10, r+r+10)),
                int(y + sin(angle + pi) * random.randint(r+10, r+r+10))), random.randint(30, 40), 0)
            p0 = (cos(angle) * r + x, sin(angle) * r + y)
            p1 = (cos(angle + an) * r + x, sin(angle + an) * r + y)
            p2 = (cos(angle - an) * r + x, sin(angle - an) * r + y)
            pg.draw.line(window, player.color, p0, p1, 5)
            pg.draw.line(window, player.color, p1, p2, 5)
            pg.draw.line(window, player.color, p2, p0, 5)
        if dv[1] == 1: # DRAW HOW TO PLAY
            anim_count = 1000
            window.fill((50, 50, 50))
            textsurface = title_font.render("How To Plat", False, (255, 255, 255))
            window.blit(textsurface, (100, 100))

            textsurface = text_font.render(
                "About this game About this game About this game About this game About this game About this game"
                "About this game About this game About this game", False, (255, 255, 255))
            window.blit(textsurface, (250, 300))
            textsurface = text_font.render(
                "About this game About this game About this game About this game About this game About this game"
                "About this game About this game About this game", False, (255, 255, 255))
            window.blit(textsurface, (250, 350))
            textsurface = text_font.render(
                "About this game About this game About this game About this game About this game About this game"
                "About this game About this game About this game", False, (255, 255, 255))
            window.blit(textsurface, (250, 400))
            textsurface = text_font.render(
                "About this game About this game About this game About this game About this game About this game"
                "About this game About this game About this game", False, (255, 255, 255))
            window.blit(textsurface, (250, 450))

            button((1620, 980), 250, 60, "draw_var", (0, 0), "Back")
        if dv[1] == 2: # DRAW OPTIONS
            anim_count = 1000
            window.fill((50, 50, 50))
            textsurface = title_font.render("Options", False, (255, 255, 255))
            window.blit(textsurface, (100, 100))

            on = (255, 255, 255)

            x, y = 300, 350
            button((x, y), 250, 60, "anim_on", 0, "Menu Anims", style="full")
            pg.draw.line(window, (255, 255, 255), (x + 270, y), (x + 270, y + 60), 3)
            pg.draw.line(window, (255, 255, 255), (x + 270, y), (x + 330, y), 3)
            pg.draw.line(window, (255, 255, 255), (x + 330, y), (x + 330, y + 60), 3)
            pg.draw.line(window, (255, 255, 255), (x + 270, y + 60), (x + 330, y + 60), 3)
            textsurface = text_font.render(
                "Turns ON/OFF main menu animation", False, (255, 255, 255))
            window.blit(textsurface, (x, y + 65))
            if anim_on == 1:
                pg.draw.rect(window, on, (x + 270, y, 60, 60))

            x, y = 300, 500
            button((x, y), 250, 60, "", 0, "EMPTY", style="full")
            pg.draw.line(window, (255, 255, 255), (x + 270, y), (x + 270, y + 60), 3)
            pg.draw.line(window, (255, 255, 255), (x + 270, y), (x + 330, y), 3)
            pg.draw.line(window, (255, 255, 255), (x + 330, y), (x + 330, y + 60), 3)
            pg.draw.line(window, (255, 255, 255), (x + 270, y + 60), (x + 330, y + 60), 3)
            textsurface = text_font.render(
                "Dummie text text text text", False, (255, 255, 255))
            window.blit(textsurface, (x, y + 65))
            #if anim_on == 1:
            #pg.draw.rect(window, on, (x + 270, y, 60, 60))

            x, y = 300, 650
            button((x, y), 250, 60, "", 0, "EMPTY", style="full")
            pg.draw.line(window, (255, 255, 255), (x + 270, y), (x + 270, y + 60), 3)
            pg.draw.line(window, (255, 255, 255), (x + 270, y), (x + 330, y), 3)
            pg.draw.line(window, (255, 255, 255), (x + 330, y), (x + 330, y + 60), 3)
            pg.draw.line(window, (255, 255, 255), (x + 270, y + 60), (x + 330, y + 60), 3)
            textsurface = text_font.render(
                "Dummie text text text text", False, (255, 255, 255))
            window.blit(textsurface, (x, y + 65))
            #if creative == 1:
            #   pg.draw.rect(window, on, (x + 270, y, 60, 60))

            button((1620, 980), 250, 60, "draw_var", (0, 0), "Back")
    if dv[0] == 1:
        if dv[1] == 1: # DRAW PAUSE MENU:
            draw_game()

            if anim_on == False:
                pause_drop = 0
            pg.draw.rect(window, (50, 50, 50), (0, 0, width, height - pause_drop), 0)

            anim_count = 1000
            textsurface = title_font.render("Pause", False, (255, 255, 255))
            window.blit(textsurface, (100, 100 - pause_drop))

            button((1580, 840 - pause_drop), 250, 60, "draw_var", (1, 0), "Return")
            button((1600, 910 - pause_drop), 250, 60, "draw_var", (0, 0), "Exit")
            button((1620, 980 - pause_drop), 250, 60, "end", 1, "Quit")

mouse_clic_time = time.time()
def button(poz, length, height, on_click0, on_click1, text, Anim=False, style="vector"):
    global draw_var, end, anim_count, anim_on, mouse_clic_time
    mouse = pg.mouse.get_pos()
    mouse_click = pg.mouse.get_pressed()

    on = (0, 0, 0)
    off = (255, 255, 255)

    if Anim == True:
        if anim_on == 1:
            poz = (poz[0] + anim_count, poz[1])

    if poz[0] + length > mouse[0] > poz[0] and poz[1] + height > mouse[1] > poz[1]:
        if mouse_click[0] == 1:
            if time.time() - mouse_clic_time > 0.25:
                mouse_clic_time = time.time()
                if on_click0 == "draw_var":
                    draw_var = on_click1
                if on_click0 == "end":
                    end = on_click1
                if on_click0 == "anim_on":
                    anim_on += 1
                    if anim_on == 2:
                        anim_on = 0
                else:
                    pass

    if style == "vector":
        if poz[0] + length > mouse[0] > poz[0] and poz[1] + height > mouse[1] > poz[1]:
            textsurface = button_font.render(text, False, on)
            pg.draw.line(window, on, (poz[0], poz[1]), (poz[0] + length, poz[1]), 3)
            pg.draw.line(window, on, (poz[0], poz[1]), (poz[0], poz[1] + height), 3)
            pg.draw.line(window, on, (poz[0], poz[1] + height), (poz[0] + length / 2, poz[1] + height), 3)
            window.blit(textsurface, (poz[0] + 10, poz[1]))
        else:
            textsurface = button_font.render(text, False, off)
            pg.draw.line(window, off, (poz[0], poz[1]), (poz[0] + length, poz[1]), 3)
            pg.draw.line(window, off, (poz[0], poz[1]), (poz[0], poz[1] + height), 3)
            pg.draw.line(window, off, (poz[0], poz[1] + height), (poz[0] + length / 2, poz[1] + height), 3)
            window.blit(textsurface, (poz[0] + 10, poz[1]))
    if style == "full":
        if poz[0] + length > mouse[0] > poz[0] and poz[1] + height > mouse[1] > poz[1]:
            textsurface = button_font.render(text, False, on)
            pg.draw.line(window, on, (poz[0], poz[1]), (poz[0] + length, poz[1]), 3)
            pg.draw.line(window, on, (poz[0], poz[1]), (poz[0], poz[1] + height), 3)
            pg.draw.line(window, on, (poz[0] + length, poz[1]), (poz[0] + length, poz[1] + height), 3)
            pg.draw.line(window, on, (poz[0], poz[1] + height), (poz[0] + length, poz[1] + height), 3)
            window.blit(textsurface, (poz[0] + 10, poz[1]))
        else:
            textsurface = button_font.render(text, False, off)
            pg.draw.line(window, off, (poz[0], poz[1]), (poz[0] + length, poz[1]), 3)
            pg.draw.line(window, off, (poz[0], poz[1]), (poz[0], poz[1] + height), 3)
            pg.draw.line(window, off, (poz[0] + length, poz[1]), (poz[0] + length, poz[1] + height), 3)
            pg.draw.line(window, off, (poz[0], poz[1] + height), (poz[0] + length, poz[1] + height), 3)
            window.blit(textsurface, (poz[0] + 10, poz[1]))

terrain = []
def terrain_manager():
    global terrain

    x = 0
    y = 100
    times = 25
    for n in range(times + 1):
        y += random.randint(0, 100) - 50
        if y < 100:
            y = 100
        if y > 400:
            y = 400
        terrain.append((x, height - y))
        x += width/times
        x = int(round(x, 0))
    terrain_done = True

def game():
    player.update()

    draw_game()

def game_over():
    global draw_var, anim_count

    window.fill((0, 0, 0))
    textsurface = main_font.render("Game over", False, (255, 255, 255))
    window.blit(textsurface, (0, 0))
    pg.display.update()

    tt = time.time()
    while time.time() - tt < 3:
        if pg.mouse.get_pressed()[0] == 1:
            break
        if get_hotkey_name().lower() == "space":
            break

    anim_count = 1000
    draw_var = (0, 0)

def draw_game():
    global terrain
    window.fill((0, 0, 0))

    for index in range(len(terrain) - 1):
        pg.draw.line(window, (255, 255, 255), terrain[index], terrain[index + 1], 1)

    # DRAWING PLAYER SHIP
    an = 2.5
    p0 = (cos(player.angle) * 20 + player.x, sin(player.angle) * 20 + player.y)
    p1 = (cos(player.angle + an) * 20 + player.x, sin(player.angle + an) * 20 + player.y)
    p2 = (cos(player.angle - an) * 20 + player.x, sin(player.angle - an) * 20 + player.y)
    pg.draw.line(window, player.color, p0, p1, 1)
    pg.draw.line(window, player.color, p1, p2, 1)
    pg.draw.line(window, player.color, p2, p0, 1)
    pg.draw.circle(window, (255, 255, 255), player.aim, 5, 5)
    if player.flame:
        for n in range(random.randint(5, 10)):
            pg.draw.circle(window, (255, 165, 0), (int(player.x + cos(player.angle+pi)*random.randint(22, 42)), int(player.y + sin(player.angle+pi)*random.randint(22, 42))), random.randint(2, 5), 0)

class Player():
    def __init__(self):
        self.x = width / 2
        self.y = height / 2
        self.x_acc = 0
        self.y_acc = 0
        self.color = (255, 255, 255)
        self.speed = 0.2
        self.max_speed = 5
        self.angle = 0
        self.aim = (width / 2, height / 2)
        self.flame = False

    def get_poz(self):
        return (self.x, self.y)

    def update(self):
        mouse = pg.mouse.get_pos()
        mouse_c = pg.mouse.get_pressed()
        keys_ = get_hotkey_name() + '+'
        keys = []
        key_ = ''
        for key in keys_:
            if key == '+':
                keys.append(key_)
                key_ = ''
            else:
                key_ = key_ + key.lower()
        for key in keys:
            pass

        GH = height / 2
        for index in range(len(terrain)):
            try:
                if terrain[index][0] >= player.x:
                    GH = abs(round((player.x - terrain[index - 1][0]) / (width / len(terrain) - 1) * (
                                terrain[index - 1][1] - terrain[index][1]), 0) - terrain[index - 1][1])
                    pg.draw.line(window, (0, 255, 0), terrain[index], terrain[index - 1], 1)
                    break
            except ZeroDivisionError:
                GH = terrain[index][1]
                pg.draw.line(window, (0, 255, 0), terrain[index], terrain[index - 1], 1)
                break

        if GH <= self.y+20:
            game_over()

        # point id the direction of the mouse
        self.angle = atan2(self.aim[0] - self.x, self.aim[1] - self.y) * -1 + pi/2
        self.aim = mouse

        self.flame = False
        if mouse_c[0] == 1:
            self.x_acc += cos(self.angle) * self.speed
            self.y_acc += sin(self.angle) * self.speed
            self.flame = True
        else:
            if self.x_acc == 0:
                self.x_acc = 1
            else:
                self.y_acc += 0.1

        if self.angle > pi*2:
            self.angle -= pi*2
        if self.angle < 0:
            self.angle += pi*2

        self.x += self.x_acc / 2
        self.y += self.y_acc / 2

        if self.x > width - 20:
            self.x = width - 20
            self.x_acc = 0
        if self.x < 0 + 20:
            self.x = 0 + 20
            self.x_acc = 0
        if self.y > height - 20:
            self.y = height - 20
            self.y_acc = 0
        if self.y < 0 + 20:
            self.y = 0 + 20
            self.y_acc = 0

        self.x = round(self.x, 0)
        self.y = round(self.y, 0)

################ Def settings !!!!!!!!! DELETE !!!!!!!!!!!!!!!
anim_on = True
################

time_b = time.time()
while True:
    # event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if draw_var[0] == 1:
                    if draw_var[1] == 0:
                        draw_var = (draw_var[0], 1)
                    elif draw_var[1] == 1:
                        draw_var = (draw_var[0], 0)
    if end == 1:
        pg.quit()
        quit()

    # activates game loop
    if draw_var[0] == 1:
        if draw_var[1] == 0:
            if time.time() - time_b >= 1/65:
                game()
                time_b = time.time()
                if pause_drop != height:
                    pause_drop = height
        if draw_var[1] == 1:
            draw(draw_var)

    # drawing menus and updating changes onto display
    if draw_var[0] == 0:
        player = Player()
        terrain = []
        terrain_manager()
        draw(draw_var)
    if draw_var == (1, 1):
        if pause_drop > 0:
            pause_drop -= int(pause_drop / 80)
            if pause_drop < 80:
                pause_drop -= 2
        if pause_drop < 0:
            pause_drop = 0
    if draw_var == (0, 0):
        if anim_count > 0:
            anim_count -= anim_count / 80
    pg.display.update()