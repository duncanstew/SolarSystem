
import pygame
import os
import random

SUN = pygame.image.load(os.path.join("spaceImgs", "sun.png"))
VENUS = pygame.image.load(os.path.join("spaceImgs", "venus.png"))
EARTH = pygame.image.load(os.path.join("spaceImgs", "earth.png"))
MARS = pygame.image.load(os.path.join("spaceImgs", "mars.png"))
JUPITER = pygame.image.load(os.path.join("spaceImgs", "jupiter.png"))
SATURN = pygame.image.load(os.path.join("spaceImgs", "saturn0.png"))
SATURN80 = pygame.image.load(os.path.join("spaceImgs", "saturn80.png"))
SATURN120 = pygame.image.load(os.path.join("spaceImgs", "saturn120.png"))
NEPTUNE = pygame.image.load(os.path.join("spaceImgs", "neptune.png"))
DEATHSTAR = pygame.image.load(os.path.join("spaceImgs", "deathstar.png"))

REPAIR = pygame.image.load(os.path.join("spaceImgs", "repair.png"))

pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 45)
WHITE = (255,255,255)

PLANETS = [
    SUN,
    VENUS,
    EARTH,
    MARS,
    JUPITER,
    SATURN,
    SATURN80,
    SATURN120,
    NEPTUNE,
    DEATHSTAR
]


STAR_IMG = pygame.image.load(os.path.join("spaceImgs", "stars.png"))
SPACESHIP_IMG = pygame.image.load(os.path.join("spaceImgs", "spaceship.png"))

WIDTH = 500
HEIGHT = 700

class SpaceShip:
    VEL = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.IMG = pygame.transform.scale(SPACESHIP_IMG, (40,80))

    def move(self):
        self.y -= self.VEL

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

    def print(self):
        print('{} {}'.format(self.x, self.y))




class Planet:
    VEL = 5
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.top = 0
        self.bottom = 0
        self.height = 0
        self.passed = False
        self.collision = False
        self.set_size()
        self.choose_image()
        self.id = random.randrange(1000,100000)

    def set_size(self):
        self.height = random.randrange(50,300)
        self.top = self.y
        self.bottom = self.y + self.height

    def move(self):
        self.y += self.VEL

    def choose_image(self):
        obj = random.randrange(0, len(PLANETS))
        self.IMG = pygame.transform.scale(PLANETS[obj], (self.height,self.height))

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

    def collide(self, spaceship):
        spaceship_mask = pygame.mask.from_surface(spaceship.IMG)
        planet_mask = pygame.mask.from_surface(self.IMG)

        offset = (int(self.x - spaceship.x), int(self.y - round(spaceship.y)))

        collision = spaceship_mask.overlap(planet_mask, offset)

        if collision:
            return True
        else:
            return False

    def print(self):
        print('id: {} [{}]'.format(self.id, self.y))


class BackGround:
    VEL = 5
    HEIGHT = STAR_IMG.get_height()
    IMG = STAR_IMG

    def __init__(self):
        self.x = 0
        self.y1 = 0
        self.y2 = -self.HEIGHT

    def move(self):
        self.y1 += self.VEL
        self.y2 += self.VEL

        if self.y1 > self.HEIGHT:
            self.y1 = self.y2 - self.HEIGHT

        if self.y2 > self.HEIGHT:
            self.y2 = self.y1 - self.HEIGHT



    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y1))
        win.blit(self.IMG, (self.x, self.y2))


    def print(self):
        print('[{} {}]'.format(self.y1, self.y2))





def draw_window(win, base, planets, spaceship, score, lives):
    base.draw(win)
    for planet in planets:
        planet.draw(win)
    rep = pygame.transform.scale(REPAIR, (60,60))
    imgWidth = rep.get_width()

    for i in range(lives):
        win.blit(rep, (WIDTH - imgWidth - imgWidth*i, 40))

    spaceship.draw(win)
    scoreText = FONT.render("Score: " + str(score), 1, WHITE)
    win.blit(scoreText, (WIDTH - scoreText.get_width() - 10, 10))
    pygame.display.update()

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    score = 0
    lives = 3
    SPEED = 10
    run = True
    base = BackGround()
    planets = [Planet(200, 0)]
    spaceship = SpaceShip(WIDTH/2, HEIGHT/2)
    clock = pygame.time.Clock()

    while run:
        if lives == 0:
            run = False

        add_planet = False
        clock.tick(30)

        rem = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        # Section to check the key presses and control movement of spaceship
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            spaceship.x -= SPEED
            if spaceship.x < 0:
                spaceship.x = 0

        elif pressed[pygame.K_RIGHT]:
            spaceship.x += SPEED
            if spaceship.x > WIDTH - spaceship.IMG.get_width():
                spaceship.x = WIDTH - spaceship.IMG.get_width()

        elif pressed[pygame.K_UP]:
            spaceship.y -= SPEED
            if spaceship.y < 0:
                spaceship.y = 0
        elif pressed[pygame.K_DOWN]:
            spaceship.y += SPEED - 3
            if spaceship.y > HEIGHT - spaceship.IMG.get_height():
                spaceship.y = HEIGHT - spaceship.IMG.get_height()




        # Section to determine if the space object has been passed and regenerate a new one
        for planet in planets:
            if planet.collide(spaceship) and planet.collision == False:
                planet.collision = True
                lives -= 1


            if spaceship.y < planet.y - planet.IMG.get_height():
                rem.append(planet)

            if not planet.passed and spaceship.y < planet.y:
                planet.passed = True
                add_planet = True

            planet.move()


        spaceship.move()
        base.move()

        draw_window(win, base, planets, spaceship, score, lives)

        if add_planet:
            score += 1
            x = random.randrange(50, WIDTH-150)
            planets.append(Planet(x, -250))

        for planet in rem:
            if planet.y > HEIGHT:
                planets.remove(planet)
    pygame.quit()
    quit()


main()