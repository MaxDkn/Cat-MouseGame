from constantes import *


def get_scaled_height(surface, height):
    return height / SCREEN_HEIGHT_REF * surface.get_height()


def get_scaled_width(surface, width):
    return width / SCREEN_WIDTH_REF * surface.get_width()


def cut_image(x, y, x2, y2, o1, o2, sprite_sheet):
    image = pygame.Surface([x2, y2])
    image.blit(sprite_sheet, (o1, o2), (x, y, x2, y2))
    return image



def load_animations(initial_animations):
    animations = {}
    for animal, animal_sprint_position_and_size_in_sheet in initial_animations.items():
        animations[animal] = {}
        for sprite_type, sprint_position_and_size in animal_sprint_position_and_size_in_sheet.items():
            animations[animal][sprite_type] = []
            sprite_sheet = pygame.image.load(f'{ROOT}/assets/Animal/{animal}/{sprite_type}.png')
            for pos in sprint_position_and_size:
                #  cut the image in the sprite sheet
                image = cut_image(
                    *pos,
                    sprite_sheet,
                )
                #  resize the image
                image = pygame.transform.scale(
                    image,
                    (pos[2] * 2, pos[3] * 2)
                )
                # and remove the black background
                image.set_colorkey([0, 0, 0])
                animations[animal][sprite_type].append(image)
    return animations
