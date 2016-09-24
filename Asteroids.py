# A Game of "RiceRocks" (clone of Asteroids)
# Author = Harkamal Jot Singh Kumar
# Completed on = 2/12/2014

import simplegui
import math
import random

# globals for user interface
WIDTH, HEIGHT = 800, 600
score, lives = 0, 3
time, teleport = 0.5, 100
started = False

# other globals
angle = 0
thrust, anim_flag = False, True

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
   
if True:  # condition to enable code folding
    # art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim   
    # debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
    #                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
    debris_info = ImageInfo([320, 240], [640, 480])
    debris_raw = "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/"
    debris_list = ['debris1_brown.png', 'debris2_brown.png', 'debris3_brown.png', 
     'debris4_brown.png', 'debris1_blue.png', 'debris2_blue.png', 
     'debris3_blue.png', 'debris4_blue.png', 'debris_blend.png']
    debris_link = debris_raw + debris_list[random.randint(0, 8)]
    debris_image = simplegui.load_image(debris_link) # random debris everytime you launch the game oh yeah! ^_-
 
    # nebula images - nebula_brown.png, nebula_blue.png
    nebula_info = ImageInfo([400, 300], [800, 600])
    nebula_image = simplegui.load_image("http://apod.nasa.gov/apod/image/0803/catspaw_noao.jpg")
    
    # splash image
    splash_info = ImageInfo([200, 150], [400, 300])
    splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
    
    # ship image
    ship_info = ImageInfo([45, 45], [90, 90], 35)
    ship_image = simplegui.load_image("http://2.bp.blogspot.com/-zfTJcElZlEA/VGb8IQBwFMI/AAAAAAAAAQM/gqAGC5lpMX0/s1600/double_ship.png")
    
    # missile image - shot1.png, shot2.png, shot3.png
    missile_info = ImageInfo([5,5], [10, 10], 3, 50)
    missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")
    
    # asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
    asteroid_info = ImageInfo([45, 45], [90, 90], 40)
    asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
    
    # animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
    explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
    explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")
    
    # sound assets purchased from sounddogs.com, please do not redistribute
    soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
    missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
    missile_sound.set_volume(.3)
    ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
    explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
    
    def angle_ctrl(self, val):
        self.angle += val
    
    def thruster(self, thrust):
        if thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
        self.thrust = thrust
        
    def update(self):
        #Position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % (WIDTH - 1)
        self.pos[1] = (self.pos[1] + self.vel[1]) % (HEIGHT - 1)
        
        #Friction udpate
        self.vel[0] *= 0.99
        self.vel[1] *= 0.99

        #Thrust update - acceleration in direction of forward vector
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0] * 0.1
            self.vel[1] += forward[1] * 0.1

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 4 * forward[0], self.vel[1] + 4 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))

    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def tp_now(self):
        self.pos = [random.randint(0, 800), random.randint(0,600)]
      
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.age * self.image_size[0]), self.image_center[1]], self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.age += 1
        
        # to remove or not to remove! :D
        remove = False
        if self.age == self.lifespan:
            remove = True
        return remove
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, second_obj):
        if dist(self.get_pos(), second_obj.get_pos()) < (self.get_radius() + second_obj.get_radius()):
            return True
        else:
            return False   
        
# key handlers to control ship
inputs = {"left": [0, -0.05],
          "right": [0, 0.05]}     # <- Useful and efficient

def controler_on(key):
    global angle, thrust, teleport, started
    for i in inputs:
        if key == simplegui.KEY_MAP[i]:
                angle = inputs[i][1]
    if key == simplegui.KEY_MAP["up"]:
        thrust = True
    if key == simplegui.KEY_MAP["space"]:
        player_ship.shoot()
    if key == simplegui.KEY_MAP["down"] and started and teleport == 100:
        player_ship.tp_now()
        teleport = 0
                   
def controler_off(key):
    global angle, thrust
    for i in inputs:
        if key == simplegui.KEY_MAP[i]:
                angle = inputs[i][0]
    if key == simplegui.KEY_MAP["up"]:
        thrust = False
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives, rock_group
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    in_width = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    in_height = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and in_width and in_height:
        started = True
        lives = 3
        score = 0

def draw(canvas):
    global time, started, lives, score, rock_group, teleport, anim_flag
    soundtrack.play()
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw ship and sprites
    player_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship and sprites
    player_ship.update()
    player_ship.thruster(thrust)
    if angle:
        player_ship.angle_ctrl(angle)
    lives -= collision_tester(rock_group, player_ship)
    score += 10 * group_collision_tester(rock_group, missile_group)
    
    # checking if the game is over
    if lives == 0:
        started = False
        rock_group = set()
        teleport = 100
 
    # draw splash screen if not started
    if not started:
        soundtrack.rewind()
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "Aqua", 'monospace')
    canvas.draw_text(str(lives), [50, 80], 22, "White", 'monospace')
    for life in range(lives): # to draw ships corresponding to number of lives
        canvas.draw_image(ship_image, [45, 45], [90, 90], [55+life*48, 75], [45, 45], 4.72)
    if started:
        canvas.draw_text("Score", [680, 50], 22, "Lime", 'monospace')
        canvas.draw_text(str(score), [680, 80], 22, "White", 'monospace')
    if not started and score == 0:
        canvas.draw_text("Score", [680, 50], 22, "Lime", 'monospace')
        canvas.draw_text(str(score), [680, 80], 22, "White", 'monospace')
    elif score > 0 and not started:
        if anim_flag:
            canvas.draw_text("Game Over!", [330, 30], 28, "Red", 'monospace')
            canvas.draw_text("Score", [680, 50], 22, "Lime", 'monospace')
            canvas.draw_text(str(score), [680, 80], 22, "White", 'monospace')
        else:
            canvas.draw_text("Game Over!", [330, 30], 28, "Aqua", 'monospace')
            canvas.draw_text("Score", [680, 50], 28, "Lime", 'monospace')
            canvas.draw_text(str(score), [680, 80], 28, "Red", 'monospace')
        
    # teleport juice bar!
    canvas.draw_text("Teleport", [45, 570], 15, "White", 'monospace')
    canvas.draw_polygon([[50, 580], [150, 580], [150, 582], [50, 582]], 5, 'Red')
    canvas.draw_polygon([[50, 580], [(50+teleport), 580], [(50+teleport), 582], [50, 582]], 5, 'Lime', 'Red')

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group   
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random()* 1.3, random.random() * 1.3]
    rock_avel = random.random() * .2 - .1
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
    if len(rock_group) < 10 and started:
        if (dist(a_rock.get_pos(), 
           player_ship.get_pos())) >(a_rock.get_radius() 
           + (1.5 * player_ship.get_radius()) + 100):
                rock_group.add(a_rock)
    # Code to stop sound on closing the frame
    if frame.get_canvas_textwidth("shiv",50) < 10:
        soundtrack.pause()
        
def process_sprite_group(sprites, canvas):  
    for sprite in set(sprites): 
        sprite.draw(canvas)
        if sprite.update():
            sprites.remove(sprite)
            
def collision_tester(group, second_obj):
    collisions = 0
    for thing in set(group):
        if thing.collide(second_obj):
            collisions += 1
            explosion = Sprite(thing.get_pos(),[0, 0], 0, 0, explosion_image,
                               explosion_info, explosion_sound)
            explosion_group.add(explosion)
            group.remove(thing)            
    return collisions

def group_collision_tester(group1, group2):   
    collisions = 0
    for item in set(group1):
        if collision_tester(group2, item) > 0:
            collisions += 1
            group1.remove(item)
    return collisions

def tp_refil():
    global teleport, anim_flag
    if teleport != 100:
        teleport += 20
        
    # animation for score display
    if anim_flag:
        anim_flag = False
    else:
        anim_flag = True
    
# initialize stuff
frame = simplegui.create_frame("Rice Rocks!", WIDTH, HEIGHT)
frame.add_label("Rice Rocks by Shiv")
frame.add_label("")
frame.add_label("Controls:")
frame.add_label("")
frame.add_label("Up = Accelerate")
frame.add_label("")
frame.add_label("Space = Fire Missile!")
frame.add_label("")
frame.add_label("Right : Rotate_Ship_Clock_Wise")
frame.add_label("")
frame.add_label("Left : Rotate_Ship_CounterClock_Wise")
frame.add_label("")
frame.add_label("Down : Teleport to random area when teleport bar is full! :D")

# initialize ship and two sprites
player_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()

# register handlers
frame.set_keyup_handler(controler_off)
frame.set_keydown_handler(controler_on)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)
tp_timer = simplegui.create_timer(1000.0, tp_refil)

# get things rolling
timer.start()
tp_timer.start()
frame.start()

