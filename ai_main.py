import pygame
import sys
import math

pygame.init()


win_width = 800
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Self-Driving Car Game")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
TRACK_COLOR = (30, 30, 30)


car_x = win_width // 2
car_y = win_height // 2
car_speed = 0
car_angle = 0
car_acceleration = 0.1
car_turn_speed = 5
car_max_speed = 5
car_friction = 0.02

track_thickness = 20


clock = pygame.time.Clock()
FPS = 60
font = pygame.font.Font(None, 36)

track_boundaries = [
    pygame.Rect(100, 100, 600, 20), 
    pygame.Rect(100, 100, 20, 400),  
    pygame.Rect(680, 100, 20, 400), 
    pygame.Rect(100, 480, 600, 20)   
]

def draw_car(x, y, angle):
    car_surface = pygame.Surface((40, 20))
    car_surface.fill(RED)
    rotated_car = pygame.transform.rotate(car_surface, angle)
    car_rect = rotated_car.get_rect(center=(x, y))
    win.blit(rotated_car, car_rect.topleft)

def draw_track():
    win.fill(TRACK_COLOR)
    for boundary in track_boundaries:
        pygame.draw.rect(win, WHITE, boundary)

def move_car():
    global car_x, car_y, car_angle, car_speed

    radians = math.radians(car_angle)
    car_x += car_speed * math.sin(radians)
    car_y -= car_speed * math.cos(radians)

def apply_friction():
    global car_speed
    if car_speed > 0:
        car_speed -= car_friction
        if car_speed < 0:
            car_speed = 0

def check_collisions():
    car_rect = pygame.Rect(car_x - 20, car_y - 10, 40, 20)
    for boundary in track_boundaries:
        if car_rect.colliderect(boundary):
            return True
    return False

def game_loop():
    global car_x, car_y, car_angle, car_speed

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            if car_speed < car_max_speed:
                car_speed += car_acceleration
        if keys[pygame.K_DOWN]:
            if car_speed > -car_max_speed:
                car_speed -= car_acceleration
        if keys[pygame.K_LEFT]:
            car_angle -= car_turn_speed
        if keys[pygame.K_RIGHT]:
            car_angle += car_turn_speed

        move_car()
        apply_friction()

        if check_collisions():
            print("Collision detected!")
            car_x, car_y = win_width // 2, win_height // 2
            car_angle = 0
            car_speed = 0

        draw_track()
        draw_car(car_x, car_y, car_angle)

        pygame.display.flip()

if __name__ == "__main__":
    game_loop()
