from math import*

def Path(length,angle):
    x = (cos(radians(angle + 90))) * length
    y = (sin(radians(angle + 90))) * length
    return(x,y)