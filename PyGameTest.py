import pygame                #import module
import os                    #import OS
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGH = 900, 500        #set screen size
WIN = pygame.display.set_mode((WIDTH, HEIGH)) #define window size
pygame.display.set_caption("First Game!")  #display windows name

WHITE = (255, 255, 255) #Color with 3 values RGB  x,x,x  0-255
BLACK = (0, 0, 0) #Color with 3 RGB 0 = none
RED = (255, 0, 0)
YELLOW = (255, 255, 0) 


BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGH)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60  #set the FPS to 60
VEL = 5 # repeated value for the moving speed when key pressed.
BULLET_VEL = 7
MAX_BULLETS = 3
SPACE_SHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40 #Since you are going to use it multiple times make a NAME so you don't need to repeat typing

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png')) #import images to pygame in the Assets folder and name of the file
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACE_SHIP_WIDTH, SPACESHIP_HEIGHT)), 90)  #scale the size of the spaceship images (transform.rotate image)

RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'spaceship_red.png')), 270)
RED_SPACESHIP =  pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACE_SHIP_WIDTH, SPACESHIP_HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),(WIDTH, HEIGH))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #from top-left to draw the images
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) #red spaceshipt to the right and using the main red= and yellow= values to start the spaceship.  
    
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
        
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
        
    pygame.display.update() #refresh to have the effect shows
    
def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #left
            yellow.x -= VEL
        if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #right
            yellow.x += VEL
        if keys_pressed[pygame.K_w] and yellow.y - VEL > 0 : #up
            yellow.y -= VEL
        if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGH - 15: #down
            yellow.y += VEL
        
def red_handle_movement(keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  #left
            red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #right
            red.x += VEL
        if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #up
            red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGH - 15: #down 
            red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)  
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet) 
 
def draw_winner(text):
     draw_text = WINNER_FONT.render(text, 1 , WHITE)
     WIN.blit(draw_text, (WIDTH/2 - draw_text_width()/2, HEIGH/2 - draw_text_height()/2))
     pygame.display.update()
     pygame.time.delay(5000)           
  
def main(): #define application with main
    red = pygame.Rect(700, 300, SPACE_SHIP_WIDTH, SPACESHIP_HEIGHT) #set the volume to have the icons move around a range of spaces
    yellow = pygame.Rect(100, 300, SPACE_SHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    
    red_health = 10
    yellow_health = 10
    
    clock = pygame.time.Clock() #add clock to time the FPS to make sure it's at 60
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False #set condition to close the loop or it won't be able to close. 
                pygame.quit()            #red.x += 1 #set the red space ship to move 1 frame faster than default 60 using += 1       # draw_window(red, yellow)= draw out the red and yellow spaceship  #refresh the windows 
                            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS :
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS :
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5 )
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
             
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
                
            if event.type == YELLOW_HIT:      
                yellow_health -= 1
                BULLET_HIT_SOUND.pay()
        
        winner_text = ""        
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        
        if yellow_health <= 0:
            winner_text = "RED Wins!"
            
        if winner_text != "":
            draw_winner(winner_text)
            break
            
            
                
        keys_pressed = pygame.key.get_pressed() #This means it will record and capture keys so that the game can respond to it.
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red) 
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()            
    #pygame.quit()  #condition when to quick the proggram
    
    
if __name__ == "__main__":
    main()   
