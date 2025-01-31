import os
import random
import turtle
import time
import winsound
import audioop
import pygame

turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")
turtle.bgpic("images/bgpic (1).png")
turtle.hideturtle()
turtle.setundobuffer(1)
turtle.tracer(0)
pygame.mixer.init()
turtle.title("Space war")

explosion_sound = pygame.mixer.Sound("Sounds/explosion.wav")
fire_sound = pygame.mixer.Sound("Sounds/fire.wav")

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1
    def move(self):
        self.fd(self.speed)
        if self.xcor() > 290 :
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290 :
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290 :
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290 :
            self.sety(-290)
            self.rt(60)
        
    
    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)) and \
        (self.ycor() <= (other.ycor() + 20)) :
            return True
        else :
            return False
        
class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.3, outline=None)
        self.speed = 4
        self.lives = 3
    def turn_left(self):
        self.lt(30)
    def turn_right(self):
        self.rt(30)
    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360))

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=random.uniform(0.1, 0.5), stretch_len=random.uniform(0.1, 0.5), outline=None)
        self.goto(-1000, 1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1
    
    def move(self):
        if self.frame > 0 :
            self.fd(10)

        if self.frame > 20:
            self.frame = 0
            self.goto(-1000, 1000)

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0, 360))

    def move(self):
        self.fd(self.speed)
        if self.xcor() > 290 :
            self.setx(290)
            self.lt(60)
        if self.xcor() < -290 :
            self.setx(-290)
            self.lt(60)
        if self.ycor() > 290 :
            self.sety(290)
            self.lt(60)
        if self.ycor() < -290 :
            self.sety(-290)
            self.lt(60)

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.3, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)
        

    def fire(self):
        if self.status == "ready":
            #winsound.PlaySound("Sounds/fire", winsound.SND_FILENAME | winsound.SND_ASYNC)
            fire_sound.play()
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"
            

    def move(self):

        if self.status == 'ready':
            self.goto(-1000, 1000)

        if self.status == "firing":
            self.fd(self.speed)
        
        if self.xcor() >= 290 or self.xcor() <= -290 or \
        self.ycor() >=290 or self.ycor() <= -290 :
            self.goto(-1000, 1000)
            self.status = 'ready'

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3
    
    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    
    def show_status(self):
        self.pen.undo()
        msg = "Score = %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))
        

game = Game()

game.draw_border()

game.show_status()



player = Player("triangle", "white", 0, 0)
#enemy = Enemy("circle", "red", -100, 0)
missile = Missile("triangle", "yellow", 0, 0)
#ally = Ally("square", "blue", 0, 0)

enemies = []
for i in range(6):
    enemies.append(Enemy("circle", "red", random.randint(-300, 300), random.randint(-300, 300)))

allies = []
for i in range(6):
    allies.append(Ally("square", "green", random.randint(-300, 300), random.randint(-300, 300)))

particles = []
for i in range(20):
    particles.append(Particle("circle", "orange",0, 0))


turtle.onkey(player.turn_left, "a")
turtle.onkey(player.turn_right, "d")
turtle.onkey(player.accelerate, "w")
turtle.onkey(player.decelerate, "s")
turtle.onkey(missile.fire, "space")
turtle.listen()


while True:
    turtle.update()
    time.sleep(0.04)

    player.move()
    for enemy in enemies:
        enemy.move()
        if player.is_collision(enemy):
            #winsound.PlaySound("Sounds/explosion", winsound.SND_FILENAME | winsound.SND_ASYNC)
            explosion_sound.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score -= 100
            game.show_status()
            
        if missile.is_collision(enemy):
            #winsound.PlaySound("Sounds/explosion", winsound.SND_FILENAME | winsound.SND_ASYNC)
            explosion_sound.play()
            for particle in particles:
                particle.explode(enemy.xcor(), enemy.ycor())
                particle.move()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = 'ready'
            game.score += 100
            game.show_status()
            
            

    
    
    missile.move()
    for ally in allies:
        ally.move()
        if missile.is_collision(ally):
            #winsound.PlaySound("Sounds/explosion", winsound.SND_FILENAME | winsound.SND_ASYNC)
            explosion_sound.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = 'ready'
            game.score -= 50
            game.show_status()
            

    for particle in particles:
        particle.move()
        particle.frame += 1
    
    


    
    
turtle.update()
delay = input("press enter to finish")