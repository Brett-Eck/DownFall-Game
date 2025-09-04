import pygame
import sys
import random

width = 1200
height = 800

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Downfall")



# Define colors
BACKGROUND = (255, 255, 255)
PLAYER = (10, 60, 120)
PLATFORM = (50, 0, 0)

gameEnd = False

class Platform:
    def __init__(self, x, y, width, height):
        self.rect =  pygame.Rect(x, y, width, height)
        self.rise = -3
        self.level = 1
        

    def draw(self, screen):
        pygame.draw.rect(screen, (PLATFORM), self.rect)


    def rand_width():
        rand_num = random.randint(30, width-30)
        return rand_num
    
    def lift(self):
        self.rect.y += self.rise
        if score % 11 == 10 :
            self.rise *= self.level

    def update(self):
        self.lift()

plat1_width = random.randint(30, (width - 180))
plat2_width = (width - plat1_width)


platforms = [
    Platform(0, height, plat1_width, 10),
    Platform((plat1_width + 150), height, plat2_width, 10),
    ]


#----------------------------------------------------------------------------------------------------------------------------------------------------


class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.3
        self.acceleration = 0.3  
        self.max_speed = 7  
        
    def rand_color():
        rand_r = random.randint(1,255)
        rand_g = random.randint(1,255)
        rand_b = random.randint(1,255)
        rand_rgb = (rand_r, rand_g, rand_b)
        return rand_rgb

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel_x -= self.acceleration
        if keys[pygame.K_RIGHT]:
            self.vel_x += self.acceleration
        # Deceleration
        if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]):
            if self.vel_x > 0:
                self.vel_x -= self.acceleration
            elif self.vel_x < 0:
                self.vel_x += self.acceleration

        # Player speed limit
        if self.vel_x > self.max_speed:
            self.vel_x = self.max_speed
        if self.vel_x < -self.max_speed:
            self.vel_x = -self.max_speed

        # Left and right boundaries
        if self.rect.left < 0:
            self.rect.right = width
            
        if self.rect.right > width:
            self.rect.left = 0
            
        

    def apply_gravity(self):
        # Apply gravity
        self.vel_y += self.gravity

        # Floor boundary
        if self.rect.bottom >= height:
            self.rect.bottom = height
            self.vel_y = 0

        # Platform collision
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 10:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
            if self.rect.colliderect(platform.rect) and (self.vel_y >= 0 and self.vel_y < 1):
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                    self.vel_x = 0
            if self.rect.colliderect(platform.rect):
                if self.vel_x < 0:
                    self.rect.left = platform.rect.right
                    self.vel_x = 0
                    
    def move(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
    
    def play_level_2(PLAYER):
        PLAYER = (0, 60, 0)
    
    def update(self):
        self.handle_keys()
        self.apply_gravity()
        self.move()     

    def draw(self, screen):
        pygame.draw.rect(screen, (PLAYER), self.rect)


player = Player(width // 2, 200, 50, 50)




#----------------------------------------------------------------------------------------------------------------------------------------------------


running = True
clock = pygame.time.Clock()
score = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    def rand_width():
        rand_num = random.randint(20, width-170)
        return rand_num

    

    screen.fill(BACKGROUND)
    player.update()
    player.draw(screen)

    added_platforms_after_66 = False
    added_platforms_after_33 = False

    for platform in platforms:
        platform.update()
        platform.draw(screen)

        if gameEnd == False:
            if platform.rect.y < height * (.66) and len(platforms) == 2 and not added_platforms_after_66:
                new_width = rand_width()
                platforms.append(Platform(0, height, new_width, 10))
                platforms.append(Platform((new_width + 150), height, (width - new_width), 10))
                added_platforms_after_66 = True
            
            if platform.rect.y < height * (.33) and len(platforms) == 4 and not added_platforms_after_33:
                new_width = rand_width()
                platforms.append(Platform(0, height, new_width, 10))
                platforms.append(Platform((new_width + 150), height, (width - new_width), 10))
                added_platforms_after_66 = True
                
            if platform.rect.bottom < 0:
                platforms.remove(platform)
                score += 1
                if len(platforms) < 6:
                    new_width = rand_width()
                    platforms.append(Platform(0, height, new_width, 10))
                    platforms.append(Platform((new_width + 150), height, (width - new_width), 10))
        else:
            for p in platforms:
                platforms.remove(p)

    if player.rect.left < 0:
        PLAYER = Player.rand_color()
        
            
    if player.rect.right > width:
        PLAYER = Player.rand_color()

    if player.rect.top < 0:
        gameEnd = True
    if gameEnd:
        font = pygame.font.SysFont(None, 100)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    pygame.display.update()


    clock.tick(70)

pygame.quit()
