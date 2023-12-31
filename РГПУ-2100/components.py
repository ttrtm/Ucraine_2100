import pygame


class Area:
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = (30, 144, 255)
        if color:
            self.fill_color = color

    def set_color(self, new_color):
        self.fill_color = new_color

    def fill(self, display_surface):
        pygame.draw.rect(display_surface, self.fill_color, self.rect)

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10, color=None):
        super().__init__(x, y, width, height, color)
        self.image = pygame.image.load(filename)

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


def create_button_image(image_path, width, height):
    button_image = pygame.image.load(image_path)
    button_image = pygame.transform.scale(button_image, (width, height))
    return button_image


class Label(Area):
    def set_text(self, text, font_size=18, text_color=(0, 0, 0)):
        self.text = text
        self.image = pygame.font.SysFont('verdana', font_size).render(text, True, text_color)

    def draw(self, window, shift_x=0, shift_y=0):
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))
