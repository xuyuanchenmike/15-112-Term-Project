from cmu_graphics import *
from PIL import Image
import random, time
import math,copy
#The Bee image is from https://www.pinterest.com/pin/572731277609446312/
#I opened all Bee images using the code Mike Taylor put on piazza:
#Lecture image / oop demos
class Bee: 
    #From CMU's piazza post by Mike Taylor
    def __init__(self,x,y): 
        myGif = Image.open('beeSprite.gif')
        self.leftSpriteList = []
        self.rightSpriteList=[]
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            image = myGif.resize((myGif.size[0]//8, myGif.size[1]//8))
            #From https://www.pinterest.com/pin/572731277609446312/
            fr = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            right=CMUImage(image)
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
        self.dx=0
        self.dy=0
        Bee.color=None
        self.direction="left"
        self.collected=False

    def drawPlayer(self):
        #From CMU's piazza post by Mike Taylor
        #Draw current kirb sprite
        if self.direction=="left":
            drawImage(self.leftSpriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
        elif self.direction=="right":
            drawImage(self.rightSpriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
    #from Mike taylor's piazza post
    def doStep(self):
        self.stepCounter += 1
        distance=(abs(self.dx)+abs(self.dy))/2
        if self.stepCounter >= 10 and distance<8: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.rightSpriteList)
            self.stepCounter = 0
        elif self.stepCounter >= 1 and distance>8:
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

class HelperBee: 
    #From CMU's piazza post by Mike Taylor
    def __init__(self,x,y): 
        myGif = Image.open('beeSprite.gif')
        #From https://www.pinterest.com/pin/572731277609446312/
        self.leftSpriteList = []
        self.rightSpriteList=[]
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            image = myGif.resize((myGif.size[0]//10, myGif.size[1]//10))
            fr = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            right=CMUImage(image)
            self.leftSpriteList.append(fr)
            self.rightSpriteList.append(right)

        ##Fix for broken transparency on frame 0
        self.leftSpriteList.pop(0)
        #Set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0
        self.x=x
        self.y=y
        self.collected=False
        HelperBee.color=None
        self.distancedic=dict()
        self.direction="left"
    #From CMU's piazza Post by Mike Taylor
    def drawPlayer(self):
        #Draw current kirb sprite
        if self.direction=="left":
            drawImage(self.leftSpriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
        elif self.direction=="right":
            drawImage(self.rightSpriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
    #From CMU's piazza post by Mike Taylor
    def doStep(self):
        self.stepCounter += 1
        if self.stepCounter >= 10: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteList)
            self.stepCounter = 0

    def playerOnStep(self,app):
        if app.targetX!=None and app.targetY!=None:
            self.dx=app.targetX-self.x
            self.dy=app.targetY-self.y
            self.x+=self.dx/28
            self.y+=self.dy/28
            if self.dx>0: 
                self.direction="left"
            else: 
                self.direction="right"
        
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
        if self.isClose(app.player)and\
            self not in Pollinator.gathered:
            Pollinator.gathered.append(self)
            self.gathered=True
            app.player.collected=True
            return True
    def gatheredStateByHelper(self,app):
        if self.isClose(app.helper)and\
            self not in Pollinator.gathered:
            Pollinator.gathered.append(self)
            app.helper.collected=True
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
        if self.isClose(app.player) and\
            self not in self.gathered:
            Flower.gathered.append(self)
            return True
    def pollinatedStateByHelper(self,app):
        if self.isClose(app.helper) and\
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
    #app.helper=[HelperBee(400,200),HelperBee(300,150)]
    app.helper=HelperBee(400,200)
    app.helper2=HelperBee(300,150)
    app.numOfPollen=0
    app.pollen=[]
    app.pollenHelper=[]
    app.targetX=None
    app.targetY=None

def redrawAll(app):
    #for bee in app.helper:
    #bee.drawPlayer()
    app.helper.drawPlayer()
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
        cx += 20
        drawCircle(app.player.x,app.player.y+35,10,fill=color)
    for (_,_,color) in app.pollenHelper:
        cy = 25
        drawCircle(cx,cy,10,fill=color)
        cx += 20
        drawCircle(app.helper.x,app.helper.y+35,10,fill=color)

def onMouseMove(app,mouseX,mouseY):
    app.cursorX=mouseX
    app.cursorY=mouseY 
                
def onStep(app):
    app.helper.findTarget(app)
    app.helper.playerOnStep(app)
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
            Bee.color=pollinator.color
            app.pollen.append((25+20*numOfPollen,25,\
                               pollinator.color))
    for pollinator in Pollinator.pollinatorList:
        if pollinator.gatheredStateByHelper(app):
            app.numOfPollen+=1
            numOfPollen=app.numOfPollen
            HelperBee.color=pollinator.color
            app.pollenHelper.append((25+20*numOfPollen,25,\
                               pollinator.color))
    colorList=[]
    for pollen in app.pollen: 
        colorList.append(pollen[2])
    colorListHelper=[]
    for pollen in app.pollenHelper: 
        colorListHelper.append(pollen[2])

    for flower in Flower.flowerList: 
        if flower.pollinatedState(app):
            if app.pollen!=[]:
                if flower.color in colorList:
                    app.pollen.pop((colorList.index(flower.color)))
                    flower.width+=20
                    flower.height+=20
                    app.numOfPollen-=1
    for flower in Flower.flowerList: 
        if flower.pollinatedStateByHelper(app):
            if app.pollenHelper!=[]:
                if flower.color in colorListHelper:
                    app.pollenHelper.pop((colorListHelper.index(flower.color)))
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