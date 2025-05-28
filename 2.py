import turtle
import random
import math

# ---------------- 터틀 설정 ----------------
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.title("Tamagotchi Turtle")

pet = turtle.Turtle()
pet.shape("turtle")
pet.color("green")
pet.penup()

width = screen.window_width() // 2
height = screen.window_height() // 2

target_x, target_y = 0, 0
is_moving = False
running = True

# ---------------- 상태 및 감정 ----------------
hunger = 100
max_hunger = 100
emotion = "평범함"
emotion_timer = None

status_writer = turtle.Turtle()
status_writer.hideturtle()
status_writer.penup()
status_writer.goto(-280, 260)

def get_hunger_status():
    if hunger >= 80:
        return "🐢 배부름"
    elif hunger >= 50:
        return "🙂 괜찮음"
    elif hunger >= 30:
        return "😟 살짝 배고픔"
    elif hunger > 0:
        return "🥺 매우 배고픔"
    else:
        return "💀 죽음"

def update_status_text():
    status_writer.clear()
    status_writer.goto(-280, 260)
    status_writer.write(
        f"허기: {hunger}/{max_hunger} {get_hunger_status()}\n감정: {emotion}",
        font=("Arial", 14, "normal")
    )

# ---------------- 감정 처리 ----------------
def set_emotion(new_emotion, duration=5000):
    global emotion, emotion_timer
    emotion = new_emotion
    update_status_text()

    if emotion_timer:
        screen.ontimer(None, emotion_timer)
    emotion_timer = screen.ontimer(reset_emotion, duration)

def reset_emotion():
    global emotion
    emotion = "평범함"
    update_status_text()

# ---------------- 쓰다듬기 감지 ----------------
def check_mouse_touch():
    if not running:
        return
    x = screen._root.winfo_pointerx() - screen._root.winfo_rootx()
    y = screen._root.winfo_pointery() - screen._root.winfo_rooty()
    canvas_x = screen.cv.canvasx(x)
    canvas_y = screen.cv.canvasy(y)
    pet_x, pet_y = pet.xcor(), pet.ycor()
    distance = math.sqrt((canvas_x - pet_x) ** 2 + (canvas_y - pet_y) ** 2)

    if distance < 20:
        set_emotion("기분 좋음")

    screen.ontimer(check_mouse_touch, 100)

# ---------------- 펫 움직임 ----------------
def pick_new_target():
    global target_x, target_y
    angle = random.randint(0, 360)
    distance = random.randint(50, 100)
    dx = distance * math.cos(math.radians(angle))
    dy = distance * math.sin(math.radians(angle))
    new_x = pet.xcor() + dx
    new_y = pet.ycor() + dy

    if -width < new_x < width and -height < new_y < height:
        target_x, target_y = new_x, new_y
    else:
        pet.setheading((angle + 180) % 360)
        pick_new_target()

def move_smoothly():
    global is_moving
    if not is_moving or not running:
        return
    x, y = pet.xcor(), pet.ycor()
    distance = math.sqrt((target_x - x) ** 2 + (target_y - y) ** 2)
    if distance < 5:
        is_moving = False
        wait_time = random.randint(1000, 3000)
        screen.ontimer(start_new_move, wait_time)
    else:
        pet.setheading(pet.towards(target_x, target_y))
        pet.forward(5)
        screen.ontimer(move_smoothly, 30)

def start_new_move():
    global is_moving
    if not running:
        return
    pick_new_target()
    is_moving = True
    move_smoothly()

# ---------------- 게임 상태 ----------------
def game_over():
    global running, is_moving
    running = False
    is_moving = False
    pet.color("gray")
    status_writer.goto(-80, 0)
    status_writer.write("💀 펫이 죽었습니다", font=("Arial", 20, "bold"))

def decrease_hunger():
    global hunger
    if not running:
        return
    hunger = max(0, hunger - 5)
    update_status_text()
    if hunger == 0:
        game_over()
        return
    screen.ontimer(decrease_hunger, 2000)

# ---------------- 키보드 이벤트 ----------------
def give_food():
    global hunger
    if not running:
        return
    hunger = min(max_hunger, hunger + 10)
    print("🍚 밥을 주었습니다!")
    update_status_text()

def print_status():
    print(f"\n현재 허기: {hunger} / {max_hunger} ({get_hunger_status()})")

def stop_game():
    global running
    running = False
    print("👋 게임을 종료합니다.")
    screen.bye()

screen.listen()
screen.onkey(give_food, "space")
screen.onkey(print_status, "s")
screen.onkey(stop_game, "q")

# ---------------- 실행 ----------------
start_new_move()
update_status_text()
screen.ontimer(decrease_hunger, 5000)
screen.ontimer(check_mouse_touch, 100)
screen.mainloop()
test
