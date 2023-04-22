from cmu_graphics import *
from PIL import Image
import random, time
import math,copy

class Bee: 
    def __init__(self,x,y): 
        myGif = Image.open('beeSprite.gif')
        self.leftSpriteList = []
        self.rightSpriteList=[]
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            image = myGif.resize((myGif.size[0]//8, myGif.size[1]//8))
            fr = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            right=CMUImage(image)
            #self.spriteList=[fr,right]
            self.leftSpriteList.append(fr)
            self.rightSpriteList.append(right)

        ##Fix for broken transparency on frame 0
        self.rightSpriteList.pop(0)
        self.leftSpriteList.pop(0)
        #Set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0
        self.x=x
        self.y=y
        self.direction="left"

    def drawPlayer(self):
        #Draw current kirb sprite
        if self.direction=="left":
            drawImage(self.leftSpriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
        elif self.direction=="right":
            drawImage(self.rightSpriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
    def doStep(self):
        self.stepCounter += 1
        if self.stepCounter >= 10: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.rightSpriteList)
            self.stepCounter = 0

    def playerOnStep(self,app):
        self.dx=app.cursorX-self.x
        self.dy=app.cursorY-self.y
        self.x+=self.dx/4
        self.y+=self.dy/4
        if self.dx>0: 
            self.direction="left"
        else: 
            self.direction="right"

class Pollinator:
    pollinatorList=[]
    gathered=[]
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.up=random.randrange(7,11)
        self.c=random.randrange(1,4)
        self.color=random.choice(["red","blue","green","purple"])
        self.gathered=False
        self.pollenGathered=0
        Pollinator.pollinatorList.append(self)
    def drawPollinator(self):
        drawCircle(self.x,self.y,15,fill=self.color)
    def isClose(self,other):
        if distance(self.x,self.y,other.x,other.y)<=40:  
            return True
        else: 
            return False
    def gatheredState(self,app):
        #for pollinator in Pollinator.pollinatorList:
            if self.isClose(app.player) and\
                self not in Pollinator.gathered:
                Pollinator.gathered.append(self)
                return True
    def pollinatorOnStep(self):
        self.y-=self.up
        self.x+=self.c*math.sin(0.005*self.y)



class Flower:
    flowerList=[]
    gathered=[]
    def __init__(self,x,y,width,height,color):
        self.x=x
        self.y=y
        self.up=random.randrange(7,11)
        self.width=35
        self.height=35
        self.color=random.choice(["red","blue","green","purple"])
        self.outBound=False
        self.c=random.randrange(1,4)
        Flower.flowerList.append(self)
    def drawFlower(self):
        drawRect(self.x,self.y,self.width,self.height,fill=self.color,\
                 align="center")
    def isClose(self,other):
        if distance(self.x,self.y,other.x,other.y)<=self.width+15 or\
        distance(self.x,self.y,other.x,other.y)<=self.height+15:
            return True
        else: 
            return False
    def pollinatedState(self,app):
        #for flower in Flower.flowerList:
            if self.isClose(app.player) and\
                self not in self.gathered:
                Flower.gathered.append(self)
                return True
    def flowerOnStep(self):
        self.y-=self.up
        self.x+=self.c*math.sin(0.005*self.y)


def onAppStart(app):
    app.stepsPerSecond=25
    app.stepTimeCounter=0
    app.width=800
    app.height=800
    app.cursorX=200
    app.cursorY=200
    app.player=Bee(200,200)
    app.numOfPollen=0
    app.pollen=[]

def redrawAll(app):
    app.player.drawPlayer()
    for flower in Flower.flowerList: 
        flower.drawFlower()
    for pollinator in Pollinator.pollinatorList:
        pollinator.drawPollinator()
    # Draw pollen list
    cx = 25
    for (_,_,color) in app.pollen:
        cy = 25
        drawCircle(cx,cy,10,fill=color)
        drawCircle(app.player.x,app.player.y+35,10,fill=color)
        cx += 20
    # if app.player.direction=="left": 
    #     app.player.leftSpriteList
    # elif app.player.direction=="right":
    #     app.player.rightSpriteList
    #app.player.drawPlayer()

def onMouseMove(app,mouseX,mouseY):
    app.cursorX=mouseX
    app.cursorY=mouseY 
                
def onStep(app):
    app.player.doStep()
    app.stepTimeCounter+=1
    app.player.playerOnStep(app)
    if app.stepTimeCounter%50==0:
        Flower(random.randrange(800),800,50,50,"blue")
        Pollinator(random.randrange(800),800,"pink")
    for pollinator in Pollinator.pollinatorList:
        if pollinator.gatheredState(app):
            app.numOfPollen+=1
            numOfPollen=app.numOfPollen
            app.pollen.append((25+20*numOfPollen,25,\
                               pollinator.color))
    colorList=[]
    for pollen in app.pollen: 
        colorList.append(pollen[2])
    for flower in Flower.flowerList: 
        if flower.pollinatedState(app):
            if app.pollen!=[]:
                if flower.color in colorList:
                    app.pollen.pop((colorList.index(flower.color)))
                    flower.width+=20
                    flower.height+=20
                    app.numOfPollen-=1
                
    for pollinator in Pollinator.pollinatorList:
        pollinator.pollinatorOnStep()
    for flower in Flower.flowerList: 
        flower.flowerOnStep()

def distance(x1,y1,x2,y2): 
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

def main():
    runApp()

main()