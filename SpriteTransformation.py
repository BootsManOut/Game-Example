import pygame

def Scale(image,amount):
    width=round(image.get_width()*amount)
    height=round(image.get_height()*amount)
    return pygame.transform.scale(image,(width,height))

def Rotate(image,amount):
    return pygame.transform.rotate(image,amount)

def Transform(image,scale_amount=1,angle=0):
    return Scale(Rotate(image,angle),scale_amount)