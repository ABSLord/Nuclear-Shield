import pygame
import pygame.locals
import time

screen = None
mouse = None
keyboard = None
music = None

for i in dir(pygame):
    if i.startswith('K_'):
        globals()[i] = getattr(pygame, i)


class Mouse(object):

    def __init__(self):
        self._is_visible = True

    def get_x(self):
        return pygame.mouse.get_pos()[0]

    def set_x(self, new_x):
        pygame.mouse.set_pos([self._x, self._y])

    x = property(get_x, set_x)

    def get_y(self):
        return pygame.mouse.get_pos()[1]

    def set_y(self, new_y):
        pygame.mouse.set_pos([self._x, self._y])

    y = property(get_y, set_y)

    def get_position(self):
        return pygame.mouse.get_pos()

    def set_position(self, new_position):
        pygame.mouse.set_pos(new_position)

    position = property(get_position, set_position)

    def get_is_visible(self):
        return self._is_visible

    def set_is_visible(self, new_visibility):
        self._is_visible = new_visibility
        pygame.mouse.set_visible(self._is_visible)

    is_visible = property(get_is_visible, set_is_visible)

    def is_pressed(self, button_num):
        return pygame.mouse.get_pressed()[button_num]


class Keyboard(object):

    def __init__(self):
        self._keys = []

    def get_keys(self):
        if not screen.virtual:
            self._keys = filter(self.is_pressed, [globals()[i] for i in globals() if i.startswith("K_")])

        return self._keys

    def set_keys(self, keys):
        if not screen.virtual:
            raise AttributeError("Cannot set keys list if not in virtual mode")
        self._keys = keys

    keys = property(get_keys, set_keys)

    def is_pressed(self, key):
        if not screen.virtual:
            return pygame.key.get_pressed()[key]


class Music(object):

    # Loads the music from filename
    def load(self, filename):
        pygame.mixer.music.load(filename)

    # Plays the loaded music
    # Args:loop: Amount of times to repeat(-1 is forever)
    def play(self, loop=0):
        pygame.mixer.music.play(loop)

    # Fadeout music in the given amount of milliseconds
    def fadeout(self, millisec):
        pygame.mixer.music.fadeout(millisec)

    # Stops music
    def stop(self):
        pygame.mixer.music.stop()


class Sprite(object):
    """
    Initializes Sprite with given parameters.
    Args:
        image: The image to display.
        angle: The angle to rotate by.
        x: The center x to place the sprite on.
        y: The center y to place the sprite on.
        top: The y location of the top of the sprite.
        bottom: The y location of the bottom of the sprite.
        left: The x location of the left of the sprite.
        right: The x location of  right of the sprite.
        dx: The x velocity (Delta x).
        dy: The y velocity (delta y).
        interval: The number of frames between tick() calls.
        is_collideable: Whether or not the sprite participates in collisions.
    """
    def __init__(self, image, angle=0, x=0, y=0, top=None,
                 bottom=None, left=None, right=None, dx=0,
                 dy=0, interval=1, is_collideable=True):
        self._angle = 0
        self._x = 0
        self._y = 0

        self._image = image
        self.interval = interval
        self.tick_timer = interval
        self.angle = angle

        if left:
            self.left = left
        elif right:
            self.right = right
        elif x:
            self.x = x
        else:
            self.x = 0

        if top:
            self.top = top
        elif bottom:
            self.bottom = bottom
        elif y:
            self.y = y
        else:
            self.y = 0

        self.dx = dx
        self.dy = dy
        self._overlapping_sprites = []
        self.is_collideable = is_collideable
        self.screen = None

    def get_image(self):
        return self._image

    def set_image(self, new_image):
        self._image = new_image
        self._rot_image = pygame.transform.rotate(self._image, -self._angle)
        self._rect = self._rot_image.get_rect()
        self._rect.centerx = self._x
        self._rect.centery = self._y

    image = property(get_image, set_image)

    def get_width(self):
        return self._rect.width

    def _set_width(self, new_width):
        raise ValueError("Can't change the width")

    width = property(get_width, _set_width)

    def get_height(self):
        return self._rect.height

    def _set_height(self, new_height):
        raise ValueError("Can't change the height")

    height = property(get_height, _set_height)

    def get_angle(self):
        return self._angle

    def set_angle(self, new_angle):
        self._angle = new_angle % 360
        self._rot_image = pygame.transform.rotate(self._image, -self._angle)
        self._rect = self._rot_image.get_rect()
        self._rect.centerx = self._x
        self._rect.centery = self._y

    angle = property(get_angle, set_angle)

    def get_x(self):
        return self._x

    def set_x(self, new_x):
        self._x = new_x
        self._rect.centerx = new_x

    x = property(get_x, set_x)

    def get_y(self):
        return self._y

    def set_y(self, new_y):
        self._y = new_y
        self._rect.centery = new_y

    y = property(get_y, set_y)

    def get_position(self):
        return self._x, self._y

    def set_position(self, new_position):
        self.x = new_position[0]
        self.y = new_position[1]

    position = property(get_position, set_position)

    def get_top(self):
        return self._rect.top

    def set_top(self, new_top):
        self._rect.top = new_top
        self._y = self._rect.centery

    top = property(get_top, set_top)

    def get_bottom(self):
        return self._rect.bottom

    def set_bottom(self, new_bottom):
        self._rect.bottom = new_bottom
        self._y = self._rect.centery

    bottom = property(get_bottom, set_bottom)

    def get_left(self):
        return self._rect.left

    def set_left(self, new_left):
        self._rect.left = new_left
        self._x = self._rect.centerx

    left = property(get_left, set_left)

    def get_right(self):
        return self._rect.right

    def set_right(self, new_right):
        self._rect.right = new_right
        self._x = self._rect.centerx

    right = property(get_right, set_right)

    def get_dx(self):
        return self._dx

    def set_dx(self, new_dx):
        self._dx = new_dx

    dx = property(get_dx, set_dx)

    def get_dy(self):
        return self._dy

    def set_dy(self, new_dy):
        self._dy = new_dy

    dy = property(get_dy, set_dy)

    def get_velocity(self):
        return self._dx, self._dy

    def set_velocity(self, new_velocity):
        self.dx = new_velocity[0]
        self.dy = new_velocity[1]

    velocity = property(get_velocity, set_velocity)

    def get_overlapping_sprites(self):
        """Returns list of other sprites overlapping this sprite."""
        self._check_overlap()
        return self._overlapping_sprites

    def _set_overlapping_sprites(self, new_list):
        raise ValueError("Can't set overlapping sprites")

    overlapping_sprites = property(get_overlapping_sprites, _set_overlapping_sprites)

    def overlaps(self, other):
        """Tells if other sprite overlaps this sprite"""
        return (self._rect.colliderect(other._rect) and self._is_collideable and
                other.is_collideable and (not self is other))

    def get_is_collideable(self):
        return self._is_collideable

    def set_is_collideable(self, new_status):
        self._is_collideable = new_status
        self._check_overlap()

    is_collideable = property(get_is_collideable,
                              set_is_collideable)

    def _check_overlap(self):
        self._overlapping_sprites = []
        if not self.is_collideable:
            return []
        for sprite in screen.all_objects:
            if self.overlaps(sprite):
                self._overlapping_sprites.append(sprite)

    def get_interval(self):
        return self._interval

    def set_interval(self, new_interval):
        self._interval = new_interval
        self.tick_timer = self._interval

    interval = property(get_interval, set_interval)

    # A function that is usually overridden.
    def update(self):
        pass

    # Similar to update() but different.
    def tick(self):
        pass

    # Destroys sprite.
    def destroy(self):
        if self.screen:
            self.screen.remove(self)

    def _move(self):
        self.x += self.dx
        self.y += self.dy

    def _draw(self):
        if self.screen:
            self.screen.buffer.blit(self._rot_image, self._rect)
            self.screen.new_dirties.append(self._rect)

    def _process_sprite(self):
        self._check_overlap()
        self._draw()
        self._move()
        self.update()
        self.tick_timer -= 1
        if not self.tick_timer:
            self.tick()
            self.tick_timer = self._interval


class Text(Sprite):
    """
    A Sprite which displays text.
    A GUI label with all the properties of a sprite.
    Attributes:
        value: The text to display.
        size: The height of the text in pixels.
        color: The color of the text (can be specified by using the color moduleor an RGB tuple).
    """

    def __init__(self, value, size, color, angle=0, x=0,
                 y=0, top=None, bottom=None, left=None,
                 right=None, dx=0, dy=0, interval=1,
                 is_collideable=True):
        """
        Initializes Text object with given parameters.
        Args:
            value: The text to display.
            size: The height of the text in pixels
            color: The color of the text.
            angle: The angle to rotate the object.
            x: The center x position where the sprite will be placed.
            y: The center y position where the sprite will be placed.
            top: The y location of the top edge of the sprite.
            bottom: The y location of the bottom edge of the sprite.
            left: The x location of the left edge of the sprite.
            right: The x location of  right edge of the sprite.
            dx: delta x is the x velocity of the sprite.
            dy: delta y is the y velocity of the sprite.
            interval: The number of frames between tick() calls.
            is_collideable: Whether or not the sprite participates in collisions.
        """

        self._size = size
        self._color = color
        self._value = value
        pygame.font.init()
        self.font = pygame.font.Font(None, size)
        Sprite.__init__(self, self.font.render(str(value), 1, color),
                        angle, x, y, top, bottom, left,
                        right, dx, dy, interval, is_collideable)

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        self._value = new_value
        self._make_image()

    value = property(get_value, set_value)

    def get_size(self):
        return self._size

    def set_size(self, new_size):
        self._size = new_size
        self.font = pygame.font.Font(None, self._size)
        self._make_image()

    size = property(get_size, set_size)

    def get_color(self):
        return self._color

    def set_color(self, new_color):
        self._color = new_color
        self._make_image()

    color = property(get_color, set_color)

    def _make_image(self):
        self.image = self.font.render(str(self._value), 1, self.color)


# An object that is displayed for a temporary period.
class Message(Text):
    def __init__(self, value, size, color, angle=0, x=0,
                 y=0, top=None, bottom=None, left=None,
                 right=None, dx=0, dy=0, lifetime=0,
                 is_collideable=True, after_death=None):
        Text.__init__(self, value, size, color, angle, x,
                      y, top, bottom, left, right, dx, dy,
                      lifetime, is_collideable)

        self.after_death = after_death

    def tick(self):
        self.destroy()
        if self.after_death:
            self.after_death()


# A subclass of Sprite that rotates through a list of images.
class Animation(Sprite):

    def __init__(self, images, angle=0, x=0, y=0, top=None,
                 bottom=None, left=None, right=None, dx=0, dy=0,
                 repeat_interval=1, n_repeats=0,
                 is_collideable=True):
        self.images = []
        for pic in images:
            if isinstance(pic, str):
                self.images.append(load_image(pic))
            else:
                self.sequence.append(pic)
        Sprite.__init__(self, self.images[0], angle, x, y, top,
                        bottom, left, right, dx, dy,
                        repeat_interval, is_collideable)
        self.n_repeats = n_repeats
        if not self.n_repeats:
            self.n_repeats -= 1
        self.pos = 0

    def tick(self):
        self.pos += 1
        self.pos %= len(self.images)
        self.image = self.images[self.pos]
        if not self.pos:
            self.n_repeats -= 1
        if not self.n_repeats:
            self.destroy()


# A screen class.
class Screen(object):

    # Initialise screen
    def __init__(self, width, height, fps, title, icon, virtual=False):
        self._width = width
        self._height = height
        self._fps = fps
        self._icon = icon
        self.running = False
        self.virtual = virtual
        if not virtual:
            pygame.init()
            pygame.display.set_icon(pygame.image.load(icon))
            pygame.display.set_caption(title)
            self.screen_surf = pygame.display.set_mode((width, height))

        start = pygame.Surface((0, 0))
        if not virtual:
            start = start.convert()
        start.fill((0, 0, 0))
        self.background = start
        # Fill background
        self.buffer = pygame.Surface((width, height))
        if not self.virtual:
            self.buffer = self.buffer.convert()
        self.buffer.fill((0, 0, 0))

        self.all_objects = []
        self.event_grab = False
        self.old_dirties = []
        self.new_dirties = []

    def get_width(self):
        return self._width

    def _set_width(self, new_width):
        raise ValueError("Can't change width")

    width = property(get_width, _set_width)

    def get_height(self):
        return self._height

    def _set_height(self, new_height):
        raise ValueError("Can't change height")

    height = property(get_height, _set_height)

    def get_fps(self):
        return self._fps

    def _set_fps(self, new_fps):
        raise ValueError("Can't change fps")

    fps = property(get_fps, _set_fps)

    def get_background(self):
        return self._background

    def set_background(self, new_background):
        self._background = new_background
        self._real_background = pygame.Surface((self.width, self.height))
        if not self.virtual:
            self._real_background = self._real_background.convert()
        self._real_background.fill((0, 0, 0))
        self._real_background.blit(self._background, (0, 0))

    background = property(get_background, set_background)

    def get_all_objects(self):
        return self.all_objects

    def get_event_grab(self):
        return self._event_grab

    def set_event_grab(self, new_status):
        self._event_grab = new_status
        if not self.virtual:
            pygame.event.set_grab(self.event_grab)

    event_grab = property(get_event_grab, set_event_grab)

    # Adds sprite to list of objects on screen.
    def add(self, sprite):
        if isinstance(sprite, Sprite):
            self.all_objects.append(sprite)
            sprite.screen = self
        else:
            raise ValueError("Method 'add' takes Sprite objects not, "
                             + type(sprite) + ".")

    def remove(self, sprite):
        if sprite in self.all_objects:
            self.all_objects.remove(sprite)
            sprite.screen = None

    def clear(self):
        for i in self.all_objects:
            self.remove(i)

    def mainloop(self):
        self.running = True
        # Event loop
        while self.running:
            start = time.time()
            self.old_dirties = self.new_dirties
            self.new_dirties = []
            self.buffer.blit(self._real_background, (0, 0))
            if not self.virtual:
                for event in pygame.event.get():
                    if event.type == pygame.locals.QUIT:
                        self.quit()
                        return
            if keyboard.is_pressed(pygame.locals.K_ESCAPE):
                self.quit()
            for sprite in self.all_objects:
                if not self.running:
                    return
                sprite._process_sprite()
            if not self.running:
                return
            if not self.virtual:
                self.screen_surf.blit(self.buffer, (0, 0))
                pygame.display.update()

            delay = (1.0 / self.fps) - (time.time() - start)
            if delay > 0:
                time.sleep(delay)

    # Stops mainloop()
    def quit(self):
        if self.running:
            self.running = False
            pygame.display.quit()
        else:
            raise ValueError("Can't quit while not running.")


def init(screen_width, screen_height, fps, title, icon, virtual=False):
    global screen, mouse, keyboard, music
    screen = Screen(screen_width, screen_height, fps, title, icon, virtual)
    mouse = Mouse()
    keyboard = Keyboard()
    music = Music()


def load_image(filename, transparent=True):
    image = pygame.image.load(filename)
    if not screen.virtual:
        image = image.convert()
    if transparent:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.locals.RLEACCEL)
    return image


def scale_image(image, x_scale, y_scale=None):
    rect = image.get_rect()
    width = rect.width * x_scale
    if y_scale:
        height = rect.height * y_scale
    else:
        height = rect.height * x_scale
    return pygame.transform.scale(image, (int(round(width)), int(round(height))))


def load_sound(filename):
    return pygame.mixer.Sound(filename)
