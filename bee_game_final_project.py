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

class Flower:
    pollinator=[]
    gathered=[]
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
        self.gathered=False
        self.pollenGathered=0
        Flower.pollinator.append(self)
    def drawFlower(self):
        drawCircle(self.x,self.y,15,fill=self.color)
    def isClose(self,other):
        if distance(self.x,self.y,other.x,other.y)<=40:  
            return True
        else: 
            return False
    def gatheredState(self,app):
        for flower in Flower.pollinator:
            if flower.isClose(app.player) and\
                flower not in Flower.gathered:
                Flower.gathered.append(flower)
                return True
    def flowerOnStep(self):
        self.y-=10

def onAppStart(app):
    #app.stepsPerSecond=5
    app.width=800
    app.height=800
    app.cursorX=200
    app.cursorY=200
    app.player=Bee(200,200)
    app.numOfPollen=0
    app.pollen=[]

def redrawAll(app):
    app.player.drawPlayer()
    for flower in Flower.pollinator:
        flower.drawFlower()

    for (cx,cy) in app.pollen:
        drawCircle(cx,cy,10,fill="red")

def onMouseMove(app,mouseX,mouseY):
    app.cursorX=mouseX
    app.cursorY=mouseY 
                

def onStep(app):
    app.player.playerOnStep(app)
    if random.randrange(800)<50:
        Flower(random.randrange(800),800,"red")
    for flower in Flower.pollinator:
        if flower.gatheredState(app):
            app.numOfPollen+=1
            numOfPollen=app.numOfPollen
            app.pollen.append((25+20*numOfPollen,25))
    for flower in Flower.pollinator:
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