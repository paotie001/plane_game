import pygame
from sys import exit
from random import randint,choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('graphics/player.png').convert_alpha()
        self.image=pygame.transform.rotozoom(self.image,0,0.5)
        self.rect=self.image.get_rect(center=(80,300))
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity=0
        self.can_jump=True

    def jump(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.can_jump:
            self.gravity -= 17
            self.can_jump = False
            pygame.time.set_timer(jump_delay, 300)
    def earthing(self):
        self.gravity += 0.5
        self.rect.y += self.gravity
    def reseting(self):
        self.rect.center = (80, 300)
        self.gravity=0
    def update(self):
        self.jump()
        self.earthing()


class Object(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        match type:
            case 'tower':
                self.image=pygame.image.load('graphics/obj1.png').convert_alpha()
                self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
                self.rect=self.image.get_rect(midbottom=(600,randint(650,800)))
            case 'air_balloon':
                self.image = pygame.image.load('graphics/obj2.png').convert_alpha()
                self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
                self.rect = self.image.get_rect(midtop=(600,randint(50,500)-150))
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
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(250,20))
    screen.blit(score_surf, score_rect)
    return current_time

pygame.init()
screen=pygame.display.set_mode((500,600))
pygame.display.set_caption('FLAPPY BIRD')
clock=pygame.time.Clock()
game_active=False
text_font = pygame.font.Font('graphics/Pixeltype.ttf', 50)
start_time=0
score=0
death=randint(2,250)
Sky_img=pygame.image.load('graphics/sky3.png')
Sky_img=pygame.transform.rotozoom(Sky_img,0,0.7)

player=pygame.sprite.GroupSingle()
obj_gr=pygame.sprite.Group()
player.add(Player())

# Intro
game_name = text_font.render('Pilot exam', False, (0,0,0))
game_name_rect = game_name.get_rect(center=(250, 250))

game_message = text_font.render('Press space to start the exam', False, (0,0,0))
game_message_rect = game_message.get_rect(center=(250,350 ))

died=pygame.image.load('graphics/died.jpeg')
died=pygame.transform.rotozoom(died,0,0.5)
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
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
                death = randint(2, 250)
                player.sprite.reseting()




    if game_active:
        screen.blit(Sky_img,(0,-300))
        score=display_score()
        player.draw(screen)
        player.update()
        obj_gr.draw(screen)
        obj_gr.update()
        if player.sprite.rect.y > 600 or player.sprite.rect.y < -300:
            game_active = False
        else:
            game_active = coslision()
        
    else:
        score_board=text_font.render(f'You flew {score}km and kill {death} people',False,'black',)
        score_board_rect=score_board.get_rect(center=(250,300))
        if score==0:
            screen.fill('#4181e8')
            screen.blit(game_name,game_name_rect)
            screen.blit(game_message,game_message_rect)
        else:
            screen.fill('#4181e8')
            #screen.blit(died,(0,0))
            screen.blit(score_board,score_board_rect)
    #debuging

    pygame.display.update()
    clock.tick(60)