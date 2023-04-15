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
    pollinator=[(500,200),(600,300),(550,450),(330,400)]
    def __init__(self,x,y,color,pollinator):
        self.x=x
        self.y=y
        self.color=color
        self.pollinator=True
        self.gathered=False

    def drawFlower(self):
        drawCircle(self.x,self.y,15,fill=self.color)
    def isClose(self,other):
        if distance(self.x,self.y,other.x,other.y)<=40:  
            return True
        else: 
            return False
        
    def gatheredState(self,app): 
        if self.pollinator:
            if not self.gathered:
                for (flowerX,flowerY) in Flower.pollinator:
                    if Flower(flowerX,flowerY,"red",None).isClose(app.player):
                        self.gathered=True
                        return True

def onAppStart(app):
    app.width=800
    app.height=800
    app.cursorX=200
    app.cursorY=200
    app.player=Bee(200,200)
    app.numOfPollen=0
    app.pollen=[]
    app.alreadyGathered=[]

def redrawAll(app):
    app.player.drawPlayer()
    for i in range(len(Flower.pollinator)):
        flowerX=Flower.pollinator[i][0]
        flowerY=Flower.pollinator[i][1]
        Flower(flowerX,flowerY,"red","pollinator").drawFlower()
    for (cx,cy) in app.pollen:
        drawCircle(cx,cy,10,fill="red")

def onMouseMove(app,mouseX,mouseY):
    app.cursorX=mouseX
    app.cursorY=mouseY
    if Flower(0,0,"red","pollinator").gatheredState(app):
            app.numOfPollen+=1
            app.pollen.append((25+10*app.numOfPollen,25))
            app.alreadyGathered.append((app.cursorX,app.cursorY))
def onStep(app): 
    app.player.playerOnStep(app)

def distance(x1,y1,x2,y2): 
    return ((x1-x2)**2+(y1-y2)**2)**(1/2)

def main():
    runApp()

main()