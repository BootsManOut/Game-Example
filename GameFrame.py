

#(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)
#IMPORTS    and    SETUP:
#(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)



import pygame
from pygame import *
import sys
import math as m
from  math import *
import random

#Created Modules:
from KeyboardInput import*
#Variable to avoid space press overload:
StopSpace=False
from LoadGraphics import*
from SpriteTransformation import*
from Reformatting import*
from BasicObjectClass import*
from Timers import*
from AnimationClass import*
from Sprites import*


#Setup the Screen:
EditScreen=pygame.display
Draw=pygame.draw
screen=pygame.display.set_mode((1200,720))
#background image:
back=LoadImage("back")
# display back:
screen.blit(back, (0, 0))

#Set Up Game FPS Clock:
clock=pygame.time.Clock()




#(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)
#CLASSES:
#(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)



#Main Player:
#**************************************************
class Player():
    def __init__(self,x,y,size,graphic,speed=5,turnspeed=3):
        #Player Location:
        self.x=x
        self.y=y
        self.size=size
        #Movement Speed:
        self.speed=speed
        #Turning Speed:
        self.turnspeed=turnspeed
        #Current angle/direction:
        self.direction=0
        #Visual:
        self.visual=Scale(LoadImage(graphic),size)
        self.turning="no"
        self.moving="no"
        self.shift=False

    def GamePosition(self):
        #Considering the displacement caused by rotation:
        xdifference=abs(round((Rotate(self.visual,self.direction).get_width()-self.visual.get_width())/2))
        ydifference=abs(round((Rotate(self.visual,self.direction).get_height()-self.visual.get_height())/2))

        #Returning the center point of the player visual:
        return(self.x-round(self.visual.get_width()/2)-xdifference,self.y-round(self.visual.get_height()/2)-ydifference)

    def GameX(self):
        return self.GamePosition()[0]
    def GameY(self):
        return self.GamePosition()[1]

    def right(self):
        return self.x+(2*self.size)
    def left(self):
        return self.x-self.size
    def up(self):
        return self.y
    def down(self):
        return self.y+round(self.size/2)
    def center(self):
        return (self.x+round(self.size/2),self.y+round(self.size/2))

#Player's fire exhaust class:
#**************************************************
class FireExhaust(Basic):
    def __init__(self,parent,x,y,size,graphic,speed=1,turnspeed=2):
        super().__init__(x,y,size,graphic,speed=1,turnspeed=2)
        self.parent=parent
        self.animation=Animation("fire exhaust",0,0,0.27,60)
    def Move(self):
        self.x=self.parent.x
        self.y=self.parent.y
        self.animation.x=self.x
        self.animation.y=self.y
        self.animation.direction=self.parent.direction
    def GamePosition(self):
        #Considering the displacement caused by rotation:
        xdifference = abs(round((Rotate(self.visual, self.parent.direction).get_width() - self.visual.get_width()) / 2))
        ydifference = abs(round((Rotate(self.visual, self.parent.direction).get_height() - self.visual.get_height()) / 2))

        # Returning the center point of the fire visual:
        return (self.x - round(self.visual.get_width() / 2) - xdifference,self.y - round(self.visual.get_height() / 2) - ydifference)

#Enemy class:
#**************************************************
class FlashFighter(Basic):
    def __init__(self,x,y,size,graphic,speed=1,turnspeed=2):
        super().__init__(x,y,size,graphic="enemy",speed=2,turnspeed=3)
        self.rotating=False
        self.aimDirection=0
        self.heartbeat=Timer(1)
        #Variable to make the spaceship shoot only once after each rotation:
        self.OncePerRotation=False
        #Timer to make the spaceship shoot in 2 seconds intervals even without rotating:
        self.shoottimer=Timer(0)
    def move(self):
        enemy1.direction%=360
        self.x += (cos(radians(self.direction+90))*self.speed)#*speedFactor
        self.y -= (sin(radians(self.direction+90))*self.speed)#*speedFactor
        border1=self.aimDirection-abs(self.turnspeed)
        border1%=360
        border2=self.aimDirection+abs(self.turnspeed)
        border2%=360

        if self.rotating:
            self.direction+=self.turnspeed
        if self.rotating and self.direction>=border1 and self.direction<=border2:
            self.rotating=False


    #ENEMIE'S    LIFE    CYCLE    AND    BEHAVIOR:
    # **************************************************

    def lifecycle(self):
        if not self.rotating and not self.OncePerRotation:
            self.OncePerRotation=True
            #Also create a timer that the enemy can shoot after 2 seconds, even if he didn't rotate at all:
            self.shoottimer.Start(2)
            #Create the explosion animation when shooting:
            gunblastflash.GamePos(self.x,self.y)
            animationlist.append(gunblastflash.Copy(gunblastflash.GetGamePos()[0],gunblastflash.GetGamePos()[1],self.direction))
            #add the animated bullet:
            flashbullet = Bullet(self.x,self.y, 0.287,self.direction, 15, "bulletflash","bullet flash gun")
            bulletlist.append(flashbullet)
        #make shooting possible again after 2 seconds of not shooting and while not rotating:
        if not self.rotating and self.shoottimer.IsExpired():
            self.OncePerRotation=False
        #turn towards the player:
        if self.heartbeat.IsExpired():
            self.TurnToObject(player)
            self.heartbeat.Start(1)


    def TurnTo(self,direction):
        directionFormat=direction
        directionFormat%=360
        self.aimDirection=directionFormat
        self.rotating=True
        #set all angles for calculation:
        #aim direction:
        aim=directionFormat
        #second check angle:
        check=aim-180
        check%=360

        #calculate in which direction to turn to reach aimed direction the fastest:
        if abs(aim-self.direction)>self.turnspeed:
            #aim<180
            if aim<180 and self.direction<check and not self.direction < aim:
                self.turnspeed = -abs(self.turnspeed)
            elif aim<180 and (self.direction>check or self.direction<aim):
                self.turnspeed = abs(self.turnspeed)
            #aim>180
            if aim>180 and self.direction<aim and not self.direction < check:
                self.turnspeed = abs(self.turnspeed)
            elif aim>180 and (self.direction>aim or self.direction < check):
                self.turnspeed = -abs(self.turnspeed)
            #aim==180:
            if aim==180:
                if self.direction<aim:
                    self.turnspeed = abs(self.turnspeed)
                else:
                    self.turnspeed = -abs(self.turnspeed)
        else:
            self.direction=aim

    def TurnToObject(self,object):
        #Calculate where the object is presumably going to be in the future, in about 2 seconds (or 40 game loops to be exact):
        y=object.y
        x=object.x
        tempdirection=object.direction
        speedfactor=1
        if object.shift:
            speedfactor=2
        for i in range(40):
            if not object.turning=="no":
                if object.turning=="right":
                    tempdirection-= (object.turnspeed) * speedfactor
                if object.turning=="left":
                    tempdirection+= (object.turnspeed) * speedfactor

            if object.moving=="up":
                x += (cos(radians(tempdirection + 90)) * object.speed) * speedfactor
                y -= (sin(radians(tempdirection + 90)) * object.speed) * speedfactor
            elif object.moving=="down":
                x += (cos(radians(tempdirection + 90 + 180)) * object.speed) * speedfactor
                y -= (sin(radians(tempdirection + 90 + 180)) * object.speed) * speedfactor

        #calculate adjacent and opposing cathetes:
        adj=y-self.y
        opp=x-self.x
        #calculate the angle:
        angle = m.degrees(m.atan2(opp, adj)) -180
        angle %= 360
        self.TurnTo(angle)



#Bullet class:
#**************************************************
class Bullet():
    def __init__(self,x,y,size,direction,speed,visual,animation=None):
        self.x=x
        self.y=y
        self.size=size
        self.direction=direction
        self.speed=speed
        self.visual=Scale(LoadImage(visual),self.size)
        self.animated=False
        self.animation=None
        if not animation==None:
            self.animation=Animation(animation,x,y,FPS=60)
            self.animated=True


    def update(self):
        self.x += (cos(radians(self.direction+90))*self.speed)#*speedFactor
        self.y -= (sin(radians(self.direction+90))*self.speed)#*speedFactor

        #update the animation position:
        if self.animated:
            self.animation.AnimateRepeat(self.x,self.y,False,False,FPS=300)
    def GamePosition(self):
        #Considering the displacement caused by rotation:
        xdifference=abs(round((Rotate(self.visual,self.direction).get_width()-self.visual.get_width())/2))
        ydifference=abs(round((Rotate(self.visual,self.direction).get_height()-self.visual.get_height())/2))
        #Returning the center point of the bullet visual:
        return(self.x-round(self.visual.get_width()/2)-xdifference,self.y-round(self.visual.get_height()/2)-ydifference)
    def GameX(self):
        return self.GamePosition()[0]
    def GameY(self):
        return self.GamePosition()[1]

    def setGamePos(self,x,y):
        self.x=x-round(self.visual.get_width()/2)
        self.y=y-round(self.visual.get_height() / 2)




#(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)
#INSTANCES,    LISTS    AND    ANIMATIONS:
#(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)



#create player:
player=Player(640,360,0.2,"spaceship")
#create player fire blast:
fire=FireExhaust(player,player.x,player.y,0.3,"fire")
#Create 1 enemy:
enemy1=FlashFighter(200,300,0.2,"enemy")
enemy1.direction=-90

#import animations:
gunblastflash=Animation("gun blast flash",0,0,0.4,60,False,False)
bulletflashgun=Animation("bullet flash gun",0,0,60)

#Create bullets inside the bullet list (you simply create as many bullets as you wish inside the list spontaneously):
bulletlist=[]
#Create simple animations inside animation list (you simply create as many animations as you wish inside the list spontaneously):
animationlist=[]

#(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)
#CONSTANT    REPEAT    GAME    LOOP    (WILL    RUN    EVEN    DURING    BLOCKED    ACTION):
#(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)

def ConstantLoop():

    #Update and handle bullets:
    for bullet in bulletlist:
        if bullet.x<-100 or bullet.x>1380 or bullet.y < -100 or bullet.y> 820:
            bulletlist.remove(bullet)
        else:
            bullet.update()
            if not bullet.animated:
                AddSprite(Rotate(bullet.visual, bullet.direction),bullet.GamePosition(),screen)
            else:
                AddSprite(Transform(bullet.animation.CurrentFrame(), bullet.size, bullet.direction),bullet.GamePosition(),screen)

    #update and draw fire exhaust when moving:
    fire.Move()
    if player.moving=="up" and not fire.animation in animationlist:
        fire.animation.AnimateRepeat(fire.animation.x, fire.animation.y, False, False, FPS=60)
        AddSprite(fire.animation.CurrentFrame(), (fire.animation.CenterX(fire.animation.x), fire.animation.CenterY(fire.animation.y)), screen)

    #Draw the player:
    AddSprite(Rotate(player.visual,player.direction),player.GamePosition(),screen)
    #screen.blit(Rotate(player.visual,player.direction),player.GamePosition())
    #move enemy:
    enemy1.move()
    #enemy life cycle:
    enemy1.lifecycle()
    AddSprite(Rotate(enemy1.visual,enemy1.direction),enemy1.GamePosition(),screen)
    #screen.blit(Rotate(enemy1.visual,enemy1.direction),enemy1.GamePosition())


    #Play auto animations:
    if len(animationlist)>0:
        for animation in animationlist:
            if not animation.finished:
                animation.Animate(animation.x, animation.y,False,False,FPS=60)
                AddSprite(animation.CurrentFrame(),(animation.CenterX(animation.x),animation.CenterY(animation.y)),screen)
            else:
                animation.finished=False
                animationlist.remove(animation)

    #Update the screen:
    EditScreen.update()

    #Keyboard Input:
    speedFactor=1
    if IsPressed(ShiftR)or IsPressed(ShiftL):
        speedFactor=2
        player.shift=True
    else:
        player.shift=False
    if IsPressed(Right):
        player.direction -= (player.turnspeed)*speedFactor
        player.turning="right"
    if IsPressed(Left):
        player.direction += (player.turnspeed)*speedFactor
        player.turning="left"
    elif not IsPressed(Right):
        player.turning="no"
    if IsPressed(Up):
        player.x += (cos(radians(player.direction+90))*player.speed)*speedFactor
        player.y -= (sin(radians(player.direction+90))*player.speed)*speedFactor
        player.moving="up"
    if IsPressed(Down):
        player.x += ((cos(radians(player.direction+90+180)))*player.speed)*speedFactor
        player.y -= ((sin(radians(player.direction+90+180)))*player.speed)*speedFactor
        player.moving="down"
    elif not IsPressed(Up):
        player.moving="no"
    global StopSpace
    if IsPressed(Space) and not StopSpace:
        StopSpace=True
        bullet=Bullet(player.x+Path(50,player.direction)[0],player.y-Path(50,player.direction)[1],0.1,player.direction,20,"bullet")
        bulletlist.append(bullet)
    if not IsPressed(Space):
        StopSpace=False

    #Draw all sprites within sprite class:
    DrawSprites(screen,back)

    #Set Frame rate:
    clock.tick(30)

    # Quit when pushing the Close Button:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()



#(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)
#ACTIVE    BLOCKABLE    GAME    LOOP:
#(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)(*)


def BlockedLoop():
    pass