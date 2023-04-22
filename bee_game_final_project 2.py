from cmu_graphics import *
from PIL import Image
import random, time
import math,copy

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
    # def pollinatedState(self,app):
    #     #for flower in Flower.flowerList:
    #         if self.isClose(app.player) and\
    #             self not in self.gathered:
    #             Flower.gathered.append(self)
    #             return True
    def flowerOnStep(self):
        self.y-=self.up
        self.x+=self.c*math.sin(0.005*self.y)

class helperBee: 
    def __init__(self,x,y): 
        myGif = Image.open('beeSprite.gif')
        self.spriteList = []
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            fr = myGif.resize((myGif.size[0]//8, myGif.size[1]//8))
            fr = fr.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            self.spriteList.append(fr)

        ##Fix for broken transparency on frame 0
        self.spriteList.pop(0)
        #Set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0
        self.x=x
        self.y=y
        self.distancedic=dict()
    def drawPlayer(self):
        #Draw current kirb sprite
        drawImage(self.spriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
    def doStep(self):
        self.stepCounter += 1
        if self.stepCounter >= 10: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteList)
            self.stepCounter = 0

    def playerOnStep(self,app):
        if app.targetX!=None and app.targetY!=None:
            self.dx=app.targetX-self.x
            self.dy=app.targetY-self.y
            self.x+=self.dx/25
            self.y+=self.dy/25
        
    def findTarget(self,app):
        minDistance=800
        closetPollen=None
        for pollen in Pollinator.pollinatorList:
            d=((self.x-self.y)**2+(pollen.x-pollen.y)**2)**(1/2)
            self.distancedic[d]=pollen
        for distance in self.distancedic: 
            if distance<minDistance:
                mindistance=distance
                closetPollen=self.distancedic[distance]
        if closetPollen!=None:
            app.targetX=closetPollen.x
            app.targetY=closetPollen.y


def onAppStart(app):
    app.stepsPerSecond=25
    app.stepTimeCounter=0
    app.width=800
    app.height=800
    app.cursorX=200
    app.cursorY=200
    app.numOfPollen=0
    app.pollen=[]
    app.player=helperBee(200,200)
    app.targetX=None
    app.targetY=None

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

# def onMouseMove(app,mouseX,mouseY):
#     app.cursorX=mouseX
#     app.cursorY=mouseY 
                
def onStep(app):
    app.stepTimeCounter+=1
    app.player.playerOnStep(app)
    if app.stepTimeCounter%50==0:
        Flower(random.randrange(800),800,50,50,"blue")
        Pollinator(random.randrange(800),800,"pink")
    # for pollinator in Pollinator.pollinatorList:
    #     if pollinator.gatheredState(app):
    #         app.numOfPollen+=1
    #         numOfPollen=app.numOfPollen
    #         app.pollen.append((25+20*numOfPollen,25,\
    #                            pollinator.color))
    # colorList=[]
    # for pollen in app.pollen: 
    #     colorList.append(pollen[2])
    # for flower in Flower.flowerList: 
    #     if flower.pollinatedState(app):
    #         if app.pollen!=[]:
    #             if flower.color in colorList:
    #                 app.pollen.pop((colorList.index(flower.color)))
    #                 flower.width+=20
    #                 flower.height+=20
    #                 app.numOfPollen-=1
                
    for pollinator in Pollinator.pollinatorList:
        pollinator.pollinatorOnStep()
    for flower in Flower.flowerList: 
        flower.flowerOnStep()
    app.player.findTarget(app)

def distance(x1,y1,x2,y2): 
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

def main():
    runApp()

main()