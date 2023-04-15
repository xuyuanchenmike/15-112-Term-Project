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
    flowerList=[(300,300),(50,50),(100,100),(150,80)]
    def __init__(self,x,y,color,pollinator):
        self.x=x
        self.y=y
        self.color=color
        self.pollinator=True
        self.gather=False

    def drawFlower(self):
        drawCircle(self.x,self.y,15,fill=self.color)
    def isClose(self,other):
        if distance(self.x,self.y,other.x,other.y)<=40:  
            return True
        else: 
            return False
    def gatheredState(self,app): 
        if self.pollinator:
            if not self.gather:
                for (flowerX,flowerY) in Flower.flowerList:
                    if Flower(flowerX,flowerY,"red",None).isClose(app.player):
                        return True

def onAppStart(app):
    app.cursorX=200
    app.cursorY=200
    app.player=Bee(200,200)

def redrawAll(app):
    app.player.drawPlayer()
    for (flowerX,flowerY) in Flower.flowerList:
        Flower(flowerX,flowerY,"red","pollinator").drawFlower()
        if Flower(flowerX,flowerY,"red","pollinator").gatheredState(app): 
            drawRect(200,200,50,50,align="center", fill="orange")

def onMouseMove(app,mouseX,mouseY):
    app.cursorX=mouseX
    app.cursorY=mouseY

def onStep(app): 
    app.player.playerOnStep(app)

def distance(x1,y1,x2,y2): 
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

def main():
    runApp()

main()