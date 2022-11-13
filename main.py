import pygame
import os
import sys
from pygame.locals import *
import random

apple_x = random.randint(0, 590)
apple_y = random.randint(0, 590)
appleIsVisible = False
gold_apple = True
golden_growth = 0
snake = [[50, 80], [50, 70], [50, 60], [50, 50]]
DIRECTION = "down"
main_menu_items = ['start', 'options', 'quit']
difficulties = ['CHILD', 'EASY', 'MEDIUM', 'HARD']
difficulty = 1
sound = '< ON >'
s = 'sounds'


def update_apple():
    global appleIsVisible, apple_x, apple_y, gold_apple, golden_growth
    if appleIsVisible:
        pass
    elif golden_growth <= 0:
        if random.randint(1, 25) == 1: gold_apple = True
        apple_x = random.randint(5, 595)
        apple_y = random.randint(5, 595)
        appleIsVisible = True
    # pygame.draw.rect(DISPLAY, RED, (apple_x, apple_y, 10, 10), 0)
    if gold_apple:
        pygame.draw.circle(DISPLAY, (240, 228, 7), (apple_x, apple_y), 5, 0)
    else:
        pygame.draw.circle(DISPLAY, RED, (apple_x, apple_y), 5, 0)


def update_snake():
    global snake, appleIsVisible, gold_apple, golden_growth
    oldHeadValue = snake[0].copy()
    oldTailValue = snake[-1].copy()

    if difficulty == 0:
        snake_speed = 5
    elif difficulty == 1:
        snake_speed = 10
    elif difficulty == 2:
        snake_speed = 15
    else:
        snake_speed = 20

    if DIRECTION == "up":
        snake[0][1] -= snake_speed
        if snake[0][1] < 0: snake[0][1] = 590
    if DIRECTION == "down":
        snake[0][1] += snake_speed
        if snake[0][1] > 600: snake[0][1] = 0
    if DIRECTION == "left":
        snake[0][0] -= snake_speed
        if snake[0][0] < 0: snake[0][0] = 590
    if DIRECTION == "right":
        snake[0][0] += snake_speed
        if snake[0][0] > 600: snake[0][0] = 0

    for i in range(len(snake) - 1, 0, -1):
        if i == 1:
            snake[i] = oldHeadValue.copy()
        else:
            snake[i] = snake[i - 1].copy()

    if apple_x - 11 < snake[0][0] < apple_x + 11 and apple_y - 11 < snake[0][1] < apple_y + 11:
        if gold_apple:
            golden_growth = 10
            appleIsVisible = False
            gold_apple = False
            if sound == '< ON >':
                pygame.mixer.Sound.play(collected_golden_item)
        else:
            appleIsVisible = False
            snake.append(oldTailValue.copy())
            if sound == '< ON >':
                pygame.mixer.Sound.play(collected_item)

    if golden_growth > 0:
        snake.append(oldTailValue.copy())
        golden_growth -= 1

    for i in range(1, len(snake)):
        if snake[i] == snake[0]:
            print("YOU LOSE")
            exit()

    for i in range(len(snake)):
        pygame.draw.rect(DISPLAY, GREEN, (snake[i][0], snake[i][1], 10, 10), 0)
        if i > 0:
            pygame.draw.rect(DISPLAY, BLACK, (snake[i][0], snake[i][1], 10, 10), 1)


def update():
    global DIRECTION
    pressed_key = pygame.key.get_pressed()
    if pressed_key[K_UP]:
        DIRECTION = "up"
    elif pressed_key[K_DOWN]:
        DIRECTION = "down"
    elif pressed_key[K_RIGHT]:
        DIRECTION = "right"
    elif pressed_key[K_LEFT]:
        DIRECTION = "left"


def set_difficulty():
    print()


def start_game():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        update_apple()
        update_snake()
        update()

        pygame.display.update()
        DISPLAY.fill(BLACK)
        FramePerSec.tick(FPS)


def main_menu():
    selected_item = 0

    while True:
        DISPLAY.fill(BLACK)
        # pygame.draw.rect(DISPLAY, RED, (123, 176, 10, 4), 0)
        pygame.draw.ellipse(DISPLAY, RED, (125, 174, 12, 10), 0)
        draw_text('SNAKE', pygame.font.SysFont('bauhaus93', 120, False, True), GREEN, DISPLAY, 300, 150)
        pygame.draw.circle(DISPLAY, (255, 255, 255), (138, 173), 2, 1)
        pygame.draw.circle(DISPLAY, (255, 255, 255), (136, 184), 2, 1)
        pygame.draw.circle(DISPLAY, BLACK, (138, 173), 1, 1)
        pygame.draw.circle(DISPLAY, BLACK, (136, 184), 1, 1)

        draw_text('START', pygame.font.SysFont('bauhaus93', 50, False), (255, 255, 255), DISPLAY, 300, 300)
        draw_text('OPTIONS', pygame.font.SysFont('bauhaus93', 50, False), (255, 255, 255), DISPLAY, 300, 375)
        draw_text('QUIT', pygame.font.SysFont('bauhaus93', 50, False), (255, 255, 255), DISPLAY, 300, 450)

        if selected_item == 0:
            pygame.draw.rect(DISPLAY, (255, 255, 255), (236, 322, 129, 5), 0)
        elif selected_item == 1:
            pygame.draw.rect(DISPLAY, (255, 255, 255), (206, 398, 190, 5), 0)
        elif selected_item == 2:
            pygame.draw.rect(DISPLAY, (255, 255, 255), (251, 476, 100, 5), 0)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_DOWN:
                    if selected_item == 2:
                        selected_item = 0
                    else:
                        selected_item += 1
                if event.key == K_UP:
                    if selected_item == 0:
                        selected_item = 2
                    else:
                        selected_item -= 1
                if event.key == K_RETURN:
                    if selected_item == 0:
                        start_game()
                    elif selected_item == 1:
                        options_menu()
                    elif selected_item == 2:
                        pygame.quit()
                        sys.exit()
        pygame.display.update()
        FramePerSec.tick(60)


def options_menu():
    global sound, difficulty
    selected_item = 0

    while True:
        DISPLAY.fill(BLACK)
        # pygame.draw.rect(DISPLAY, RED, (123, 176, 10, 4), 0)
        pygame.draw.ellipse(DISPLAY, RED, (125, 174, 12, 10), 0)
        draw_text('SNAKE', pygame.font.SysFont('bauhaus93', 120, False, True), GREEN, DISPLAY, 300, 150)
        pygame.draw.circle(DISPLAY, (255, 255, 255), (138, 173), 2, 1)
        pygame.draw.circle(DISPLAY, (255, 255, 255), (136, 184), 2, 1)
        pygame.draw.circle(DISPLAY, BLACK, (138, 173), 1, 1)
        pygame.draw.circle(DISPLAY, BLACK, (136, 184), 1, 1)

        draw_text('SOUND: ' + sound, pygame.font.SysFont('bauhaus93', 50, False), (255, 255, 255), DISPLAY, 300, 300)
        draw_text('DIFFICULTY: ' + difficulties[difficulty], pygame.font.SysFont('bauhaus93', 50, False),
                  (255, 255, 255), DISPLAY, 300, 375)
        draw_text('BACK', pygame.font.SysFont('bauhaus93', 50, False), (255, 255, 255), DISPLAY, 300, 450)

        if selected_item == 0:
            pygame.draw.rect(DISPLAY, (255, 255, 255), (236, 322, 129, 5), 0)
        elif selected_item == 1:
            pygame.draw.rect(DISPLAY, (255, 255, 255), (206, 398, 190, 5), 0)
        elif selected_item == 2:
            pygame.draw.rect(DISPLAY, (255, 255, 255), (251, 476, 100, 5), 0)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
                if event.key == K_DOWN:
                    if selected_item == 2:
                        selected_item = 0
                    else:
                        selected_item += 1
                if event.key == K_UP:
                    if selected_item == 0:
                        selected_item = 2
                    else:
                        selected_item -= 1
                if (event.key == K_RIGHT or event.key == K_LEFT) and selected_item == 0:
                    if sound == '< OFF >':
                        sound = '< ON >'
                        pygame.mixer.music.unpause()
                    else:
                        sound = '< OFF >'
                        pygame.mixer.music.pause()
                if (event.key == K_RIGHT or event.key == K_LEFT) and selected_item == 1:
                    if difficulty == 0 and event.key == K_LEFT:
                        difficulty = len(difficulties) - 1
                    elif difficulty == len(difficulties) - 1 and event.key == K_RIGHT:
                        difficulty = 0
                    elif event.key == K_LEFT:
                        difficulty -= 1
                    else:
                        difficulty += 1
                if event.key == K_RETURN:
                    if selected_item == 2:
                        main_menu()
        pygame.display.update()
        FramePerSec.tick(60)


def draw_text(text, font, clr, surface, x, y):
    text_object = font.render(text, 1, clr)
    text_rect = text_object.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_object, text_rect)


pygame.init()
pygame.mixer.init()
music = pygame.mixer.music.load(os.path.join(s, 'background_music.mp3'))
collected_item = pygame.mixer.Sound(os.path.join(s, 'item.wav'))
collected_golden_item = pygame.mixer.Sound(os.path.join(s, 'gold_item.wav'))

pygame.mixer.music.play(-1)

FPS = 15
FramePerSec = pygame.time.Clock()

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

DISPLAY = pygame.display.set_mode((600, 600))
DISPLAY.fill(BLACK)
pygame.display.set_caption("Snake")

main_menu()
