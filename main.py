from pyray import *
from math import floor


WIN_WIDTH=800
WIN_HEIGHT=600


class SceneTexture:
    def __init__(self, texture, init_vel, x, y, width):
        self.acc = 5
        self.vel = init_vel
        self.texture = texture
        self.source = Rectangle(0, 0, texture.width, texture.height)
        self.dest = Rectangle(x, y, width, texture.height)

    def update(self, frame_time):
        self.source.x += self.vel * frame_time
        self.vel += self.acc * frame_time
        draw_texture_pro(self.texture, self.source, self.dest, Vector2(0, 0), 0, WHITE)

class Player:
    def __init__(self, texture_dead, texture_run1, texture_run2, texture_duck1, texture_duck2, x, y):
        self.timer = 0
        self.state = 0

        self.pos = Vector2(x, y)
        self.acc = 0
        self.vel = 0
        self.floor_pos = y
        self.texture_list = [texture_run1, texture_run2, texture_duck1, texture_duck2, texture_dead]

    def jump(self):
        if self.acc == 0:
            self.vel = -700

    def duck(self, cmd):
        if cmd is True:
            self.state = 2
        else:
            self.state = 0

    def update(self, frame_time):
        self.vel += self.acc
        self.pos.y += (self.vel * frame_time)

        if self.pos.y < self.floor_pos:
            if self.acc < 35:
                self.acc += 3
        else:
            self.pos.y = self.floor_pos
            self.acc = 0
            self.vel = 0
        
        self.timer = (self.timer + (frame_time * 4)) % 2
        texture_index = floor(self.timer) + self.state

        draw_texture_ex(self.texture_list[texture_index], self.pos, 0, 1, WHITE)

class Cactus:
    def __init__(self, texture, x, y):
        self.pos = Vector2(x, y)
        self.texture = texture

    def update(self, time_frame, vel):
        if self.pos.x <= 0:
            self.pos.x = 800
        else:
            self.pos.x -= vel * time_frame * 0.89

        draw_texture_ex(self.texture, self.pos, 0, 1, WHITE)


if __name__ == "__main__":
    set_config_flags(FLAG_VSYNC_HINT)
    init_window(WIN_WIDTH, WIN_HEIGHT, "Dino")
    set_target_fps(144)

    road_texture = load_texture("graphics/road_template.png")
    cloud_texture = load_texture("graphics/cloud_template.png")
    dino_dead_texture = load_texture("graphics/dino1.png")
    dino_run1_texture = load_texture("graphics/dino2.png")
    dino_run2_texture = load_texture("graphics/dino3.png")
    dino_duck1_texture = load_texture("graphics/dino4.png")
    dino_duck2_texture = load_texture("graphics/dino5.png")
    cactus_texture = load_texture("graphics/cactus.png")

    road = SceneTexture(road_texture, 200, 0, 500, WIN_WIDTH)
    cloud = SceneTexture(cloud_texture, 100, 0, 300, WIN_WIDTH)
    player = Player(dino_dead_texture, dino_run1_texture, dino_run2_texture, dino_duck1_texture, dino_duck2_texture, 150, 450)
    cactus = Cactus(cactus_texture, 700, 450)

    while window_should_close() is False:
        frame_time = get_frame_time()
        if road.vel > 500:
            road.acc = -5
            cloud.acc = -5
        elif road.vel < 200:
            road.acc = 5
            cloud.acc = 5 

        if is_key_pressed(KEY_UP):
            player.jump()
        elif is_key_pressed(KEY_DOWN):
            player.duck(True)
        elif is_key_released(KEY_DOWN):
            player.duck(False)

    
        if (cactus.pos.x - player.pos.x) < 20*(road.vel*frame_time) and cactus.pos.x > player.pos.x:
            player.jump()


        begin_drawing()
        clear_background(WHITE)
        draw_fps(10, 10)

        road.update(frame_time)
        cactus.update(frame_time, road.vel)
        cloud.update(frame_time)
        player.update(frame_time)

        end_drawing()

    unload_texture(road_texture)
    unload_texture(cloud_texture)
    unload_texture(dino_dead_texture)
    unload_texture(dino_run1_texture)
    unload_texture(dino_run2_texture)
    unload_texture(dino_duck1_texture)
    unload_texture(dino_duck2_texture)
    unload_texture(cactus_texture)

    close_window()


