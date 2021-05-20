# Sign your name:Ian
# You will use the starting code below and build the program "BB8 Attack" as you go through Chapter 15.

import random
import arcade

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 40
SW = 800
SH = 600
SP = 4


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
            arcade.play_sound(self.laser_sound)
        elif self.right > SW:
            self.right = SW
            arcade.play_sound(self.laser_sound)
        elif self.top > SH:
            self.top = SH
            arcade.play_sound(self.laser_sound)
        elif self.bottom < 0:
            self.bottom = 0
            arcade.play_sound(self.laser_sound)


class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)

    def update(self):
        pass


# ------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def reset(self):

        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()

        # Scoreboard
        self.score = 0

        # Create our Player
        self.BB8 = Player()
        self.BB8.center_x = SW/2
        self.BB8.center_y = SH / 2
        self.player_list.append(self.BB8)

        # Create a lot of troopers
        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randrange(trooper.w, SW - trooper.w)
            trooper.center_y = random.randrange(trooper.h, SH - trooper.h)
            self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.trooper_list.draw()

        # print the score
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

        # how many troopers are left
        tc = f"Troopers left: {len(self.trooper_list)}"
        arcade.draw_text(tc, 10, 40, arcade.color.BLACK, 14)

    def on_update(self, dt):
        self.player_list.update()
        self.trooper_list.update()

        trooper_hit_list = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
        for trooper in trooper_hit_list:
            trooper.kill()  # order 67
            arcade.play_sound(self.BB8.laser_sound)
            self.score += 1

        if not self.trooper_list:
            self.reset()

        # Controls
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.BB8.change_y = SP
        elif key == arcade.key.LEFT:
            self.BB8.change_x = -SP
        elif key == arcade.key.RIGHT:
            self.BB8.change_x = SP
        elif key == arcade.key.DOWN:
            self.BB8.change_y = -SP

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.BB8.change_y = 0
        elif key == arcade.key.LEFT:
            self.BB8.change_x = 0
        elif key == arcade.key.RIGHT:
            self.BB8.change_x = 0
        elif key == arcade.key.DOWN:
            self.BB8.change_y = 0


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Attack")
    window.reset()
    arcade.run()

# ------Run Main Function-----


if __name__ == "__main__":
    main()
