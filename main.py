# Tre Howard
# 9/13/23
# CSC285 - Python Programming II

import pygame
import sys
import os

# --------- initialization ---------
pygame.init()
pygame.mixer.init()

# screen size (this changes the SCREEN size, not the IMAGE size)
# all images in directory are 351x351
screen_width = 351
screen_height = 351

# creates the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AI Image Viewer")

# variables for font
font = pygame.font.Font(None, 36)
font_color = (255, 255, 255)

# variables for game (time/images)
next_image_time = 0  # how long until change image
index = 0  # index for image list below
my_images = []  # creates empty image list

# variables for sound
pygame.mixer.music.load("Superhero_background.wav")  # load the music into the program
pygame.mixer.music.play(-1)  # (-1) makes it loop infinitely
pygame.mixer.music.set_volume(0.1)  # set volume to .1

# --------- functions ---------

# function to fill up empty image list with local directory
def get_images(directory_path):
    try:
        # grabs all the files in the specified directory (same location as the python script)
        file_list = os.listdir(directory_path)

        # include only images
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        my_images = [os.path.join(directory_path, file) for file in file_list if os.path.splitext(file)[1].lower()
                     in image_extensions]

        return my_images
    except Exception as e:
        print(f"Error has occurred: {str(e)}")
        return []


# function to load and display the next image
def loop_picture(images):
    global index
    if len(images) == 0:  # if list is empty, return and do nothing
        return

    # load the image using pygame.image.load
    image = pygame.image.load(images[index])

    # get the size of the image
    image_width, image_height = image.get_size()

    # initial position of image (centers it basically)
    x, y = (screen_width - image_width) // 2 , (screen_height - image_height) // 2

    # clear screen
    screen.fill((0, 0, 0))

    # draw image
    screen.blit(image, (x, y))

    # create text surface/area and apply image name
    image_name = os.path.basename(images[index])
    text_surface = font.render(image_name, True, font_color)

    # set position for text on screen
    text_x = (screen_width - text_surface.get_width()) // 2
    text_y = y + image_height - 30

    # draw text surface
    screen.blit(text_surface, (text_x, text_y))

    # update display
    pygame.display.flip()

    # adds 1 to index so next image will load when ran again
    index += 1

    # if over max in list, place index back to first image (0)
    if index >= len(images):
        index = 0


# --------- game loop ---------

# get images from local directory, add them to empty image list above
my_images = get_images(os.path.dirname(__file__))

# run until quit/escape
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:  # go back an image
                index = (index + 1) % len(my_images)
                next_image_time = 0
                loop_picture(my_images)

                sound = pygame.mixer.Sound("Leftbuttonclick.wav")
                sound.play()
            elif event.key == pygame.K_RIGHT:  # go forward an image
                index = (index - 1) % len(my_images)
                next_image_time = 0
                loop_picture(my_images)

                sound = pygame.mixer.Sound("Rightbuttonclick.wav")
                sound.play()

    # checks when to switch
    current_time = pygame.time.get_ticks()
    if current_time > next_image_time and my_images:
        loop_picture(my_images)
        next_image_time = current_time + 3000


    # if sound variable is true or if sound ends, play again
    # code here

# quit game/application/program
pygame.quit()
sys.exit()
