import pygame
import random

#colours
white = [255, 255, 255]
black = [0, 0, 0]
red = [255, 0, 0]
blue = [0, 0, 255]
green = [0, 255, 0]
grey = [ 40, 40, 40]

class Paddle(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos):
        super().__init__()

        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self, change_x):
        '''
        input: int
        updates the position of the paddles
        '''
        self.rect.x += change_x


    def check_boundaries(self):
        '''
        stops paddle moving past the left and right edges of the screen
        '''
        if self.rect.x > screen_width - self.width:
            self.rect.x = screen_width - self.width
        elif self.rect.x <= 0:
            self.rect.x = 0
    
class Brick(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.width = 48
        self.height = 13
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.bricks = []

    def update(self, change_x):
        '''
        input: int
        updates position of the aliens
        '''
        self.rect.x += change_x
    
    def kill_bricks(self):
        '''
        destroys the object
        '''
        self.kill()

class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.width = 10
        self.height = 10
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.x_speed = 0
        self.y_speed = 0
        self.rect.x = screen_width / 2
        self.rect.y = screen_height - (self.height + 40)
        self.launched = False 

    def update(self, y_speed):
        '''
        input: int
        updates the balls positition        
        '''
        self.rect.x += self.x_speed        
        self.rect.y += y_speed

    def check_boundaries(self):
        '''
        resets ball when it hits top of screen
        '''
        if self.rect.y <= 0:
            self.reset(-10, screen_height - (self.height + 40))
            self.launched = False

    def reset(self, x_pos, y_pos):
        '''
        resets the ball
        '''
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.x_speed = 0
        self.y_speed = 0


       

def display_text(display_text, text_coords, text_size, colour):
    '''
    inputs: string, list, int, list
    blits text to the display
    '''
    font = pygame.font.Font(None, text_size)
    text = font.render(display_text, 1, colour)
    text_pos = text.get_rect(centerx = text_coords[0], centery = text_coords[1])
    screen.blit(text, text_pos)

def player_lose():
    '''
    informs player of gameover
    '''
    display_text('Game Over!', screen_center, 60, white)
    pygame.display.flip()
    pygame.time.wait(2000)


def play_again(game_over):
    '''
    input: boolean
    output: boolean
    checks to see if player wants to play again or exit
    '''
    while game_over:
        screen.fill(black)
        display_text('Push y to play again or n to exit', screen_center, 50, white)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

def create_bricks(start, stop, jump):
    '''
    input: 3 tuples
    initiates rows and columns of bricks
    '''
    for x in range(start[0], stop[0], jump[0]):
        for y in range(start[1], stop[1], jump[1]):
            brick = Brick(x, y)
            bricks.add(brick)
            breakout_sprites.add(brick)
    

pygame.init()
clock = pygame.time.Clock()

#create the surface
screen_width = 700
screen_height = 800
screen_center = ((screen_width / 2), (screen_height / 2))
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(black)
pygame.display.set_caption('Space Invaders')

#set up variables
paddle_speed = 0
ball_y_speed = -10
alien_direction = 'right'
alien_x_speed = 10
level_complete = False
score = 0
lives = 3
destroyed_blocks = []
launched = False
levels_won = 0
game_over = False

#initiate ball object
ball = Ball()
balls = pygame.sprite.Group()
balls.add(ball)

#initate laser object
laser = Ball()
laser.rect.y = 90
lasers = pygame.sprite.Group()
lasers.add(laser)

#initiate paddle object
paddle = Paddle(screen_width / 2, screen_height - 50)
paddles = pygame.sprite.Group()
paddles.add(paddle)

#create sprite groups
breakout_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()

#initiate first set of aliens
create_bricks((100, 60), (600, 120), (100, 30))

#add objects to sprite group
breakout_sprites.add(ball)
breakout_sprites.add(paddle)
breakout_sprites.add(bricks)
breakout_sprites.add(laser)

#create event to move bricks
move_bricks_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_bricks_event, 1000)

#create event to shoot laser
shoot_laser_event = pygame.USEREVENT + 2
pygame.time.set_timer(shoot_laser_event, 2500)

running = True
while running:

    clock.tick(30)
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            break
        
        elif event.type == pygame.KEYDOWN:   
            #left and right movement keys
            if event.key == pygame.K_LEFT:
                paddle_speed = -10
            elif event.key == pygame.K_RIGHT:
                paddle_speed = 10
            #stop movement when key is depressed
            if event.key == pygame.K_UP:                 
                        ball.launched = True
                        ball.y_speed = -10             
        #stops movement when key is no longer pressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle_speed = 0
        
        #moves aliens        
        elif event.type == move_bricks_event:
            brick_coord_list = []
            for brick in bricks.sprites():
                brick_coord_list.append((brick.rect.x + brick.width, brick.rect.y))
            
            brick_x_list = [coord[0] for coord in brick_coord_list]
            #changes direction of all aliens when one reaches the edge of the screen
            if max(brick_x_list) >= screen_width:
                alien_x_speed = -10
            elif min(brick_x_list) <= 0 + brick.width:                
                alien_x_speed = 10
            
            for brick in bricks.sprites():
                brick.update(alien_x_speed)

        #shoot alien laser
        elif event.type == shoot_laser_event:
            brick_x_list = [coord[0] for coord in brick_coord_list]
            laser.rect.x = random.choice(brick_x_list)
            laser.rect.y = 90 #need to update this to change y coord depending on y coord of alien
            laser.y_speed = 10

    #sticks player bullets to paddle until launched
    if not ball.launched:
        ball.rect.x = paddle.rect.x + (paddle.width / 2)

    #checks for collision between aliens and bullets
    destroyed_blocks = pygame.sprite.spritecollide(ball, bricks, True)    
    if len(destroyed_blocks) > 0:
        ball.reset(-10, screen_height - (ball.height + 40)) 
        ball.launched = False      
    if len(bricks) == 0:
        level_complete = True

    #checks for collision between the player sprite and the alien lasers
    if pygame.sprite.spritecollide(paddle, lasers, False):
        lives -= 1
        laser.reset(-10, -10)
    
    #update object positions and score
    paddle.update(paddle_speed)
    paddle.check_boundaries()
    ball.update(ball.y_speed)
    ball.check_boundaries()
    laser.update(laser.y_speed)
    laser.check_boundaries()
    score += len(destroyed_blocks) * 10

    #checks for player loss
    if lives <= 0:
        player_lose()
        game_over = True
    if game_over:
        running = play_again(game_over)
        if running:
            for brick in bricks.sprites():
                brick.kill_bricks()
            ball.reset(0, screen_height - (ball.height + 40))
            launched = False
            game_over = False    
            lives = 3
            score = 0
            create_bricks((50, 60), (650, 120), (100, 30))

    #update positions on screen
    screen.fill(black)
    breakout_sprites.draw(screen)
    display_text('score: ' + str(score), (50,30), 30, white)
    display_text('lives: ' + str(lives), (screen_width - 100, 30), 30, white)
    
    #checks for level complete and initiates aliens for level 2
    if level_complete:
        levels_won += 1
        ball.reset(0 , screen_height - (ball.height + 40))
        display_text('Level Complete!', screen_center, 60, white)
        pygame.display.flip()
        pygame.time.wait(1500)
        create_bricks((50, 60), (650,150), (100, 30)) #update this to create more levels
        level_complete = False

    #checks if all levels are complete
    if levels_won == 2:
        game_over = True

    pygame.display.flip()
    
pygame.quit()
