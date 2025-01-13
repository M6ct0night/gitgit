import pygame
import os
import random
pygame.init()

# Global Constants
SCREEN_HEIGHT = 320
SCREEN_WIDTH = 480
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")), (40, 40)),
           pygame.transform.scale(pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png")), (40, 40))]
JUMPING = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png")), (40, 40))
DUCKING = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")), (40, 30)),
           pygame.transform.scale(pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png")), (40, 30))]

SMALL_CACTUS = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")), (30, 30)),
                pygame.transform.scale(pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")), (30, 30)),
                pygame.transform.scale(pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png")), (30, 30))]
LARGE_CACTUS = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")), (40, 40)),
                pygame.transform.scale(pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")), (40, 40)),
                pygame.transform.scale(pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png")), (40, 40))]

BIRD = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")), (40, 30)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bird", "Bird2.png")), (40, 30))]

CLOUD = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Other", "Cloud.png")), (80, 40))

BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Other", "Track.png")), (480, 30))


class Dinosaur:
    X_POS = 40
    Y_POS = 240
    Y_POS_DUCK = 250
    JUMP_VEL = 6.0

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_w] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_s] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_s]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(200, 300)
        self.y = random.randint(40, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(200, 300)
            self.y = random.randint(40, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH + 50

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 250


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 250


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 220
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 270
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        SCREEN.blit(text, (350, 20))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            SCREEN.blit(score, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
        SCREEN.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 - 100))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
