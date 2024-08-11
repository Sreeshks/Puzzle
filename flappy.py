# Importing the libraries
import pygame
import sys
import time
import random

# Initializing the pygame
pygame.init()

# Frames per second
clock = pygame.time.Clock()

# Function to draw the floor
def draw_floor():
    screen.blit(floor_img, (floor_x, screen_height - 100))
    screen.blit(floor_img, (floor_x + screen_width, screen_height - 100))


# Function to create pipes
def create_pipes():
    pipe_y = random.choice(pipe_height)
    top_pipe = pipe_img.get_rect(midbottom=(-67, pipe_y - 300))  # Change initial x-position to -67 (left side)
    bottom_pipe = pipe_img.get_rect(midtop=(-67, pipe_y))        # Change initial x-position to -67 (left side)
    return top_pipe, bottom_pipe


# Function for animation
def pipe_animation():
    global game_over, score_time
    for pipe in pipes:
        if pipe.top < 0:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            screen.blit(pipe_img, pipe)

        pipe.centerx += 1.5  # Change direction to right and reduce speed
        if pipe.left > screen_width:  # Remove pipes when they move off-screen to the right
            pipes.remove(pipe)

        if bird_rect.colliderect(pipe):
            game_over = True


# Function to draw the score
def draw_score(game_state):
    if game_state == "game_on":
        score_text = score_font.render(str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(screen_width // 2, 66))
        screen.blit(score_text, score_rect)
    elif game_state == "game_over":
        score_text = score_font.render(f" Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(screen_width // 2, 66))
        screen.blit(score_text, score_rect)

        high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(screen_width // 2, screen_height - 116))
        screen.blit(high_score_text, high_score_rect)


# Function to update the score
def score_update():
    global score, score_time, high_score
    if pipes:
        for pipe in pipes:
            if screen_width // 2 - 2 < pipe.centerx < screen_width // 2 + 2 and score_time:
                score += 1
                score_time = False
            if pipe.right >= screen_width:  # Update condition for scoring
                score_time = True

    if score > high_score:
        high_score = score


# Get screen resolution and set game window
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Flappy Bird")

# Setting background and base image
back_img = pygame.image.load("img_46.png").convert()
back_img = pygame.transform.scale(back_img, (screen_width, screen_height))
floor_img = pygame.image.load("img_50.png").convert()
floor_img = pygame.transform.scale(floor_img, (screen_width, 100))
floor_x = 0

# Different stages of bird
bird_up = pygame.image.load("img_47.png").convert_alpha()
bird_down = pygame.image.load("img_48.png").convert_alpha()
bird_mid = pygame.image.load("img_49.png").convert_alpha()
birds = [bird_up, bird_mid, bird_down]
bird_index = 0
bird_flap = pygame.USEREVENT
pygame.time.set_timer(bird_flap, 200)
bird_img = birds[bird_index]
bird_rect = bird_img.get_rect(center=(screen_width // 4, screen_height // 2))
bird_movement = 0
gravity = 0.05  # Reduce gravity

# Loading pipe image
pipe_img = pygame.image.load("greenpipe.png").convert_alpha()
pipe_height = [screen_height // 2, screen_height // 2.5, screen_height // 1.5, screen_height // 1.75]

# For the pipes to appear
pipes = []
create_pipe = pygame.USEREVENT + 1
pygame.time.set_timer(create_pipe, 1600)  # Increase the interval for creating pipes

# Displaying game over image
game_over = False
over_img = pygame.image.load("img_45.png").convert_alpha()
over_img = pygame.transform.scale(over_img, (screen_width // 2, screen_height // 2))
over_rect = over_img.get_rect(center=(screen_width // 2, screen_height // 2))

# Setting variables and font for score
score = 0
high_score = 0
score_time = True
score_font = pygame.font.Font("freesansbold.ttf", 27)

# Game loop
running = True
while running:
    clock.tick(120)

    # For checking the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # QUIT event
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:  # Key pressed event
            if event.key == pygame.K_SPACE and not game_over:  # If space key is pressed
                bird_movement = 0
                bird_movement = -3.5  # Reduce the bird's upward speed

            if event.key == pygame.K_SPACE and game_over:
                game_over = False
                pipes = []
                bird_movement = 0
                bird_rect = bird_img.get_rect(center=(screen_width // 4, screen_height // 2))
                score_time = True
                score = 0

        # To load different stages
        if event.type == bird_flap:
            bird_index += 1

            if bird_index > 2:
                bird_index = 0

            bird_img = birds[bird_index]
            bird_rect = bird_img.get_rect(center=bird_rect.center)

        # To add pipes in the list
        if event.type == create_pipe:
            pipes.extend(create_pipes())

    screen.blit(floor_img, (floor_x, screen_height - 100))
    screen.blit(back_img, (0, 0))

    # Game over conditions
    if not game_over:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)

        if bird_rect.top < 5 or bird_rect.bottom >= screen_height - 100:
            game_over = True

        screen.blit(rotated_bird, bird_rect)
        pipe_animation()
        score_update()
        draw_score("game_on")
    elif game_over:
        screen.blit(over_img, over_rect)
        draw_score("game_over")

    # To move the base
    floor_x -= 1
    if floor_x < -screen_width:
        floor_x = 0

    draw_floor()

    # Update the game window
    pygame.display.update()

# Quitting the pygame and sys
pygame.quit()
sys.exit()