import game_lib as games
import color
import json
import random
import os

FPS = 150
BOMBS = {"resolution": (100, 100),
         "images": ("assets/sprites/bomb_1r.png", "assets/sprites/bomb_2r.png",
                    "assets/sprites/bomb_3r.png", "assets/sprites/bomb_4r.png")}
ANIMATION = {"resolution": (150, 150), "images": ("assets/sprites/animation/1.png", "assets/sprites/animation/2.png",
                                                  "assets/sprites/animation/3.png", "assets/sprites/animation/4.png",
                                                  "assets/sprites/animation/5.png", "assets/sprites/animation/6.png",
                                                  "assets/sprites/animation/7.png", "assets/sprites/animation/8.png",
                                                  "assets/sprites/animation/9.png", "assets/sprites/animation/10.png",
                                                  "assets/sprites/animation/11.png", "assets/sprites/animation/12.png",
                                                  "assets/sprites/animation/13.png", "assets/sprites/animation/14.png",
                                                  "assets/sprites/animation/15.png")}
SOURCE_SPRITE = {"resolution": (300, 150),
                 "image": "assets/sprites/ufo.png"}
PLATFORM = {"resolution": (300, 122),
            "image": "assets/sprites/shield.png"}
MAIN_SOUND = "assets/audio/main.wav"
SOUND_EFFECT = "assets/audio/bang.wav"
RESOLUTION = (1024, 768)


def difficulty():
    with open("settings.txt", "r") as f:
        df = f.readlines()[0].replace("\n", "")
    return int(df)


def background():
    with open("settings.txt", "r") as f:
        bg = f.readlines()[1]
    return bg


def change_direction(curr_x, fps=FPS):
    eps = abs(int(curr_x - games.screen.width / 2))
    if eps < int(games.screen.width / 5):
        res = random.choice(range(1, int(fps / 1.5)))
    elif eps < int(games.screen.width / 4):
        res = random.choice(range(1, int(fps)))
    elif eps < int(games.screen.width / 3):
        res = random.choice(range(1, int(fps * 2)))
    else:
        res = random.choice(range(1, int(fps * 6)))
    if res == random.choice(range(1, fps)):
        return True
    else:
        return False


# return speed of sprite
def sprite_speed():
    d = difficulty()
    if d == 0:
        return random.randint(1, 3)  # easy
    elif d == 1:
        return random.randint(2, 4)  # medium
    elif d == 2:
        return random.randint(3, 5)  # hard
    else:
        return random.randint(4, 8)  # unreal


def update_records(file, curr_record):
    with open(file, "r") as f:
        global_records = json.load(f)
    if curr_record > global_records["1"]:
        global_records["3"] = global_records["2"]
        global_records["2"] = global_records["1"]
        global_records["1"] = curr_record
    elif curr_record > global_records["2"]:
        global_records["3"] = global_records["2"]
        global_records["2"] = curr_record
    elif curr_record > global_records["3"]:
        global_records["3"] = curr_record
    with open(file, "w") as f:
        json.dump(global_records, f)


class Explosion(games.Animation):

    images = ANIMATION["images"]

    def __init__(self, x, y):
        super(Explosion, self).__init__(images=Explosion.images, x=x, y=y,
                                        repeat_interval=5, n_repeats=1, is_collideable=False)
        self.sound = games.load_sound(SOUND_EFFECT)
        self.sound.play(0)


class BigExplosion(games.Animation):

    images = ANIMATION["images"]

    def __init__(self, x, y):
        super(BigExplosion, self).__init__(images=BigExplosion.images, x=x, y=y,
                                           repeat_interval=5, n_repeats=1, is_collideable=False)
        self.sound = games.load_sound(SOUND_EFFECT)
        self.sound.play(0)


class Bomb(games.Sprite):

    list_of_sprites = BOMBS["images"]

    def __init__(self, x):
        self.name_of_image = random.choice(Bomb.list_of_sprites)
        super().__init__(image=games.load_image(self.name_of_image),
                         x=x, y=int(BOMBS["resolution"][1]/2 + SOURCE_SPRITE["resolution"][1]/2))
        self.dy = sprite_speed()
        Bomb.in_game = True

    def update(self):
        if not Bomb.in_game:
            self.destroy()
        if self.bottom > games.screen.height or Platform.score >= 300000:
            self.destroy()
            update_records("records.json", Platform.score)
            Bomb.in_game = False
            Bomb.game_over()

    def die(self):
        new_explosion = Explosion(self.x, self.y)
        games.screen.add(new_explosion)

    @staticmethod
    def game_over():
        if Platform.score >= 300000:
            mes = "{0} Score: {1}".format("You Win!", Platform.score)
        else:
            mes = "{0} Score: {1}".format("Game Over:(", Platform.score)
        message = games.Message(value=mes, size=50, color=color.dark_red,
                                x=games.screen.width / 2, y=games.screen.height / 2,
                                lifetime=FPS * 2, after_death=Bomb.quit)
        games.screen.add(message)

    @staticmethod
    def quit():
        games.screen.quit()
        Platform.score = 0


class Platform(games.Sprite):

    score = 0

    def __init__(self, image_name):
        super().__init__(image=games.load_image(image_name), x=games.screen.width/2, y=games.screen.height - 200)
        self.text_score = games.Text(value="0" + "$", size=int(games.screen.width/17), color=color.black,
                                     top=5, right=int(games.screen.width - 10))
        games.screen.add(self.text_score)
        games.screen.add(games.Text(value="For quit press q", size=int(games.screen.width/40), color=color.black,
                         top=5, left=5))
        self.main_sound = games.load_sound(MAIN_SOUND)
        self.main_sound.play()

    def update(self):
        # self.x = games.mouse.x
        if games.keyboard.is_pressed(games.K_LEFT):
            self.x -= 5
        elif games.keyboard.is_pressed(games.K_RIGHT):
            self.x += 5
        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width
        if games.keyboard.is_pressed(games.K_q):
            Bomb.in_game = True
            Platform.score = 0
            games.screen.quit()
        self.check_collide()

    def check_collide(self):
        for sprite in self.overlapping_sprites:
            sprite.die()
            Platform.score += 500 + 100 * difficulty()
            self.text_score.value = str(Platform.score) + "$"
            self.text_score.right = games.screen.width - 10
            sprite.destroy()


class UFO(games.Sprite):

    def __init__(self, image_name):
        super().__init__(image=games.load_image(image_name), x=games.screen.width/2, y=SOURCE_SPRITE["resolution"][1]/2, dx=sprite_speed() + 2)
        self.time_before_next_sprite = 0
        self.start = int(FPS/2)

    def update(self):
        if self.left < 0 or self.right > games.screen.width or change_direction(self.x):
            self.dx = -self.dx
        if Bomb.in_game:
            self.next_sprite()

    def next_sprite(self):
        if self.start == 0:
            if self.time_before_next_sprite > 0:
                self.time_before_next_sprite -= 1
            else:
                new_sprite = Bomb(self.x)
                if Bomb.in_game:
                    games.screen.add(new_sprite)
                self.time_before_next_sprite = FPS / random.randint(1, 9)
        else:
            mes = games.Message(value="Start!", size=100, color=color.dark_red,
                                x=games.screen.width / 2, y=games.screen.height / 2,
                                lifetime=10)
            games.screen.add(mes)
            self.start -= 1


def init_game():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    games.init(screen_width=RESOLUTION[0], screen_height=RESOLUTION[1], fps=FPS,
               title="Nuclear Shield", icon="assets/sprites/nuclear_mini.png")
    main_theme = games.load_image(background(), transparent=False)
    games.screen.background = main_theme
    main_platform = Platform(PLATFORM["image"])
    games.screen.add(main_platform)
    ufo = UFO(SOURCE_SPRITE["image"])
    games.screen.add(ufo)
    games.mouse.is_visible = False
    games.screen.event_grab = True
    Bomb.in_game = True
    games.screen.mainloop()
    main_platform.main_sound.stop()
