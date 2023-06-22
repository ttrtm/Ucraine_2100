import pygame
from components import *

# Ініціалізація Pygame
pygame.init()

# Розміри вікна
width = 1280
height = 720

# Ініціалізація вікна
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("РГПУ-2100")
clock = pygame.time.Clock()

# Фон та кольори
blue = (0, 255, 255)
brown = (153, 51, 0)
green = (124, 252, 0)

# об'єкти для початкового меню
menu_start_button = Picture("graphics/menu_start_button.png", 550, 300, width=160, height=160)
darken_start_button = Picture("graphics/dark_menu_start_button.png", 550, 300, width=160, height=160)

menu_settings_button = Picture("graphics/menu_settings.png", 425, 450, width=110, height=110)
darken_settings_button = Picture("graphics/dark_menu_settings.png", 425, 450, width=110, height=110)

menu_credits_button = Picture("graphics/menu_credits.png", 575, 550, width=110, height=110)
darken_credits_button = Picture("graphics/dark_menu_credits.png", 575, 550, width=110, height=110)

menu_exit_button = Picture("graphics/exit_button.png", 725, 450, width=110, height=110)
darken_exit_button = Picture("graphics/dark_exit_button.png", 725, 450, width=110,height=110)

#об'єкти для налаштувань
how_to_play = Label(25,125,100,50)
how_to_play.set_text("Донесіть прапор до фінішу, натискаючи на клавіші, які будуть появлятись на екрані, для того щоб стрибати по платформах")

something_to_dramatize = Label(25,200,100,50)
something_to_dramatize.set_text("Прапор потрібен зверху. Донесіть туди його, де він потрібен.")


# універсальні об'єкти
back_button = Picture("graphics/back_button.png", 40, 30, width=95, height=75)
darken_back_button = Picture("graphics/dark_back_button.png", 40, 30, width=95, height=75)

# Клас для головного персонажа
player_image = pygame.image.load("graphics/player.png")
player_image = pygame.transform.scale(player_image, (50, 50))


class Player:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = 650
        self.size = size
        self.color = color
        self.vel_x = 0  # Швидкість руху по горизонталі
        self.vel_y = 0  # Швидкість руху по вертикалі
        self.jump_power = 15  # Сила стрибка
        self.gravity = 1  # Гравітація
        self.jumps_remaining = 2  # Кількість можливих стрибків

        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window):
        window.blit(player_image, (self.x, self.y))

    def jump(self):
        if self.on_ground or self.jumps_remaining >= 2:
            self.vel_y = -self.jump_power
            self.on_ground = False
            self.jumps_remaining -= 1

    def move_left(self):
        self.vel_x = -5

    def move_right(self):
        self.vel_x = 5

    def stop_moving(self):
        self.vel_x = 0

    def update(self):
        self.vel_y += self.gravity
        self.x += self.vel_x
        self.y += self.vel_y

        # Перевірка колізії з нижньою платформою
        if self.y + self.size >= platforms[0].y:
            self.y = platforms[0].y - self.size
            self.vel_y = 0
            self.on_ground = True
            self.jumps_remaining = 2
        else:
            self.on_ground = False

        # Перевірка колізії з рухомими платформами
        if self.x < 0:
            self.x = 0
        elif self.x + self.size > width:
            self.x = width - self.size





    def check_collision(self, platform):
        if self.rect.colliderect(platform.rect):
            self.stop_moving()
            if self.vel_y > 0:
                self.y = platform.y - self.size
                self.vel_y = 0
                self.on_ground = True
                self.jumps_remaining = 2

class MovingPlatform:
    def __init__(self, x, y, width, height, speed, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = direction  # Напрямок руху платформи (1 - праворуч, -1 - ліворуч)

    def draw(self, window):
        pygame.draw.rect(window, brown, self.rect)

    def update(self):
        self.rect.x += self.speed * self.direction

        if self.rect.left <= 0 or self.rect.right >= width:
            self.direction *= -1

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)



# Ініціалізація персонажа
player_size = 50
player = Player(width // 2 - player_size // 2, height // 2 - player_size // 2, player_size, (0, 0, 255))

# Платформи
platforms = [
    pygame.Rect(0, height - 20, width, 40),  # Платформа знизу
]

# Рухомі платформи
moving_platforms = [
    MovingPlatform(600, 600, 65, 15, 2, 1),
    MovingPlatform(600, 500, 65, 15, 2, -1.5),
    MovingPlatform(600, 400, 80, 15, 2, 2),
    MovingPlatform(600, 300, 65, 15, 2, 1) 
]



# Головний цикл гри
running = True
full_screen = False
screen = "menu"

while running:
    window.fill(blue)

    if screen == "menu":
        for event in pygame.event.get():
            # вихід
            if event.type == pygame.QUIT:
                running = False

            # зміна форми вікна
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if menu_settings_button.rect.collidepoint(x, y):
                    screen = "settings"
                elif menu_credits_button.rect.collidepoint(x, y):
                    screen = "credits"
                elif menu_start_button.rect.collidepoint(x, y):
                    screen = "game"
                elif menu_exit_button.rect.collidepoint(x,y):
                    running = False
                

        # Кнопка старту
        mouse_pos = pygame.mouse.get_pos()
        if menu_start_button.rect.collidepoint(mouse_pos):
            darken_start_button.draw(window)
        else:
            menu_start_button.draw(window)

        # Кнопка налаштування
        if menu_settings_button.rect.collidepoint(mouse_pos):
            darken_settings_button.draw(window)
        else:
            menu_settings_button.draw(window)

        # Кнопка credits
        if menu_credits_button.rect.collidepoint(mouse_pos):
            darken_credits_button.draw(window)
        else:
            menu_credits_button.draw(window)
        
        #кнопка виходу з гри
        if menu_exit_button.rect.collidepoint(mouse_pos):
            darken_exit_button.draw(window)
        else:
            menu_exit_button.draw(window)

    elif screen == "settings":
        for event in pygame.event.get():
            # вихід
            if event.type == pygame.QUIT:
                running = False

            # зміна форми вікна
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button.rect.collidepoint(x, y):
                    screen = "menu"

        # Вихід
        mouse_pos = pygame.mouse.get_pos()
        if back_button.rect.collidepoint(mouse_pos):
            darken_back_button.draw(window)
        else:
            back_button.draw(window)
        
        how_to_play.draw(window)
        something_to_dramatize.draw(window)

    elif screen == "credits":
        for event in pygame.event.get():
            # вихід
            if event.type == pygame.QUIT:
                running = False

            # зміна форми вікна
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button.rect.collidepoint(x, y):
                    screen = "menu"

        # Вихід
        mouse_pos = pygame.mouse.get_pos()
        if back_button.rect.collidepoint(mouse_pos):
            darken_back_button.draw(window)
        else:
            back_button.draw(window)
        # Автори

    elif screen == "game":
        for event in pygame.event.get():
            # вихід
            if event.type == pygame.QUIT:
                running = False

            # зміна форми вікна
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        window = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        window = pygame.display.set_mode((width, height), pygame.RESIZABLE)

                # рух персонажа
                if event.key == pygame.K_SPACE:
                    player.jump()

                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_SPACE:
                    player.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop_moving()

        
        for platform in platforms:
            pygame.draw.rect(window, green, platform)

        #оновлення платформ
        for platform in moving_platforms:
            platform.draw(window)

        # Оновлення персонажа
        player.update()
        # Відображення персонажа
        player.draw(window)

        pygame.draw.rect(window, green, platform)

       # Оновлення рухомих платформ
        for platform in moving_platforms:
            platform.update()
            platform.check_collision(player)
            platform.draw(window)

    pygame.display.update()
    clock.tick(60)

# Завершення гри
pygame.quit()
