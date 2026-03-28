import random
import time
import math
import pygame
import sys
import pygame_gui

#TODO: Add angle adjuster
#TODO: Randomize cannon positions
#TODO: add sound effects
#TODO: Add scoring system
#TODO: Add main menu before game starts where you choose: Computer difficulty, terrain type, cannon colours...
#TODO: Better graphics
#TODO: Allow player to move cannon position
#TODO: Add wind effect
#TODO: Add different terrain types(tough to implement)
#TODO: Add different environments (night, day, sunset)
#TODO: multiplayer mode????
#TODO: Make a round based system?
#TODO: Have different cannon types with different projectiles(more health, less damage/less health, more damage etc)
#TODO: Maybe building structures? 
#TODO: Practice range? 
#TODO: Level based tank based on rounds progressed? 

#Gravity 
g = 9.8 #m/s^2
#Time step 
dt = 0.05 #s
y = 0 
cannonA = (150, 0) #Cannon A position (will change later to random)
cannonB = (850, 0) #Cannon B position (will change later to random)
detection_margin = 5 #Margin of error for hit detection

def launch_projectileA(cannon, angle, speed):
    """Launches a projectile from cannon A. Returns the trajectory as a list of (x, y) tuples."""
    angle_rad = math.radians(angle) #Convert inputed angle to radians from degrees.
    vx = speed * math.cos(angle_rad) #Calculate x component of velocity
    vy = speed * math.sin(angle_rad) #Calculate y component of velocity
    x, y = cannon #Starting position of the cannon
    trajectory = [] #List to store trajectory points
    
    while y >= 0: #While projectile is above ground
        trajectory.append((x, y)) #Add current position to trajectory
        x += vx * dt #Update x position
        y += vy * dt #Update y position
        vy -= g * dt #Update y velocity due to gravity
    
    return trajectory

def launch_projectileB(cannon, angle, speed):
    """Launches a projectile from cannon B. Returns the trajectory as a list of (x, y) tuples."""
    angle_rad = math.radians(180 - angle) #Adjust angle since cannon B faces left
    vx = speed * math.cos(angle_rad)
    vy = speed * math.sin(angle_rad)
    x, y = cannon
    trajectory = []
    
    while y >= 0:
        trajectory.append((x, y))
        x += vx * dt
        y += vy * dt
        vy -= g * dt
    
    return trajectory

def contact_detected(position, trajectory):
    """Returns True if the projectile's final x position is within the detection margin of the target position."""
    if trajectory[-1][0] >= position[0] - detection_margin and trajectory[-1][0] <= position[0] + detection_margin:
        return True
    return False

def computer_launch(difficulty, cannon, target):
    """Generates random launch parameter based on difficulty level."""
    angle = 45 #Keep set angle for now until new implementation later. 
    perfect_speed = math.sqrt((g * abs(target[0] - cannon[0])) / math.sin(2 * math.radians(angle))) #Speed needed to hit target 
    if difficulty == "easy":
        if perfect_speed > 30:
            speed = perfect_speed + random.randint(-30, 30) #Large random variation
        elif perfect_speed > 15:
            speed = perfect_speed + random.randint(-15, 30)
        elif perfect_speed > 5:
            speed = perfect_speed + random.randint(-5, 25)
        else:
            speed = perfect_speed + random.randint(0, 20)
    elif difficulty == "medium":
        if perfect_speed > 15:
            speed = perfect_speed + random.randint(-15, 15) #Medium random variation
        elif perfect_speed > 10:
            speed = perfect_speed + random.randint(-10, 10)
        elif perfect_speed > 5:
            speed = perfect_speed + random.randint(-5, 10)
        else:
            speed = perfect_speed + random.randint(0, 10)
    else: #hard
        if perfect_speed > 5:
            speed = perfect_speed + random.randint(-5, 5) #Small random variation
        elif perfect_speed > 3:
            speed = perfect_speed + random.randint(-3, 3)
        elif perfect_speed > 2:
            speed = perfect_speed + random.randint(-2, 2)
        else:
            speed = perfect_speed + random.randint(0, 2)
    return angle, speed

result_start_time = None
def start_shot(shooter):
    """Starts the shot for the given shooter ('player' or 'computer') and resets necessary variables."""
    global trajectory, traj_index, projectile_active, trail_points, result_start_time
    global shot_result, impact_time, effect_started, show_missed_marker, show_hit_effect
    global impact_x, impact_y, phase, result_start_time

    trail_points = []
    traj_index = 0
    projectile_active
    impact_time
    effect_started
    show_hit_effect = False 
    show_missed_marker = False
    impact_x = None
    impact_y = None
    result_start_time = None

    if shooter == "player":
        power = power_slider.get_current_value()


pygame.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Artillery Strike Game")
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)
value_font = pygame.font.SysFont(None, 28)
message_font = pygame.font.SysFont(None, 36)

turn = "player"
phase = "aiming"

GROUND_Y = HEIGHT - 50

def coord_to_screen(x, y):
    return int(x), int(GROUND_Y - y)

def draw_cannon(position, color):
    x, y = coord_to_screen(position[0], position[1])
    cannon_width = 20
    cannon_height = 10
    pygame.draw.rect(
        screen,
        color,
        (x - cannon_width // 2, y - cannon_height, cannon_width, cannon_height)
    )

trajectory = []
traj_index = 0
projectile_active = False
trail_points = []
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
shot_result = None
impact_time = None
effect_started = False
show_missed_marker = False
show_hit_effect = False
result_start_time = None
POWER_SPEED = 20
player_angle = 45
ANGLE_MIN, ANGLE_MAX = 0.0, 90.0
ANGLE_SPEED = 20.0
SCROLL_ANGLE_STEP = 1.0
WHEEL_COOLDOWN = 100  # milliseconds
last_wheel_time = 0

impact_x = None
impact_y = None

power_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((100, HEIGHT - 40), (800,30)),
    start_value=50,
    value_range=(0, 100),
    manager=manager
)
power_slider.allow_keyboard_input = False


def start_shot(shooter):
    """Starts the shot for the given shooter ('player' or 'computer') and resets necessary variables."""
    global trajectory, traj_index, projectile_active, trail_points, result_start_time
    global shot_result, impact_time, effect_started, show_missed_marker, show_hit_effect
    global impact_x, impact_y, phase, result_start_time

    trail_points = []
    traj_index = 0
    projectile_active = True
    impact_time = None
    effect_started = False
    show_hit_effect = False 
    show_missed_marker = False
    impact_x = None
    impact_y = None
    result_start_time = None

    if shooter == "player":
        power = power_slider.get_current_value() #Value from the slider
        #Angle editor added later
        trajectory = launch_projectileA(cannonA, player_angle, power) #Set at 45 degrees for now
        shot_result = "hit" if contact_detected(cannonB, trajectory) else "miss"
    else: #Computer shot 
        angle, speed = computer_launch("medium", cannonB, cannonA) #Set at medium difficulty for now until difficulty selector added
        trajectory = launch_projectileB(cannonB, angle, speed)
        shot_result = "hit" if contact_detected(cannonA, trajectory) else "miss"
    phase = "firing"

running  = True
power_left = False
power_right = False
while running:
    time_delta = clock.tick(60)/1000.0
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if turn == "player" and phase == "aiming":
                start_shot("player")

    keys = pygame.key.get_pressed()
    if turn == "player" and phase == "aiming":
        a_speed = ANGLE_SPEED
        p_speed = POWER_SPEED

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            a_speed *= 2
            p_speed *= 2

        if event.type == pygame.MOUSEWHEEL:
            now = pygame.time.get_ticks()
            if now - last_wheel_time >= WHEEL_COOLDOWN:
                if event.y > 0:
                    direction = 1
                else:
                    direction = -1
                player_angle += direction * SCROLL_ANGLE_STEP
                player_angle = max(ANGLE_MIN, min(ANGLE_MAX, player_angle))
                last_wheel_time = now

        # angle
        if keys[pygame.K_UP]:
            player_angle += a_speed * time_delta
        if keys[pygame.K_DOWN]:
            player_angle -= a_speed * time_delta
        player_angle = max(ANGLE_MIN, min(ANGLE_MAX, player_angle))

        # power
        current_power = power_slider.get_current_value()
        power_delta = p_speed * time_delta

        if keys[pygame.K_LEFT]:
            current_power -= power_delta
        elif keys[pygame.K_RIGHT]:
            current_power += power_delta
            current_power = max(0, min(100, current_power))
        power_slider.set_current_value(current_power)
        power_slider.current_value = current_power
        player_angle = max(ANGLE_MIN, min(ANGLE_MAX, player_angle))


    if turn == "computer" and phase == "aiming":
        start_shot("computer")
    manager.update(time_delta)

    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)
    draw_cannon(cannonA, RED)
    draw_cannon(cannonB, BLUE)
    
    power_value = int(power_slider.get_current_value())
    power_text = value_font.render(f'Power: {power_value}', True, BLACK)
    screen.blit(power_text, (5, HEIGHT- 35))

    angle_text = value_font.render(f'Angle: {int(player_angle)}°', True, BLACK)
    screen.blit(angle_text, (5, HEIGHT - 75))

    #Projectile animation
    if phase == "firing" and projectile_active:
        if traj_index < len(trajectory):
            proj_x, proj_y = trajectory[traj_index]
            screen_x, screen_y = coord_to_screen(proj_x, proj_y)
            pygame.draw.circle(screen, BLACK, (screen_x, screen_y), 3)
            traj_index += 1
            trail_points.append((screen_x, screen_y))
        else:
            projectile_active = False
            impact_time = pygame.time.get_ticks()
            impact_x, impact_y = trajectory[-1]
            phase = "result"
            result_start_time = impact_time

    if len(trail_points) > 1:
        pygame.draw.lines(screen, BLACK, False, trail_points, 6)
    
    if phase == "result" and impact_time and not effect_started: 
        if pygame.time.get_ticks() - impact_time >= 100:
            if shot_result == "miss":
                show_missed_marker = True
            elif shot_result == "hit":
                show_hit_effect = True
            effect_started = True

    # miss marker and text
    if show_missed_marker and impact_x is not None:
        x1, y1 = coord_to_screen(impact_x - 5, impact_y - 5)
        x2, y2 = coord_to_screen(impact_x + 5, impact_y + 5)
        x3, y3 = coord_to_screen(impact_x - 5, impact_y + 5)
        x4, y4 = coord_to_screen(impact_x + 5, impact_y - 5)
        pygame.draw.line(screen, RED, (x1, y1), (x2, y2), 4)
        pygame.draw.line(screen, RED, (x3, y3), (x4, y4), 4)
        miss_text = message_font.render("MISS", True, RED)
        screen.blit(miss_text, miss_text.get_rect(center=(WIDTH // 2, 50)))

    # hit effect and text
    if show_hit_effect and impact_x is not None:
        x, y = coord_to_screen(impact_x, impact_y)
        for radius in range(5, 30, 5):
            pygame.draw.circle(screen, RED, (x, y), radius, 2)
        hit_text = message_font.render("HIT!", True, GREEN)
        screen.blit(hit_text, hit_text.get_rect(center=(WIDTH // 2, 50)))

    # Switch turns after result phase
    if phase == "result" and result_start_time is not None:
        if pygame.time.get_ticks() - result_start_time >= 800:
            if turn == "player":
                turn = "computer"
            else:
                turn = "player"
            phase = "aiming"        

    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
