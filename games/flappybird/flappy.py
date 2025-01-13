import pygame, sys, random 

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 270))
    screen.blit(floor_surface, (floor_x_pos + 480, 270))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(520, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(520, random_pipe_pos - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 320:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def remove_pipes(pipes):
    return [pipe for pipe in pipes if pipe.centerx > -50]

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= 270:
        return False

    return True

def rotate_bird(bird):
    return pygame.transform.rotozoom(bird, -bird_movement * 3, 1)

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(240, 40))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(240, 40))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(240, 250))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    return max(score, high_score)

pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((480, 320))
clock = pygame.time.Clock()
game_font = pygame.font.Font('x.ttf', 20)

# Game Variables
gravity = 0.15
bird_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (480, 320))

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (480, 50))
floor_x_pos = 0

bird_downflap = pygame.transform.scale(pygame.image.load('assets/bluebird-downflap.png').convert_alpha(), (34, 24))
bird_midflap = pygame.transform.scale(pygame.image.load('assets/bluebird-midflap.png').convert_alpha(), (34, 24))
bird_upflap = pygame.transform.scale(pygame.image.load('assets/bluebird-upflap.png').convert_alpha(), (34, 24))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 160))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (52, 320))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 250, 300]

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (200, 200))
game_over_rect = game_over_surface.get_rect(center=(240, 160))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 160)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % 3
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        pipe_list = remove_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -480:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
