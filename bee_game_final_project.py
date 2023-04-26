from cmu_graphics import *
from PIL import Image
import random, time
import math,copy
#The Bee image is from http://clipart-library.com/clipart/rcnrMnyei.htm
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
            #From http://clipart-library.com/clipart/rcnrMnyei.htm
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
        if self.stepCounter >= 10 and distance<8:
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
        #From http://clipart-library.com/clipart/rcnrMnyei.htm 
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
        self.distancedic2=dict()
        self.direction="left"
        self.pollenHelper=[]
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

    def playerOnStep2(self,app):
        if app.targetX2!=None and app.targetY2!=None:
            self.dx=app.targetX2-self.x
            self.dy=app.targetY2-self.y
            self.x+=self.dx/30
            self.y+=self.dy/30
            if self.dx+10>0: 
                self.direction="left"
            else: 
                self.direction="right"

    #This function directs the first helper bee to collect the closet pollen
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
    
    #This function directs the second helper bee to collect the pollen from upper
    #half of the screen
    def findTarget2(self,app):
        for pollen in Pollinator.pollinatorList:
            if pollen.y<400 and pollen.x<800: 
                app.targetX2=pollen.x
                app.targetY2=pollen.y

class Pollinator:
    pollinatorList=[]
    gathered=[]
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.up=random.randrange(7,11)
        self.c=random.randrange(1,4)
        self.color=random.choice(["red","blue","green","purple"])
        self.pollenGathered=0
        Pollinator.pollinatorList.append(self)
    def drawPollinator(self):
        drawCircle(self.x,self.y,15,fill=self.color)
    def isClose(self,other):
        if distance(self.x,self.y,other.x,other.y)<=40:  
            return True
        else: 
            return False
    #This checks collision with the pollinator by the player Bee
    def gatheredState(self,app):
        if self.isClose(app.player)and\
            self not in Pollinator.gathered:
            Pollinator.gathered.append(self)
            app.player.collected=True
            return True
    #This checks This checks collision with the pollinator by the first helper bee
    def gatheredStateByHelper1(self,app):
        if self.isClose(app.helper[0])and\
            self not in Pollinator.gathered:
            Pollinator.gathered.append(self)
            app.helper[0].collected=True
            return True
    #This checks collision with the pollinator by the second bee
    def gatheredStateByHelper2(self,app):
        if self.isClose(app.helper[1])and\
            self not in Pollinator.gathered:
            Pollinator.gathered.append(self)
            app.helper[1].collected=True
            return True
    #makes the pollinator move in sin wave
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
    #checks collision with the flower
    def pollinatedState(self,app):
        if self.isClose(app.player) and\
            self not in self.gathered:
            Flower.gathered.append(self)
            return True
    def pollinatedStateByHelper1(self,app):
        if self.isClose(app.helper[0]) and\
            self not in self.gathered:
            Flower.gathered.append(self)
            return True
    def pollinatedStateByHelper2(self,app):
        if self.isClose(app.helper[1]) and\
            self not in self.gathered:
            Flower.gathered.append(self)
            return True
    #makes the flower move in sin wave
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
    app.player=Bee(400,400)
    app.helper=[HelperBee(300,200),HelperBee(500,200)]
    app.numOfPollen=0
    app.pollen=[]
    app.targetX=None
    app.targetY=None
    app.targetX2=None
    app.targetY2=None
    firstBee=app.helper[0]
    secondBee=app.helper[1]

def redrawAll(app):
    firstBee=app.helper[0]
    secondBee=app.helper[1]
    firstBee.drawPlayer()
    secondBee.drawPlayer()
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

    for (_,_,color) in firstBee.pollenHelper:
        cy = 25
        drawCircle(cx,cy,10,fill=color)
        cx += 20  
        drawCircle(firstBee.x,firstBee.y+35,10,fill=color)
    for (_,_,color) in secondBee.pollenHelper:
        cy = 25
        drawCircle(cx,cy,10,fill=color)
        cx += 20 
        drawCircle(secondBee.x,secondBee.y+35,10,fill=color)

def onMouseMove(app,mouseX,mouseY):
    app.cursorX=mouseX
    app.cursorY=mouseY 
                
def onStep(app):
    firstBee=app.helper[0]
    secondBee=app.helper[1]
    for i in range(len(app.helper)):
        if i==0:
            app.helper[0].findTarget(app)
            app.helper[0].playerOnStep(app)
        else: 
            app.helper[1].findTarget2(app)
            app.helper[1].playerOnStep2(app)
    app.player.doStep()
    app.stepTimeCounter+=1
    app.player.playerOnStep(app)
    #generate the flowers once in a while
    if app.stepTimeCounter%25==0:
        Flower(random.randrange(800),800,50,50,"blue")
        Pollinator(random.randrange(800),800,"pink")
    #check if a pollen is picked up
    for pollinator in Pollinator.pollinatorList:
        if pollinator.gatheredState(app):
            app.numOfPollen+=1
            numOfPollen=app.numOfPollen
            Bee.color=pollinator.color
            app.pollen.append((25+20*numOfPollen,25,\
                               pollinator.color))
            
    for pollinator in Pollinator.pollinatorList:
        if pollinator.gatheredStateByHelper1(app):
            app.numOfPollen+=1
            numOfPollen=app.numOfPollen
            firstBee.color=pollinator.color
            firstBee.pollenHelper.append((25+20*numOfPollen,25,\
                            pollinator.color))
    for pollinator in Pollinator.pollinatorList:        
        if pollinator.gatheredStateByHelper2(app):
            app.numOfPollen+=1
            numOfPollen=app.numOfPollen
            secondBee.color=pollinator.color
            secondBee.pollenHelper.append((25+20*numOfPollen,25,\
                            pollinator.color))
            
    colorList=[]
    for pollen in app.pollen: 
        colorList.append(pollen[2])
    colorListHelper=[]
    colorListHelper2=[]
    for pollen in firstBee.pollenHelper: 
        colorListHelper.append(pollen[2])
    for pollen in secondBee.pollenHelper: 
        colorListHelper2.append(pollen[2])
    #check if a flower is pollianted
    for flower in Flower.flowerList: 
        if flower.pollinatedState(app):
            if app.pollen!=[]:
                if flower.color in colorList:
                    app.pollen.pop((colorList.index(flower.color)))
                    flower.width+=20
                    flower.height+=20
                    app.numOfPollen-=1
    for flower in Flower.flowerList: 
        if flower.pollinatedStateByHelper1(app):
            if firstBee.pollenHelper!=[]:
                if flower.color in colorListHelper:
                    firstBee.pollenHelper.pop((colorListHelper.index(flower.color)))
                    flower.width+=20
                    flower.height+=20
                    app.numOfPollen-=1
    for flower in Flower.flowerList: 
        if flower.pollinatedStateByHelper2(app):
            if secondBee.pollenHelper!=[]:
                if flower.color in colorListHelper2:
                    secondBee.pollenHelper.pop((colorListHelper2.index(flower.color)))
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