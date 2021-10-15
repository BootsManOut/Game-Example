import pygame
from pygame import *

#Simplified dictionary:
M=K_m
Right=K_RIGHT
Left=K_LEFT
Down=K_DOWN
Up=K_UP
ShiftR=K_RSHIFT
ShiftL=K_LSHIFT
Space=K_SPACE

def IsPressed(name):
    return pygame.key.get_pressed()[name]



#key[pygame.K_LEFT]