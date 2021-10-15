from SpriteTransformation import*
from LoadGraphics import*

class Basic():
    def __init__(self,x,y,size,graphic,speed=1,turnspeed=5):
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

    def GamePosition(self):
        #Considering the displacement caused by rotation:
        xdifference=abs(round((Rotate(self.visual,self.direction).get_width()-self.visual.get_width())/2))
        ydifference=abs(round((Rotate(self.visual,self.direction).get_height()-self.visual.get_height())/2))

        #Returning the center point of the visual sprite:
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