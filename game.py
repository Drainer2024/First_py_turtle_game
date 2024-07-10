import os
import random
import turtle
import time
import winsound
import audioop
import pygame
import customtkinter as CTK
from tkinter import *

root1 = CTK.CTk()
root1.geometry("800x300+500+300")

def play_game():
    root1.destroy()

state_var = CTK.IntVar(value = 0)
multishot_var = CTK.BooleanVar(value=False)
piercing_var = CTK.BooleanVar(value = False)
bouncing_var = CTK.BooleanVar(value=False)

label1 = CTK.CTkLabel(root1, text="Chose your level:", font=("Helavita", 19))
label1.grid(row = 0, column = 0, padx = 25, pady = 15)



level1 = CTK.CTkRadioButton(root1, text="Easy",variable=state_var, value = 1)
level1.grid(row = 1, column = 0, padx = 25, pady = 15,)

level2 = CTK.CTkRadioButton(root1, text="Normal",variable=state_var, value = 2)
level2.grid(row = 2, column = 0, padx = 25, pady = 15,)

level3 = CTK.CTkRadioButton(root1, text="Hard",variable=state_var, value = 3)
level3.grid(row = 3, column = 0, padx = 25, pady = 15,)


label2 = CTK.CTkLabel(root1, text="Choose your powers:", font=("Helavita", 19) )
label2.grid(row = 0, column = 1, padx = 50, pady = 15)

multishot = CTK.CTkCheckBox(root1, text="Multishot", variable=multishot_var, onvalue = True, offvalue=False)
multishot.grid(row = 1, column = 1, padx = 50, pady = 15)
piercing = CTK.CTkCheckBox(root1, text ="Piercing missiles", variable=piercing_var, onvalue = True, offvalue = False)
piercing.grid(row = 2, column = 1, padx = 50, pady = 15)
bouncing = CTK.CTkCheckBox(root1, text ="Bouncing missiles", variable=bouncing_var, onvalue = True, offvalue = False)
bouncing.grid(row = 3, column = 1, padx = 50, pady = 15)

play = CTK.CTkButton(root1, text = "PLAY!", font = ("Helavita", 28), height=100, command=play_game)
play.grid(row = 2, column = 2, padx = 50, pady = 10 )


level2.select()


root1.mainloop()
print(multishot_var.get())


num_missiles = 1


state = state_var.get()
is_multishot = multishot_var.get()
is_piercing = piercing_var.get()
is_bouncing = bouncing_var.get()


if state == 1 :
    amount_enemy = 4
    amount_ally = 2
    enemy_speed = 4
if state == 2 :
    amount_enemy = 5
    amount_ally = 4
    enemy_speed = 6

if state == 3 :
    amount_enemy = 6
    amount_ally = 6
    enemy_speed = 8



turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")
turtle.bgpic("images/bgpic (1).png")
turtle.hideturtle()
turtle.setundobuffer(1)
turtle.tracer(0)
pygame.mixer.init()
turtle.title("Space war")
bounces = 0
bounces2 = 0
bounces3 = 0


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
        self.speed = enemy_speed
        self.setheading(random.randint(0, 360))

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=random.uniform(0.1, 1), stretch_len=random.uniform(0.1, 0.5), outline=None)
        self.goto(-1000, 1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1
    
    def move(self):
        if self.frame > 0 :
            self.fd(10)

        if self.frame > 15:
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

class Missile(Sprite):
    
    def __init__(self, spriteshape, color, startx, starty, heading):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.3, stretch_len=0.3, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)
        self.setheading(heading)

    def multi_fire(self, other, other2, heading):
        if self.status == "ready" and other.status == "ready" and other2.status == "ready":
            #winsound.PlaySound("Sounds/fire", winsound.SND_FILENAME | winsound.SND_ASYNC)
            fire_sound.play()
            self.goto(player.xcor(), player.ycor())
            other.goto(player.xcor(), player.ycor())
            other2.goto(player.xcor(), player.ycor())
            self.setheading(heading)
            
            other.setheading(self.heading() + 15)
            other2.setheading(self.heading() - 15)
            self.status = "firing"
            other.status = "firing"
            other2.status = "firing"
    
    def fire(self, heading):
        if self.status == "ready":
            #winsound.PlaySound("Sounds/fire", winsound.SND_FILENAME | winsound.SND_ASYNC)
            fire_sound.play()
            self.goto(player.xcor(), player.ycor())
            self.setheading(heading)
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

    def multi_move(self, other, other2):

        if self.status and other.status and other2.status == 'ready':
            self.goto(-1000, 1000)
            other.goto(-1000, 1000)
            other2.goto(-1000, 100)
        if self.status and other.status and other2.status == "firing":
            self.fd(self.speed)
            other.fd(other.speed)
            other2.fd(other2.speed)

        if (self.xcor() >= 290 or self.xcor() <= -290 or \
        self.ycor() >=290 or self.ycor() <= -290)  :
            self.goto(-1000, 1000)
            self.status = 'ready'

        if (other.xcor() >= 290 or other.xcor() <= -290 or \
        other.ycor() >=290 or other.ycor() <= -290)  :
            other.goto(-1000, 1000)
            other.status = 'ready'

        if (other2.xcor() >= 290 or other2.xcor() <= -290 or \
        other2.ycor() >=290 or other2.ycor() <= -290)  :
            other2.goto(-1000, 1000)
            other2.status = 'ready'

    def bouncing_move(self):
        global bounces

        if self.status == 'ready':
            self.goto(-1000, 1000)

        if self.status == "firing":
            
            self.fd(self.speed)
            if self.xcor() > 280:
                self.setx(280)
                self.setheading(self.heading() + 60)
                
                bounces += 1
            if self.xcor() < -280:
                self.setx(-280)
                self.setheading(self.heading() + 60)
                bounces += 1
            if self.ycor() > 280:
                self.sety(280)
                self.setheading(self.heading() + 60)
                bounces += 1
            if self.ycor() < -280:
                self.sety(-280)
                self.setheading(self.heading() + 60)
                bounces += 1
            if bounces >= 5:
                self.status = "ready"
                bounces = 0
            
    def multi_bounce_move(self, other, other2):
        global bounces
        global bounces2
        global bounces3
        

        if self.status and other.status and other2.status == 'ready':
            self.goto(-1000, 1000)
            other.goto(-1000, 1000)
            other2.goto(-1000, 100)
            
        if self.status and other.status and other2.status == "firing":
            self.fd(self.speed)
            other.fd(other.speed)
            other2.fd(other2.speed)
            if self.xcor() > 280:
                self.setx(280)
                self.setheading(self.heading() + 60)
                bounces += 1
            if other.xcor() > 280:
                other.setx(280)
                other.setheading(other.heading() + 60)
                bounces2 += 1
            if other2.xcor() > 280:
                other2.setx(280)
                other2.setheading(other2.heading() + 60)
                bounces3 += 1
            if self.xcor() < -280:
                self.setx(280)
                self.setheading(self.heading() + 60)
                bounces += 1
            if other.xcor() < -280:
                other.setx(-280)
                other.setheading(other.heading() + 60)
                bounces2 += 1
            if other2.xcor() < -280:
                other2.setx(-280)
                other2.setheading(other2.heading() + 60)
                bounces3 += 1
            if self.ycor() > 280:
                self.sety(280)
                self.setheading(self.heading() + 60)
                bounces += 1
            if other.ycor() > 280:
                other.sety(280)
                other.setheading(other.heading() + 60)
                bounces2 += 1
            if other2.ycor() > 280:
                other2.sety(280)
                other2.setheading(other2.heading() + 60)
                bounces3 += 1
            if self.ycor() < -280:
                self.sety(-280)
                self.setheading(self.heading() + 60)
                bounces += 1
            if other.ycor() < -280:
                other.sety(-280)
                other.setheading(other.heading() + 60)
                bounces2 += 1
            if other2.ycor() < -280:
                other2.sety(-280)
                other2.setheading(other2.heading() + 60)
                bounces3 += 1

            if bounces >= 5 and bounces2 >= 5 and bounces3 >= 5 :
                self.status = "ready"
                other.status = "ready"
                other2.status = "ready"
                bounces = 0
                bounces2 = 0
                bounces3 = 0

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
missile1 = Missile("triangle", "yellow", 0, 0, player.heading() )
#ally = Ally("square", "blue", 0, 0)

enemies = []
for i in range(amount_enemy):
    enemies.append(Enemy("circle", "red", random.randint(-300, 300), random.randint(-300, 300)))

allies = []
for i in range(amount_ally):
    allies.append(Ally("square", "green", random.randint(-300, 300), random.randint(-300, 300)))



particles = []
for i in range(20):
    particles.append(Particle("circle", "orange",0, 0))


missile2 = Missile("triangle", "yellow", 0, 0, player.heading() + 15)
missile3 = Missile("triangle", "yellow", 0, 0, player.heading() - 15)



turtle.onkey(player.turn_left, "a")
turtle.onkey(player.turn_right, "d")
turtle.onkey(player.accelerate, "w")
turtle.onkey(player.decelerate, "s")
if is_multishot:
    turtle.onkey(lambda: missile1.multi_fire(missile2, missile3, player.heading()), "space")
else:
    turtle.onkey(lambda: missile1.fire(player.heading()), "space")
turtle.listen()


while True:
    turtle.update()
    time.sleep(0.04)
    


    #missile1.setheading(player.heading())
    #missile2.setheading(player.heading() + 15)
    #missile3.setheading(player.heading() - 15)

    player.move()
    for enemy in enemies:
        global score
        enemy.move()
        if player.is_collision(enemy):
            
            explosion_sound.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score -= 100
            game.show_status()
            
        if missile1.is_collision(enemy):
            
            explosion_sound.play()
            for particle in particles:
                particle.explode(enemy.xcor(), enemy.ycor())
                particle.move()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            if is_piercing == False:
                missile1.status = 'ready'
            game.score += 100
            game.show_status()
        
        if missile2.is_collision(enemy):
            #winsound.PlaySound("Sounds/explosion", winsound.SND_FILENAME | winsound.SND_ASYNC)
            explosion_sound.play()
            for particle in particles:
                particle.explode(enemy.xcor(), enemy.ycor())
                particle.move()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            if is_piercing == False:
                missile2.status = 'ready'
            game.score += 100
            game.show_status()

        if missile3.is_collision(enemy):
            #winsound.PlaySound("Sounds/explosion", winsound.SND_FILENAME | winsound.SND_ASYNC)
            explosion_sound.play()
            for particle in particles:
                particle.explode(enemy.xcor(), enemy.ycor())
                particle.move()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            if is_piercing == False:
                missile3.status = 'ready'
            game.score += 100
            game.show_status()

        

            
    for ally in allies:
        ally.move()
        if missile1.is_collision(ally):
            #winsound.PlaySound("Sounds/explosion", winsound.SND_FILENAME | winsound.SND_ASYNC)
            explosion_sound.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            if is_piercing == False:
                missile1.status = 'ready'
            game.score -= 50
            game.show_status()
        if missile2.is_collision(ally):
            #winsound.PlaySound("Sounds/explosion", winsound.SND_FILENAME | winsound.SND_ASYNC)
            explosion_sound.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            if is_piercing == False:
                missile2.status = 'ready'
            game.score -= 50
            game.show_status()
        if missile3.is_collision(ally):
            #winsound.PlaySound("Sounds/explosion", winsound.SND_FILENAME | winsound.SND_ASYNC)
            explosion_sound.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            if is_piercing == False:
                missile3.status = 'ready'
            game.score -= 50
            game.show_status()



    for particle in particles:
        particle.move()
        particle.frame += 1
    
    if is_multishot == True and is_bouncing == False:
        missile1.multi_move(missile2, missile3)

    if is_bouncing == True and is_multishot == False:
        missile1.bouncing_move()
    if is_multishot == True and is_piercing == True:
        missile1.multi_bounce_move(missile2, missile3)
    if is_bouncing == False and is_multishot== False:
        missile1.move()
    
    if game.score >= 1000 :
            break
    

if game.score >= 1000 :
    root2 = CTK.CTk()
    root2.geometry("400x150+800+300")
    congrats = CTK.CTkLabel(root2, text = "Congratulations, You won!!", font = ("Helvetica", 20), text_color=("Green"))
    congrats.grid(row = 1, column = 0, pady = 50, padx = 100)





    root2.mainloop()

