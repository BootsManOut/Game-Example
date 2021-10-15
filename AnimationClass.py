import os
import pygame
from Timers import*
from SpriteTransformation import*

ANIMATIONPATH="Graphics/Animation/"

def LoadFolder(folder, Flipped=False, Backwards=False):
    animationlist=[]
    path=ANIMATIONPATH+folder
    for path, dirs, files in os.walk(path):
        for f in files:
            filename = os.path.join(path, f)
            if filename[-4:]==".png":
                img = pygame.image.load("{}".format(filename))
                if Flipped:
                    animationlist.append(flip(img,True))
                else:
                    animationlist.append(img)
    if Backwards:
        animationlist.reverse()
    return animationlist

#Set global animation path when loading animations:
def SetAnimationPath(path):
    global ANIMATIONPATH
    ANIMATIONPATH=path

#flip all images in a list (flip the entire animation list):
def flip(OriginalList):
    NEWlist=OriginalList.copy()
    for img in NEWlist:
        if type(img)==pygame.Surface:
            NEWimg=pygame.transform.flip(img, True,False)
            NEWlist.insert(NEWlist.index(img),NEWimg)
            NEWlist.remove(img)
    return NEWlist

class Animation():
    def __init__(self,folder, x=0, y=0, size=1, FPS=10, flipped=False,backwards=False):
        self.name=folder.replace(" ","")
        self.folder=folder
        self.framelist=LoadFolder(folder,flipped,backwards)
        self.animation=self.framelist
        self.backwardslist=self.framelist.copy()
        self.backwardslist.reverse()
        self.flippedlist=flip(self.framelist)
        self.flipped=False
        self.backwards=False
        self.FPS=FPS
        self.delay=1/self.FPS
        self.FPStimer=Timer(0)
        self.currentFrameID=0
        self.x=x
        self.y=y
        self.Position=(x,y)
        #Define weather the animation is finished (when you animate it only once):
        self.animating=False
        self.finished=False
        self.size=size
        self.direction=0

    def Animate(self,x,y, Flipped=False,Backwards=False,FPS=None):
        self.x=x
        self.y=y
        self.Position=(x,y)
        self.flipped=Flipped
        self.backwards=Backwards
        if FPS==None:
            FPS=self.FPS
        self.delay = 1 / FPS
        if self.animating==False and self.finished==False:
            self.animating=True
            self.FPStimer.Start(self.delay)
        if self.FPStimer.IsExpired():
            if self.currentFrameID<len(self.framelist)-1:
                self.currentFrameID+=1
                self.FPStimer.Start(self.delay)
            else:
                self.currentFrameID=0
                self.animating=False
                self.finished=True
    def AnimateRepeat(self,x,y,Flipped=False,Backwards=False,FPS=None):
        self.x=x
        self.y=y
        self.Position=(x,y)
        self.flipped=Flipped
        self.backwards=Backwards
        if FPS==None:
            FPS=self.FPS
        self.delay = 1 / FPS
        if self.animating==False and self.finished==False:
            self.animating=True
            self.FPStimer.Start(self.delay)
        if self.FPStimer.IsExpired():
            if self.currentFrameID<len(self.framelist)-1:
                self.currentFrameID+=1
                self.FPStimer.Start(self.delay)
            else:
                self.currentFrameID=0
                self.FPStimer.Start(self.delay)
    def CurrentFrame(self):
        if self.flipped:
            if self.backwards:
                endFrame= self.flippedlist.reverse()[self.currentFrameID]
            else:
                endFrame= self.flippedlist[self.currentFrameID]
        else:
            if self.backwards:
                endFrame= self.framelist.reverse()[self.currentFrameID]
            else:
                endFrame= self.framelist[self.currentFrameID]
        if not self.direction==0:
            endFrame=Rotate(endFrame,self.direction)
        if not self.size==1:
            endFrame = Scale(endFrame,self.size)
        return endFrame
    #Create a copy of the animation, to save lag from creating a completely new animation:
    def Copy(self,x=None,y=None,direction=0,size=None):
        if x==None:
            x=self.x
        if y==None:
            y=self.y
        if size==None:
            size=self.size
        animationCopy=AnimationCopy(self.folder,self.framelist,self.backwardslist,self.flippedlist,x,y,size,direction,self.FPS)
        return animationCopy
    #Set position of the animation:
    def pos(self,x,y):
        self.x=x
        self.y=y
        self.Position=(x,y)
    #Get the center position from the animation:
    def GetGamePos(self):
        #Considering the displacement caused by rotation:
        xdifference=abs(round((Rotate(self.CurrentFrame(),self.direction).get_width()-self.CurrentFrame().get_width())/2))
        ydifference=abs(round((Rotate(self.CurrentFrame(),self.direction).get_height()-self.CurrentFrame().get_height())/2))
        #Returning the center point of the player CurrentFrame():
        return(self.x+round(self.CurrentFrame().get_width()/2)+xdifference,self.y+round(self.CurrentFrame().get_height()/2)+ydifference)
    #Set the center position of the animation:
    def GamePos(self,x,y):
        xdifference = abs(round((Rotate(self.CurrentFrame(), self.direction).get_width() - self.CurrentFrame().get_width()) / 2))
        ydifference = abs(round((Rotate(self.CurrentFrame(), self.direction).get_height() - self.CurrentFrame().get_height()) / 2))
        self.x=x-round(self.CurrentFrame().get_width()/2) - xdifference
        self.y=y-round(self.CurrentFrame().get_height() / 2) - ydifference
        self.Position=(x,y)
    def CenterX(self,x):
        return x-round(self.CurrentFrame().get_width()/2)
    def CenterY(self,y):
        return y-round(self.CurrentFrame().get_height() / 2)





#For creating an animation copy without causing any lagging time:
class AnimationCopy():
    def __init__(self,folder, framelist,backwardslist,flippedlist, x=0, y=0, size=1, direction=0,FPS=10):
        self.name=folder.replace(" ","")
        self.folder=folder
        self.framelist=framelist.copy()
        self.animation=self.framelist
        self.backwardslist=backwardslist.copy()
        self.flippedlist=flippedlist
        self.flipped=False
        self.backwards=False
        self.FPS=FPS
        self.delay=1/self.FPS
        self.FPStimer=Timer(0)
        self.currentFrameID=0
        self.x=x
        self.y=y
        self.Position=(x,y)
        #Define weather the animation is finished (when you animate it only once):
        self.animating=False
        self.finished=False
        self.size=size
        self.direction=direction

    def Animate(self,x,y,Flipped=False,Backwards=False,FPS=None):
        self.x=x
        self.y=y
        self.Position=(x,y)
        self.flipped=Flipped
        self.backwards=Backwards
        if FPS==None:
            FPS=self.FPS
        self.delay = 1 / FPS
        if self.animating==False and self.finished==False:
            self.animating=True
            self.FPStimer.Start(self.delay)
        if self.FPStimer.IsExpired():
            if self.currentFrameID<len(self.framelist)-1:
                self.currentFrameID+=1
                self.FPStimer.Start(self.delay)
            else:
                self.currentFrameID=0
                self.animating=False
                self.finished=True
    def AnimateRepeat(self,x,y,Flipped=False,Backwards=False,FPS=None):
        self.x=x
        self.y=y
        self.Position=(x,y)
        self.flipped=Flipped
        self.backwards=Backwards
        if FPS==None:
            FPS=self.FPS
        self.delay = 1 / FPS
        if self.animating==False and self.finished==False:
            self.animating=True
            self.FPStimer.Start(self.delay)
        if self.FPStimer.IsExpired():
            if self.currentFrameID<len(self.framelist)-1:
                self.currentFrameID+=1
                self.FPStimer.Start(self.delay)
            else:
                self.currentFrameID=0
    def CurrentFrame(self):
        if self.flipped:
            if self.backwards:
                endFrame= self.flippedlist.reverse()[self.currentFrameID]
            else:
                endFrame= self.flippedlist[self.currentFrameID]
        else:
            if self.backwards:
                endFrame= self.framelist.reverse()[self.currentFrameID]
            else:
                endFrame= self.framelist[self.currentFrameID]
        if not self.direction==0:
            endFrame=Rotate(endFrame,self.direction)
        if not self.size==1:
            endFrame = Scale(endFrame,self.size)
        return endFrame

    #Create a copy of the animation, to save lag from creating a completely new animation:
    def Copy(self,x=None,y=None,direction=0,size=None):
        if x==None:
            x=self.x
        if y==None:
            y=self.y
        if size==None:
            size=self.size
        animationCopy=AnimationCopy(self.folder,self.framelist,self.backwardslist,self.flippedlist,x,y,size,direction,self.FPS)
        return animationCopy
    #Get the center position from the animation:
    def GetGamePos(self):
        #Considering the displacement caused by rotation:
        xdifference=abs(round((Rotate(self.CurrentFrame(),self.direction).get_width()-self.CurrentFrame().get_width())/2))
        ydifference=abs(round((Rotate(self.CurrentFrame(),self.direction).get_height()-self.CurrentFrame().get_height())/2))
        #Returning the center point of the player CurrentFrame():
        return(self.x+round(self.CurrentFrame().get_width()/2)+xdifference,self.y+round(self.CurrentFrame().get_height()/2)+ydifference)
    #Set the center position of the animation:
    def GamePos(self,x,y):
        xdifference = abs(round((Rotate(self.CurrentFrame(), self.direction).get_width() - self.CurrentFrame().get_width()) / 2))
        ydifference = abs(round((Rotate(self.CurrentFrame(), self.direction).get_height() - self.CurrentFrame().get_height()) / 2))
        self.x=x-round(self.CurrentFrame().get_width()/2) - xdifference
        self.y=y-round(self.CurrentFrame().get_height() / 2) - ydifference
        self.Position=(x,y)
    def CenterX(self,x):
        return x-round(self.CurrentFrame().get_width()/2)
    def CenterY(self,y):
        return y-round(self.CurrentFrame().get_height() / 2)


