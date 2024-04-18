import pygame, sys
from pygame.locals import *
import time
import math
import mysql.connector
from utils import scale_image, blit_rotate_center, blit_text_center

pygame.font.init()

pygame.init()

# Ekran boyutunu ve başlığını belirle
map = scale_image(pygame.image.load('images/harita.png'), 0.9)
screen_width = map.get_width()
screen_height = map.get_height()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Araba Yarışı")
background_image = pygame.image.load('images/arkaplan2.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
grass = scale_image(pygame.image.load('images/cimen.jpg'), 2.5)
mapborder = scale_image(pygame.image.load('images/Yolkenar.png'), 0.9)
mapbordermask = pygame.mask.from_surface(mapborder)
finish = pygame.image.load('images/bitis.png')
finishmask = pygame.mask.from_surface(finish)
finish_position = (130, 250)
redcar = scale_image(pygame.image.load('images/Kırmızıaraba.png'), 0.55)
greencar = scale_image(pygame.image.load('images/Yesilaraba.png'), 0.55)
WIDTH, HEIGHT = map.get_width(), map.get_height()
MAIN_FONT = pygame.font.SysFont("arialblack", 33)
skorpage = pygame.image.load('images/sss.jpg')
skorpage = pygame.transform.scale(skorpage, (screen_width, screen_height))
FPS = 60
PATH = PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551),
               (613, 715), (736, 713),
               (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377),
               (176, 388), (178, 260)]


class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)


muzik = pygame.mixer.Sound('./sounds/music.mp3')
muzik.play(-1)

font_name = pygame.font.get_default_font()
info_font = pygame.font.SysFont(font_name, 60)

# Ses çubuğu boyutları ve konumu
slider_width = 300
slider_height = 50
slider_x = (screen_width - slider_width) // 2
slider_y = (screen_height - slider_height) // 2

# Ses çubuğu renkleri
bar_color = (255, 228, 196)
knob_color = (72, 118, 255)

# Ses çubuğu nesneleri
slider_bar = pygame.Rect(slider_x, slider_y, slider_width, 10)
slider_knob = pygame.Rect(slider_x, slider_y - slider_height // 2, 20, slider_height)

# Ses çubuğu için metin ve font
font = pygame.font.SysFont("arialblack", 25)
text = font.render("Ses Seviyesi", True, (240, 255, 255))

# Butonlar için renkler
button_color = (193, 255, 193)
hover_color = (205, 200, 177)

# Buton boyutları ve konumları
button_width = 340
button_height = 55
button_spacing = 35
button_x = (screen_width - button_width) // 2
button_y = (screen_height - (button_height * 4 + button_spacing * 3)) // 2

# Buton metinleri ve font
font = pygame.font.SysFont("arialblack", 38)
text0 = font.render("Tokyo'ya Hoşgeldin", True, (240, 255, 255))
text1 = font.render("Oyuna Başla", True, (0, 0, 0))
text2 = font.render("En Yüksek Skor", True, (0, 0, 0))
text3 = font.render("Ayarlar", True, (0, 0, 0))
text4 = font.render("Çıkış", True, (0, 0, 0))

# Buton nesneleri
button0 = pygame.Rect(button_x, button_y, button_width, button_height)
button1 = pygame.Rect(button_x, button_y, button_width, button_height)
button2 = pygame.Rect(button_x, button_y + button_height + button_spacing, button_width, button_height)
button3 = pygame.Rect(button_x, button_y + 2 * (button_height + button_spacing), button_width, button_height)
button4 = pygame.Rect(button_x, button_y + 3 * (button_height + button_spacing), button_width, button_height)

# Butonlar için renkler
backbutton_color = (224, 238, 238)
backhover_color = (205, 200, 177)

# Geri butonu konumu
backbutton_width = 140
backbutton_height = 50
backbutton_spacing = 2
backbutton_x = (screen_width * 0.5 - button_width) // 2
backbutton_y = (screen_height - (button_height * 12.5 + button_spacing * 3)) // 2

# Geri butonu
font = pygame.font.SysFont("arialblack", 38)
backtext = font.render("Geri", True, (0, 0, 0))
surf = font.render('Geri', True, 'Green')
backbutton = pygame.Rect(backbutton_x, backbutton_y + backbutton_height + backbutton_spacing, backbutton_width,
                         backbutton_height)


def main_menu():
    screen.blit(background_image, (0, 0))

    # Ana menü butonları
    pygame.draw.rect(screen, button_color, button1)
    pygame.draw.rect(screen, button_color, button2)
    pygame.draw.rect(screen, button_color, button3)
    pygame.draw.rect(screen, button_color, button4)
    screen.blit(text1, (button_x + 45, button_y + 0))
    screen.blit(text2, (button_x + 10, button_y + button_height + button_spacing + 0))
    screen.blit(text3, (button_x + 95, button_y + 2 * (button_height + button_spacing) + 0))
    screen.blit(text4, (button_x + 117, button_y + 3 * (button_height + button_spacing) + 0))
    screen.blit(text0, (button_x + 128, button_y + 4 * (button_height + button_spacing) + 0))


# Arabanın hız ayarları
class AbstractCar():
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, screen):
        blit_rotate_center(screen, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):
    IMG = redcar
    START_POS = (185, 200)

    # W'dan el çekince arabanın yavaşlayarak durması
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


# Bot'un konumu, hız ayarı vs.
class ComputerCar(AbstractCar):
    IMG = greencar
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, screen):
        for point in self.path:
            pygame.draw.circle(screen, (255, 0, 0), point, 5)

    def draw(self, screen):
        super().draw(screen)
        # self.draw_points(screen)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0


def enyuksekskor():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="faruk123",
        database="racecar"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM skorlar ORDER BY level DESC")
    myresult = mycursor.fetchall()
    text_name = MAIN_FONT.render(('1.{0}'.format(myresult[0][1])), 1, (0, 0, 0))
    text_name1 = MAIN_FONT.render(('2.{0}'.format(myresult[1][1])), 1, (0, 0, 0))
    text_name2 = MAIN_FONT.render(('3.{0}'.format(myresult[2][1])), 1, (0, 0, 0))
    text_points = MAIN_FONT.render(('  |  {0}'.format(myresult[0][2])), 1, (0, 0, 0))
    text_points1 = MAIN_FONT.render(('  |  {0}'.format(myresult[1][2])), 1, (0, 0, 0))
    text_points2 = MAIN_FONT.render(('  |  {0}'.format(myresult[2][2])), 1, (0, 0, 0))
    screen.blit(text_name, (110, 220))
    screen.blit(text_name1, (110, 250))
    screen.blit(text_name2, (110, 280))
    screen.blit(text_points, (220, 220))
    screen.blit(text_points1, (220, 250))
    screen.blit(text_points2, (220, 280))


def draw(screen, images, player_car, computer_car, game_info):
    for img, pos in images:
        screen.blit(img, pos)

    level_text = MAIN_FONT.render(f"Level {game_info.level}", 1, (240, 255, 255))
    screen.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = MAIN_FONT.render(f"Süre: {game_info.get_level_time()}s", 1, (240, 255, 255))
    screen.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    player_car.draw(screen)
    computer_car.draw(screen)
    pygame.display.update()


# Tuş ayarları
def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


def handle_collision(player_car, computer_car, game_info):
    if player_car.collide(mapbordermask) != None:
        player_car.bounce()

    computer_finish_poi_collide = computer_car.collide(finishmask, *finish_position)
    if computer_finish_poi_collide != None:
        blit_text_center(screen, MAIN_FONT, "Kaybettin!")

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="faruk123",
            database="racecar"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO skorlar (id,level) VALUES (%s, %s)"
        val = (None, game_info.level)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "eklendi")

        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(finishmask, *finish_position)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            computer_car.next_level(game_info.level)
            game_info.next_level()


# Oyun döngüsü
running = True
clock = pygame.time.Clock()

images = [(grass, (0, 0)), (map, (0, 0)), (finish, finish_position), (mapborder, (0, 0))]
player_car = PlayerCar(4, 4)
computer_car = ComputerCar(2, 4, PATH)
game_info = GameInfo()

while running:
    clock.tick(FPS)
    # Olayları yakala
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1.collidepoint(event.pos):
                run1 = True
                while run1:
                    game = GameInfo(1)
                    draw(screen, images, player_car, computer_car, game_info)

                    while not game_info.started:
                        blit_text_center(screen, MAIN_FONT, f"Başlamak için bir tuşa basınız level= {game_info.level}")
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                break

                            if event.type == pygame.KEYDOWN:
                                game_info.start_level()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run1 = False
                            break

                    move_player(player_car)
                    computer_car.move()

                    handle_collision(player_car, computer_car, game_info)

                    if game_info.game_finished():
                        blit_text_center(screen, MAIN_FONT, "Kazandın!")
                        pygame.time.wait(5000)
                        game_info.reset()
                        player_car.reset()
                        computer_car.reset()



            elif button2.collidepoint(event.pos):
                run2 = True
                while run2:
                    screen.blit(skorpage, (0, 0))
                    enyuksekskor()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # Geri tuşuna tıklama
                            if backbutton.collidepoint(event.pos):
                                run2 = False
                                main_menu()

                    # Geri butonunu çiz
                    pygame.draw.rect(screen, backbutton_color, backbutton)
                    screen.blit(backtext,
                                (backbutton_x + 25, backbutton_y + backbutton_height + backbutton_spacing - 3))

                    # Ekranı güncelle
                    pygame.display.update()

            elif button3.collidepoint(event.pos):
                run3 = True
                while run3:
                    screen.blit(background_image, (0, 0))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # Ses çubuğu üzerine tıklama
                            if slider_bar.collidepoint(event.pos):
                                slider_knob.centerx = event.pos[0]
                                # Burada yapılacak işlemler:
                                # Ses seviyesini ayarla
                                if slider_knob.x <= slider_x:
                                    muzik.set_volume(0)
                                if slider_knob.x > slider_x:
                                    muzik.set_volume(0.1)
                                if slider_knob.x > slider_x and slider_knob.x <= slider_x + 60:
                                    muzik.set_volume(0.2)
                                if slider_knob.x > slider_x + 60 and slider_knob.x <= slider_x + 90:
                                    muzik.set_volume(0.3)
                                if slider_knob.x > slider_x + 90 and slider_knob.x <= slider_x + 120:
                                    muzik.set_volume(0.4)
                                if slider_knob.x > slider_x + 120 and slider_knob.x <= slider_x + 150:
                                    muzik.set_volume(0.5)
                                if slider_knob.x > slider_x + 150 and slider_knob.x <= slider_x + 180:
                                    muzik.set_volume(0.6)
                                if slider_knob.x > slider_x + 180 and slider_knob.x <= slider_x + 210:
                                    muzik.set_volume(0.7)
                                if slider_knob.x > slider_x + 210 and slider_knob.x <= slider_x + 240:
                                    muzik.set_volume(0.8)
                                if slider_knob.x > slider_x + 240 and slider_knob.x <= slider_x + 270:
                                    muzik.set_volume(0.9)
                                if slider_knob.x > slider_x + 270:
                                    muzik.set_volume(1)
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                # Geri tuşuna tıklama
                                if backbutton.collidepoint(event.pos):
                                    run3 = False
                                    main_menu()

                    # Geri butonunu çiz
                    pygame.draw.rect(screen, backbutton_color, backbutton)
                    screen.blit(backtext,
                                (backbutton_x + 25, backbutton_y + backbutton_height + backbutton_spacing - 3))

                    # Ses çubuğunu çiz ve metnini ekle
                    pygame.draw.rect(screen, bar_color, slider_bar)
                    pygame.draw.rect(screen, knob_color, slider_knob)
                    screen.blit(text, (slider_x + slider_width // 2 - 85, slider_y + slider_height))

                    # Ekranı güncelle
                    pygame.display.update()
            elif button4.collidepoint(event.pos):
                running = False

    main_menu()

    # Ekranı güncelle
    pygame.display.update()

pygame.quit()
