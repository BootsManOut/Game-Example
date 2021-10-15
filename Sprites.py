import pygame

AllSprites = pygame.sprite.Group()

def AddSprite(image,pos,screen):
    sprite = pygame.sprite.Sprite()
    sprite.image = image
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = pos[0]
    sprite.rect.y = pos[1]
    AllSprites.add(sprite)

def DrawSprites(screen,back):
    AllSprites.clear(screen,back)
    AllSprites.draw(screen)
    AllSprites.remove(AllSprites.sprites())