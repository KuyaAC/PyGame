import pygame
import os

WIDTH, HEIGHT = 960, 540

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("StarWars!")

VEL = 4
BULLET_VEL = 7
BULLET_NO = 10
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets','spaceship_yellow.png'))
Y_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets','spaceship_red.png'))
R_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def draw_window(yellow, red, red_bullets, yellow_bullets):
    WIN.blit(SPACE,(0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(Y_SPACESHIP,(yellow.x, yellow.y))
    WIN.blit(R_SPACESHIP,(red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)


    pygame.display.update()

def yellow_moves(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x - VEL > 0: #left
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x : #right
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y - VEL > 0 : #up
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT -15: #down
        yellow.y += VEL

def red_moves(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #left
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH : #right
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y - VEL > 0 : #up
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: #down
        red.y += VEL

def handel_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():
    yellow = pygame.Rect(170, 230, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(740, 230, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < BULLET_NO:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < BULLET_NO:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)


        key_pressed = pygame.key.get_pressed()
        yellow_moves(key_pressed, yellow)
        red_moves(key_pressed, red)
       
        handel_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, red_bullets, yellow_bullets)
    
    pygame.quit()

if __name__ == "__main__":
    main()