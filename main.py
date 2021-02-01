import pygame, random, time

# Global constants
RED = './images/red.png'
RED_CROWN = './images/redcrown.png'
BLUE = './images/blue.png'
BLUE_CROWN = './images/blue crown.png'
PINK = './images/pink.png'
PINK_CROWN = './images/pink crown.png'
CROWN = './images/crown.png'

CROWN_LIST = [RED_CROWN, BLUE_CROWN, PINK_CROWN]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED_COLOUR = (255, 0, 0)
PINK_COLOUR = (255, 0, 255)
BLUE_COLOUR = (0, 255, 255)
SKY_BLUE = (95, 165, 228)
YELLOW = (255, 255, 0)

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800


class Player(pygame.sprite.Sprite):

    # -- Methods
    def __init__(self, image, crown_image):
        """ Constructor function """

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block

        self.image = pygame.image.load(image)
        self.crown_image = crown_image
        self.base_image = image
        self.image = pygame.transform.scale(self.image, (40, 60))

        self.has_crown = False
        self.score = 0

        # self.image.fill(colour)
        # self.colour = colour

        # Set a reference to the image rect.i
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.vel_x = 0
        self.vel_y = 0

        self.level = None

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.vel_x

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.vel_x > 0:
                self.rect.right = block.rect.left
            elif self.vel_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.vel_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
            elif self.vel_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.vel_y = 0

    def hit(self):
        if self.vel_x == 0:
            self.vel_x = random.choice([5, -5])

        if abs(self.vel_x) >= 10:
            self.vel_x = 0

        self.vel_x *= -2
        self.vel_y = -10

    def crown(self, player):

        if self.has_crown:
            self.has_crown = False
            player.has_crown = True
            self.image = pygame.image.load(self.base_image)
            self.image = pygame.transform.scale(self.image, (40, 60))
            player.image = pygame.image.load(player.crown_image)
            player.image = pygame.transform.scale(player.image, (40, 60))

        elif player.has_crown:
            self.has_crown = True
            player.has_crown = False
            self.image = pygame.image.load(self.crown_image)
            self.image = pygame.transform.scale(self.image, (40, 60))
            player.image = pygame.image.load(player.base_image)
            player.image = pygame.transform.scale(player.image, (40, 60))

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.vel_y == 0:
            self.vel_y = 1
        else:
            self.vel_y += .35

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.vel_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.vel_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.vel_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.vel_x = 0


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Crown(pygame.sprite.Sprite):
    """ Crown spawns somewhere random at the start """

    def __init__(self):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.image.load(CROWN)
        self.image = pygame.transform.scale(self.image, (56, 38))
        self.rect = self.image.get_rect()
        self.captured = False

    def crown(self, player):
        player.has_crown = True
        player.image = pygame.image.load(player.crown_image)
        player.image = pygame.transform.scale(player.image, (40, 60))
        self.kill()


class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.player = player

        # TODO: Background image?
        self.background = None

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(SKY_BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [[210, 30, 160, 600],
                 [210, 30, 500, 700],
                 [210, 30, 580, 450],
                 [100, 30, 0, 475],
                 [300, 30, 900, 600]
                 ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


def main():
    """ Main Program """
    pygame.init()
    timerFont = pygame.font.Font(None, 80)
    scoreFont = pygame.font.SysFont("Verdana", 50)

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Crown")

    # Create the player
    player = Player(RED, RED_CROWN)
    player2 = Player(BLUE, BLUE_CROWN)
    player3 = Player(PINK, PINK_CROWN)
    crown = Crown()

    # Create all the levels
    level_list = [Level_01(player), Level_01(player2), Level_01(player3)]

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    playergroup = pygame.sprite.Group()
    player2group = pygame.sprite.Group()
    player3group = pygame.sprite.Group()
    crown_group = pygame.sprite.Group()

    player.level = current_level
    player2.level = current_level
    player3.level = current_level

    player.rect.x = SCREEN_WIDTH / 3
    player.rect.y = SCREEN_HEIGHT - player.rect.height

    player2.rect.x = (SCREEN_WIDTH / 3) * 2
    player2.rect.y = SCREEN_HEIGHT - player.rect.height

    player3.rect.x = SCREEN_WIDTH - 80
    player3.rect.y = SCREEN_HEIGHT - player.rect.height

    crown.rect.x = random.randrange(SCREEN_WIDTH - crown.rect.width)
    crown.rect.y = random.randrange(200, SCREEN_HEIGHT - 400)

    active_sprite_list.add(player)
    active_sprite_list.add(player2)
    active_sprite_list.add(player3)
    active_sprite_list.add(crown)
    crown_group.add(crown)

    playergroup.add(player)

    player2group.add(player2)

    player3group.add(player3)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    timer = 4

    def score():
        if player.has_crown:
            player.score += 1
        elif player2.has_crown:
            player2.score += 1
        elif player3.has_crown:
            player3.score += 1

    # -------- Main Program Loop -----------

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

                if event.key == pygame.K_a:
                    player2.go_left()
                if event.key == pygame.K_d:
                    player2.go_right()
                if event.key == pygame.K_w:
                    player2.jump()

                if event.key == pygame.K_j:
                    player3.go_left()
                if event.key == pygame.K_l:
                    player3.go_right()
                if event.key == pygame.K_i:
                    player3.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.vel_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.vel_x > 0:
                    player.stop()

                if event.key == pygame.K_a and player2.vel_x < 0:
                    player2.stop()
                if event.key == pygame.K_d and player2.vel_x > 0:
                    player2.stop()

                if event.key == pygame.K_j and player3.vel_x < 0:
                    player3.stop()
                if event.key == pygame.K_l and player3.vel_x > 0:
                    player3.stop()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        player_collide1 = pygame.sprite.spritecollideany(player, player2group, collided=None)
        if player_collide1:
            player.hit()
            player2.hit()
            player.crown(player2)

        player_collide2 = pygame.sprite.spritecollideany(player2, player3group, collided=None)
        if player_collide2:
            player2.hit()
            player3.hit()
            player2.crown(player3)

        player_collide3 = pygame.sprite.spritecollideany(player, player3group, collided=None)
        if player_collide3:
            player.hit()
            player3.hit()
            player.crown(player3)

        p1_capture = pygame.sprite.spritecollideany(crown, playergroup, collided=None)
        if p1_capture:
            if not crown.captured:
                crown.crown(player)
                crown.captured = True

        p2_capture = pygame.sprite.spritecollideany(crown, player2group, collided=None)
        if p2_capture:
            if not crown.captured:
                crown.crown(player2)
                crown.captured = True

        p3_capture = pygame.sprite.spritecollideany(crown, player3group, collided=None)
        if p3_capture:
            if not crown.captured:
                crown.crown(player3)
                crown.captured = True

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        if player2.rect.right > SCREEN_WIDTH:
            player2.rect.right = SCREEN_WIDTH

        if player3.rect.right > SCREEN_WIDTH:
            player3.rect.right = SCREEN_WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

        if player2.rect.left < 0:
            player2.rect.left = 0

        if player3.rect.left < 0:
            player3.rect.left = 0

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # Limit to 60 frames per second
        clock.tick(60)

        if timer <= 0:

            done = True

        timer_text = timerFont.render(str(round(timer, 1)), True, BLACK)
        score1_text = scoreFont.render(str(round(player.score, 0)), True, RED_COLOUR)
        score2_text = scoreFont.render(str(round(player2.score, 0)), True, BLUE_COLOUR)
        score3_text = scoreFont.render(str(round(player3.score, 0)), True, PINK_COLOUR)
        screen.blit(timer_text, (550, 70))
        screen.blit(score1_text, (70, 70))
        screen.blit(score2_text, (170, 70))
        screen.blit(score3_text, (270, 70))

        timer -= 0.015

        # add point to player with crown
        score()
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # End Screen
    winner = ""
    winner_colour = BLACK
    if player.score > player2.score:
        if player.score > player3.score:
            winner = "Red Wins!"
            winner_colour = RED_COLOUR
        else:
            winner = "Pink Wins!"
            winner_colour = PINK_COLOUR

    elif player2.score > player.score:
        if player2.score > player3.score:
            winner = "Blue Wins!"
            winner_colour = BLUE_COLOUR
        else:
            winner = "Pink Wins!"
            winner_colour = PINK_COLOUR

    score1 = "Red: " + str(round(player.score, 0))
    score2 = "Blue: " + str(round(player2.score, 0))
    score3 = "Pink: " + str(round(player3.score, 0))
    winner_text = scoreFont.render(winner, True, winner_colour)
    score1_text = scoreFont.render(score1, True, RED_COLOUR)
    score2_text = scoreFont.render(score2, True, BLUE_COLOUR)
    score3_text = scoreFont.render(score3, True, PINK_COLOUR)
    screen.fill(SKY_BLUE)
    screen.blit(winner_text, (550, 200))
    screen.blit(score1_text, (450, 400))
    screen.blit(score2_text, (450, 500))
    screen.blit(score3_text, (450, 600))
    pygame.display.update()
    pygame.time.wait(5000)


    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.

if __name__ == "__main__":
    main()

pygame.quit()
