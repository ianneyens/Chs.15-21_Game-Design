import random
import arcade

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 100
bullet_scale = 1
bullet_speed = 10
SW = 1200
SH = 800
SPD = 4
TSPD = 5


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
        self.laser = arcade.load_sound("sounds/laser.mp3")
        self.explosion = arcade.load_sound("sounds/explosion.mp3")

    def update(self):
        self.center_x += self.change_x

        if self.right < 0:
            self.left = SW
        elif self.left > SW:
            self.right = 0


class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)

    def update(self):
        self.center_y -= TSPD
        if self.top < 0:
            self.center_x = random.randint(self.w, SW - self.w)
            self.center_y = random.randint(SH + self.h, SH * 2)


class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png", bullet_scale)
        self.w = int(self.width)
        self.h = int(self.height)

    def update(self):
        self.center_y += bullet_speed
        if self.bottom > SH:
            self.kill()


# ------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        self.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def reset(self):

        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.gameover = False

        # Scoreboard
        self.score = 0

        # Create our Player
        self.BB8 = Player()
        self.BB8.center_x = SW/2
        self.BB8.center_y = SH / 20
        self.player_list.append(self.BB8)

        # Create a lot of troopers
        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randrange(trooper.w // 2, SW - trooper.w // 2)
            trooper.center_y = random.randrange(SH // 2, SH * 2)
            self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.trooper_list.draw()
        self.bullets.draw()

        # print the score
        the_score = f"Score: {self.score}"
        arcade.draw_text(the_score, SH - 80, SH - 20, arcade.color.BLACK, 14)

        # "Game over" screen
        if self.gameover:
            arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game Over: press P to Play Again", SW / 2 - 110, SH / 2 - 30, arcade.color.GHOST_WHITE)

    def on_update(self, dt):
        self.player_list.update()
        self.trooper_list.update()
        self.bullets.update()

        if not self.trooper_list:
            self.gameover = True

        bb8_hit = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
        if len(bb8_hit) > 0:
            self.BB8.kill()
            arcade.play_sound(self.BB8.explosion)
            self.gameover = True

        for bullet in self.bullets:
            bullet_hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)
            if len(bullet_hit_list) > 0:
                bullet.kill()

                for trooper in bullet_hit_list:
                    trooper.kill()
                    self.score += 2

            if len(self.trooper_list) == 0:
                self.gameover = True

        # Controls
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.BB8.change_y = SPD
        elif key == arcade.key.LEFT:
            self.BB8.change_x = -SPD
        elif key == arcade.key.RIGHT:
            self.BB8.change_x = SPD
        elif key == arcade.key.DOWN:
            self.BB8.change_y = -SPD
        elif key == arcade.key.P:
            self.reset()
        elif key == arcade.key.SPACE and not self.gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.bottom = self.BB8.top
            self.bullet.angle = 90
            self.bullets.append(self.bullet)
            # self.score -= 1
            arcade.play_sound(self.BB8.laser)

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
    window = MyGame(SW, SH, "BB8 Bullets")
    window.reset()
    arcade.run()

# ------Run Main Function-----


if __name__ == "__main__":
    main()
