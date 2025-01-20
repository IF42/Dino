# zavedení knivhony raylib do programu
from pyray import *
from math import sqrt, floor
from enum import Enum

WIN_WIDTH = 800
WIN_HEIGHT = 600


class GameState_ID(Enum):
    INIT = 0
    RUNNING = 1
    GAMEOVER = 2


class GameContext:
    def __init__(self):
        self.state = GameState_ID.INIT
        self.road_x = 0
        self.cloud_x = 0
        self.dino = Vector2(150, 450)
        self.cactus = Vector2(700, 440)
        self.floor_y = 450
        self.score = 0

# deklarace (vytvoření) třídy
class GameState:
    def draw(self, contex, frame_time):
        pass


class GameState_Init(GameState): 
    def __init__(self, road_texture, cloud_texture, dino_texture):
        self.road_texture = road_texture
        self.dino_texture = dino_texture
        self.cloud_texture = cloud_texture

    def _handle_input(self, context):
        # reakce na stisk klávsy shift, která iniciuje změnu herního stavu
        if is_key_pressed(KEY_SPACE):
            context.state = GameState_ID.RUNNING

    def draw(self, context, frame_time):
        self._handle_input(context)
        
        draw_texture_pro(
            self.cloud_texture
            , Rectangle(0, 0, WIN_WIDTH, self.cloud_texture.height)  # čtverec výřezu obrázku
            , Rectangle(0, 200, WIN_WIDTH, self.cloud_texture.height)     # pozice a velikost v okně programu
            , Vector2(0, 0)                                         # posun počátečního bodu vykreslení
            , 0                                                     # úhel natočení obrázku
            , WHITE                                                 # barva pozadí
        )
        draw_texture_pro(
            self.road_texture
            , Rectangle(0, 0, WIN_WIDTH, self.road_texture.height)  # čtverec výřezu obrázku
            , Rectangle(0, 500, WIN_WIDTH, self.road_texture.height)     # pozice a velikost v okně programu
            , Vector2(0, 0)                                         # posun počátečního bodu vykreslení
            , 0                                                     # úhel natočení obrázku
            , WHITE                                                 # barva pozadí
        )
        draw_texture_ex(self.dino_texture, context.dino, 0, 1, WHITE)
        draw_text("Press space", 250, 100, 50, GRAY)


class GameState_Running(GameState): 
    def __init__(self, road_texture, cloud_texture, cactus_texture, dino_texture_list):
        self.road_texture = road_texture
        self.dino_texture_list = dino_texture_list
        self.cloud_texture = cloud_texture
        self.cactus_texture = cactus_texture
        self.timer = 0
        self.pose = 0
        self.acc = 0
        self.vel = 0


    def _handle_input(self, context):
        # reakce na stisk klávsy shift, která iniciuje změnu herního stavu
        if is_key_pressed(KEY_UP):
            self._jump()
        elif is_key_down(KEY_DOWN):
            self.pose = 2
        else:
            self.pose = 0

    def _jump(self):
        if self.vel == 0:
            self.vel = -1000

    def _dino_texture(self):
        return self.dino_texture_list[floor(self.timer) + self.pose]

    def draw(self, context, frame_time):
        self._handle_input(context)
        self.timer = (self.timer + (frame_time * 4)) % 2

        self.vel += self.acc * frame_time
        context.dino.y += self.vel * frame_time

        if context.dino.y < context.floor_y:
            self.acc += 10000*frame_time
        else:
            context.dino.y = context.floor_y 
            self.vel = 0
            self.acc = 0
        
        context.road_x = (context.road_x + (300 * frame_time)) % self.road_texture.width
        context.cloud_x = (context.cloud_x + (150 * frame_time)) % self.cloud_texture.width

        if context.cactus.x > 0:
            context.cactus.x = (context.cactus.x - (300 * frame_time * 0.98))
        else:
            context.score += 1
            context.cactus.x = WIN_WIDTH
        
        distance = sqrt((context.dino.x - context.cactus.x)**2 + (context.dino.y - context.cactus.y)**2)
        if distance < (self._dino_texture().width + self.cactus_texture.width) / 2 and context.dino.x < context.cactus.x:
            context.state = GameState_ID.GAMEOVER
        elif distance < (self._dino_texture().width + self.cactus_texture.width) and context.dino.x < context.cactus.x:
            self._jump()
             
        draw_texture_pro(
            self.cloud_texture
            , Rectangle(context.cloud_x, 0, WIN_WIDTH, self.cloud_texture.height)  # čtverec výřezu obrázku
            , Rectangle(0, 200, WIN_WIDTH, self.cloud_texture.height)     # pozice a velikost v okně programu
            , Vector2(0, 0)                                         # posun počátečního bodu vykreslení
            , 0                                                     # úhel natočení obrázku
            , WHITE                                                 # barva pozadí
        )
        draw_texture_pro(
            self.road_texture
            , Rectangle(context.road_x, 0, WIN_WIDTH, self.road_texture.height)  # čtverec výřezu obrázku
            , Rectangle(0, 500, WIN_WIDTH, self.road_texture.height)     # pozice a velikost v okně programu
            , Vector2(0, 0)                                         # posun počátečního bodu vykreslení
            , 0                                                     # úhel natočení obrázku
            , WHITE                                                 # barva pozadí
        )
        
        draw_texture_ex(self._dino_texture(), context.dino, 0, 1, WHITE)
        draw_texture_ex(self.cactus_texture, context.cactus, 0, 1, WHITE)
        draw_text(f"Score: {context.score}", 600, 50, 30, GRAY)

class GameState_GameOver(GameState): 
    def __init__(self, road_texture, cloud_texture, cactus_texture, dino_texture):
        self.road_texture = road_texture
        self.cactus_texture = cactus_texture
        self.dino_texture = dino_texture
        self.cloud_texture = cloud_texture

    def _handle_input(self, context):
        # reakce na stisk klávsy shift, která iniciuje změnu herního stavu
        if is_key_pressed(KEY_SPACE):
            context.cactus.x = 700
            context.road_x = 0
            context.cloud_x = 0 
            context.state = GameState_ID.RUNNING
            context.score = 0

    def draw(self, context, frame_time):
        self._handle_input(context)
        
        draw_texture_pro(
            self.cloud_texture
            , Rectangle(context.cloud_x, 0, WIN_WIDTH, self.cloud_texture.height)  # čtverec výřezu obrázku
            , Rectangle(0, 200, WIN_WIDTH, self.cloud_texture.height)     # pozice a velikost v okně programu
            , Vector2(0, 0)                                         # posun počátečního bodu vykreslení
            , 0                                                     # úhel natočení obrázku
            , WHITE                                                 # barva pozadí
        )
        draw_texture_pro(
            self.road_texture
            , Rectangle(context.road_x, 0, WIN_WIDTH, self.road_texture.height)  # čtverec výřezu obrázku
            , Rectangle(0, 500, WIN_WIDTH, self.road_texture.height)     # pozice a velikost v okně programu
            , Vector2(0, 0)                                         # posun počátečního bodu vykreslení
            , 0                                                     # úhel natočení obrázku
            , WHITE                                                 # barva pozadí
        )
        draw_texture_ex(self.dino_texture, context.dino, 0, 1, WHITE)
        draw_texture_ex(self.cactus_texture, context.cactus, 0, 1, WHITE)
        draw_text(f"Score: {context.score}", 600, 50, 30, GRAY)
        draw_text("Game Over", 250, 100, 50, GRAY)

# inicializace grafického okna
set_config_flags(FLAG_VSYNC_HINT)
init_window(WIN_WIDTH, WIN_HEIGHT, "Dino")
set_target_fps(144)

# načtení grafických textur do programu
road_texture = load_texture("graphics/road_template.png")
cloud_texture = load_texture("graphics/cloud_template.png")

cactus_texture = load_texture("graphics/cactus.png")

dino1_texture = load_texture("graphics/dino1.png")
dino2_texture = load_texture("graphics/dino2.png")
dino3_texture = load_texture("graphics/dino3.png")
dino4_texture = load_texture("graphics/dino4.png")
dino5_texture = load_texture("graphics/dino5.png")

game_context = GameContext()
strategy = [
    GameState_Init(road_texture, cloud_texture, dino2_texture)
    , GameState_Running(
        road_texture
        , cloud_texture
        , cactus_texture
        , [dino2_texture, dino3_texture, dino4_texture, dino5_texture]
        )
    , GameState_GameOver(road_texture, cloud_texture, cactus_texture, dino1_texture)
]

# herní smyčka
while window_should_close() is False:
    frame_time = get_frame_time()

    begin_drawing()

    # vykreslení stavu hry
    clear_background(WHITE)
    draw_fps(10, 10)
    strategy[game_context.state.value].draw(game_context, frame_time)
    end_drawing()

# korektní ukončení programu a uvolění zdrojů
unload_texture(road_texture)
unload_texture(dino1_texture)
unload_texture(dino2_texture)
unload_texture(dino3_texture)
unload_texture(dino4_texture)
unload_texture(dino5_texture)
unload_texture(cactus_texture)
close_window()
