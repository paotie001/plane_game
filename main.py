import pygame
from sys import exit
from random import randint,choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('player.png').convert_alpha()
        self.image=pygame.transform.rotozoom(self.image,0,0.5)
        self.rect=self.image.get_rect(center=(80,300))
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity=0
        self.can_jump=True

    def jump(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.can_jump:
            self.gravity -= 20
            self.can_jump = False
            pygame.time.set_timer(jump_delay, 300)
    def earthing(self):
        self.gravity += 0.5
        self.rect.y += self.gravity

    def update(self):
        self.jump()
        self.earthing()


class Object(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        match type:
            case 'tower':
                self.image=pygame.image.load('obj1.png').convert_alpha()
                self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
                self.rect=self.image.get_rect(midbottom=(600,randint(650,800)))
            case 'air_balloon':
                self.image = pygame.image.load('obj2.png').convert_alpha()
                self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
                self.rect = self.image.get_rect(midtop=(600,randint(50,-100)))
        self.mask = pygame.mask.from_surface(self.image)
    def destroy(self):
        if self.rect.x<-200:
            self.kill()
    def update(self):
        self.destroy()
        self.rect.x -= 5
def coslision():
    if pygame.sprite.spritecollide(player.sprite,obj_gr,False,pygame.sprite.collide_mask):
        obj_gr.empty()
        return False
    return True
pygame.init()
screen=pygame.display.set_mode((500,600))
pygame.display.set_caption('FLAPPY BIRD')
clock=pygame.time.Clock()
game_active=True
test_font = pygame.font.Font('Pixeltype.ttf', 50)

Sky_img=pygame.image.load('sky.png')
Sky_img=pygame.transform.rotozoom(Sky_img,0,0.7)

player=pygame.sprite.GroupSingle()
obj_gr=pygame.sprite.Group()
player.add(Player())


# Timer
jump_delay=pygame.USEREVENT+1
spawn_timer=pygame.USEREVENT+2
pygame.time.set_timer(spawn_timer,3000)
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
                obj_gr.add(Object(choice(['tower','air_balloon'])))



    if game_active:
        screen.blit(Sky_img,(0,-300))
        player.draw(screen)
        player.update()
        obj_gr.draw(screen)
        obj_gr.update()
        if player.sprite.rect.y > 600 or player.sprite.rect.y < -300:
            game_active = False
        else:
            game_active = coslision()
        
    else:
        screen.fill('green')
    #debuging


    pygame.display.update()
    clock.tick(60)