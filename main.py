import os
import  pygame

pygame.font.init()
pygame.mixer.init()
# 0,0 co ordinate are at the top left of the screen
path = "/home/dev16/Pygame/Basic"
WIDTH,HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("FIrst Game !")
WHITE = (255,255,255)
BLACK = (0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

HEALTH_FONT =pygame.font.SysFont('comicsans',40)
WINNER_FONT =pygame.font.SysFont('comicsans',100)

FPS = 60
SPACESHIP_WIDTH,SPACESHIP_HEIGHT=55,40

# Creating manual events for bullet collision
YELLOW_HIT = pygame.USEREVENT+1
RED_HIT = pygame.USEREVENT +2

SPACE = pygame.transform.scale(pygame.image.load(os.path.join(path,'Assets','space.png')),(WIDTH,HEIGHT))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(path,'Assets','spaceship_yellow.png'))

# Below resizes the image
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,
                                        (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(path,'Assets','spaceship_red.png'))

RED_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,
                                     (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

BULLET_HIT_SOUND =pygame.mixer.Sound(os.path.join(path,'Assets','shoot.wav'))
BULLET_FIRE_SOUND =pygame.mixer.Sound(os.path.join(path,'Assets','Grenade+1.wav'))

VEL=5
BULLET_VEL=8
MAX_BULLETS=5

BORDER=pygame.Rect(WIDTH//2-5,0,10,HEIGHT)


# Key bindings For  YELLOW
YELLOW_LEFT=pygame.K_a
YELLOW_RIGHT=pygame.K_d
YELLOW_UP=pygame.K_w
YELLOW_DOWN=pygame.K_s


# key bindings for RED
RED_LEFT=pygame.K_LEFT
RED_RIGHT=pygame.K_RIGHT
RED_UP=pygame.K_UP
RED_DOWN=pygame.K_DOWN

def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    
     # Below fills the window with color pass a tuple 
     # of hex
    WIN.fill(WHITE)
    WIN.blit(SPACE,(0,0))
    
    # Below is used to display text
    red_health_text=HEALTH_FONT.render("Health: "+str(red_health),1,WHITE)
    yellow_health_text=HEALTH_FONT.render("Health: "+str(yellow_health),1,WHITE)
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))
    
    # Use below when you want draw surfaces like text or images
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)
        
    pygame.draw.rect(WIN,BLACK,BORDER)
    pygame.display.update()
    
    
def yellow_handle_movement(keys_pressed,yellow):
    
    if keys_pressed[YELLOW_LEFT] and yellow.x -VEL > 0:
        yellow.x-=VEL
    if keys_pressed[YELLOW_RIGHT] and yellow.x+VEL+yellow.width < BORDER.x:
        yellow.x+=VEL
    if keys_pressed[YELLOW_UP] and yellow.y-VEL > 0:
        yellow.y-=VEL
    if keys_pressed[YELLOW_DOWN] and yellow.y+VEL+ yellow.height < HEIGHT:
        yellow.y+=VEL
        
def red_handle_movement(keys_pressed,red):
    
    if keys_pressed[RED_LEFT] and red.x -VEL> BORDER.x+BORDER.width:
        red.x-=VEL 
    if keys_pressed[RED_RIGHT] and red.x+VEL+red.width < WIDTH:
        red.x+=VEL
    if keys_pressed[RED_UP] and red.y-VEL > 0:
        red.y-=VEL
    if keys_pressed[RED_DOWN] and red.y+VEL+red.height < HEIGHT:
        red.y+=VEL     
        

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    
    for bullet in yellow_bullets:
        bullet.x+=BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x> WIDTH:
            yellow_bullets.remove(bullet)  
            
    for bullet in red_bullets:
        bullet.x-=BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
            
def draw_winner(text):
    draw_text=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()//2,
                        HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    
def main():
    red_health=10
    yellow_health=10
    red = pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    # Below makes sure that while loop runs at 60 fps on all
    # machines
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        
        # Below gives the list of all events that are  occuring
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
            if event.type == RED_HIT:
                red_health-=1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.play()
                
        winner_text=""
        if red_health <= 0:
            winner_text= "YELLOW WINS !!!!"
        if yellow_health <= 0:
            winner_text= "RED WINS !!!!"
        if winner_text !='' :
            draw_winner(winner_text)
            break
                
        # Below line tells us which keys are curently pressed        
        keys_pressed=pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)
                
    main()

if __name__ == "__main__":
    print(os.getcwd())
    main()