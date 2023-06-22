import pygame
from components import Picture

pygame.init()

# Розміри вікна
width = 1280
height = 720

# Ініціалізація вікна
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("РГПУ-2100")
clock = pygame.time.Clock()

# Фон та кольори
background_color = (0, 255, 255)  # Голубий
platform_color = (0, 255, 0)  # Зелений

# об'єкти для початкового меню
menu_start_button = Picture("graphics/menu_start_button.png", 550, 300, width=160, height=160)
darken_start_button = Picture("graphics/dark_menu_start_button.png", 550, 300, width=160, height=160)

menu_settings_button = Picture("graphics/menu_settings.png", 450, 550, width=110, height=110)
darken_settings_button = Picture("graphics/dark_menu_settings.png", 450, 550, width=110, height=110)

menu_credits_button = Picture("graphics/menu_credits.png", 700, 550, width=110, height=110)
darken_credits_button = Picture("graphics/dark_menu_credits.png", 700, 550, width=110, height=110)

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
        self.jump_power = 12  # Сила стрибка
        self.gravity = 1  # Гравітація
        self.on_ground = False  # Флаг, що вказує, чи перебуває гравець на землі
        self.jumps_remaining = 2  # Кількість можливих стрибків

    def draw(self, window):
        window.blit(player_image, (self.x, self.y))
    def move_left(self):
        self.vel_x = -5

    def move_right(self):
        self.vel_x = 5

    def stop_moving(self):
        self.vel_x = 0

    def jump(self):
        if self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
            self.jumps_remaining -= 1
        elif self.jumps_remaining >= 1:
            self.vel_y = -self.jump_power
            self.jumps_remaining -= 1

    def update(self):
        self.vel_y += self.gravity
        self.x += self.vel_x
        self.y += self.vel_y

        for platform in platforms:
            if self.y + self.size >= platform.y:
                self.y = platform.y - self.size
                self.vel_y = 0
                self.on_ground = True
                self.jumps_remaining = 2

    def check_collision(self, platform):
        return pygame.Rect(self.x, self.y, self.size, self.size).colliderect(platform)


# NPC
class NPC:
    def __init__(self, x, y, size, color, message):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.message = message
        self.display_message = False

    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, self.size, self.size))

    def show_message(self, window):
        font = pygame.font.Font(None, 30)
        text = font.render(self.message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height - 50))
        window.blit(text, text_rect)

    def check_collision(self, player):
        if pygame.Rect(self.x, self.y, self.size, self.size).colliderect(
                pygame.Rect(player.x, player.y, player.size, player.size)
        ):
            self.display_message = True
        else:
            self.display_message = False


# Ініціалізація персонажа
player_size = 50
player = Player(width // 2 - player_size // 2, height // 2 - player_size // 2, player_size, (0, 0, 255))

# Ініціалізація НПС
npc = NPC(50, 640, 60, (255, 0, 0), "Ти повинен донести прапор. Не втрать його.")

# Платформи
platforms = [
    pygame.Rect(0, height - 20, width, 40),  # Платформа знизу
]

# Головний цикл гри
running = True
full_screen = False
screen = "menu"
following = False  # Флаг, що вказує, чи слідкує камера за гравцем

while running:
    window.fill(background_color)

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if menu_settings_button.rect.collidepoint(x, y):
                    screen = "settings"
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if menu_credits_button.rect.collidepoint(x, y):
                    screen = "credits"
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if menu_start_button.rect.collidepoint(x, y):
                    screen = "game"
                    following = True  # Початок слідкування за гравцем

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button.rect.collidepoint(x, y):
                    screen = "menu"

        # Вихід
        mouse_pos = pygame.mouse.get_pos()
        if back_button.rect.collidepoint(mouse_pos):
            darken_back_button.draw(window)
        else:
            back_button.draw(window)

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
            if event.type == pygame.MOUSEBUTTONDOWN:
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
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_SPACE:
                    player.jump()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop_moving()

        # Оновлення персонажа
        player.update()

        # Перевірка колізій з платформами
        for platform in platforms:
            if player.check_collision(platform):
                player.on_ground = True
                break
        else:
            player.on_ground = False

        # Перевірка колізії з NPC
        npc.check_collision(player)

        # Малювання NPC
        npc.draw(window)

        # Малювання персонажа
        player.draw(window)

        # Малювання платформ
        for platform in platforms:
            pygame.draw.rect(window, platform_color, platform)
            
        # Показ повідомлення NPC
        if npc.display_message:
            npc.show_message(window)

        # Слідкування за гравцем
        if following:
            if player.x > width / 2:
                camera_x = player.x - width / 2
                player.x -= camera_x
                for platform in platforms:
                    platform.x -= camera_x
                npc.x -= camera_x
            elif player.x < width / 4:
                camera_x = player.x - width / 4
                player.x -= camera_x
                for platform in platforms:
                    platform.x -= camera_x
                npc.x -= camera_x

    pygame.display.update()
    clock.tick(60)

pygame.quit()
