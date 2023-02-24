import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.graphics import Rectangle, Color
from kivy.uix.button import Button
import time


def collides(r1, r2):
    r1x = r1[0][0]
    r1y = r1[0][1]
    r2x = r2[0][0]
    r2y = r2[0][1]
    r1w = r1[1][0]
    r1h = r1[1][1]
    r2w = r2[1][0]
    r2h = r2[1][1]
    if r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y:
        return True
    else:
        return False


class Board(Widget):
    velocity_x = NumericProperty(0)
    rect = Rectangle(source='./board.png', pos=(100, Window.height / 32.), size=(248, 24))

    def move(self):
        x = self.rect.pos[0]
        y = self.rect.pos[1]
        x = self.velocity_x + x
        self.rect.pos = (x, y)


class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    rect = Rectangle(source='./ball.png', pos=(
        Window.width / 2.0, Window.height / 2. + 24), size=(22, 22))

    def move(self):
        x = self.rect.pos[0]
        y = self.rect.pos[1]
        x = self.velocity_x + x
        y = self.velocity_y + y
        self.rect.pos = (x, y)


class GameControl(Widget):
    ball = Ball()
    board = Board()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        # with self.canvas.before:
        #     Rectangle(pos=self.pos, size=(Window.width, Window.height))
        #     Color(rgba=(1, 1, 1, 1))
        with self.canvas:
            self.board.rect = Rectangle(source='./board.png', pos=(100, Window.height / 32.), size=(248, 24))
            self.ball.rect = Rectangle(source='./ball.png', pos=(
                (self.board.pos[0] + 248) / 2., Window.height / 2. + 24), size=(22, 22))
        # self.button = Button(size_hint=(None, None), text='Start', on_release=self.ball_move)
        self.keys_pressed = set()
        self.ball.velocity_x = 5
        self.ball.velocity_y = 5
        self.board.velocity_x = 10
        Clock.schedule_interval(self.move_step_board, 0)
        Clock.schedule_interval(self.move_step_ball, 0)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifier):
        self.keys_pressed.add(keycode[1])

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in self.keys_pressed:
            self.keys_pressed.remove(keycode[1])

    def move_step_board(self, delta_time):
        # self.board.move()
        pos_x = self.board.rect.pos[0]
        pos_y = self.board.rect.pos[1]
        if 'd' in self.keys_pressed:
            pos_x += self.board.velocity_x
        if 'a' in self.keys_pressed:
            pos_x -= self.board.velocity_x
        self.board.rect.pos = (pos_x, pos_y)

    def move_step_ball(self, delta_time):

        self.ball.move()
        if collides((self.board.rect.pos, self.board.rect.size), (self.ball.rect.pos, self.ball.rect.size)):
            self.ball.velocity_x *= -1
            self.ball.velocity_y *= -1
        if self.ball.rect.pos[1] < self.y or self.ball.rect.pos[1] > self.top:
            self.ball.velocity_y *= -1
        if self.ball.rect.pos[0] < self.x or self.ball.rect.pos[0] > self.width:
            self.ball.velocity_x *= -1


class Main(App):

    def build(self):
        return GameControl()


if __name__ == '__main__':
    app = Main()
    app.run()
