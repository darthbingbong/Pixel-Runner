import pygame
from sys import exit
from random import randint, choice

# Initialize Pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner game')
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/game_font.ttf', 50)
game_active = False

# Background and ground surfaces
sky_surface = pygame.image.load('Graphics/Sky.png').convert()
ground_surface = pygame.image.load('Graphics/ground.png').convert()

#Background music
bg_music=pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops=-1)


# Intro screen settings
player_stand = pygame.image.load('Graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

intro_surf = text_font.render('Pixel Runner', False, (70, 70, 70))
intro_rect = intro_surf.get_rect(midtop=(400, 25))

instruction_surf = text_font.render('Press Space to start', False, (70, 70, 70))
instruction_rect = instruction_surf.get_rect(midbottom=(400, 350))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Graphics/Player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('Graphics/Player/jump.png').convert_alpha()
        self.player_index = 0
        self.player_list = [player_walk_1, player_walk_2]
        
        self.image = self.player_list[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound=pygame.mixer.Sound('audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_list):
                self.player_index = 0
            self.image = self.player_list[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_frame1 = pygame.image.load('Graphics/Fly/Fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('Graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load('Graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('Graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomright=(randint(900, 1100), y_pos))

    def animation(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation()
        self.rect.x -= 5
        self.destroy()

# Display score function
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = text_font.render(f'{current_time}', False, (70, 70, 70))
    score_rect = score_surf.get_rect(center=(400, 50))
    
    pygame.draw.rect(screen, '#c0e8ec', score_rect)
    pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
    screen.blit(score_surf, score_rect)
    return current_time

# Player instance
player = pygame.sprite.GroupSingle()
player.add(Player())

# Obstacle group
obstacle_group = pygame.sprite.Group()

# Timer settings
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer, 200)

snail_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(snail_animation_timer, 400)

start_time = 0
score = 0

while True:
    for event in pygame.event.get():  # gets all the possible events for player input
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail'])))

        if not game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True
            start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        score = display_score()

        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()

        if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
            game_active = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_group.empty()
        player.sprite.rect.midbottom = (80, 300)
        player.sprite.gravity = 0

        score_message = text_font.render(f'Your score: {score}', False, (70, 70, 70))
        score_message_rect = score_message.get_rect(midbottom=(400, 400))
        if score == 0:
            screen.blit(intro_surf, intro_rect)
            screen.blit(instruction_surf, instruction_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)  # setting max frame rate


#made by Anand Venukrishnan- 10/07/2024