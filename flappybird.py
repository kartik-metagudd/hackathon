import pygame
import random

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game variables
bird_x, bird_y = 50, HEIGHT // 2
bird_width, bird_height = 30, 30
bird_vel = 0
gravity = 0.5
jump = -10

pipe_width = 50
pipe_gap = 150
pipe_vel = 3
pipe_frequency = 1500  # time in ms

score = 0
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)

# Bird rectangle
bird = pygame.Rect(bird_x, bird_y, bird_width, bird_height)

# Generate pipe
def create_pipe():
    pipe_height = random.randint(100, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(WIDTH, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap)
    return top_pipe, bottom_pipe

pipes = []
pygame.time.set_timer(pygame.USEREVENT, pipe_frequency)

# Draw function
def draw_window():
    win.fill(WHITE)
    pygame.draw.rect(win, BLACK, bird)
    for pipe in pipes:
        pygame.draw.rect(win, GREEN, pipe)
    score_text = font.render(f"Score: {score}", True, BLACK)
    win.blit(score_text, (10, 10))
    pygame.display.update()

# Main game loop
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_vel = jump
        if event.type == pygame.USEREVENT:
            pipes.append(create_pipe())

    # Bird movement
    bird_vel += gravity
    bird.y += bird_vel

    # Pipe movement
    for pipe in pipes:
        pipe[0].x -= pipe_vel
        pipe[1].x -= pipe_vel

    # Remove pipes that go off-screen
    pipes = [pipe for pipe in pipes if pipe[0].x + pipe_width > 0]

    # Collision detection
    for pipe in pipes:
        if bird.colliderect(pipe[0]) or bird.colliderect(pipe[1]):
            running = False
    if bird.y > HEIGHT or bird.y < 0:
        running = False

    # Score update
    if pipes and pipes[0][0].x + pipe_width < bird_x and not pipes[0][0].x < 0:
        score += 1

    draw_window()

pygame.quit()