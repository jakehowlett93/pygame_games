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
        self.rect.y = screen_height - (self.height + 50) 

    def update(self, y_speed):
        '''
        input: int
        updates the balls positition        
        '''
        self.rect.x += self.x_speed        
        self.rect.y += y_speed

    def check_boundries(self):
        '''
        changes balls direction when it hits the top of the screen or the left and right edges
        '''
        if self.rect.y <= 0:
            self.y_speed = abs(self.y_speed)
   
        if self.rect.x <= 0:
            self.x_speed = abs(self.x_speed)       
        elif self.rect.x >= screen_width:
            self.x_speed = abs(self.x_speed) * -1

    def lost_ball_check(self):
        '''
        checks if ball passes the bottom of the screen
        '''
        if self.rect.y >= screen_height:
            return True

    def reset(self):
        '''
        resets the ball
        '''
        self.rect.x = screen_width / 2
        self.rect.y = screen_height - (self.height + 50) 
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

def player_lose(player_lives):
    '''
    input: int
    output: boolean
    checks to see if a player has won
    '''
    if player_lives == 0:
        display_text('Game Over!', screen_center, 60, white)
        pygame.display.flip()
        pygame.time.wait(2000)
        return True

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
pygame.display.set_caption('Breakout')

#set up variables
paddle_speed = 0
ball_y_speed = -10
winner = False
score = 0
lives = 3
level = 1
destroyed_bricks = []
launched = False

#initiate ball object
ball = Ball()
balls = pygame.sprite.Group()
balls.add(ball)

#initiate paddle object
paddle = Paddle(screen_width / 2, screen_height - 50)
paddles = pygame.sprite.Group()
paddles.add(paddle)

#create sprite groups
breakout_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()

#initiate first set of bricks
create_bricks((50, 60), (650, 90), (50, 15))

#add objects to sprite group
breakout_sprites.add(ball)
breakout_sprites.add(paddle)
breakout_sprites.add(bricks)

running = True
while running:

    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        
        if event.type == pygame.KEYDOWN:   
            #left and right movement keys
            if event.key == pygame.K_LEFT:
                paddle_speed = -10
            elif event.key == pygame.K_RIGHT:
                paddle_speed = 10

            if event.key == pygame.K_UP:
                #launches the ball when upkey is pressed    
                launched = True
                ball.y_speed = -20
                ball.x_speed = 2   
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #stops movement when key is no longer pressed                
                paddle_speed = 0

    if not launched:
        #sticks ball to the paddle until it is launched
        ball.rect.x = paddle.rect.x

    #checks for collision between bricks and the ball
    destroyed_bricks = (pygame.sprite.spritecollide(ball, bricks, True))
    if len(destroyed_bricks) > 0:
        ball.y_speed = ball.y_speed * -1            
    if len(bricks) == 0:
        winner = True

    #checks for collision between paddle and the ball
    if pygame.sprite.spritecollide(paddle, balls, False):
        #some reason abs(ball.y_speed * -1 doesnt work)
        ball.y_speed = -20
        

    #update object positions and score
    paddle.update(paddle_speed)
    paddle.check_boundaries()
    ball.update(ball.y_speed)
    ball.check_boundries()
    score += len(destroyed_bricks) * 10

    #checks if player has lost the ball
    lost_ball = ball.lost_ball_check()
    if lost_ball == True:
        lives -= 1
        pygame.time.wait(1000)
        ball.reset()
        launched = False

    game_over = player_lose(lives)
    if game_over:
        running = play_again(game_over)
        if running:
            lives = 3
            score = 0
            create_bricks((50, 60), (650, 90), (50, 15))


    #update positions on screen
    screen.fill(black)
    breakout_sprites.draw(screen)

    #displays score and lives
    display_text('score: ' + str(score), (50,30), 30, white)
    display_text('lives: ' + str(lives), (screen_width - 100, 30), 30, white)
    if not launched:
        display_text('Use the up arrow to launch the ball', screen_center, 30, white)
    
    if winner:
        ball.reset()
        display_text('Level 2!', screen_center, 60, white)
        pygame.display.flip()
        pygame.time.wait(1500)
        create_bricks((50, 60), (650,150), (100, 30))
        winner = False


    pygame.display.flip()
    

pygame.quit()
