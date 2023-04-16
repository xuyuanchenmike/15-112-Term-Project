from cmu_graphics import *
import math,copy
import random

class Bee: 
    def __init__(self,x,y): 
        self.x=x
        self.y=y
    def drawPlayer(self):
        drawCircle(self.x,self.y,25,fill="orange")
    def playerOnStep(self,app):
        self.x=app.cursorX
        self.y=app.cursorY

class Pollinator:
    pollinatorList=[]
    gathered=[]
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color="red"
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
                return True
    def pollinatorOnStep(self):
        self.y-=10

class Flower:
    flowerList=[]
    gathered=[]
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        #self.width=20
        #self.height=20
        self.color="blue"
        Flower.flowerList.append(self)
    def drawFlower(self):
        drawCircle(self.x,self.y,15,fill=self.color)
    def isClose(self,other):
        if distance(self.x,self.y,other.x,other.y)<=40:  
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
    app.player.drawPlayer()
    for pollinator in Pollinator.pollinatorList:
        pollinator.drawPollinator()
    for flower in Flower.flowerList: 
        flower.drawFlower()

    for (cx,cy) in app.pollen:
        drawCircle(cx,cy,10,fill="red")

def onMouseMove(app,mouseX,mouseY):
    app.cursorX=mouseX
    app.cursorY=mouseY 
                

def onStep(app):
    app.stepTimeCounter+=1
    app.player.playerOnStep(app)
    if app.stepTimeCounter%50==0:
        Pollinator(random.randrange(800),800,"red")
        Flower(random.randrange(800),800,"blue")
    for pollinator in Pollinator.pollinatorList:
        if pollinator.gatheredState(app):
            app.numOfPollen+=1
            numOfPollen=app.numOfPollen
            app.pollen.append((25+20*numOfPollen,25))
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


# flower1=Flower(random.randrange(800),800,"red")
# flower2=Flower(random.randrange(800),800,"red")
# flower3=Flower(random.randrange(800),800,"red")
# flower4=Flower(random.randrange(800),800,"red")

def distance(x1,y1,x2,y2): 
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

def main():
    runApp()

main()