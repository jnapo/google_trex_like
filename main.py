import random
import pgzrun
from pgzero import music
from pgzero.keyboard import keyboard
from pgzhelper import *

WIDTH = 1000
HEIGHT = 600

background_image = "background.png"
BACKG = Actor(background_image)
BACKG2 = Actor(background_image)
BACKG3 = Actor(background_image)

BACKG.scale = 0.6
BACKG.x = 500
BACKG.y = 275

BACKG2.scale = 0.6
BACKG2.x = 1652
BACKG2.y = 275

BACKG3.scale = 0.6
BACKG3.x = 2804
BACKG3.y = 275

runner = Actor('run1.png')
run_images = ['run1.png', 'run2.png', 'run3.png', 'run4.png', 'run5.png', 'run6.png']
runner.images = run_images
runner.fps = 8
runner.scale = 2
runner.x = 100
runner.y = 300

velocity_y = 0
gravity = 1.0
speed = 8

obstacles = []
obstacles_timeout = 0
obstacles_timeout_values = [45, 55, 65, 75, 85, 95]
score = 0
game_over = False

music.play('soundtrack')


def update():
    runner.animate()
    global velocity_y, obstacles_timeout, score, game_over, speed, gravity
    if not game_over:
        obstacles_timeout += 1
        if obstacles_timeout > random.choice(obstacles_timeout_values):
            actor = Actor('rock.png')
            actor.x = 1050
            if random.randint(1, 10) % 5 == 0:
                actor.y = 400
            else:
                actor.y = 520
            actor.scale = 3
            obstacles.append(actor)
            obstacles_timeout = 0

        for actor in obstacles:
            actor.x -= speed
            if actor.x < 0:
                obstacles.remove(actor)
                score += 1
                if score%5 == 0:
                    speed += 0.5
                    for i in range(len(obstacles_timeout_values)):
                        if obstacles_timeout_values[i] > 25:
                            obstacles_timeout_values[i] -= 1
                    gravity += 0.07
        if runner.y == 500:
            if keyboard.space:
                sounds.jump.play()
                velocity_y = -20

        runner.y += velocity_y
        velocity_y += gravity
        if runner.y > 500:
            velocity_y = 0
            runner.y = 500

        if runner.collidelist(obstacles) != -1:
            game_over = True
            music.stop()
            sounds.lose.play()

        if BACKG.x > -1152:
            BACKG.x -= speed - 3
        else:
            BACKG.x = 2304

        if BACKG2.x > -1152:
            BACKG2.x -= speed - 3
        else:
            BACKG2.x = 2304

        if BACKG3.x > -1152:
            BACKG3.x -= speed - 3
        else:
            BACKG3.x = 2304


def draw():
    BACKG.draw()
    BACKG2.draw()
    BACKG3.draw()
    if game_over:
        screen.draw.text("Game over", centerx=500, centery=200, color=(255, 255, 255), fontsize=60)
        screen.draw.text(f'Score: {score*10}', centerx=500, centery=300, color=(255, 255, 255), fontsize=60)
    else:
        runner.draw()
        for actor in obstacles:
            actor.draw()
        screen.draw.text(f'Score: {score*10}', (10, 15), color=(255, 255, 255), fontsize=60)


pgzrun.go()
