import pygame, sys, random

pygame.init()
screen_width, screen_height = 550, 500
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
snake_surface = pygame.Surface((30, 60), pygame.SRCALPHA)  
pygame.draw.rect(snake_surface, (0, 0, 255), snake_surface.get_rect())  
snake_rect = snake_surface.get_rect(center=(screen_width // 2, screen_height // 2))
snake_speed = 3 

red_surface = pygame.Surface((30, 30))  
red_surface.fill((255, 0, 0))
red_rect = red_surface.get_rect()

direction = (0, 0) 
game_started = False  
game_over = False 

color_light = (175, 215, 70)
color_dark = (155, 195, 50)
color_border = (0, 100, 0) 

def generate_red_position():
    return (
        random.randint(0, (screen_width - 30) // 30) * 30,
        random.randint(0, (screen_height - 30) // 30) * 30
    )

red_rect.topleft = generate_red_position()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not game_started:
                game_started = True  
            elif game_over:
                if event.key == pygame.K_RETURN:
                    snake_rect.center = (screen_width // 2, screen_height // 2)
                    direction = (0, 0)
                    snake_surface = pygame.Surface((30, 50), pygame.SRCALPHA)
                    pygame.draw.rect(snake_surface, (0, 0, 255), snake_surface.get_rect())
                    red_rect.topleft = generate_red_position()
                    game_over = False

    keys = pygame.key.get_pressed()

    if game_started and not game_over:
        snake_rect.x += direction[0] * snake_speed
        snake_rect.y += direction[1] * snake_speed

        if snake_rect.left <= 0 or snake_rect.right >= screen_width or snake_rect.top <= 0 or snake_rect.bottom >= screen_height:
            game_over = True

    if keys[pygame.K_UP] and direction != (0, 1):
        direction = (0, -1)  
    elif keys[pygame.K_DOWN] and direction != (0, -1):
        direction = (0, 1) 
    elif keys[pygame.K_LEFT] and direction != (1, 0):
        direction = (-1, 0)  
    elif keys[pygame.K_RIGHT] and direction != (-1, 0):
        direction = (1, 0)  

    angle = pygame.math.Vector2(direction).angle_to((0, -1))
    rotated_snake_surface = pygame.transform.rotate(snake_surface, angle)
    rotated_snake_rect = rotated_snake_surface.get_rect(center=snake_rect.center)

    if rotated_snake_rect.colliderect(red_rect):
        snake_surface = pygame.Surface((30, snake_surface.get_height() + 10), pygame.SRCALPHA)
        pygame.draw.rect(snake_surface, (0, 0, 255), snake_surface.get_rect())
        red_rect.topleft = generate_red_position()

    for row in range(0, screen_height, 30):
        for col in range(0, screen_width, 30):
            if (row // 30 + col // 30) % 2 == 0:
                pygame.draw.rect(screen, color_light, (col, row, 30, 30))
            else:
                pygame.draw.rect(screen, color_dark, (col, row, 30, 30))

    pygame.draw.rect(screen, color_border, (0, 0, screen_width, 30))
    pygame.draw.rect(screen, color_border, (0, screen_height - 30, screen_width, 30))  
    pygame.draw.rect(screen, color_border, (0, 0, 30, screen_height)) 
    pygame.draw.rect(screen, color_border, (screen_width - 30, 0, 30, screen_height)) 

    screen.blit(rotated_snake_surface, rotated_snake_rect)
    screen.blit(red_surface, red_rect)

    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

    pygame.display.update()
    clock.tick(60)  