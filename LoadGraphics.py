import pygame

def LoadImage(name,folder="Main"):
    image=pygame.image.load("Graphics/" + folder + "/" + name +".png")
    return image