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

        self.width = 15
        self.height = 75
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos

    def update(self, change_y):
        '''
        input: int
        updates the position of the paddles
        also checks to make sure paddles dont move past the top or bottom boundry
        '''
        self.rect.y += change_y


    def check_boundaries(self):
        '''
        stops paddle moving pass the top and bottom of the screen
        '''
        if self.rect.y > screen_height - self.height:
            self.rect.y = screen_height - self.height
        elif self.rect.y <= 0:
            self.rect.y = 0
    

class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.width = 10
        self.height = 10
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.x_speed = 4
        self.y_speed = 4
        self.rect.x = 200
        self.rect.y = 30
        self.direction = 0

    def update(self, x_speed):
        '''
        input: int
        updates the balls positition        
        '''
        self.rect.y += self.y_speed
        self.rect.x += x_speed

    def check_boundries(self):
        '''
        changes balls direction when it hits the top or bottom of the screen
        '''
        if self.rect.y >= 390:
            self.y_speed = abs(self.y_speed) * -1
        elif self.rect.y <= 0:
            self.y_speed = abs(self.y_speed)

    def reset(self, scorer):
        '''
        input:string
        resets the ball depending on who scored
        '''
        if scorer == 'left':
            self.rect.x = 150
            self.rect.y = random.randrange(100, 300, 50)
            self.x_speed = 4
            self.y_speed = random.choice([4, -4])
        elif scorer == 'right':
            self.rect.x = 450
            self.rect.y = random.randrange(100, 300, 50)
            self.x_speed = -4
            self.y_speed = random.choice([4, -4])            

def display_text(display_text, text_coords, text_size, colour):
    '''
    inputs: string, list, int, list
    blits text to the display
    '''
    font = pygame.font.Font(None, text_size)
    text = font.render(display_text, 1, colour)
    text_pos = text.get_rect(centerx = text_coords[0], centery = text_coords[1])
    screen.blit(text, text_pos)

def display_scores(player_score):
    '''
    input: string
    blits the scores to the screen
    '''
    display_text(str(player_score[0]), ((screen_width / 2) - 100, 100) , 150, grey)
    display_text(str(player_score[1]), ((screen_width / 2) + 100, 100), 150, grey)

def player_scored(scorer):
    '''
    input: string
    calls function to reset the ball
    blits goal to the display
    '''  
    ball.reset(scorer)
    display_text('Goal!', screen_center, 60, white)
    display_scores(player_score)
    pygame.display.flip()
    pygame.time.wait(2000)

def player_win(player_score):
    '''
    input: list
    output: boolean
    checks to see if a player has won
    '''
    if player_score[0] == 3:
        display_text('Left player wins!', screen_center, 60, white)
        pygame.display.flip()
        pygame.time.wait(2000)
        return True
    elif player_score[1] == 3:
        display_text('Right player wins!', screen_center, 60, white)
        pygame.display.flip()
        pygame.time.wait(2000)
        return True
    else:
        return False

def play_again(winner):
    '''
    input: boolean
    output: boolean
    checks to see if player wants to play again or exit
    '''
    while winner:
            screen.fill(black)
            display_text('Push y to play again or n to exit', screen_center, 50, white)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        winner = False
                        return True
                    elif event.key == pygame.K_n:
                        winner = False
                        return False
        
#initiate pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

#initiate ball object
ball = Ball()
balls = pygame.sprite.Group()
balls.add(ball)

#create the surface
screen_width = 600
screen_height = 400
screen_center = ((screen_width / 2), (screen_height / 2))
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(black)
pygame.display.set_caption('PONG')

#initiate paddle objects
left_paddle = Paddle(10, screen_height / 2)
right_paddle = Paddle(575, screen_height / 2)

#add objects to sprite group
moving_sprites = pygame.sprite.Group()
moving_sprites.add(left_paddle)
moving_sprites.add(right_paddle)
moving_sprites.add(ball)

#set up variables
font = pygame.font.Font(None, 36)
left_paddle_speed = 0
right_paddle_speed = 0
player_score = [0,0]
clock = pygame.time.Clock()
hit_counter = ball.x_speed
paused = True
winner = False

#game loop
running = True
while running:

    for event in pygame.event.get():
        
        #quit program if exit is clicked
        if event.type == pygame.QUIT:
            running = False
            break
            
        if event.type == pygame.KEYDOWN:
            #w and s movement keys
            if event.key == pygame.K_w:
                left_paddle_speed = -6
            elif event.key == pygame.K_s:
                left_paddle_speed = 6

            #up and down movement keys
            if event.key == pygame.K_UP:
                right_paddle_speed = -6
            elif event.key == pygame.K_DOWN:
                right_paddle_speed = 6

            #pause / unpause with p
            if event.key == pygame.K_p:
                paused = not paused

        #stops movement when key is no longer pressed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                left_paddle_speed = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                right_paddle_speed = 0
   
    #limit fps to 30    
    clock.tick(30)

    if not paused:

        #check for collision between balls and paddles
        if pygame.sprite.spritecollide(left_paddle, balls, False):
            hit_counter = abs(hit_counter) + 2
            ball.x_speed = hit_counter
        
        if pygame.sprite.spritecollide(right_paddle, balls, False):
            hit_counter = (abs(hit_counter) * - 1 ) - 2
            ball.x_speed = hit_counter

        #check for goal and update score
        if ball.rect.x > screen_width:
            player_score[0] += 1
            player_scored('left')
            hit_counter = ball.x_speed
        elif ball.rect.x <= 0:
            player_score[1] += 1
            player_scored('right')
            hit_counter = ball.x_speed

        #update object positions
        left_paddle.update(left_paddle_speed)
        left_paddle.check_boundaries()
        right_paddle.update(right_paddle_speed)
        right_paddle.check_boundaries()
        ball.update(ball.x_speed)
        ball.check_boundries()

        #update positions on screen
        screen.fill(black)
        moving_sprites.draw(screen)
   
    elif paused:
        display_text("Paused press P to start", screen_center, 30, grey)
        display_text("W", (40, (screen_height / 2) - 20), 30, grey)
        display_text("S", (40, (screen_height / 2) + 20), 30, grey)
        display_text("Up", ((screen_width - 40), (screen_height / 2 - 20)), 30, grey)
        display_text("Down", ((screen_width - 40), (screen_height / 2 + 20)), 30, grey)        

    #update display
    pygame.display.flip()

    #check for winner
    winner = player_win(player_score)
    if winner:          
        running = play_again(winner)
        if running:
            player_score = [0,0]        
 
#exit game
pygame.quit()
