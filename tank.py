import arcade
import math
import random

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
bullet_scale = 1
bullet_speed = 5
bullet_pts = -1
SW = 800
SH = 600
SPD = 4
TSPD = 2
EXPLOSION_TEXTURE_COUNT = 50
MOVEMENT_SPEED = 2
ANGLE_SPEED = 2.5
wall_scale = 0.5

"""
Instructions page = 0
Level 1 = Map 1
Level 2 = Map 2
Level 3 = Map 3
Level 4 = End of Game
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


class EnemyBullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/rbullet.png", bullet_scale)
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
        self.speed = 0

    def update(self):
        angle_shoot = math.radians(self.angle - 90)
        self.center_x += -self.speed * math.sin(angle_shoot)
        self.center_y += self.speed * math.cos(angle_shoot)

        if self.bottom > SH or self.top < 0 or self.right < 0 or self.left > SW:
            self.kill()


class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)
        self.explosion = arcade.load_sound("sounds/explosion.mp3")
        self.speed = 0

    def update(self):
        angle_shoot = math.radians(self.angle - 90)
        self.center_x += -self.speed*math.sin(angle_shoot)
        self.center_y += self.speed * math.cos(angle_shoot)

        if self.bottom > SH or self.top < 0 or self.right < 0 or self.left > SW:
            self.kill()


# ------MyGame Class--------------
class MyGame(arcade.Window):
    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        self.set_mouse_visible(False)
        self.current_state = 0
        self.gameover = True

        self.explosion_texture_list = []
        for i in range(EXPLOSION_TEXTURE_COUNT):
            texture_name = f"Images/explosions/explosion{i:04}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

    def reset(self):

        if self.current_state == 1:
            self.background = arcade.load_texture("Images/sky1.png")
        if self.current_state == 2:
            self.background = arcade.load_texture("Images/sky2.png")
        if self.current_state == 3:
            self.background = arcade.load_texture("Images/sky3.png")

        # create walls
        self.walls = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()
        coordinate_list = [[212, 500],
                          [276, 500],
                          [336, 500],
                          [400, 500],
                          [464, 500],
                          [528, 500],
                          [592, 500],
                          [656, 500],
                          [720, 500],
                          [720, 436],
                          [720, 372],
                          [720, 308],
                          [720, 244],
                          [720, 180],
                          [720, 116],
                          [80, 500],
                          [80, 436],
                          [80, 372],
                          [80, 308],
                          [80, 244],
                          [80, 180],
                          [80, 116],
                          [144, 116],
                          [208, 116],
                          [272, 116],
                          [336, 116],
                          [400, 116],
                          [464, 116],
                          [528, 116],
                          [592, 116]]
        for coordinate in coordinate_list:
           wall = arcade.Sprite("Images/wall.png", wall_scale)
           wall.center_x = coordinate[0]
           wall.center_y = coordinate[1]
           self.walls.append(wall)
           self.all_sprites.append(wall)

        # for y in range(20):
        #     wall = arcade.Sprite("Images/wall.png", wall_scale)
        #     wall.center_x = random.randint(100, 700)
        #     wall.center_y = random.randint(100, 500)
        #     self.walls.append(wall)
        #     self.all_sprites.append(wall)

        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        self.ebullets = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        # Create our Player
        self.BB8 = Player()
        self.BB8.center_x = SW - 25
        self.BB8.center_y = SH / 2
        self.player_list.append(self.BB8)
        self.all_sprites.append(self.BB8)

        self.Trooper = Trooper()
        self.Trooper.center_x = 25
        self.Trooper.center_y = SH / 2
        self.trooper_list.append(self.Trooper)
        self.all_sprites.append(self.Trooper)

    def on_draw(self):
        arcade.start_render()

        if self.current_state == 0:
            arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Use arrow keys to move BB8 and SPACE to fire. Choose Map 1, 2, 3.", SW / 2, SH / 2 - 30,
                             arcade.color.GHOST_WHITE, 14, align="center", anchor_x="center")
        elif not self.gameover:
            arcade.draw_texture_rectangle(SW // 2, SH // 2, SW, SH, self.background)
            self.player_list.draw()
            self.trooper_list.draw()
            self.bullets.draw()
            self.ebullets.draw()
            self.explosions.draw()
            self.walls.draw()
            self.all_sprites.draw()

        # "Gameover" screen
        else:
            # output = f"Score: {self.score}"
            arcade.draw_rectangle_filled(SW / 2, SH / 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game Over! Choose a level to Play Again.", SW / 2, SH / 2
                             - 30, arcade.color.GHOST_WHITE, 14, align="center", anchor_x="center")
            # arcade.draw_text(output, SW / 2, SH / 2 - 50, arcade.color.GHOST_WHITE, 14, align="center",
            #                  anchor_x="center")

    def on_update(self, dt):
        self.BB8.angle += self.BB8.change_angle
        self.Trooper.angle += self.Trooper.change_angle
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

            # check to see if BB8/Trooper hit wall
            bb8_hit_wall = arcade.check_for_collision_with_list(self.BB8, self.walls)
            if len(bb8_hit_wall) > 0:
                self.BB8.speed = 0
                bb8_hit_wall.clear()
            trooper_hit_wall = arcade.check_for_collision_with_list(self.Trooper, self.walls)
            if len(trooper_hit_wall) > 0:
                self.Trooper.speed = 0
                trooper_hit_wall.clear()

            # check to see if bullets hit wall
            for bullet in self.bullets:
                bullet_hit_wall = arcade.check_for_collision_with_list(bullet, self.walls)
                if len(bullet_hit_wall) > 0:
                    bullet.kill()
                    bullet_hit_wall.clear()
            for ebullet in self.ebullets:
                ebullet_hit_wall = arcade.check_for_collision_with_list(ebullet, self.walls)
                if len(ebullet_hit_wall) > 0:
                    ebullet.kill()
                    ebullet_hit_wall.clear()

            bb8_bombed = arcade.check_for_collision_with_list(self.BB8, self.ebullets)
            if len(bb8_bombed) > 0 and not self.gameover:
                arcade.play_sound(self.BB8.explosion)
                self.BB8.kill()
                bb8_bombed[0].kill()
                self.current_state = 4

            trooper_bombed = arcade.check_for_collision_with_list(self.Trooper, self.bullets)
            if len(trooper_bombed) > 0 and not self.gameover:
                arcade.play_sound(self.BB8.explosion)
                self.BB8.kill()
                trooper_bombed[0].kill()
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
                    self.all_sprites = arcade.SpriteList()

            for ebullet in self.ebullets:
                ebullet_hit_list = arcade.check_for_collision_with_list(ebullet, self.player_list)
                if len(ebullet_hit_list) > 0:
                    arcade.play_sound(ebullet.explosion)
                    ebullet.kill()
                    explosion = Explosion(self.explosion_texture_list)
                    explosion.center_x = ebullet_hit_list[0].center_x
                    explosion.center_y = ebullet_hit_list[0].center_y
                    self.explosions.append(explosion)
                    self.all_sprites = arcade.SpriteList()

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
        elif key == arcade.key.W and not self.gameover:
            self.Trooper.speed = MOVEMENT_SPEED
        elif key == arcade.key.A and not self.gameover:
            self.Trooper.change_angle = ANGLE_SPEED
        elif key == arcade.key.D and not self.gameover:
            self.Trooper.change_angle = -ANGLE_SPEED
        elif key == arcade.key.S and not self.gameover:
            self.Trooper.speed = -MOVEMENT_SPEED
        elif key == arcade.key.P:
            self.reset()
            self.current_state = 0
            # self.score = 0
        elif key == arcade.key.M and not self.gameover:
            self.bullet = Bullet()
            self.bullet.center_x = self.BB8.center_x
            self.bullet.center_y = self.BB8.center_y
            self.bullet.angle = self.BB8.angle + 90
            self.bullet.speed = bullet_speed
            self.bullets.append(self.bullet)
            arcade.play_sound(self.BB8.laser)
        elif key == arcade.key.C and not self.gameover:
            self.ebullet = EnemyBullet()
            self.ebullet.center_x = self.Trooper.center_x
            self.ebullet.center_y = self.Trooper.center_y
            self.ebullet.angle = self.Trooper.angle + 90
            self.ebullet.speed = bullet_speed
            self.ebullets.append(self.ebullet)
            arcade.play_sound(self.Trooper.laser)

        # Level Chooser
        if key == arcade.key.I and self.gameover:
            self.current_state = 0
        elif key == arcade.key.KEY_1 and self.gameover:
            self.current_state = 1
            self.reset()
        elif key == arcade.key.KEY_2 and self.gameover:
            self.current_state = 2
            self.reset()
        elif key == arcade.key.KEY_3 and self.gameover:
            self.current_state = 3
            self.reset()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.BB8.speed = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.BB8.change_angle = 0
        if key == arcade.key.W or key == arcade.key.S:
            self.Trooper.speed = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.Trooper.change_angle = 0


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "Tanks")
    window.reset()
    arcade.run()

# ------Run Main Function-----


if __name__ == "__main__":
    main()
