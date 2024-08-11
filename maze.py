import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Set up display
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Game")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Set up the clock for a decent frame rate
clock = pygame.time.Clock()

# Define the player and maze size
cell_size = 40
maze_width, maze_height = width // cell_size, height // cell_size

# Define the player's starting position
player_pos = [1, 1]

# Define the maze structure: 1 is a wall, 0 is a path
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Define the goal position
goal_pos = [14, 9]

# Define the font for the timer and points
font = pygame.font.Font(None, 36)

# Set up the timer and score
start_time = time.time()
time_limit = 90  # More time for medium-level difficulty
points = 0  # Points variable
game_won = False  # Track if the player has won

def draw_button(text, position, size):
    """Draw a button with given text and return the button rect."""
    button_rect = pygame.Rect(position[0], position[1], size[0], size[1])
    pygame.draw.rect(window, green, button_rect)
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=button_rect.center)
    window.blit(text_surface, text_rect)
    return button_rect

def maze_game():
    global start_time, game_won, player_pos, points
    
    while True:
        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - int(elapsed_time))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Movement keys
            if event.type == pygame.KEYDOWN and not game_won:
                if event.key == pygame.K_LEFT:
                    if maze[player_pos[1]][player_pos[0] - 1] == 0:
                        player_pos[0] -= 1
                if event.key == pygame.K_RIGHT:
                    if maze[player_pos[1]][player_pos[0] + 1] == 0:
                        player_pos[0] += 1
                if event.key == pygame.K_UP:
                    if maze[player_pos[1] - 1][player_pos[0]] == 0:
                        player_pos[1] -= 1
                if event.key == pygame.K_DOWN:
                    if maze[player_pos[1] + 1][player_pos[0]] == 0:
                        player_pos[1] += 1

            # Handle "Next" button click
            if event.type == pygame.MOUSEBUTTONDOWN and game_won:
                mouse_pos = event.pos
                if next_button_rect.collidepoint(mouse_pos):
                    # Move to Sudoku game (Placeholder)
                    print("Moving to Sudoku game...")
                    return  # Exits maze_game to move to next game

        # Fill the background
        window.fill(black)

        # Draw the maze
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                if maze[y][x] == 1:
                    pygame.draw.rect(window, blue, rect)
                elif maze[y][x] == 0:
                    pygame.draw.rect(window, white, rect)

        # Draw the player
        player_rect = pygame.Rect(player_pos[0] * cell_size, player_pos[1] * cell_size, cell_size, cell_size)
        pygame.draw.rect(window, red, player_rect)

        # Draw the goal
        goal_rect = pygame.Rect(goal_pos[0] * cell_size, goal_pos[1] * cell_size, cell_size, cell_size)
        pygame.draw.rect(window, green, goal_rect)

        # Draw the timer and points
        timer_text = font.render(f"Time Left: {remaining_time}", True, white)
        window.blit(timer_text, (10, 10))
        points_text = font.render(f"Points: {points}", True, white)
        window.blit(points_text, (width - 150, 10))

        # Check for win condition
        if (player_pos == goal_pos or 
           (player_pos[0] == goal_pos[0] and abs(player_pos[1] - goal_pos[1]) == 1) or 
           (player_pos[1] == goal_pos[1] and abs(player_pos[0] - goal_pos[0]) == 1)):
            if not game_won:
                points += 10  # Add 10 points when reaching the goal
                print(f"You win! Your final score is {points}.")
                game_won = True  # Mark game as won
            win_text = font.render(f"You Win! Points: {points}", True, green)
            window.blit(win_text, (width // 2 - 100, height // 2))
            next_button_rect = draw_button("Next", (width // 2 - 50, height // 2 + 50), (100, 50))  # Draw the "Next" button

        # Check for time running out
        if remaining_time <= 0 and not game_won:
            print("Time's up! You lose!")
            pygame.quit()
            sys.exit()

        # Refresh the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(30)

# Run the maze game
maze_game()

# Placeholder for Sudoku game (Implement Sudoku game here)
print("Starting Sudoku game... (Placeholder)")
# Add your Sudoku game implementation here

# End of the main program
pygame.quit()