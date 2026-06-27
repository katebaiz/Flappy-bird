from tkinter import *
from time import sleep
from random import randint

HEIGHT = 600
WIDTH = 800
BIRD_SIZE = 30
PILLAR = 30
PILLAR_HEAD_W = 5
PILLAR_HEAD_H = 30
SHOW_HITBOX = True
G = .1 #px/frame**2
root = Tk()
canvas = Canvas(height=HEIGHT, width=WIDTH, bg="lightblue")
canvas.pack()
bird = canvas.create_oval(3*BIRD_SIZE, (.5*HEIGHT-BIRD_SIZE)//2, 4*BIRD_SIZE, (.5*HEIGHT+BIRD_SIZE)//2, fill="yellow", outline="black")
bird_start_coords = canvas.coords(bird)
hitbox = (canvas.create_rectangle(bird_start_coords[0], bird_start_coords[1]+BIRD_SIZE/4, bird_start_coords[2], bird_start_coords[3]-BIRD_SIZE/4, outline="black"),
          canvas.create_rectangle(bird_start_coords[0]+BIRD_SIZE/4, bird_start_coords[1], bird_start_coords[2]-BIRD_SIZE/4, bird_start_coords[1]+BIRD_SIZE/4, outline="black"),
          canvas.create_rectangle(bird_start_coords[0]+BIRD_SIZE/4, bird_start_coords[3]-BIRD_SIZE/4, bird_start_coords[2]-BIRD_SIZE/4, bird_start_coords[3], outline="black"))
score = 0
best_score = 0
label1 = canvas.create_text(2*BIRD_SIZE, BIRD_SIZE, fill="black", text="SCORE", font=("Arial", BIRD_SIZE//2))
label2 = canvas.create_text(5*BIRD_SIZE, BIRD_SIZE, fill="black", text="BEST", font=("Arial", BIRD_SIZE//2))
score_label = canvas.create_text(2*BIRD_SIZE, 2*BIRD_SIZE, fill="black", text=score, font=("Arial", BIRD_SIZE//2))
best_score_label = canvas.create_text(5*BIRD_SIZE, 2*BIRD_SIZE, fill="black", text=best_score, font=("Arial", BIRD_SIZE//2))
v_bird = 0
v_bird_multiplyer = 1
canvas.update()
walls = []
force = 0
play = False
calls = 0
def jump(event):
    global force, play
    if (event.keysym == "Up" or event.keysym == "w" or event.keysym == "space") and force == 0:
        force = 20
    elif event.keysym == "c":
        print("O")
        play = False
        exit()
    elif event.keysym == "Down" or event.keysym == "s":
        force = -1
def move_bird():
    global bird, force, v_bird, BIRD_SIZE
    if force > 0:
        force -= 1
        v_bird = -BIRD_SIZE/10
    else:
        if force == -1:
            v_bird += BIRD_SIZE//5
        v_bird += G
    canvas.move(bird, 0, v_bird*v_bird_multiplyer)
    for i in hitbox:
        canvas.move(i, 0, v_bird*v_bird_multiplyer)
    if force == -1:
        force = 0
        v_bird -= BIRD_SIZE//5
def create_wall():
    gap = randint(4*BIRD_SIZE, HEIGHT//2)
    height = randint(0,HEIGHT-gap)
    w1 = canvas.create_rectangle(WIDTH, 0, WIDTH+PILLAR, height, fill="green")
    w2 = canvas.create_rectangle(WIDTH, height+gap, WIDTH+PILLAR, HEIGHT, fill="green")
    h1 = canvas.create_rectangle(WIDTH-PILLAR_HEAD_W, height-PILLAR_HEAD_H, WIDTH+PILLAR+PILLAR_HEAD_W, height, fill="green")
    h2 = canvas.create_rectangle(WIDTH-PILLAR_HEAD_W, height+gap, WIDTH+PILLAR+PILLAR_HEAD_W, height+PILLAR_HEAD_H+gap, fill="green")
    walls.append((w1, w2, h1, h2))
def move_wall():
    for i in walls:
        for j in i:
            try:
                canvas.move(j, -WIDTH/300, 0)
            except IndexError:
                break
def destroy_wall():
    global score
    for i in range(len(walls)-1, -1, -1):
        try:
            if canvas.coords(walls[i][0])[2] <= 0:
                for j in walls[i]:
                    canvas.delete(j)
                del walls[i]
                score += 1
        except IndexError:
            break
def check_collision():
    global HEIGHT
    for i in hitbox:
        bird_coords = canvas.coords(i)
        if bird_coords[1] < 0 or bird_coords[3] > HEIGHT:
            return True
        for k in walls:
            for j in k:
                wall_coords = canvas.coords(j)
                try:
                    if ((bird_coords[0] >= wall_coords[0] and bird_coords[0] <= wall_coords[2]) or (bird_coords[2] >= wall_coords[0] and bird_coords[2] <= wall_coords[2])) and ((bird_coords[1] >= wall_coords[1] and bird_coords[1] <= wall_coords[3]) or (bird_coords[3] >= wall_coords[1] and bird_coords[3] <= wall_coords[3])):
                        return True
                except IndexError:
                    break
    return False
def check_score():
    global score, best_score, score_label, best_score_label, label1, label2
    canvas.lift(label1)
    canvas.lift(label2)
    canvas.lift(score_label)
    canvas.lift(best_score_label)
    canvas.itemconfig(score_label, text=score)
    if score > best_score: best_score = score
    canvas.itemconfig(best_score_label, text=best_score)
def inversion():
    global v_bird_multiplyer, calls, v_bird, force
    if calls == 1:
        canvas.configure(bg="blue")
    elif calls == 2:
        v_bird = 0
        force = 0
        if v_bird_multiplyer == 1:
            canvas.configure(bg="lightgreen")
        else:
            canvas.configure(bg="lightblue")
        v_bird_multiplyer *= -1
canvas.bind_all("<Key>", jump)
def game(event):
    global bird, v_bird, HEIGHT, WIDTH, BIRD_SIZE, PILLAR, G, force, score, score_label, label1, label2, best_score_label, play, calls, v_bird_multiplyer, hitbox, SHOW_HITBOX
    play = False
    canvas.delete("all")
    bird = canvas.create_oval(3*BIRD_SIZE, (.5*HEIGHT-BIRD_SIZE)//2, 4*BIRD_SIZE, (.5*HEIGHT+BIRD_SIZE)//2, fill="yellow", outline="black")
    hitbox = (canvas.create_rectangle(bird_start_coords[0], bird_start_coords[1]+BIRD_SIZE/4, bird_start_coords[2], bird_start_coords[3]-BIRD_SIZE/4, outline="black"),
              canvas.create_rectangle(bird_start_coords[0]+BIRD_SIZE/4, bird_start_coords[1], bird_start_coords[2]-BIRD_SIZE/4, bird_start_coords[1]+BIRD_SIZE/4, outline="black"),
              canvas.create_rectangle(bird_start_coords[0]+BIRD_SIZE/4, bird_start_coords[3]-BIRD_SIZE/4, bird_start_coords[2]-BIRD_SIZE/4, bird_start_coords[3], outline="black"))
    if not SHOW_HITBOX:
        for i in hitbox:
            canvas.itemconfig(i,state="hidden")
    t = 0
    v_bird = 0
    force = 0
    walls = []
    score = 0
    label1 = canvas.create_text(2*BIRD_SIZE, BIRD_SIZE, fill="black", text="SCORE", font=("Arial", BIRD_SIZE//2))
    label2 = canvas.create_text(5*BIRD_SIZE, BIRD_SIZE, fill="black", text="BEST", font=("Arial", BIRD_SIZE//2))
    score_label = canvas.create_text(2*BIRD_SIZE, 2*BIRD_SIZE, fill="black", text=score, font=("Arial", BIRD_SIZE//2))
    best_score_label = canvas.create_text(5*BIRD_SIZE, 2*BIRD_SIZE, fill="black", text=best_score, font=("Arial", BIRD_SIZE//2))
    game_over = canvas.create_text(WIDTH//2, HEIGHT//2, fill="red", text="GAME OVER", font=("Arial", 3*BIRD_SIZE), state="hidden")
    sleep(0.1)
    play = True
    wait1 = randint(75, 250)
    calls = 0
    v_bird_multiplyer = 1
    canvas.configure(bg="lightblue")
    wait2 = randint(500, 1500)
    while play:
        wait1 -= 1
        wait2 -= 1
        move_bird()
        if wait1 == 0:
            create_wall()
            wait1 = randint(75, 250)
        if wait2 == 0:
            calls = (calls+1)%3
            if calls == 1:
                wait2 = 100
            inversion()
        move_wall()
        destroy_wall()
        if check_collision():
            canvas.itemconfig(game_over, state="normal")
            canvas.lift(game_over)
            play = False
        check_score()
        canvas.update()
        sleep(.01)
canvas.bind_all("<r>",game)
game(0)
root.mainloop()
