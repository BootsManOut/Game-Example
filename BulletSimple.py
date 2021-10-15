import pygame
from LoadGraphics import *

bullet=LoadImage("bullet")

class Bullet():
    def __init__(self,x,y,size):
        self.x=0
        self.y=0
        self.image=Scalebullet
