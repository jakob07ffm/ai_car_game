import pygame
import sys
import math
import random
import os

pygame.init()

win_width = 1000
win_height = 1000
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Car_game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
TRACK_GREEN = (10, 168, 18)
BLUE = (0, 0, 255)

car_x = 500
car_y = 200
car_speed = 0
car_img_bad = pygame.image.load("car_pixel.png")
car_img = pygame.transform.scale(car_img_bad, (32, 52))
car_angle = -40
car_acceleration = 0.05
car_turn_speed = 5
car_max_speed = 7
car_friction = 0.05

track1_img = pygame.image.load("track.png")

clock = pygame.time.Clock()
FPS = 60

menu_img_small = pygame.image.load("menu.jpg")
menu_img = pygame.transform.scale(menu_img_small, (1000, 1000))

pygame.font.init()
font = pygame.font.Font(None, 36)

start_time = pygame.time.get_ticks()

checkpoints = [
    pygame.Rect(390, 90, 10, 150),
    pygame.Rect(25, 359, 150, 10),
    pygame.Rect(790, 790, 155, 10),
    pygame.Rect(410, 230, 180, 10)
]

current_checkpoint = 0

directions = [
    "a", "d"
    ]

def get_color_at_position(x, y):
    return track1_img.get_at((int(x), int(y)))[:3]

def game_over():
    global car_x, car_y, car_angle, start_time, car_speed, current_checkpoint
    car_x = 500
    car_y = 200
    car_angle = -40
    car_speed = 0
    start_time = pygame.time.get_ticks()
    current_checkpoint = 0
    pygame.display.flip()

    if current_checkpoint <= 1:
        with open("x.txt", "w") as file:
            pass 
        with open("y.txt", "w") as file:
            pass
        with open("angle.txt", "w") as file:
            pass



running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    win.blit(track1_img, (0, 0))

    if car_speed < car_max_speed:
        car_speed += car_acceleration

    rand_dir = random.choice(directions)
    
    if rand_dir == "a":
        car_angle -= car_turn_speed
    if rand_dir == "d":
        car_angle += car_turn_speed

    if car_speed > car_max_speed:
        car_speed = car_max_speed

    radians = math.radians(car_angle)
    car_x += car_speed * math.sin(radians)
    car_y -= car_speed * math.cos(radians)

    rotated_car_img = pygame.transform.rotate(car_img, -car_angle)
    new_rect = rotated_car_img.get_rect(center=(car_x, car_y))

    win.blit(rotated_car_img, new_rect.topleft)

    speed_text = font.render(f'Speed: {car_speed:.2f} x: {car_x} y: {car_y}', True, WHITE)
    win.blit(speed_text, (100, 10))

    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  
    timer_text = font.render(f'Time: {elapsed_time}', True, WHITE)
    win.blit(timer_text, (100, 50))

    for i in checkpoints:
        pygame.draw.rect(win, RED, i)

    car_center_color = get_color_at_position(car_x, car_y)
    if car_center_color == TRACK_GREEN:
        car_speed = 0
        game_over()

    if new_rect.colliderect(checkpoints[current_checkpoint]):
        current_checkpoint += 1
        if current_checkpoint >= len(checkpoints):
            current_checkpoint = 0
            print("All checkpoints passed in correct order!")
            game_over()

    with open("x.txt", "a") as file:
        file.write(f"{car_x}\n")
    with open("y.txt", "a") as file:
        file.write(f"{car_y}\n")
    with open("angle.txt", "a") as file:
        file.write(f"{car_angle}\n")

    checkpoint_text = font.render(f'Current Checkpoint: {current_checkpoint + 1}', True, WHITE)
    win.blit(checkpoint_text, (100, 100))

    pygame.display.flip()

pygame.quit()
sys.exit()
