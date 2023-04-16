from cmu_graphics import *
import math,copy

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
    pollinator=[(200,200,"red"),(500,500,"red"),(100,200,"red")]
    gathered=[]
    def __init__(self,x,y,color):
        self.x=x
        self.y=y
        self.color=color
        self.gathered=False
        self.pollenGathered=0
    def drawFlower(self):
        drawCircle(self.x,self.y,15,fill=self.color)
    def isClose(self,other):
        if distance(self.x,self.y,other.x,other.y)<=40:  
            return True
        else: 
            return False
    def gatheredState(self,app):
        for (flowerX,flowerY,color) in Flower.pollinator:
            if Flower(flowerX,flowerY,color).isClose(app.player) and\
                (flowerX,flowerY,color) not in Flower.gathered:
                Flower.gathered.append((flowerX,flowerY,color))
                return True
    def flowerOnStep(self):
        self.y+=10

def onAppStart(app):
    app.width=800
    app.height=800
    app.cursorX=200
    app.cursorY=200
    app.player=Bee(200,200)
    app.numOfPollen=0
    app.pollen=[]

def redrawAll(app):
    app.player.drawPlayer()
    for i in range(len(Flower.pollinator)):
        flowerX=Flower.pollinator[i][0]
        flowerY=Flower.pollinator[i][1]
        color=Flower.pollinator[i][2]
        Flower(flowerX,flowerY,color).drawFlower()

    for (cx,cy) in app.pollen:
        drawCircle(cx,cy,10,fill="red")

def onMouseMove(app,mouseX,mouseY):
    app.cursorX=mouseX
    app.cursorY=mouseY 
                

def onStep(app):
    app.player.playerOnStep(app)
    if Flower(0,0,"red").gatheredState(app):
        app.numOfPollen+=1
        numOfPollen=app.numOfPollen
        app.pollen.append((25+20*numOfPollen,25))
    for (flowerX,flowerY,color) in Flower.pollinator:
        Flower(flowerX,flowerY,color).flowerOnStep()

def distance(x1,y1,x2,y2): 
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

def main():
    runApp()

main()