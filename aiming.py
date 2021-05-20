import random
import arcade
import math

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
bullet_scale = 1
bullet_speed = 10
bullet_pts = -1
trooper_pts = 1
SW = 1000
SH = 800
SPD = 4
TSPD = 2
EXPLOSION_TEXTURE_COUNT = 50
MOVEMENT_SPEED = 5
ANGLE_SPEED = 5

"""
Instructions page = 0
Level 1 = 10
Level 2 = 15
Level 3 = 20
Level 4 = 25
Level 5 = 30
Level 6 = 35
Level 7 = 40
Level 8 = 45
Level 9 = 50
Level 10 = 100
End of Game = 11
"""


class Explosion(arcade.Sprite):
    def __init__(self, texture_list):
        super().__init__("Images/explosions/explosion0000.png")

        self.current_texture = 0
        self.textures = texture_list
        self.explosion_sound = arcade.load_sound("sounds/explosion.mp3")

    def update(self):
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
        self.laser = arcade.load_sound("sounds/laser.mp3")
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
        self.speed = 0
        self.change_angle = 0

    def update(self):
        self.angle += self.change_x
        angle_rad = math.radians(self.angle)
        self.center_x += -self.speed*math.sin(angle_rad)
        self.center_y += self.speed*math.cos(angle_rad)

        if self.left < 0:
            self.left = 0
        elif self.right > SW:
            self.right = SW
        elif self.top > SH:
            self.top = SH
        elif self.bottom < 0:
            self.bottom = 0


class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)
        self.dx = random.randrange(-1, 2, 2)
        self.dy = random.randrange(-1, 2, 2)

    def update(self):
        self.center_y += self.dy
        self.center_x += self.dx

        if self.top > SH or self.bottom < 0:
            self.dy *= -1
        elif self.right > SW or self.left < 0:
            self.dx *= -1


class EnemyBullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png", bullet_scale)
        self.angle_list = [0, 90, 180, 270]
        self.angle = random.choice(self.angle_list)

    def update(self):
        if self.angle == 0:
            self.center_x += bullet_speed
        elif self.angle == 90:
            self.center_y += bullet_speed
        elif self.angle == 180:
            self.center_x -= bullet_speed
        elif self.angle == 270:
            self.center_y -= bullet_speed

        if self.top < 0 or self.bottom > SH or self.right < 0 or self.left > SW:
            self.kill()


class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
        self.speed = 0

    def update(self):
        angle_shoot = math.radians(self.angle - 90)
        self.center_x += -self.speed * math.sin(angle_shoot)
        self.center_y += self.speed * math.cos(angle_shoot)

        if self.bottom > SH or self.top < 0 or self.right < 0 or self.left > SW:
            self.kill()


# ------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        self.score = 0
        self.set_mouse_visible(False)
        self.current_state = 0
        self.trooper_count = 0
        self.gameover = True

        self.explosion_texture_list = []
        for i in range(EXPLOSION_TEXTURE_COUNT):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def reset(self):

        if self.current_state == 1:
            self.background = arcade.load_texture("Images/sky1.png")
            self.trooper_count = 5
        if self.current_state == 2:
            self.background = arcade.load_texture("Images/sky2.png")
            self.trooper_count = 10
        if self.current_state == 3:
            self.background = arcade.load_texture("Images/sky3.png")
            self.trooper_count = 15

        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.ebullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()

        # Create our Player
        self.BB8 = Player()
        self.BB8.center_x = SW / 2
        self.BB8.center_y = SH / 2
        self.player_list.append(self.BB8)

        # Create a lot of troopers
        for i in range(self.trooper_count):
            trooper = Trooper()

            if i % 2 == 0:
                trooper.center_x = random.randrange(trooper.w, int(SW / 3))
            else:
                trooper.center_x = random.randrange(int(SW * 2 / 3), SW - trooper.w)

            trooper.center_y = random.randrange(trooper.h, SH - trooper.h)
            self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()

        if self.current_state == 0:
            arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Use arrow keys to move BB8 and SPACE to fire. Choose level 1, 2, 3.", SW / 2, SH / 2 - 30,
                             arcade.color.GHOST_WHITE, 14, align="center", anchor_x="center")
        elif not self.gameover:
            arcade.draw_texture_rectangle(SW // 2, SH // 2, SW, SH, self.background)
            self.player_list.draw()
            self.trooper_list.draw()
            self.bullets.draw()
            self.ebullets.draw()
            self.explosions.draw()

            # print the score
            arcade.draw_lrtb_rectangle_filled(SW - 95, SW, SH, SH - 35, arcade.color.WHITE)
            the_level = f"Level: {self.current_state}"
            arcade.draw_text(the_level, SW - 90, SH - 20, arcade.color.BLACK, 14)
            the_score = f"Score: {self.score}"
            arcade.draw_text(the_score, SW - 90, SH - 35, arcade.color.BLACK, 14)

        # "Gameover" screen
        else:
            output = f"Score: {self.score}"
            arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game Over! Choose a level to Play Again.", SW / 2, SH / 2
                             - 30, arcade.color.GHOST_WHITE, 14, align="center", anchor_x="center")
            arcade.draw_text(output, SW / 2, SH / 2 - 50, arcade.color.GHOST_WHITE, 14, align="center",
                             anchor_x="center")

    def on_update(self, dt):
        self.BB8.angle += self.BB8.change_angle
        if 0 < self.current_state < 4:
            self.gameover = False
        else:
            self.gameover = True

        if not self.gameover:
            self.player_list.update()
            self.trooper_list.update()
            self.bullets.update()
            self.ebullets.update()
            self.explosions.update()

            if not self.trooper_list:
                self.gameover = True

            # detect BB8 colliding with trooper
            bb8_hit = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
            if len(bb8_hit) > 0 and not self.gameover:
                self.BB8.kill()
                arcade.play_sound(self.BB8.explosion)
                self.current_state = 4

            # randomly shoot bombs
            for trooper in self.trooper_list:
                if random.randrange(1000) == 0 and not self.gameover:
                    ebullet = EnemyBullet()
                    ebullet.center_x = trooper.center_x
                    ebullet.center_y = trooper.center_y
                    self.ebullets.append(ebullet)

            bb8_bombed = arcade.check_for_collision_with_list(self.BB8, self.ebullets)
            if len(bb8_bombed) > 0 and not self.gameover:
                arcade.play_sound(self.BB8.explosion)
                self.BB8.kill()
                bb8_bombed[0].kill()
                self.current_state = 4

            for bullet in self.bullets:
                bullet_hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)
                if len(bullet_hit_list) > 0:
                    arcade.play_sound(bullet.explosion)
                    bullet.kill()
                    explosion = Explosion(self.explosion_texture_list)
                    explosion.center_x = bullet_hit_list[0].center_x
                    explosion.center_y = bullet_hit_list[0].center_y
                    self.explosions.append(explosion)

                for trooper in bullet_hit_list:
                    trooper.kill()
                    self.score += trooper_pts

                if len(self.trooper_list) == 0:
                    self.current_state += 1
                    self.reset()

    # Controls
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and not self.gameover:
            self.BB8.speed = MOVEMENT_SPEED
        elif key == arcade.key.LEFT and not self.gameover:
            self.BB8.change_angle = ANGLE_SPEED
        elif key == arcade.key.RIGHT and not self.gameover:
            self.BB8.change_angle = -ANGLE_SPEED
        elif key == arcade.key.DOWN and not self.gameover:
            self.BB8.speed = -MOVEMENT_SPEED
        elif key == arcade.key.P:
            self.reset()
            self.current_state = 0
            self.score = 0
        elif key == arcade.key.SPACE and not self.gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.center_y = self.BB8.center_y
            self.bullet.angle = self.BB8.angle + 90
            self.bullet.speed = bullet_speed
            self.bullets.append(self.bullet)
            arcade.play_sound(self.BB8.laser)

        # Level Chooser
        if key == arcade.key.I and self.gameover:
            self.current_state = 0
            self.score = 0
        elif key == arcade.key.KEY_1 and self.gameover:
            self.current_state = 1
            self.score = 0
            self.reset()
        elif key == arcade.key.KEY_2 and self.gameover:
            self.current_state = 2
            self.score = 0
            self.reset()
        elif key == arcade.key.KEY_3 and self.gameover:
            self.current_state = 3
            self.score = 0
            self.reset()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.BB8.speed = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.BB8.change_angle = 0


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Aiming")
    window.reset()
    arcade.run()

# ------Run Main Function-----


if __name__ == "__main__":
    main()
