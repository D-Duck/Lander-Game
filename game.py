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

# Death messages
msg_ground_hit = [
    "Failed to at least hit the land pad",
    "You can't park there",
    "Use your mouse"]
msg_hard_landing = [
    "Can you be more gentle ?",
    "You have to slow down",
    "didn't you hear, cargo is sensitive !!!"]
msg_travel_far = [
    "You went too far from the course",
    "Oh I see, you want to be an explorer",
    "Can you find the secret in te far land ?"]

# Creating window
width, height = pyautogui.size()
if width != 1920 and height != 1080:
        print(f"ERROR : Screen resolution is not 1920x1080\nIt's not recommended to play it because it was not build with your resolution({width}x{height}) in mind\n")
        answ = str(input("Do you still want to try it out (Y/N) < "))
        if answ.lower() == "y":
            print("\n You were warned (wait 3 sec)")
            time.sleep(3)
        else:
            print(f"Your answer was detected as NO, press any key to exit.")
            input()
            pg.quit()
            quit()
pg.init()
window = pg.display.set_mode((1920,1080), pg.FULLSCREEN)

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
            window.blit(textsurface, (200, 100))

            button((1300, 600), 250, 60, "draw_var", (1, 2), "Start", Anim=True)
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
            pg.draw.line(window, (255, 255, 255), p0, p1, 5)
            pg.draw.line(window, (255, 255, 255), p1, p2, 5)
            pg.draw.line(window, (255, 255, 255), p2, p0, 5)
        if dv[1] == 1: # DRAW HOW TO PLAY
            anim_count = 1000
            window.fill((50, 50, 50))
            textsurface = title_font.render("How To Plat", False, (255, 255, 255))
            window.blit(textsurface, (100, 100))

            textsurface = text_font.render(
                '"Welcome pilot, your orbital ship is ready to detach, have a save fall."', False, (255, 255, 255))
            window.blit(textsurface, (250, 300))
            textsurface = text_font.render(
                "", False, (255, 255, 255))
            window.blit(textsurface, (250, 350))
            textsurface = text_font.render(
                "You are a pilot of a orbital drop ship and your mission is to land on one of landing pads, every "
                "landing pad is fully lit with red lights, you", False, (255, 255, 255))
            window.blit(textsurface, (250, 400))
            textsurface = text_font.render(
                "can't miss it. Your cargo is impact sensitive so don't crash into landing pad too hard and don't "
                "even think about landing on the surface.", False, (255, 255, 255))
            window.blit(textsurface, (250, 450))
            textsurface = text_font.render(
                "You can rotate your ship by moving your mouse, ship will automatically point toward it."
                "", False, (255, 255, 255))
            window.blit(textsurface, (250, 500))
            textsurface = text_font.render(
                "If you need additional thrust just press LEFT mouse button, you will accelerate in a no time."
                "", False, (255, 255, 255))
            window.blit(textsurface, (250, 550))
            textsurface = text_font.render(
                ""
                "", False, (255, 255, 255))
            window.blit(textsurface, (250, 600))
            textsurface = text_font.render(
                "Now you know everything important, save fall pilot!"
                "", False, (255, 255, 255))
            window.blit(textsurface, (250, 650))

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

            button((1560, 770 - pause_drop), 250, 60, "draw_var", (1, 0), "Return")
            button((1580, 840 - pause_drop), 250, 60, "draw_var", (1, 2), "Restart")
            button((1600, 910 - pause_drop), 250, 60, "draw_var", (0, 0), "Exit")
            button((1620, 980 - pause_drop), 250, 60, "end", 1, "Quit")

mouse_clic_time = time.time()
def button(poz, length, height, on_click0, on_click1, text, Anim=False, style="vector"):
    global draw_var, end, anim_count, anim_on, mouse_clic_time, score, round_time
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
                    if on_click1 == (1, 2):
                        round_time = time.time()
                        score = 0
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
end_platform = (0, 0, 0)
def world_manager():
    global terrain, end_platform

    x = 0
    y = 100
    times = 25
    for nn in range(11):
        terrain.append([])
        for n in range(times + 1):
            if n == times + 1:
                x = width
            y += random.randint(0, 100) - 50
            if y < 100:
                y = 100
            if y > 400:
                y = 400
            terrain[nn].append((x, height - y))
            x += width/times
            x = int(round(x, 0))
        x = 0

    endP = False
    while not endP:
        n = random.randint(2, len(terrain[5]) - 3)
        try:
            if terrain[5][n - 1][1] > terrain[5][n][1] < terrain[5][n - 2][1]:
                end_platform = (terrain[5][n][0], terrain[5][n][1], 0)
                endP = True
            if terrain[5][n + 1][1] > terrain[5][n][1] < terrain[5][n + 2][1]:
                end_platform = (terrain[5][n][0], terrain[5][n][1], 1)
                endP = True
        except:
            pass

round_time = 0
def game():
    player.update()

    draw_game()

wins = 0
def win():
    global draw_var, anim_count, wins, best_score, score, round_time
    wins += 1

    current_score = (10 * int(player.fuel / 10) - int(round((time.time() - round_time) * 5, 0 ))) + 100
    if current_score < 0:
        current_score = 0
    score += current_score

    blink = 300
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        window.fill((0, 0, 0))
        textsurface = main_font.render("YOU LANDED", False, (255, 255, 255))
        window.blit(textsurface, (int(width / 10), 100))
        if blink > 100:
            textsurface = text_font.render("PRESS SPACE TO CONTINUE", False, (255, 255, 255))
            window.blit(textsurface, (int(1550 ), height-100))
        blink -= 1
        if blink == 0:
            blink = 300

        txt = f"CURRENT SCORE : {current_score}"
        textsurface = title_font.render(txt, False, (255, 255, 255))
        window.blit(textsurface, (int(width / 10), 500))

        txt = f"TOTAL SCORE : {score}"
        textsurface = title_font.render(txt, False, (255, 255, 255))
        window.blit(textsurface, (int(width / 10), 600))

        txt = f"BEST SCORE : {best_score}"
        textsurface = title_font.render(txt, False, (255, 255, 255))
        window.blit(textsurface, (int(width / 10), 700))
        pg.display.update()

        if get_hotkey_name().lower() == "space":
            break

    draw_var = (1, 2)

score = 0
best_score = 0
def game_over(msg):
    global draw_var, anim_count, best_score, score

    if best_score < score:
        best_score = score

    blink = 300
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        window.fill((0 , 0, 0))
        textsurface = main_font.render("YOU LOST", False, (255, 255, 255))
        window.blit(textsurface, (int(width / 10), 100))
        textsurface = button_font.render(msg, False, (255, 255, 255))
        window.blit(textsurface, (int(width / 10) + 430, 150))

        if blink > 100:
            textsurface = text_font.render("PRESS SPACE TO RESTART", False, (255, 255, 255))
            window.blit(textsurface, (1550, height - 100))
            textsurface = text_font.render("PRESS ESC TO CONTINUE", False, (255, 255, 255))
            window.blit(textsurface, (1550, height - 70))
        blink -= 1
        if blink == 0:
            blink = 300

        txt = f"YOUR SCORE : {score}"
        textsurface = title_font.render(txt, False, (255, 255, 255))
        window.blit(textsurface, (int(width / 10), 500))

        txt = f"BEST SCORE : {best_score}"
        textsurface = title_font.render(txt, False, (255, 255, 255))
        window.blit(textsurface, (int(width / 10), 600))
        pg.display.update()

        if get_hotkey_name().lower() == "space":
            score = 0
            draw_var = (1, 2)
            break
        if get_hotkey_name().lower() == "esc":
            score = 0
            anim_count = 1000
            draw_var = (0, 0)
            break

def draw_game():
    global terrain, end_platform
    window.fill((0, 0, 0))

    # DRAWING GROUND
    for index in range(len(terrain[player.world]) - 1):
        pg.draw.line(window, (255, 255, 255), terrain[player.world][index], terrain[player.world][index + 1], 1)

    # DRAWING END PLATFORM
    if player.world == 5:
        if end_platform[2] == 0:
            GH = height / 2
            for index in range(len(terrain[player.world])):
                try:
                    if terrain[player.world][index][0] >= end_platform[0] - 100:
                        GH = abs(round((end_platform[0] - 100 - terrain[player.world][index - 1][0]) / (
                                    width / len(terrain[player.world]) - 1) * (
                                               terrain[player.world][index - 1][1] - terrain[player.world][index][1]),
                                       0) - terrain[player.world][index - 1][1])
                        break
                except ZeroDivisionError:
                    GH = terrain[player.world][index][1]
                    break
            GH = GH - end_platform[1]

            pg.draw.circle(window, (255, 0, 0), (end_platform[0] - 100, end_platform[1] - 10), 3, 0)
            pg.draw.circle(window, (255, 0, 0), (end_platform[0], end_platform[1] - 10), 3, 0)
            pg.draw.line(window, (255, 255, 255), (end_platform[0] - 100, end_platform[1]), (end_platform[0] - 100, end_platform[1] - 10), 1)
            pg.draw.line(window, (255, 255, 255), (end_platform[0], end_platform[1]), (end_platform[0], end_platform[1] - 10), 1)
            pg.draw.line(window, (255, 255, 255), (end_platform[0], end_platform[1]), (end_platform[0] - 100, end_platform[1]), 1)
            pg.draw.polygon(window, (255, 255, 255), ((end_platform[0], end_platform[1]), (end_platform[0] - 100, end_platform[1]), (end_platform[0] - 100, end_platform[1] + GH)), 0)
        else:
            GH = height / 2
            for index in range(len(terrain[player.world])):
                try:
                    if terrain[player.world][index][0] >= end_platform[0] + 100:
                        GH = abs(round((end_platform[0] + 100 - terrain[player.world][index - 1][0]) / (
                                width / len(terrain[player.world]) - 1) * (
                                               terrain[player.world][index - 1][1] - terrain[player.world][index][1]),
                                       0) - terrain[player.world][index - 1][1])
                        break
                except ZeroDivisionError:
                    GH = terrain[player.world][index][1]
                    break
            GH = GH - end_platform[1]

            pg.draw.circle(window, (255, 0, 0), (end_platform[0] + 100, end_platform[1] - 10), 3, 0)
            pg.draw.circle(window, (255, 0, 0), (end_platform[0], end_platform[1] - 10), 3, 0)
            pg.draw.line(window, (255, 255, 255), (end_platform[0] + 100, end_platform[1]), (end_platform[0] + 100, end_platform[1] - 10), 1)
            pg.draw.line(window, (255, 255, 255), (end_platform[0], end_platform[1]), (end_platform[0], end_platform[1] - 10), 1)
            pg.draw.line(window, (255, 255, 255), (end_platform[0], end_platform[1]), (end_platform[0] + 100, end_platform[1]), 1)
            pg.draw.polygon(window, (255, 255, 255), ((end_platform[0], end_platform[1]), (end_platform[0] + 100, end_platform[1]), (end_platform[0] + 100, end_platform[1] + GH)), 0)

    # DRAW FUEL BAR
    pg.draw.rect(window, (255, 255 ,255), (10, height-60, 502, 50),1)
    if player.fuel != 0:
        rect_width = int(player.fuel / 180 * 300)
        pg.draw.rect(window, (255, 255, 0), (10, height-59, rect_width, 48), 0)

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
        self.x = random.randint(0 + 50, width - 50)
        self.y = 20
        self.x_acc = random.uniform(0, 8) - 4
        self.y_acc = 10
        self.color = (255, 255, 255)
        self.speed = 0.2
        self.angle = 0
        self.fuel = 300
        self.world = 5
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

        # over the edge prevention
        if self.x > width - 20:
            self.x = 20
            self.world += 1
            if self.world > 10:
                game_over(random.choice(msg_travel_far))
        if self.x < 20:
            self.x = width - 20
            self.world -= 1
            if self.world < 0:
                game_over(random.choice(msg_travel_far))
        if self.y > height:
            quit()

        # GROUND COLLISION CALCULATION
        GH = height / 2
        for index in range(len(terrain[player.world])):
            try:
                if terrain[player.world][index][0] >= player.x:
                    GH = abs(round((player.x - terrain[player.world][index - 1][0]) / (width / len(terrain[player.world]) - 1) * (
                                terrain[player.world][index - 1][1] - terrain[player.world][index][1]), 0) - terrain[player.world][index - 1][1])
                    break
            except ZeroDivisionError:
                GH = terrain[player.world][index][1]
                break

        if end_platform[2] == 0:
            if end_platform[0] > player.x > end_platform[0] - 100:
                if end_platform[1] - 20 > player.y > end_platform[1] - 30:
                    GH = end_platform[1]
        else:
            if end_platform[0] < player.x < end_platform[0] + 100:
                if end_platform[1] - 20 > player.y > end_platform[1] - 30:
                    GH = end_platform[1]

        if GH <= self.y+20:
            print("GH <<<<<<<<<<<<")
            game_over(random.choice(msg_ground_hit))

        # END PLATFORM COLLISION CALCULATION
        if player.world == 5:
            if end_platform[2] == 0:
                if end_platform[0] > player.x > end_platform[0] - 100:
                    if end_platform[1] - 19 > player.y > end_platform[1] - 30:
                        if player.x_acc < 4:
                            if player.y_acc < 5:
                                win()
                            else:
                                if player.y < end_platform[1] - 20:
                                    game_over(random.choice(msg_hard_landing))
                        else:
                            if player.y < end_platform[1] - 20:
                                game_over(random.choice(msg_hard_landing))
            else:
                if end_platform[0] < player.x < end_platform[0] + 100:
                    if end_platform[1] - 20 > player.y > end_platform[1] - 30:
                        if player.x_acc < 4:
                            if player.y_acc < 5:
                                win()
                            else:
                                if player.y < end_platform[1] - 20:
                                    game_over(random.choice(msg_hard_landing))
                        else:
                            if player.y < end_platform[1] - 20:
                                game_over(random.choice(msg_hard_landing))

        # point in the direction of the mouse
        self.angle = atan2(self.aim[0] - self.x, self.aim[1] - self.y) * -1 + pi/2
        self.aim = mouse

        # ACCELERATION if mouse == 1
        self.flame = False
        if mouse_c[0] == 1 and self.fuel > 0:
            self.x_acc += cos(self.angle) * self.speed
            self.y_acc += sin(self.angle) * self.speed
            self.fuel -= 1
            self.flame = True
        else:
            if self.x_acc == 0:
                self.x_acc = 1
            else:
                self.y_acc += 0.1

        # beautifying PLAYER DATA
        if self.angle > pi*2:
            self.angle -= pi*2
        if self.angle < 0:
            self.angle += pi*2

        self.x += self.x_acc / 2
        self.y += self.y_acc / 2

        self.x = round(self.x, 0)
        self.y = round(self.y, 0)

################ developer custom settings !!!!!!!!! DELETE !!!!!!!!!!!!!!!
anim_on = False
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
        draw(draw_var)
    if draw_var == (1, 1):
        if pause_drop > 0:
            pause_drop -= int(pause_drop / 80)
            if pause_drop < 80:
                pause_drop -= 2
        if pause_drop < 0:
            pause_drop = 0
    if draw_var == (1, 2):
        player = Player()
        terrain = []
        world_manager()
        time.sleep(0.1)
        round_time = time.time()
        draw_var = (1, 0)
    if draw_var == (0, 0):
        if anim_count > 0:
            anim_count -= anim_count / 80
    pg.display.update()