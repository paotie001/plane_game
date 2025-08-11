import pygame
from sys import exit
from random import randint,choice
# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('graphics/player.png').convert_alpha()
        self.original_image = pygame.transform.rotozoom(self.original_image, 0, 0.5)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(80, 300))
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0
        self.can_jump = True
        self.angle = 0

    def jump(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.can_jump:
            self.angle += 34
            self.gravity -= 17
            self.can_jump = False
            pygame.time.set_timer(jump_delay, 300)

    def earthing(self):
        self.gravity += 0.5
        self.rect.y += self.gravity

    def reseting(self):
        self.rect.center = (80, 300)
        self.gravity = 0
        self.angle = 0
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.rect.center)
        self.can_jump = True

    def tilting(self):
        if self.angle > -90:
            self.angle -= 1
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.jump()
        self.earthing()
        self.tilting()


class GameObject(pygame.sprite.Sprite):
    def __init__(self, kind: str):
        super().__init__()
        self.kind = kind

        if kind == 'tower':
            self.image = pygame.image.load('graphics/obj1.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
            self.rect = self.image.get_rect(midbottom=(600, randint(650, 800)))
            self.speed = 5
            self.destroy_limit_x = -200

        elif kind == 'air_balloon':
            self.image = pygame.image.load('graphics/obj2.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
            self.rect = self.image.get_rect(midtop=(600, randint(50, 500) - 150))
            self.speed = 5
            self.destroy_limit_x = -200

        elif kind == 'plane2':
            self.image = pygame.image.load('graphics/plane2.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(center=(800, randint(100, 500)))
            self.speed = 10
            self.destroy_limit_x = -400

        elif kind == 'plane3':
            self.image = pygame.image.load('graphics/plane3.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, 0.5)
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(center=(800, randint(100, 500)))
            self.speed = 10
            self.destroy_limit_x = -400

        else:
            self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
            self.rect = self.image.get_rect(center=(-1000, -1000))
            self.speed = 0
            self.destroy_limit_x = -1000

        self.mask = pygame.mask.from_surface(self.image)

    def destroy(self):
        if self.rect.x < self.destroy_limit_x:
            self.kill()

    def update(self):
        self.destroy()
        self.rect.x -= self.speed


class Sky(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        self.image = pygame.image.load('graphics/sky4.png')
        self.image = pygame.transform.rotozoom(self.image, 0, 1)
        if type == 'sky':
            self.rect = self.image.get_rect(topleft=(0, -250))
        if type == 'sky2':
            self.rect = self.image.get_rect(topleft=(940, -250))
    def update(self):
        self.rect.x-=1
        if self.rect.right<=0:
            self.rect.left=940

# Function
def collision():
    if pygame.sprite.spritecollide(player.sprite, obj_gr, False, pygame.sprite.collide_mask):
        obj_gr.empty()
        return False
    return True
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(225,20))
    screen.blit(score_surf, score_rect)
    return current_time
# Variables
pygame.init()
screen=pygame.display.set_mode((450,600))
pygame.display.set_caption('PLANE GAME')
clock=pygame.time.Clock()
game_active=False
text_font = pygame.font.Font('graphics/Pixeltype.ttf', 50)
start_time=0
score=0
death=randint(2,250)
# Class create

Sky_gr=pygame.sprite.Group()
Sky_gr.add(Sky('sky'))
Sky_gr.add(Sky('sky2'))
player=pygame.sprite.GroupSingle()
obj_gr=pygame.sprite.Group()
player.add(Player())

# Intro
game_name = text_font.render('PLANE GAME', False, (0,0,0))
game_name_rect = game_name.get_rect(center=(225,100))

game_message = text_font.render('Press space to play', False, (0,0,0))
game_message_rect = game_message.get_rect(center=(225,150 ))

ap_background=pygame.image.load('graphics/intro2.png')
ap_background=pygame.transform.rotozoom(ap_background,0,0.5)

crash=pygame.image.load('graphics/crash.png')
crash=pygame.transform.rotozoom(crash,0,0.52)
# Timer
jump_delay=pygame.USEREVENT+1
spawn_timer=pygame.USEREVENT+2
pygame.time.set_timer(spawn_timer,randint(2000,4000))
moving_obj_timer=pygame.USEREVENT+3
pygame.time.set_timer(moving_obj_timer,10000)  # 10 seconds = 10000 milliseconds
sky_timer=pygame.USEREVENT+4
pygame.time.set_timer(sky_timer,70)
game_over_time = None
# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == jump_delay:
                player.sprite.can_jump = True
                pygame.time.set_timer(jump_delay, 0)
            if event.type== spawn_timer:
                obj_gr.add(GameObject(choice(['tower','air_balloon'])))
            if event.type == moving_obj_timer:
                obj_gr.add(GameObject(choice(['plane2','plane3'])))
            if event.type == sky_timer:
                Sky_gr.update()

        else:
            if game_over_time is None:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
                    death = randint(2, 250)
                    obj_gr.empty()
                    player.sprite.reseting()
                    game_over_time=pygame.time.get_ticks()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_time=pygame.time.get_ticks()
                if current_time-game_over_time>=3000:
                    game_active = True
                    start_time = int(pygame.time.get_ticks()/1000)
                    death = randint(2, 250)
                    obj_gr.empty()
                    player.sprite.reseting()
                    game_over_time = None




    if game_active:

        Sky_gr.draw(screen)

        score=display_score()
        player.draw(screen)
        player.update()
        obj_gr.draw(screen)
        obj_gr.update()
        if player.sprite.rect.y > 600 or player.sprite.rect.y < -300:
            game_active = False
        else:
            game_active = collision()
        
    else:
        score_board=text_font.render(f'You flew {score}km and kill {death} people',False,'black',)
        score_board_rect=score_board.get_rect(center=(225,200))
        if score==0:
            screen.blit(ap_background,(0,0))
            screen.blit(game_name,game_name_rect)
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(crash,(0,-60))
            screen.blit(score_board,score_board_rect)

    # Debuging

    pygame.display.update()
    clock.tick(60)