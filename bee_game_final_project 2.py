from cmu_graphics import *
from PIL import Image
import random, time
import math,copy
#import random

class Bee: 
    def __init__(self,x,y): 
        myGif = Image.open('beeSprite.gif')
        self.spriteList = []
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            fr = myGif.resize((myGif.size[0]//10, myGif.size[1]//10))
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
        self.x=app.cursorX
        self.y=app.cursorY

class Pollinator:
    pollinatorList=[]
    gathered=[]
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
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
        for pollinator in Pollinator.pollinatorList:
            if pollinator.isClose(app.player) and\
                pollinator not in Pollinator.gathered:
                Pollinator.gathered.append(pollinator)
                self.gathered=True
                return True
    def pollinatorOnStep(self):
        self.y-=10

class Flower:
    flowerList=[]
    gathered=[]
    def __init__(self,x,y,width,height,color):
        self.x=x
        self.y=y
        self.width=50
        self.height=50
        self.color=color
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
        for flower in Flower.flowerList:
            if flower.isClose(app.player) and\
                flower not in flower.gathered:
                Flower.gathered.append(flower)
                return True
    def flowerOnStep(self):
        self.y-=10

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
    #drawRect(400,400,800,800,fill="cyan",align="center")
    app.player.drawPlayer()
    for flower in Flower.flowerList: 
        flower.drawFlower()
    for pollinator in Pollinator.pollinatorList:
        pollinator.drawPollinator()
    for (cx,cy,color) in app.pollen:
        drawCircle(cx,cy,10,fill=color)

def onMouseMove(app,mouseX,mouseY):
    app.cursorX=mouseX
    app.cursorY=mouseY 
                
def onStep(app):
    app.player.doStep()
    app.stepTimeCounter+=1
    app.player.playerOnStep(app)
    if app.stepTimeCounter%50==0:
        Pollinator(random.randrange(800),800,"pink")
        Flower(random.randrange(800),800,50,50,"blue")
    for pollinator in Pollinator.pollinatorList:
        color=pollinator.color
        print(color)
        if pollinator.gatheredState(app):
            app.numOfPollen+=1
            numOfPollen=app.numOfPollen
            app.pollen.append((25+20*numOfPollen,25,color))
    print(app.pollen)
    for flower in Flower.flowerList: 
        if flower.pollinatedState(app):
            if app.pollen!=[]:
                app.pollen.pop()
                app.numOfPollen-=1
                numOfPollen=app.numOfPollen
    for pollinator in Pollinator.pollinatorList:
        pollinator.pollinatorOnStep()
    for flower in Flower.flowerList: 
        flower.flowerOnStep()

def distance(x1,y1,x2,y2): 
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

def main():
    runApp()

main()