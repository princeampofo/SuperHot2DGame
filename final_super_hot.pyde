'''
Prince Ampofo
Ramon Wrzosek 
'''
import os ,time
add_library('minim')  #library for sounds
path = os.getcwd()
audioplayer = Minim(this) #to create a new audio player
from random import randint


block_size=20 #pixels 

 
RES_X=800 #Width
RES_Y=600 #Height

color_list=[color(255,51,52), color(12,150,228), color(30,183,66), color(246,187,0),
      color(76,0,153), color(255,255,255), color(0,0,0)]

 
class Characters:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.r=block_size/2
      
class Player(Characters):
    def __init__(self,x,y):
        Characters.__init__(self,x,y)
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.clicked = False
        self.colr = 6
        self.bullets = []
        self.img= loadImage(path+'/Sprites/sol_1.png')
        self.f=0
        self.dir = RIGHT
        self.F=4
        self.w=55
        self.h= 25
        self.moved = False
        self.shoots = audioplayer.loadFile(path + "/Sounds/Playergunshot.mp3")#load a soundfile
        
    def move(self): #method for player movement
        if self.right == True and self.x+self.w <RES_X:
            self.x += 8
            self.moved = True
            self.dir = RIGHT
        elif self.left == True and self.x >0:
            self.x -=8
            self.moved = True
            self.dir = LEFT
        elif self.up == True and self.y >0:
            self.y -=8
            self.moved = True
        elif self.down == True and self.y +self.h <RES_Y:
            self.y +=8
            self.moved = True
        
    
    def bullet_movement(self): #method to append bullet when mouse is clicked
        if self.clicked == True:
            self.shoots.rewind()
            self.shoots.play() #method that plays the sound
            self.bullets.append(Bullet_player(self.x,self.y,self.colr,mouseX,mouseY)) #append bullet
            self.clicked = False
        if len(self.bullets)!=0:
            for n in self.bullets:
                if 0<=n.x<=RES_X-(n.r*2) and 0<=n.y<=RES_Y-(n.r*2):
                    n.display() # display bullet
                else:
                    self.bullets.remove(n) #remove bullet if out of the game screen
        
    
    def display(self): #method to display player
        self.move()
        self.bullet_movement()
        if self.moved == True:
            self.f=(self.f+0.5)%self.F
            self.moved = False
        if self.dir == RIGHT :
            image(self.img,self.x,self.y,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif self.dir == LEFT :
            image(self.img,self.x,self.y,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)

    
class Enemies(Characters):
    def __init__(self, x, y, xplayer, yplayer):
        Characters.__init__(self, x, y)
        self.vx= randint(1,5)
        self.vy= randint(1,5)
        self.colr=0 #red color
        self.img= loadImage(path+'/Sprites/sol_2.png')
        self.f= 0
        self.F=4
        self.w=44
        self.h= 20
        self.bullets=[]
        
        self.xpl=xplayer
        self.ypl=yplayer
        
        self.shoot()
        #no sounds for enemies because it becomes very noisy
    
    def shoot(self): #appending bullets
        self.bullets.append(Bullet_enemy(self.x, self.y, self.colr, self.xpl, self.ypl))
        
    def update_vx(self): #updating vx value 
        if (self.x) >= (RES_X-self.w):
            self.vx = -self.vx
        elif self.x <= 0:
            if self.vx < 0:
                self.vx *= -1
        self.vx = self.vx
    
            
    def update_vy(self): #updating vy value
        if (self.y) >= (RES_Y-self.h):
            self.vy = -self.vy
        elif self.y <= 0:
            if self.vy < 0:
                self.vy *= -1
        self.vy = self.vy
        
        
    def update(self): # updating self.x and self.y values
        self.update_vx()
        self.update_vy()
        self.x += self.vx
        self.y += self.vy  #ynext = y + N*dy  N=frames
    
    def update_xypl(self):
        self.xpl = game.xpl
        self.ypl = game.ypl
        
    def display(self): #method to display the object
        self.update()
        if (self.vx==0):
            if (self.y % randint(26,28))== 0: #modulus so enemy shoots in a non predictable way
                self.shoot()
        elif (self.x % randint(26,28))== 0: #Enemies will  shoot at player based on x coord
            self.shoot()
            
        self.f=(self.f+0.5)%self.F
        if game.player.x >= self.x:
            image(self.img,self.x,self.y,self.w,self.h,int(self.f)*self.w,0,int(self.f+1)*self.w,self.h)
        elif game.player.x < self.x:
            image(self.img,self.x,self.y,self.w,self.h,int(self.f+1)*self.w,0,int(self.f)*self.w,self.h)
        
        
        for b in self.bullets:
            if 0<=b.x<=RES_X-(b.r*2) and 0<=b.y<=RES_Y-(b.r*2):
                b.display() # display bullet
            else:
                self.bullets.remove(b) #remove bullet from list if out of game screen



class Bullet_enemy():
    def __init__(self, x, y, colr, xpl, ypl):
        self.x=x
        self.y=y
        self.tx=(xpl+block_size/2)-x # xcomponent of target vector, xpl is players(target) x pos
        self.ty=(ypl+block_size/2)-y #blocksize/2 so enemies aim the center of player, not corner
        self.colr=colr
        self.r=2
        
        self.v= 10 #speed of bullet
        self.vx=self.v*(self.tx/(((self.tx**2)+(self.ty**2))**0.5)) # v*normalized vector
        self.vy=self.v*(self.ty/(((self.tx**2)+(self.ty**2))**0.5))
        
    def update(self): #updating self.x and self.y values
        self.x += self.vx
        self.y += self.vy  #ynext = y + N*dy  N=frames
        
    def display(self): #method to display bullet
        self.update()
        fill (color_list[self.colr])
        rect(self.x, self.y, self.r*2, self.r*2)
    
class Bullet_player():
    def __init__(self, x, y, colr, mouseX, mouseY):
        self.x=x+(game.player.w - 10)
        self.y=y+(game.player.h -15)
        if game.player.dir == LEFT:
            self.x = x
            self.y = y+(game.player.h -15)
        self.tx = (mouseX+block_size/2)-x  # blocksize/2 so that player aims at center
        self.ty = (mouseY+block_size/2)-y
        self.colr=colr
        self.r=2
    
        self.v= 10 #speed of bullet
        self.vx=self.v*(self.tx/(((self.tx**2)+(self.ty**2))**0.5)) # v*normalized vector
        self.vy = self.v*(self.ty/(((self.tx**2)+(self.ty**2))**0.5))
        
    def update(self): #updating self.x and self.y values
        self.x += self.vx
        self.y += self.vy  #ynext = y + N*dy  N=frames
        
    def display(self): # method to display bullet
        self.update()
        fill (color_list[self.colr])
        rect(self.x, self.y, self.r*2, self.r*2)
    
 
class Game(list):
    def __init__(self, w, h, speed, score,startpage,highscore):
        self.w = w
        self.h = h
        self.speed=speed
        self.score=score
        self.highscore = highscore
        self.player = Player(10,100)
        self.xpl=self.player.x
        self.ypl=self.player.y
        self.game_over=False
        self.win=False
        self.bg = loadImage(path+"/Sprites/tiles.png")
        self.startimage = loadImage(path+"/Sprites/Super_Hot_Icon.png")
        self.startpage = startpage

        self.enemies=[]
    
        self.level=1
        self.level_enemies=[0,1,2,4,7] #level/index 1 has 1 enemy, level 4 has 7 enemies
        for e in range(self.level_enemies[self.level]):
            self.enemies.append(Enemies(randint(60,RES_X-100),randint(60,RES_Y-100), self.xpl, self.ypl))
            
    def start_menu(self): #displays start menu
        if self.startpage == True:
            m_cord_x = mouseX
            m_cord_y = mouseY
            image(self.startimage,0,0,RES_X, RES_Y)
            fill(color_list[6])
            noStroke()
            rect(((RES_X//2)-265), ((RES_Y//2)+100), 200 , 50)
            noStroke()
            rect(((RES_X//2)+100), ((RES_Y//2)+100), 200 , 50)
            textSize(20)
            text("High Score:"+str(self.highscore), RES_X-140, 20)
            textSize(150)
            text("2D",((RES_X//2)-100), ((RES_Y//2)+70))
            textSize(25)
            text("KILL ALL ENEMIES TO MOVE TO THE NEXT LEVEL", ((RES_X//2)-280), ((RES_Y//2)+200))
            text("DO NOT GET HIT BY A BULLET", ((RES_X//2)-180), ((RES_Y//2)+250))
            fill(color_list[5])
            textSize(40)
            text("PLAY", ((RES_X//2)-210), ((RES_Y//2)+140))
            text("QUIT", ((RES_X//2)+155), ((RES_Y//2)+140))
            if ((RES_X//2)-265 <=m_cord_x <= ((RES_X//2)-265)+200) and ((RES_Y//2)+100 <=m_cord_y <= ((RES_Y//2)+100)+50):
                stroke(255)
                noFill()
                rect(((RES_X//2)-265), ((RES_Y//2)+100), 200 , 50)
                if mousePressed:
                    self.startpage = False  #starts game from level 1
            elif ((RES_X//2)+100 <=m_cord_x <= ((RES_X//2)+100)+200) and ((RES_Y//2)+100 <=m_cord_y <= ((RES_Y//2)+100)+50):
                stroke(255)
                noFill()
                rect(((RES_X//2)+100), ((RES_Y//2)+100), 200 , 50)
                if mousePressed:
                    exit() #exits processing
        
            
    def display(self): #displays game
        image(self.bg,0,0,RES_X, RES_Y)
        if self.game_over==True and self.win==False: #game over and final score
            noStroke() #no borders in figures
            textSize(25)
            randcolor=randint(0,6)
            fill (color_list[randcolor])
            text("GAME OVER", (RES_X//2-70), (RES_Y//2-30))
            text("Final Score:"+str(self.score), (RES_X//2-75), (RES_Y//2+10))

            
        elif self.game_over==True and self.win==True:
            noStroke() #no borders in figures
            textSize(25)
            randcolor=randint(0,6)
            fill (color_list[randcolor])
            text("YOU WON!", (RES_X//2-60), (RES_Y//2-50))
            text("Final Score:"+str(self.score), (RES_X//2-75), (RES_Y//2))
            text("Thanks for Playing!", (RES_X//2-115), (RES_Y//2+50))
            
    
        else:
            noStroke()
            textSize(20)
            fill(0)
            text("Score:"+str(self.score), RES_X-90, 20)
            text("Level "+str(self.level), (RES_X//2)-50, 20)
    
            self.player.display()
            self.update_xypl()
    
            for e in self.enemies:
                e.display() #e is every instantiated enemy
                e.update_xypl()
                for b in self.player.bullets: #condition so player bullets kill enemies
                    if (e.x-e.r) <= b.x <= (e.x+2*e.r) and (e.y-e.r) <= b.y <= (e.y+2*e.r):
                        self.enemies.remove(e)
                        self.player.bullets.remove(b)
                        self.score += 1
                        self.next_lvl()
                
    
                for b in e.bullets: #condition so enemies' bullets kill player
                    if (self.player.x) <= b.x <= (self.player.x+2*self.player.r) and (self.player.y) <= b.y <= (self.player.y+2*self.player.r):
                        self.game_over=True
    
                
    def next_lvl(self): #moving to the next level
        if len(self.enemies) == 0:
            if self.level != len(self.level_enemies)-1: #so no index out of range error
                self.level += 1
                for e in range(self.level_enemies[self.level]):
                    self.enemies.append(Enemies(randint(60,RES_X-50),randint(60,RES_Y-50), self.xpl, self.ypl))
            if self.level==len(self.level_enemies)-1 and len(self.enemies) == 0:
                self.game_over=True
                self.win=True

    
    
    def update_xypl(self): 
        self.xpl=self.player.x
        self.ypl=self.player.y
    
    def change_speed(self): #resetting speed
        self.speed=6
    def reset_speed(self): #resetting speed
        self.speed=0.1

    

game = Game(RES_X, RES_Y, 0.01, 0,True,0) #width, height, speed, score

def setup():
    size(RES_X, RES_Y)


def draw():
    if frameCount%(max(1, int(8-game.speed)))==0 or frameCount==1: #slow game by not displaying every frame
        background(210)
        game.start_menu() #displays start menu
        if game.startpage == False:
            game.display()  #class method to display game
    
    
def keyPressed():
    if keyCode == LEFT or key == 'a':
        game.player.left = True
    elif keyCode == RIGHT or key == 'd':
        game.player.right = True
    elif keyCode == UP or key == 'w':
        game.player.up = True
    elif keyCode == DOWN or key == 's':
        game.player.down = True
    game.change_speed()
    
    
def keyReleased():
    if keyCode == LEFT or key == 'a':
        game.player.left = False
    elif keyCode == RIGHT or key == 'd':
        game.player.right = False  
    elif keyCode == UP or key == 'w':
        game.player.up = False
    elif keyCode == DOWN or key == 's':
        game.player.down = False
    game.reset_speed()
      
def mousePressed():
    global game
    if game.startpage ==False:
        game.player.clicked = True

    if game.game_over == True:
        if game.highscore <= game.score:
            game.highscore = game.score
        game = Game(RES_X, RES_Y, 0.1, 0,True,game.highscore)
        
