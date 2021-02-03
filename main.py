# Crown
# Fun 3-player game inspired by Crown Capture from Pummel Party
# Instructions:
#      Fight to hold the crown the longest!
#      Capture the crown by making contact with crown, or player holding the crown
#      * Player 1 Moves with "W,A,D"
#      * Player 2 Moves with Arrow Keys
#      * Player 3 Moves with "I,J,L"

import pygame, random

# Global constants

# Images
RED = './images/red.png'
RED_CROWN = './images/redcrown.png'

BLUE = './images/blue.png'
BLUE_CROWN = './images/blue crown.png'

PINK = './images/pink.png'
PINK_CROWN = './images/pink crown.png'

CROWN = './images/crown.png'

BACKGROUND = './images/neon.jpg'
RESULT_BG = './images/result_bg.jpg'

# Define images that hold a crown
CROWN_LIST = [RED_CROWN, BLUE_CROWN, PINK_CROWN]

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORANGEY = (232, 93, 89)
WHITE = (255, 255, 255)
RED_COLOUR = (255, 0, 0)
PINK_COLOUR = (255, 0, 255)
BLUE_COLOUR = (0, 255, 255)
SKY_BLUE = (95, 165, 228)
YELLOW = (255, 255, 0)

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Sounds for game
pygame.mixer.init()
background_song = pygame.mixer.Sound("./sounds/background_song.mp3")

# Hit sounds
hit_sound = pygame.mixer.Sound("./sounds/hit_sound.mp3")
crown_sound = pygame.mixer.Sound("./sounds/crown_sound.mp3")


class Player(pygame.sprite.Sprite):

    # -- Methods
    def __init__(self, image, crown_image):
        """ Constructor function, takes in arguments for
        image of player without crown and with crown"""

        # Call the parent's constructor
        super().__init__()

        # Create an image of the block
        self.image = pygame.image.load(image)

        # store the two images of player so we can switch between them
        self.crown_image = crown_image
        self.base_image = image
        self.image = pygame.transform.scale(self.image, (40, 60))

        # all players start without crown
        self.has_crown = False

        self.score = 0

        # Set a reference to the image rect
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

        # See if we hit platform
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

    # Knockback if collide with another player
    def hit(self):
        # stops game from breaking when landing on top of afk player
        if self.vel_x == 0:
            self.vel_x = random.choice([5, -5])

        # stop collisions from teleporting across the screen
        if abs(self.vel_x) >= 10:
            self.vel_x = 0

        # bump player backwards and up
        self.vel_x *= -2
        self.vel_y = -10

    # Handle transfer of crown between players
    def crown(self, player):

        if self.has_crown:
            self.has_crown = False
            player.has_crown = True

            # Change sprite image to show which player has crown
            self.image = pygame.image.load(self.base_image)
            self.image = pygame.transform.scale(self.image, (40, 60))
            player.image = pygame.image.load(player.crown_image)
            player.image = pygame.transform.scale(player.image, (40, 60))
            pygame.mixer.Sound.play(crown_sound)

        elif player.has_crown:
            self.has_crown = True
            player.has_crown = False

            # Change sprite image to show which player has crown
            self.image = pygame.image.load(self.crown_image)
            self.image = pygame.transform.scale(self.image, (40, 60))
            player.image = pygame.image.load(player.base_image)
            player.image = pygame.transform.scale(player.image, (40, 60))
            pygame.mixer.Sound.play(crown_sound)

        # if both players don't have crown play different sound
        else:
            pygame.mixer.Sound.play(hit_sound)

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
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.vel_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left designated button. """
        self.vel_x = -6

    def go_right(self):
        """ Called when the user hits the right designated button. """
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
        self.image.fill(ORANGEY)

        self.rect = self.image.get_rect()


class Crown(pygame.sprite.Sprite):
    """ Crown spawns at start of the game"""

    def __init__(self):

        super().__init__()

        self.image = pygame.image.load(CROWN)
        self.image = pygame.transform.scale(self.image, (56, 38))
        self.rect = self.image.get_rect()

        # captured argument prevents crown from being captured infinitely
        self.captured = False

    # Give crown to player who makes contact with crown
    def crown(self, player):
        player.has_crown = True
        player.image = pygame.image.load(player.crown_image)
        player.image = pygame.transform.scale(player.image, (40, 60))
        pygame.mixer.Sound.play(crown_sound)

        # Remove crown sprite from screen
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

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the platforms
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

    # Fonts for score text and timer text
    timerFont = pygame.font.Font(None, 80)
    scoreFont = pygame.font.SysFont("Verdana", 50)

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    # Variables for background
    background_image = pygame.image.load(BACKGROUND).convert()
    result_bg = pygame.image.load(RESULT_BG).convert()

    # Play background song
    pygame.mixer.Sound.play(background_song)

    # Title of game
    pygame.display.set_caption("Crown")

    # Create the players and crown
    player = Player(RED, RED_CROWN)
    player2 = Player(BLUE, BLUE_CROWN)
    player3 = Player(PINK, PINK_CROWN)
    crown = Crown()

    # Create the levels with the controllable players
    level_list = [Level_01(player), Level_01(player2), Level_01(player3)]

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    # initialize sprite groups needed
    active_sprite_list = pygame.sprite.Group()
    playergroup = pygame.sprite.Group()
    player2group = pygame.sprite.Group()
    player3group = pygame.sprite.Group()
    crown_group = pygame.sprite.Group()

    player.level = current_level
    player2.level = current_level
    player3.level = current_level

    # Spawn in each player
    player.rect.x = SCREEN_WIDTH / 3
    player.rect.y = SCREEN_HEIGHT - player.rect.height

    player2.rect.x = (SCREEN_WIDTH / 3) * 2
    player2.rect.y = SCREEN_HEIGHT - player.rect.height

    player3.rect.x = SCREEN_WIDTH - 80
    player3.rect.y = SCREEN_HEIGHT - player.rect.height

    # Crown spawns somewhere random, but within reach of players
    crown.rect.x = random.randrange(SCREEN_WIDTH - crown.rect.width)
    crown.rect.y = random.randrange(300, SCREEN_HEIGHT - 400)

    active_sprite_list.add(player)
    active_sprite_list.add(player2)
    active_sprite_list.add(player3)
    active_sprite_list.add(crown)
    crown_group.add(crown)

    # individual sprite groups for collision to work
    playergroup.add(player)
    player2group.add(player2)
    player3group.add(player3)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Timer to end game when finished
    timer = 45

    # update score while a player holds the crown
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

            # Player 1 controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

                # Player 2 controls
                if event.key == pygame.K_a:
                    player2.go_left()
                if event.key == pygame.K_d:
                    player2.go_right()
                if event.key == pygame.K_w:
                    player2.jump()

                # Player 3 controls
                if event.key == pygame.K_j:
                    player3.go_left()
                if event.key == pygame.K_l:
                    player3.go_right()
                if event.key == pygame.K_i:
                    player3.jump()

            # Stop player movement when they let go of keys
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

        # Update the players
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # Handle collisions for each player
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

        # Handle capturing of crown at the start of the game
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

        # Stop player from running outside screen
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        if player2.rect.right > SCREEN_WIDTH:
            player2.rect.right = SCREEN_WIDTH

        if player3.rect.right > SCREEN_WIDTH:
            player3.rect.right = SCREEN_WIDTH

        if player.rect.left < 0:
            player.rect.left = 0

        if player2.rect.left < 0:
            player2.rect.left = 0

        if player3.rect.left < 0:
            player3.rect.left = 0

        # Limit to 60 frames per second
        clock.tick(60)

        if timer <= 0:
            done = True

        # Text strings for timer and scores
        timer_text = timerFont.render(str(round(timer, 1)), True, WHITE)
        score1_text = scoreFont.render(str(round(player.score, 0)), True, RED_COLOUR)
        score2_text = scoreFont.render(str(round(player2.score, 0)), True, BLUE_COLOUR)
        score3_text = scoreFont.render(str(round(player3.score, 0)), True, PINK_COLOUR)

        # Background image
        screen.blit(background_image, [0, 0])
        # Show timer and scores on screen
        screen.blit(timer_text, (550, 70))
        screen.blit(score1_text, (50, 70))
        screen.blit(score2_text, (170, 70))
        screen.blit(score3_text, (290, 70))

        # Draw Screen
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # reduce timer
        timer -= 0.015

        # add points to player with crown
        score()
        # Update the screen with what we've drawn.
        pygame.display.flip()

    # End Screen

    # initialize winner variables
    winner = ""
    winner_colour = BLACK

    # Determine winner
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

    # Format the scores into strings
    score1 = "Red: " + str(round(player.score, 0))
    score2 = "Blue: " + str(round(player2.score, 0))
    score3 = "Pink: " + str(round(player3.score, 0))

    # Text strings for results
    winner_text = scoreFont.render(winner, True, winner_colour)
    score1_text = scoreFont.render(score1, True, RED_COLOUR)
    score2_text = scoreFont.render(score2, True, BLUE_COLOUR)
    score3_text = scoreFont.render(score3, True, PINK_COLOUR)

    # Clear Screen and show results
    screen.blit(result_bg, [0, 0])
    screen.blit(winner_text, (450, 100))
    screen.blit(score1_text, (450, 300))
    screen.blit(score2_text, (450, 400))
    screen.blit(score3_text, (450, 500))
    pygame.display.update()

    # Give time for users to look at scores before quitting
    pygame.time.wait(5000)


if __name__ == "__main__":
    main()

pygame.quit()
