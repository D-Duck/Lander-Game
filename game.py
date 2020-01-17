from math import pi, sin, cos, atan2
from keyboard import get_hotkey_name
import pygame as pg
import pyautogui
import random
import time
import sys

'''
MADE WITH PYTHON 3.3.x AND 3.8.3
MADE BY ERIK KOVÁČ 
DEVELOPER CONTACT [eerriikk1212@gmail.com]

PROJECT VERSION [0.7]
'''

# Loading all fonts / font settings
pg.font.init()
button_font = pg.font.SysFont('Arial', 45)
main_font = pg.font.SysFont('Arial', 100)
title_font = pg.font.SysFont('Arial', 50)
text_font = pg.font.SysFont('Arial', 25)
medium_font = pg.font.SysFont('Arial', 40)

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
    print(f"ERROR : Screen resolution is not 1920x1080\nIt's not recommended to play it because it "
          f"was not build with your resolution({width}x{height}) in mind\n")
    answ = str(input("Do you still want to try it out (Y/N) < "))
    if answ.lower() == "y":
        print("\n You were warned (wait 3 sec)")
        time.sleep(3)
    else:
        print(f"Your answer was detected as NO, press any key to exit.")
        input()
        pg.quit()
        sys.exit()
pg.init()
window = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)

# calculates ground height at point(x)
def ground_height(x):
    global height, terrain
    groundheight = height / 2
    for index in range(len(terrain[player.world])):
        try:
            if terrain[player.world][index][0] >= x:
                groundheight = abs(round(
                    (x - terrain[player.world][index - 1][0]) / (width / len(terrain[player.world]) - 1) * (
                            terrain[player.world][index - 1][1] - terrain[player.world][index][1]), 0) -
                                   terrain[player.world][index - 1][1])
                break
        except ZeroDivisionError:
            groundheight = terrain[player.world][index][1]
            break
    return groundheight

# draw function only draws menus, game is rendered in game function
nonstop_mode = False
end = 0
draw_var = (0, 0)
anim_on = True
anim_count = 1000
pause_drop = height
game_stats = [[0, "Fuel spend", "L"], [0, "Won", "Times"], [0, "Lost", "Times"], [0, "Time played", ""], [0, "Target hit", "Times"], [0, "At the edge of the world", ""], [0, "Best score", ""]]
def draw(dv):
    global anim_count, pause_drop, text_stats
    if dv[0] == 0: # DRAW MAIN-SCREEN
        if dv[1] == 0: # DRAW FIRST-MENU
            window.fill((50, 50, 50))
            textsurface = main_font.render("Project Lander Oldschool", False, (255, 255, 255))
            window.blit(textsurface, (200, 100))

            button((1300, 500), 250, 60, "draw_var", (1, 2), "Start", Anim=True)
            button((1320, 570), 250, 60, "draw_var", (0, 3), "My ship", Anim=True)
            button((1340, 640), 250, 60, "draw_var", (0, 1), "How To Play", Anim=True)
            button((1360, 710), 250, 60, "draw_var", (0, 4), "Stats", Anim=True)
            button((1380, 780), 250, 60, "draw_var", (0, 2), "Options", Anim=True)
            button((1400, 850), 250, 60, "end", 1, "Quit", Anim=True)

            an, x, y, angle, r = 2.5, 500, 600, pi+pi/2, 100
            for n in range(random.randint(5, 10)):
                pg.draw.circle(window, (255, 165, 0), (
                int(x + cos(angle + pi) * random.randint(r+10, r+r+10)),
                int(y + sin(angle + pi) * random.randint(r+10, r+r+10))), random.randint(30, 40), 0)
            p0 = (int(cos(angle) * r + x), int(sin(angle) * r + y))
            p1 = (int(cos(angle + an) * r + x), int(sin(angle + an) * r + y))
            p2 = (int(cos(angle - an) * r + x), int(sin(angle - an) * r + y))
            pg.draw.line(window, (255, 255, 255), p0, p1, 5)
            pg.draw.line(window, (255, 255, 255), p1, p2, 5)
            pg.draw.line(window, (255, 255, 255), p2, p0, 5)
        if dv[1] == 1: # DRAW HOW TO PLAY
            anim_count = 1000
            window.fill((50, 50, 50))
            textsurface = title_font.render("How To Play", False, (255, 255, 255))
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
                "But be careful winds can be extreme on those planets, they will blow you off your coarse very "
                "easily", False, (255, 255, 255))
            window.blit(textsurface, (250, 600))
            textsurface = text_font.render(
                "Try to get highest score and when you are done, just do it again and again and again and ..."
                "", False, (255, 255, 255))
            window.blit(textsurface, (250, 650))
            textsurface = text_font.render(
                "You get my point, good luck pilot."
                "", False, (255, 255, 255))
            window.blit(textsurface, (250, 750))
            textsurface = text_font.render(
                'Oh and one last thing, some pilots are claiming that they saw "red" ground and they are '
                "calling it target. You can get reward by titting it.", False, (255, 255, 255))
            window.blit(textsurface, (250, 800))

            button((1620, 980), 250, 60, "draw_var", (0, 0), "Back")
        if dv[1] == 2: # DRAW OPTIONS
            anim_count = 1000
            window.fill((50, 50, 50))
            textsurface = title_font.render("Options", False, (255, 255, 255))
            window.blit(textsurface, (100, 100))

            on = (255, 255, 255)

            x, y = 300, 350
            button((x, y), 250, 60, "anim_on", 0, "menu anims", style="full")
            pg.draw.line(window, (255, 255, 255), (x + 270, y), (x + 270, y + 60), 3)
            pg.draw.line(window, (255, 255, 255), (x + 270, y), (x + 330, y), 3)
            pg.draw.line(window, (255, 255, 255), (x + 330, y), (x + 330, y + 60), 3)
            pg.draw.line(window, (255, 255, 255), (x + 270, y + 60), (x + 330, y + 60), 3)
            textsurface = text_font.render(
                "Turns ON/OFF menu animations", False, (255, 255, 255))
            window.blit(textsurface, (x, y + 65))
            if anim_on == 1:
                pg.draw.rect(window, on, (x + 270, y, 60, 60))

            x, y = 300, 500
            button((x, y), 250, 60, "nonstop_mode", 0, "nonstop mode", style="full")
            pg.draw.line(window, (255, 255, 255), (x + 270, y), (x + 270, y + 60), 3)
            pg.draw.line(window, (255, 255, 255), (x + 270, y), (x + 330, y), 3)
            pg.draw.line(window, (255, 255, 255), (x + 330, y), (x + 330, y + 60), 3)
            pg.draw.line(window, (255, 255, 255), (x + 270, y + 60), (x + 330, y + 60), 3)
            textsurface = text_font.render(
                "No end-screen, win-screen or score", False, (255, 255, 255))
            window.blit(textsurface, (x, y + 65))
            if nonstop_mode:
                pg.draw.rect(window, on, (x + 270, y, 60, 60))

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
        if dv[1] == 3: # DRAW GARAGE
            window.fill((50, 50, 50))
            textsurface = main_font.render("Garage", False, (255, 255, 255))
            window.blit(textsurface, (200, 100))

            x, y = 1500, 300
            angle, size = -pi/2, 100
            pg.draw.rect(window, (0, 0, 0), (x-150, y-150, 300, 300), 0)
            pg.draw.line(window, (255, 255, 255), (x+150, y+150), (x+150, y-150), 5)
            pg.draw.line(window, (255, 255, 255), (x+150, y+150), (x-150, y+150), 5)
            pg.draw.line(window, (255, 255, 255), (x-150, y-150), (x+150, y-150), 5)
            pg.draw.line(window, (255, 255, 255), (x-150, y-150), (x-150, y+150), 5)
            if player_model == 0:
                an = 2.5
                p0 = (int(cos(angle) * size + x), int(sin(angle) * size + y))
                p1 = (int(cos(angle + an) * size + x), int(sin(angle + an) * size + y))
                p2 = (int(cos(angle - an) * size + x), int(sin(angle - an) * size + y))
                pg.draw.polygon(window, (0, 0, 0), [p0, p1, p2], 0)
                pg.draw.line(window, player_color, p0, p1, 5)
                pg.draw.line(window, player_color, p1, p2, 5)
                pg.draw.line(window, player_color, p2, p0, 5)
            if player_model == 1:
                an = 2.5
                p0 = (int(cos(angle) * size + x), int(sin(angle) * size + y))
                p1 = (int(cos(angle + an) * size + x), int(sin(angle + an) * size + y))
                p2 = (int(cos(angle - an) * size + x), int(sin(angle - an) * size + y))
                pg.draw.polygon(window, (0, 0, 0), [p0, p1, (x, y), p2], 0)
                pg.draw.line(window, player_color, p0, p1, 5)
                pg.draw.line(window, player_color, p1, (x, y), 5)
                pg.draw.line(window, player_color, p2, p0, 5)
                pg.draw.line(window, player_color, p2, (x, y), 5)
            if player_model == 2:
                an = 2.5
                p0 = (int(cos(angle) * size + x), int(sin(angle) * size + y))
                p1 = (int(cos(angle + an) * size + x),int(sin(angle + an) * size + y))
                p2 = (int(cos(angle - an) * size + x),int(sin(angle - an) * size + y))
                pg.draw.polygon(window, (0, 0, 0), [p0, p1, (x, y), p2], 0)
                pg.draw.line(window, player_color, p0, p1, 5)
                pg.draw.line(window, player_color, p1, (x, y), 5)
                pg.draw.line(window, player_color, p2, p0, 5)
                pg.draw.line(window, player_color, p2, p1, 5)
                pg.draw.line(window, player_color, p2, (x, y), 5)
            if player_model == 3:
                an = 2.5
                p0 = (int(cos(angle) * size + x), int(sin(angle) * size + y))
                p1 = (int(cos(angle + an) * size + x), int(sin(angle + an) * size + y))
                p2 = (int(cos(angle - an) * size + x), int(sin(angle - an) * size + y))
                pg.draw.polygon(window, (0, 0, 0), [p0, p1, p2], 0)
                pg.draw.line(window, player_color, p0, p1, 5)
                pg.draw.line(window, player_color, p2, p0, 5)
            if player_model == 4:
                an = 2.3
                p0 = (int(cos(angle) * size + x), int(sin(angle) * size + y))
                p1 = (int(cos(angle + an) * size + x), int(sin(angle + an) * size + y))
                p2 = (int(cos(angle - an) * size + x), int(sin(angle - an) * size + y))
                p3 = (int(cos(angle - pi) * size + x), int(sin(angle - pi) * size + y))
                pg.draw.polygon(window, (0, 0, 0), [p0, p1, p2], 0)
                pg.draw.line(window, player_color, p0, p1, 5)
                pg.draw.line(window, player_color, p2, p0, 5)
                pg.draw.line(window, player_color, p3, p1, 5)
                pg.draw.line(window, player_color, p2, p3, 5)

            # SHIP DESIGN TYPE
            textsurface = medium_font.render("SHIP TYPE", False, (255, 255, 255))
            window.blit(textsurface, (200, 550))
            button((200, 600), 75, 75, "player_model", 0, "1", style="full", fill=True, fill_color=(255, 255, 255), text_color=(0, 0, 0), lock=unlocked[0][0])
            button((300, 600), 75, 75, "player_model", 1, "2", style="full", fill=True, fill_color=(255, 255, 255), text_color=(0, 0, 0), lock=unlocked[0][1])
            button((400, 600), 75, 75, "player_model", 2, "3", style="full", fill=True, fill_color=(255, 255, 255), text_color=(0, 0, 0), lock=unlocked[0][2])
            button((500, 600), 75, 75, "player_model", 3, "4", style="full", fill=True, fill_color=(255, 255, 255), text_color=(0, 0, 0), lock=unlocked[0][3])
            button((600, 600), 75, 75, "player_model", 4, "5", style="full", fill=True, fill_color=(255, 255, 255), text_color=(0, 0, 0), lock=unlocked[0][4])

            # SHIP COLOR SETTING
            textsurface = medium_font.render("SHIP COLOR", False, (255, 255, 255))
            window.blit(textsurface, (200, 750))
            button((200, 800), 75, 75, "player_color", (255, 255, 255), "", style="full", fill=True, fill_color=(255, 255, 255), lock=unlocked[1][0])
            button((300, 800), 75, 75, "player_color", (255, 0, 0), "", style="full", fill=True, fill_color=(255, 0, 0), lock=unlocked[1][1])
            button((400, 800), 75, 75, "player_color", (0, 255, 0), "", style="full", fill=True, fill_color=(0, 255, 0), lock=unlocked[1][2])
            button((500, 800), 75, 75, "player_color", (0, 0, 255), "", style="full", fill=True, fill_color=(0, 0, 255), lock=unlocked[1][3])
            button((600, 800), 75, 75, "player_color", (255, 255, 0), "", style="full", fill=True, fill_color=(255, 255, 0), lock=unlocked[1][4])
            button((700, 800), 75, 75, "player_color", (0, 255, 255), "", style="full", fill=True, fill_color=(0, 255, 255), lock=unlocked[1][5])
            button((800, 800), 75, 75, "player_color", (255, 0, 255), "", style="full", fill=True, fill_color=(255, 0, 255), lock=unlocked[1][6])
            button((900, 800), 75, 75, "player_color", (255, 165, 0), "", style="full", fill=True, fill_color=(255, 165, 0), lock=unlocked[1][7])
            button((1000, 800), 75, 75, "player_color", (255,20,147), "", style="full", fill=True, fill_color=(255,20,147), lock=unlocked[1][8])
            button((1100, 800), 75, 75, "player_color", (149,202,228), "", style="full", fill=True, fill_color=(149,202,228), lock=unlocked[1][9])

            button((1620, 980), 250, 60, "draw_var", (0, 0), "Back")
        if dv[1] == 4: # DRAW STATS
            window.fill((50, 50, 50))
            textsurface = main_font.render("Stats" , False, (255, 255, 255))
            window.blit(textsurface, (200, 100))

            y, x = 220, 200
            for stat in game_stats:
                if stat[1] == "Time played":
                    hours = int(stat[0] / 60 / 60)
                    minutes = int(stat[0] / 60 % 60)
                    txt = f"Time played = {hours}:{minutes}:{int(stat[0]%60)}"
                else:
                    txt = f"{stat[1]} = {stat[0]} {stat[2]}"
                textsurface = text_font.render(txt , False, (255, 255, 255))
                window.blit(textsurface, (x, y))
                if x == 200:
                    x = 1000
                else:
                    x = 200
                    y += 50

            pg.draw.rect(window, (0, 0, 0), (200, 950, 1000, 50), 0)
            textsurface = text_font.render(text_stats, False, (255 ,255 ,255))
            window.blit(textsurface, (210, 960))

            # SHIP DESIGN TYPE
            textsurface = text_font.render("UNLOCKS FOR SHIP TYPE", False, (255, 255, 255))
            window.blit(textsurface, (200, 650))
            button((200, 700), 75, 75, "txt", "DEFAULT SHIP DESIGN", "1", style="full", fill=True, fill_color=(255, 255, 255), text_color=(0, 0, 0))
            button((300, 700), 75, 75, "txt", "TO UNLOCK : GET AT LEAST 2500 BEST-SCORE", "2", style="full", fill=True, fill_color=(255, 255, 255), text_color=(0, 0, 0))
            button((400, 700), 75, 75, "txt", "TO UNLOCK : WIN AT LEAST 250 TIMES", "3", style="full", fill=True, fill_color=(255, 255, 255), text_color=(0, 0, 0))
            button((500, 700), 75, 75, "txt", "TO UNLOCK : HIT TARGET AT LEAST ONCE", "4", style="full", fill=True, fill_color=(255, 255, 255), text_color=(0, 0, 0))
            button((600, 700), 75, 75, "txt", "TO UNLOCK : PLAY AT LEAST 30 MIN", "5", style="full", fill=True, fill_color=(255, 255, 255),text_color=(0, 0, 0))

            # SHIP COLOR SETTING
            textsurface = text_font.render("UNLOCKS FOR SHIP COLOR", False, (255, 255, 255))
            window.blit(textsurface, (200, 800))
            button((200, 850), 75, 75, "txt", "DEFAULT SHIP COLOR", "", style="full", fill=True, fill_color=(255, 255, 255))
            button((300, 850), 75, 75, "txt", "DEFAULT SHIP COLOR", "", style="full", fill=True, fill_color=(255, 0, 0))
            button((400, 850), 75, 75, "txt", "DEFAULT SHIP COLOR", "", style="full", fill=True, fill_color=(0, 255, 0))
            button((500, 850), 75, 75, "txt", "DEFAULT SHIP COLOR", "", style="full", fill=True, fill_color=(0, 0, 255))
            button((600, 850), 75, 75, "txt", "TO UNLOCK : PLAY AT LEAST 5 MINUTES", "", style="full", fill=True, fill_color=(255, 255, 0))
            button((700, 850), 75, 75, "txt", "TO UNLOCK : WIN AT LEAST 10 TIMES", "", style="full", fill=True, fill_color=(0, 255, 255))
            button((800, 850), 75, 75, "txt", "TO UNLOCK : SPEND AT LEAST 900 LITERS OF FUEL", "", style="full", fill=True, fill_color=(255, 0, 255))
            button((900, 850), 75, 75, "txt", "TO UNLOCK : SPEND AT LEAST 30000 LITERS OF FUEL", "", style="full", fill=True, fill_color=(255, 165, 0))
            button((1000, 850), 75, 75, "txt", "TO UNLOCK : WIN AT LEAST 100 TIMES", "", style="full", fill=True, fill_color=(255, 20, 147))
            button((1100, 850), 75, 75, "txt", "TO UNLOCK : LOSE AT LEAST 100 TIMES", "", style="full", fill=True, fill_color=(149, 202, 228))

            button((1620, 980), 250, 60, "draw_var", (0, 0), "Back")
    if dv[0] == 1:
        if dv[1] == 1: # DRAW PAUSE MENU:
            draw_game()

            if not anim_on:
                pause_drop = 0
            pg.draw.rect(window, (50, 50, 50), (0, 0, width, height - pause_drop), 0)

            anim_count = 1000
            textsurface = title_font.render("Pause", False, (255, 255, 255))
            window.blit(textsurface, (100, 100 - pause_drop))

            button((1560, 770 - pause_drop), 250, 60, "draw_var", (1, 0), "Return")
            button((1580, 840 - pause_drop), 250, 60, "draw_var", (1, 2), "Restart")
            button((1600, 910 - pause_drop), 250, 60, "draw_var", (0, 0), "Exit")
            button((1620, 980 - pause_drop), 250, 60, "end", 1, "Quit")
unlocked = [[True, False, False, False, False], [True, True, True, True, False, False, False, False, False, False]]
text_stats = ""
mouse_click_time = time.time()
def button(poz, length, height_, on_click0, on_click1, text, Anim=False, style="vector", fill=False, fill_color=(255, 255, 255), text_color=(255, 255, 255), text_color_hover=(0, 0, 0), lock=True):
    global draw_var, end, anim_count, anim_on, mouse_click_time, unlocked
    global score, round_time, nonstop_mode, player_model, player_color, text_stats
    mouse = pg.mouse.get_pos()
    mouse_click = pg.mouse.get_pressed()

    on = text_color_hover
    off = text_color

    if Anim:
        if anim_on == 1:
            poz = (poz[0] + anim_count, poz[1])

    if lock:
        if poz[0] + length > mouse[0] > poz[0] and poz[1] + height_ > mouse[1] > poz[1]:
            if mouse_click[0] == 1:
                if time.time() - mouse_click_time > 0.25:
                    mouse_click_time = time.time()
                    if on_click0 == "draw_var":
                        draw_var = on_click1
                        if on_click1 == (1, 2):
                            round_time = time.time()
                            score = 0
                    if on_click0 == "end":
                        end = on_click1
                    if on_click0 == "txt":
                        text_stats = on_click1
                    if on_click0 == "anim_on":
                        anim_on += 1
                        if anim_on == 2:
                            anim_on = 0
                    if on_click0 == "player_model":
                        player_model = on_click1
                    if on_click0 == "player_color":
                        player_color = on_click1
                    if on_click0 == "nonstop_mode":
                        if not nonstop_mode:
                            nonstop_mode = True
                        else:
                            nonstop_mode = False
                    else:
                        pass

    if style == "vector":
        if poz[0] + length > mouse[0] > poz[0] and poz[1] + height_ > mouse[1] > poz[1]:
            textsurface = button_font.render(text, False, on)
            pg.draw.line(window, (0, 0, 0), (poz[0], poz[1]), (poz[0] + length, poz[1]), 3)
            pg.draw.line(window, (0, 0, 0), (poz[0], poz[1]), (poz[0], poz[1] + height_), 3)
            pg.draw.line(window, (0, 0, 0), (poz[0], poz[1] + height_), (int(poz[0] + length / 2), poz[1] + height_), 3)
            window.blit(textsurface, (poz[0] + 10, poz[1]))
        else:
            textsurface = button_font.render(text, False, off)
            pg.draw.line(window, (255, 255, 255), (poz[0], poz[1]), (poz[0] + length, poz[1]), 3)
            pg.draw.line(window, (255, 255, 255), (poz[0], poz[1]), (poz[0], poz[1] + height_), 3)
            pg.draw.line(window, (255, 255, 255), (poz[0], poz[1] + height_), (int(poz[0] + length / 2), poz[1] + height_), 3)
            window.blit(textsurface, (poz[0] + 10, poz[1]))
    if style == "full":
        if poz[0] + length > mouse[0] > poz[0] and poz[1] + height_ > mouse[1] > poz[1]:
            if fill:
                pg.draw.rect(window, (fill_color), (poz[0], poz[1], length, height_),0)
            pg.draw.line(window, (0, 0, 0), (poz[0], poz[1]), (poz[0] + length, poz[1]), 3)
            pg.draw.line(window, (0, 0, 0), (poz[0], poz[1]), (poz[0], poz[1] + height_), 3)
            pg.draw.line(window, (0, 0, 0), (poz[0] + length, poz[1]), (poz[0] + length, poz[1] + height_), 3)
            pg.draw.line(window, (0, 0, 0), (poz[0], poz[1] + height_), (poz[0] + length, poz[1] + height_), 3)
            textsurface = button_font.render(text, False, on)
            window.blit(textsurface, (poz[0] + 10, poz[1]))
        else:
            if fill:
                pg.draw.rect(window, (fill_color), (poz[0], poz[1], length, height_),0)
            pg.draw.line(window, (255, 255, 255), (poz[0], poz[1]), (poz[0] + length, poz[1]), 3)
            pg.draw.line(window, (255, 255, 255), (poz[0], poz[1]), (poz[0], poz[1] + height_), 3)
            pg.draw.line(window, (255, 255, 255), (poz[0] + length, poz[1]), (poz[0] + length, poz[1] + height_), 3)
            pg.draw.line(window, (255, 255, 255), (poz[0], poz[1] + height_), (poz[0] + length, poz[1] + height_), 3)
            pg.draw.line(window, (255, 255, 255), (poz[0], poz[1]), (poz[0] + length, poz[1]), 3)
            pg.draw.line(window, (255, 255, 255), (poz[0], poz[1]), (poz[0], poz[1] + height_), 3)
            pg.draw.line(window, (255, 255, 255), (poz[0] + length, poz[1]), (poz[0] + length, poz[1] + height_), 3)
            pg.draw.line(window, (255, 255, 255), (poz[0], poz[1] + height_), (poz[0] + length, poz[1] + height_), 3)
            textsurface = button_font.render(text, False, off)
            window.blit(textsurface, (poz[0] + 10, poz[1]))
        if not lock:
            pg.draw.line(window, (0, 0, 0), (poz[0], poz[1]), (poz[0] + length, poz[1] + height_), 5)
            pg.draw.line(window, (0, 0, 0), (poz[0] + length, poz[1]), (poz[0], poz[1] + height_), 5)

def update_unlocks():
    global unlocked

    # SHIP MODELD
    unlocked[0][0] = True
    unlocked[0][1] = game_stats[6][0] >= 2500
    unlocked[0][2] = game_stats[1][0] >= 250
    unlocked[0][3] = game_stats[4][0] > 0
    unlocked[0][4] = game_stats[3][0] >= 1800

    # SHIP COLORS
    unlocked[1][0] = True
    unlocked[1][1] = True
    unlocked[1][2] = True
    unlocked[1][3] = True
    unlocked[1][4] = game_stats[3][0] >= 300
    unlocked[1][5] = game_stats[1][0] >= 10
    unlocked[1][6] = game_stats[0][0] >= 900
    unlocked[1][7] = game_stats[0][0] >= 30000
    unlocked[1][8] = game_stats[1][0] >= 100
    unlocked[1][9] = game_stats[2][0] >= 100

stars = []
terrain = []
wind = []
wind_particles = []
target = (0, 0)
end_platform = (0, 0, 0)
def world_manager():
    global terrain, end_platform, wind, stars, wind_particles, target
    wind_particles, wind, terrain, stars, end_platform, target = [], [], [], [], (0, 0, 0), (0, 0)

    # GENERATING GROUND POINTS
    x, y = 0, 100
    ground_points = 18 # ground_points + 1
    for nn in range(11):
        terrain.append([])
        for n in range(ground_points + 1):
            if n == ground_points + 1:
                x = width
            y += random.randint(0, 100) - 50
            if y < 100:
                y = 100
            if y > 400:
                y = 400
            terrain[nn].append((x, height - y))
            x += width/ground_points
            x = int(round(x, 0))
        x = 0

    # GENERATE TARGET
    if random.randint(0, 1) == 0:
        target = (0, random.randint(2, ground_points - 1))
    else:
        target = (10, random.randint(2, ground_points - 1))

    # GENERATE WIND
    wind_sections = random.randint(2, 4)
    Wind_particles = 250
    y = 0
    for n in range(wind_sections +1):
        wind.append((y, y+int(round(height/wind_sections, 0)), random.randint(0, 10) - 5))
        y += int(round(height/wind_sections, 0))
    for n in range(Wind_particles):
        wind_particles.append(WindParticle())

    # GENERATING STARS
    num_stars = 100
    for n in range(num_stars):
        stars.append((random.randint(0, width), random.randint(0, height-100)))

    # GENERATING LANDING PLATFORM
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
end_platform_lights = 1
def game():
    player.update()
    for w in wind_particles:
        w.update()
    draw_game()

wins = 0
def win():
    global draw_var, anim_count, wins, best_score, score, round_time, nonstop_mode, game_stats, nonstop_mode
    wins += 1
    if not nonstop_mode:
        game_stats[1][0] += 1

    if not nonstop_mode:
        current_score = (10 * int(player.fuel / 10) - int(round((time.time() - round_time) * 5, 0 ))) + 100
        if current_score < 0:
            current_score = 0
        score += current_score
        if best_score < score:
            best_score = score
            game_stats[6][0] = score

    save_data()
    blink = 300
    while not nonstop_mode:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
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
    global draw_var, anim_count, best_score, score, nonstop_mode, game_stats, nonstop_mode

    if not nonstop_mode:
        game_stats[2][0] += 1
    if not nonstop_mode:
        if best_score < score:
            best_score = score
            game_stats[6][0] = best_score

    save_data()
    blink = 300
    while not nonstop_mode:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
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

    if nonstop_mode:
        draw_var = (1, 2)

def draw_player_model_0():
    an = 2.5
    p0 = (int(cos(player.angle) * player.size + player.x), int(sin(player.angle) * player.size + player.y))
    p1 = (int(cos(player.angle + an) * player.size + player.x), int(sin(player.angle + an) * player.size + player.y))
    p2 = (int(cos(player.angle - an) * player.size + player.x), int(sin(player.angle - an) * player.size + player.y))
    pg.draw.polygon(window, player.color_inner, [p0, p1, p2], 0)
    pg.draw.line(window, player.color_outer, p0, p1, 1)
    pg.draw.line(window, player.color_outer, p1, p2, 1)
    pg.draw.line(window, player.color_outer, p2, p0, 1)

def draw_player_model_1():
    an = 2.5
    p0 = (int(cos(player.angle) * player.size + player.x), int(sin(player.angle) * player.size + player.y))
    p1 = (int(cos(player.angle + an) * player.size + player.x), int(sin(player.angle + an) * player.size + player.y))
    p2 = (int(cos(player.angle - an) * player.size + player.x), int(sin(player.angle - an) * player.size + player.y))
    pg.draw.polygon(window, player.color_inner, [p0, p1, player.get_poz(), p2], 0)
    pg.draw.line(window, player.color_outer, p0, p1, 1)
    pg.draw.line(window, player.color_outer, p1, player.get_poz(), 1)
    pg.draw.line(window, player.color_outer, p2, p0, 1)
    pg.draw.line(window, player.color_outer, p2, player.get_poz(), 1)

def draw_player_model_2():
    an = 2.5
    p0 = (int(cos(player.angle) * player.size + player.x), int(sin(player.angle) * player.size + player.y))
    p1 = (int(cos(player.angle + an) * player.size + player.x), int(sin(player.angle + an) * player.size + player.y))
    p2 = (int(cos(player.angle - an) * player.size + player.x), int(sin(player.angle - an) * player.size + player.y))
    pg.draw.polygon(window, player.color_inner, [p0, p1, player.get_poz(), p2], 0)
    pg.draw.line(window, player.color_outer, p0, p1, 1)
    pg.draw.line(window, player.color_outer, p1, player.get_poz(), 1)
    pg.draw.line(window, player.color_outer, p2, p0, 1)
    pg.draw.line(window, player.color_outer, p2, p1, 1)
    pg.draw.line(window, player.color_outer, p2, player.get_poz(), 1)

def draw_player_model_3():
    an = 2.5
    p0 = (int(cos(player.angle) * player.size + player.x), int(sin(player.angle) * player.size + player.y))
    p1 = (int(cos(player.angle + an) * player.size + player.x), int(sin(player.angle + an) * player.size + player.y))
    p2 = (int(cos(player.angle - an) * player.size + player.x), int(sin(player.angle - an) * player.size + player.y))
    pg.draw.polygon(window, player.color_inner, [p0, p1, p2], 0)
    pg.draw.line(window, player.color_outer, p0, p1, 1)
    pg.draw.line(window, player.color_outer, p2, p0, 1)

def draw_player_model_4():
    an = 2.3
    p0 = (int(cos(player.angle) * player.size + player.x), int(sin(player.angle) * player.size + player.y))
    p1 = (int(cos(player.angle + an) * player.size + player.x), int(sin(player.angle + an) * player.size + player.y))
    p2 = (int(cos(player.angle - an) * player.size + player.x), int(sin(player.angle - an) * player.size + player.y))
    p3 = (int(cos(player.angle - pi) * player.size + player.x), int(sin(player.angle - pi) * player.size + player.y))
    pg.draw.polygon(window, player.color_inner, [p0, p1, p2], 0)
    pg.draw.line(window, player.color_outer, p0, p1, 1)
    pg.draw.line(window, player.color_outer, p2, p0, 1)
    pg.draw.line(window, player.color_outer, p3, p1, 1)
    pg.draw.line(window, player.color_outer, p2, p3, 1)

player_color = (255, 255, 255)
player_model = 0
def draw_game():
    global terrain, end_platform, wind_particles, player, end_platform_lights
    window.fill((0, 0, 0))

    # DRAWING GROUND
    for index in range(len(terrain[player.world]) - 1):
        if player.world == target[0]:
            if index + 1 == target[1] or index == target[1] or index - 1 == target[1]:
                pg.draw.line(window, (255, 0, 0), terrain[player.world][index], terrain[player.world][index + 1], 3)
            else:
                pg.draw.line(window, (255, 255, 255), terrain[player.world][index], terrain[player.world][index + 1], 3)
        else:
            pg.draw.line(window, (255, 255, 255), terrain[player.world][index], terrain[player.world][index + 1], 3)

    # DRAWING STARS
    pixelARR = pg.PixelArray(window)
    for star in stars:
        if star[1] < ground_height(star[0]):
            try:
                pg.draw.line(window, (255, 255, 255), (star[0]+2, star[1]), (star[0]-2, star[1]), 1)
                pg.draw.line(window, (255, 255, 255), (star[0], star[1] + 2), (star[0], star[1] - 2), 1)
            except:
                pass

    # DRAWING WIND
    for w in wind_particles:
        if width > w.get_poz()[0] > 0:
            if height > w.get_poz()[1] > 0:
                pixelARR[w.get_poz()[0]][w.get_poz()[1]] = (255, 255 , 255)
    del pixelARR

    # DRAWING END PLATFORM
    if player.world == 5:
        if end_platform[2] == 0:
            end_platform_lights -= 1
            if end_platform_lights <= 90:
                pg.draw.circle(window, (255, 0, 0), (end_platform[0] - 100, end_platform[1] - 10), 6, 0)
                pg.draw.circle(window, (255, 0, 0), (end_platform[0], end_platform[1] - 10), 6, 0)
                if end_platform_lights == 0:
                    end_platform_lights = 120
            pg.draw.polygon(window, (255, 255, 255), (
            (end_platform[0], end_platform[1]), (end_platform[0] - 100, end_platform[1]),
            (end_platform[0] - 100, end_platform[1] + int(ground_height(end_platform[0] - 100)) - end_platform[1])), 0)
            pg.draw.line(window, (255, 255, 255), (end_platform[0] - 100, end_platform[1]),
                         (end_platform[0] - 100, end_platform[1] - 10), 1)
            pg.draw.line(window, (255, 255, 255), (end_platform[0], end_platform[1]),
                         (end_platform[0], end_platform[1] - 10), 1)
            pg.draw.line(window, (255, 255, 255), (end_platform[0], end_platform[1]),
                         (end_platform[0] - 100, end_platform[1]), 1)

        else:
            end_platform_lights -= 1
            if end_platform_lights <= 90:
                pg.draw.circle(window, (255, 0, 0), (end_platform[0] + 100, end_platform[1] - 10), 6, 0)
                pg.draw.circle(window, (255, 0, 0), (end_platform[0], end_platform[1] - 10), 6, 0)
                if end_platform_lights == 0:
                    end_platform_lights = 120
            pg.draw.line(window, (255, 255, 255), (end_platform[0] + 100, end_platform[1]),
                         (end_platform[0] + 100, end_platform[1] - 10), 1)
            pg.draw.line(window, (255, 255, 255), (end_platform[0], end_platform[1]),
                         (end_platform[0], end_platform[1] - 10), 1)
            pg.draw.line(window, (255, 255, 255), (end_platform[0], end_platform[1]),
                         (end_platform[0] + 100, end_platform[1]), 1)
            pg.draw.polygon(window, (255, 255, 255), (
            (end_platform[0], end_platform[1]), (end_platform[0] + 100, end_platform[1]),
            (end_platform[0] + 100, end_platform[1] + int(ground_height(end_platform[0] + 100)) - end_platform[1])), 0)

    # DRAW FUEL BAR
    pg.draw.rect(window, (255, 255 ,255), (10, height-60, 502, 50),1)
    if player.fuel != 0:
        rect_width = int(player.fuel / 180 * 300)
        pg.draw.rect(window, (255, 255, 0), (10, height-59, rect_width, 48), 0)

    # DRAWING PLAYER SHIP
    if player_model == 0:
        draw_player_model_0()
    if player_model == 1:
        draw_player_model_1()
    if player_model == 2:
        draw_player_model_2()
    if player_model == 3:
        draw_player_model_3()
    if player_model == 4:
        draw_player_model_4()
    pg.draw.circle(window, (255, 255, 255), player.aim, 5, 5)
    if player.flame:
        for n in range(random.randint(5, 10)):
            pg.draw.circle(window, (255, 165, 0), (int(player.x + cos(player.angle + pi) * random.randint(22, 42)),
                                                   int(player.y + sin(player.angle + pi) * random.randint(22, 42))),
                           random.randint(2, 5), 0)


class WindParticle:
    def __init__(self):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)

    def update(self):
        for w in wind:
            if w[1] > self.y > w[0]:
                self.x += w[2]

        self.y += 1

        if self.y > height - 1:
            self.y = 2
        if self.x > width - 1:
            self.x = 2
        if self.x < 0 + 1:
            self.x = width - 2

    def get_poz(self):
        return (int(round(self.x, 0)), int(round(self.y, 0)))

class Player:
    def __init__(self, color=(255, 255, 255)):
        self.x = random.randint(0 + 50, width - 50)
        self.y = 20
        self.x_acc = random.uniform(0, 8) - 4
        self.size = 20
        self.y_acc = 10
        self.color_inner = (0,0,0)
        self.color_outer = color
        self.speed = 0.2
        self.angle = 0
        self.fuel = 300
        self.windD = (0.0, 0) #(wind power multiplier, wind index)
        self.world = 5
        self.aim = (width / 2, height / 2)
        self.flame = False

    def get_poz(self):
        return (int(round(self.x)), int(round(self.y)))

    def update(self):
        global game_stats, nonstop_mode
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

            # ACCELERATION if mouse == 1
            self.flame = False
            if mouse_c[0] == 1 and self.fuel > 0:
                self.x_acc += cos(self.angle) * self.speed
                self.y_acc += sin(self.angle) * self.speed
                self.fuel -= 1
                if not nonstop_mode:
                    game_stats[0][0] += 1
                self.flame = True
            else:
                self.y_acc += 0.1
                if self.x_acc > 0:
                    self.x_acc -= 0.01
                else:
                    self.x_acc += 0.01

        # APPLY WIND MOVEMENT TO PLAYER
        for index in range(len(wind) - 1):
            if wind[index][1] > player.y > wind[index][0]:
                if self.windD[1] != index:
                    self.windD = (0.0, index)
                self.x_acc += (wind[index][2]/60) * self.windD[0]
                if self.windD[0] < 1:
                    self.windD = (round(self.windD[0] + 0.05, 2), self.windD[1])
                break

        # over the edge prevention
        if self.x > width - player.size:
            self.x = player.size
            self.world += 1
            if self.world > 10:
                game_over(random.choice(msg_travel_far))
                if not nonstop_mode:
                    game_stats[5][0] += 1
                self.world = 5
        if self.x < player.size:
            self.x = width - player.size
            self.world -= 1
            if self.world < 0:
                game_over(random.choice(msg_travel_far))
                if not nonstop_mode:
                    game_stats[5][0] += 1
                self.world = 5
        if self.y > height:
            sys.exit()

        # GROUND COLLISION CALCULATION
        GH = ground_height(self.x)

        if end_platform[2] == 0:
            if end_platform[0] > player.x > end_platform[0] - 100:
                if end_platform[1] - player.size > player.y > end_platform[1] - 30:
                    GH = end_platform[1]
        else:
            if end_platform[0] < player.x < end_platform[0] + 100:
                if end_platform[1] - player.size > player.y > end_platform[1] - 30:
                    GH = end_platform[1]

        if GH <= self.y+player.size:
            if terrain[player.world][target[1] - 1][0] < player.x < terrain[player.world][target[1] + 1][
                1] and player.world == target[0]:
                if not nonstop_mode:
                    game_stats[4][0] += 1
                game_over("but you at least hit te TARGET")
            else:
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
                                if player.y < end_platform[1] - player.size:
                                    game_over(random.choice(msg_hard_landing))
                        else:
                            if player.y < end_platform[1] - player.size:
                                game_over(random.choice(msg_hard_landing))
            else:
                if end_platform[0] < player.x < end_platform[0] + 100:
                    if end_platform[1] - player.size > player.y > end_platform[1] - 30:
                        if player.x_acc < 4:
                            if player.y_acc < 5:
                                win()
                            else:
                                if player.y < end_platform[1] - player.size:
                                    game_over(random.choice(msg_hard_landing))
                        else:
                            if player.y < end_platform[1] - player.size:
                                game_over(random.choice(msg_hard_landing))

        # point in the direction of the mouse
        self.angle = atan2(self.aim[0] - self.x, self.aim[1] - self.y) * -1 + pi/2
        self.aim = mouse

        # beautifying PLAYER DATA
        if self.angle > pi*2:
            self.angle -= pi*2
        if self.angle < 0:
            self.angle += pi*2

        self.x += self.x_acc / 2
        self.y += self.y_acc / 2

        self.x = round(self.x, 2)
        self.y = round(self.y, 2)

################ developer custom settings !!!!!!!!! DELETE !!!!!!!!!!!!!!!
anim_on = False
nonstop_mode = False
################
# SAVING DATA TO A FILE
def save_data():
    global game_stats, player_color, player_model

    try:
        file = open("save.sav", "w")
    except:
        file = open("save.sav", "x")
    save = f"{game_stats[0][0]};{game_stats[1][0]};{game_stats[2][0]};{game_stats[3][0]};{game_stats[4][0]};{game_stats[5][0]};{game_stats[6][0]};{player_color[0]};{player_color[1]};{player_color[2]};{player_model};"
    num = 0
    for n in save:
        for nn in n:
            try:
                num += int(nn)
            except:
                pass
    save = save + str(num) + ";"
    file.write(save)
    print("\n[CONSOLE][O] Data saved")

    del file
    file = open("save.sav", "r")

def read_data():
    global game_stats, player_color, player_model, best_score
    try:
        file = open("save.sav", "r")
    except:
        print("\n[CONSOLE][E] save file not existing")
        return 0
    file = file.read()
    items, item = [], ""
    for char in file:
        if char == ";":
            try:
                items.append(int(item))
            except:
                pass
            item = ""
        else:
            item = item + char
    num = 0
    for item in items:
        item = str(item)
        for n in item:
            try:
                num += int(n)
            except:
                pass
    num -= int(str(items[-1])[0])
    num -= int(str(items[-1])[1])

    if items[-1] == num:
        game_stats[0][0] = items[0]
        game_stats[1][0] = items[1]
        game_stats[2][0] = items[2]
        game_stats[3][0] = items[3]
        game_stats[4][0] = items[4]
        game_stats[5][0] = items[5]
        game_stats[6][0] = items[6]
        player_color = (items[7], items[8], items[9])
        player_model = items[10]
        best_score = game_stats[6][0]

        print("\n[CONSOLE][O] Data correctly loaded")
    else:
        print("\n[CONSOLE][E] Game data corrupted, deleting data")
        print("[CONSOLE][E] Data deleted")

count = 0
time_b = time.time()
read_data()
while True:
    # event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            save_data()
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if draw_var[0] == 1:
                    if draw_var[1] == 0:
                        draw_var = (draw_var[0], 1)
                    elif draw_var[1] == 1:
                        draw_var = (draw_var[0], 0)
    if end == 1:
        save_data()
        pg.quit()
        sys.exit()

    # activates game loop
    if draw_var[0] == 1:
        if draw_var[1] == 0:
            if time.time() - time_b >= 1/65:
                game()
                count += 1
                if count == 60:
                    count = 0
                    if not nonstop_mode:
                        game_stats[3][0] += 1
                time_b = time.time()
                if pause_drop != height:
                    pause_drop = height
        if draw_var[1] == 1:
            draw(draw_var)
    # drawing menus and updating changes onto display
    if draw_var[0] == 0:
        update_unlocks()
        draw(draw_var)
    if draw_var == (1, 1):
        if pause_drop > 0:
            pause_drop -= int(pause_drop / 80)
            if pause_drop < 80:
                pause_drop -= 2
        if pause_drop < 0:
            pause_drop = 0
    if draw_var == (1, 2):
        player = Player(color=player_color)
        world_manager()
        time.sleep(0.1)
        round_time = time.time()
        draw_var = (1, 0)
    if draw_var == (0, 0):
        text_stats = ""
        if anim_count > 0:
            anim_count -= anim_count / 80
    pg.display.update()