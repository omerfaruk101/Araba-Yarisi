import pygame

pygame.init()

# Ekran boyutunu ve başlığını belirle
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Araba Yarışı")

background_image = pygame.image.load('images/arkaplan2.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Butonlar için renkler
button_color = (240,255,255)
hover_color = (205,200,177)
active_color = (150,150,150)

# Buton boyutları ve konumları
button_width = 200
button_height = 50
button_spacing = 20
button_x = (screen_width - button_width) // 2
button_y = (screen_height - (button_height * 2 + button_spacing)) // 2

# Buton metinleri ve font
font = pygame.font.SysFont("comicsansms", 30)
text1 = font.render("Ses Azalt", True, (0,0,0))
text2 = font.render("Ses Arttır", True, (0,0,0))

# Buton nesneleri
button1 = pygame.Rect(button_x, button_y, button_width, button_height)
button2 = pygame.Rect(button_x, button_y + button_height + button_spacing, button_width, button_height)

# Oyun döngüsü
running = True
while running:
    # Olayları yakala
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Ses Azalt butonuna tıklama
            if button1.collidepoint(event.pos):
                print("Ses azalt butonuna tıklandı")
                # Burada yapılacak işlemler:
                # Ses seviyesini azalt
            # Ses Arttır butonuna tıklama
            elif button2.collidepoint(event.pos):
                print("Ses arttır butonuna tıklandı")
                # Burada yapılacak işlemler:
                # Ses seviyesini arttır

    screen.blit(background_image, (0, 0))

    # Butonları çiz ve metinlerini ekle
    if button1.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, hover_color, button1)
    else:
        pygame.draw.rect(screen, active_color, button1)
    if button2.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, hover_color, button2)
    else:
        pygame.draw.rect(screen, active_color, button2)
    screen.blit(text1, (button_x + 60, button_y + 10))
    screen.blit(text2, (button_x + 50, button_y + button_height + button_spacing + 10))

    # Ekranı güncelle
    pygame.display.update()

pygame.quit()
