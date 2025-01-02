import math
import random
import pygame
from pygame import mixer

#initialise the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((700,500))

#background
background=pygame.image.load('space background.png')

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#caption and icon
pygame.display.set_caption("COSMIC SHOWDOWN")
logo=pygame.image.load('logo.png')
pygame.display.set_icon(logo)

#Player
playerImg=pygame.image.load('player.png')
playerX=320
playerY=380
playerX_change=0

#Enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
no_of_enemies=8

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,636))
    enemyY.append(random.randint(20,200))
    enemyX_change.append(4)
    enemyY_change.append(0)


#Bullet
#Ready state means bullet is ready but can't be seen on screen
#Fire state means bullet is seen firing on the screen
bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=380
bulletX_change=0
bulletY_change=12
bullet_state="ready"

#Score
score=0
font = pygame.font.Font('font.ttf', 32) #font and size

# GAME OVER
game_over_font = pygame.font.Font('font.ttf', 64) 
game_over=False

#Reset Icon
def Reset():
    pygame.draw.rect(screen,(0,0,0),(300,300,120,50))
    reset_icon=font.render("RESET",True,(255,255,255))
    screen.blit(reset_icon,(315,310))

#Reset Functionality
def Reset_game():
    global playerX, playerY, bulletX, bulletY, bullet_state, score, game_over, enemyX, enemyY
    playerX = 320
    playerY = 380
    bulletX = 0
    bulletY = 380
    bullet_state = "ready"
    score = 0
    game_over = False
    for i in range(no_of_enemies):
        enemyX[i] = random.randint(0, 636)
        enemyY[i] = random.randint(20, 200)


#SCORE
textX=550
textY=10

def show_score(x, y):
    score_text = font.render("SCORE:"+ str(score),True,(255,255,255))
    screen.blit(score_text, (x, y))

#Game Over
def game_over_text(x, y):
    pygame.draw.rect(screen, (50,50,50), (0, y - 20, 700, 100))
    text = game_over_font.render("GAME OVER",True,(0,150,0))
    screen.blit(text, (x, y))

#Player
def player(x,y) :
    screen.blit(playerImg,(x,y)) #to draw player on screen

#Enemy
def enemy(x,y,i) :
    screen.blit(enemyImg[i],(x,y))  #to draw enemy on screen

#Bullet functionality
def fire_bullet(x,y) :
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))  #to draw bullet on screen

#Collision detection   
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance= math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False



#game loop
running=True
while running:

    #RGB= red,green,blue 
    #Their values go till 255
    screen.fill((0,0,0))  

    # Background 
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        #setting an event so pygame window can be exited
        if event.type==pygame.QUIT:
            running=False

        # setting an event for resetting the game
        if event.type==pygame.MOUSEBUTTONDOWN:
            if game_over==True: #only if game is over
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 400 and 300 <= mouse_pos[1] <= 350:
                    Reset_game()  # Reset the game when button is clicked
           
        #setting an event to manage movement of our player using keystrokes
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                if game_over==False:
                    playerX_change-=5
                    bulletX_change-=5
            if event.key==pygame.K_RIGHT:
                if game_over==False:
                    playerX_change+=5
                    bulletX_change+=5
            if event.key==pygame.K_SPACE:
                if game_over==False:
                    if bullet_state is "ready":
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        # Get the current x cordinate of the spaceship
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                    

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
            if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                playerY_change=0
               

    #checking for boundaries for player
    playerX+=playerX_change   
    if playerX<=0:
        playerX=0 
    elif playerX>=636:
        playerX=636 
    player(playerX,playerY)

    #Bullet Movement
    if bullet_state=="fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change
    if bulletY<=0:
        bulletY=380
        bullet_state="ready"
    
    #movement mechanics of enemy 
    for i in range(no_of_enemies) :
        if enemyY[i]>=playerY-40 and abs(enemyX[i]-playerX)>=30:
            for j in range (no_of_enemies):
                enemyY[j]=2000
            game_over_text(180,200)
            game_over=True
            Reset()
            
        if enemyX[i]<=0:
            enemyY[i]+=30
            enemyX_change[i]=4
        elif enemyX[i]>=636:
            enemyY[i]+=30
            enemyX_change[i]=-4

        if isCollision(enemyX[i],enemyY[i],bulletX,bulletY):
            bulletY=380
            bullet_state="ready"
            score+=1 
            enemyX[i]=random.randint(0,636)
            enemyY[i]=random.randint(20,200) 
            collision_sound=mixer.Sound('explosion.wav')
            collision_sound.play()   
        enemyX[i]+=enemyX_change[i]    
        enemy(enemyX[i],enemyY[i],i)

    show_score(textX,textY)
    pygame.display.update()
