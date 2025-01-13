import pygame
import random

def space_warriors():
    # Pygame'i başlat
    pygame.init()

    # Ekran boyutları
    WIDTH, HEIGHT = 480, 320
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Warriors - Ters Roket Düşmanlar")

    # Renkler
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)  # Oyuncu roketi mavi
    YELLOW = (255, 255, 0)
    GRAY = (169, 169, 169)  # Duman rengi
    LIGHT_BLUE = (173, 216, 230)  # Pencere rengi (açık mavi)

    # FPS ayarı
    clock = pygame.time.Clock()
    FPS = 60

    # Oyun fonksiyonu
    def game_loop():
        # Oyuncu konumu
        player_x = WIDTH // 2
        player_y = HEIGHT - 70
        player_speed = 5

        # Mermiler
        bullets = []
        bullet_speed = 7

        # Düşmanlar
        enemy_count = 5
        enemies = [{"x": random.randint(0, WIDTH - 30), "y": random.randint(-100, -40), "speed": random.randint(1, 3)} for _ in range(enemy_count)]

        # Puanlama
        score = 0
        font = pygame.font.Font(None, 36)

        # Oyun durumu
        game_over = False

        # Oyuncu roketini profesyonel şekilde çiz
        def draw_rocket(x, y):
            # Roket gövdesi (daha aerodinamik şekil)
            pygame.draw.polygon(screen, BLUE, [(x + 15, y), (x + 5, y + 30), (x + 25, y + 30)])
            # Roket motoru
            pygame.draw.polygon(screen, BLUE, [(x + 5, y + 30), (x + 25, y + 30), (x + 15, y + 40)])
            # Roket kanatları
            pygame.draw.polygon(screen, BLUE, [(x + 5, y + 15), (x + 10, y + 20), (x + 5, y + 25)])
            pygame.draw.polygon(screen, BLUE, [(x + 25, y + 15), (x + 20, y + 20), (x + 25, y + 25)])
            # Pencereyi yuvarlak çiz
            pygame.draw.ellipse(screen, LIGHT_BLUE, (x + 10, y + 10, 12, 12))  # Yuvarlak pencere

        # Düşman roketini profesyonel şekilde çiz
        def draw_enemy_rocket(x, y):
            # Düşman roketinin gövdesi (aerodinamik tasarım)
            pygame.draw.polygon(screen, RED, [(x + 5, y), (x + 25, y), (x + 15, y + 40)])
            # Düşman roket motoru
            pygame.draw.polygon(screen, RED, [(x + 5, y + 40), (x + 25, y + 40), (x + 15, y + 50)])
            # Düşman roket kanatları
            pygame.draw.polygon(screen, RED, [(x + 5, y + 15), (x + 10, y + 20), (x + 5, y + 25)])
            pygame.draw.polygon(screen, RED, [(x + 25, y + 15), (x + 20, y + 20), (x + 25, y + 25)])
            # Pencereyi yuvarlak çiz
            pygame.draw.ellipse(screen, LIGHT_BLUE, (x + 10, y + 10, 12, 12))  # Yuvarlak pencere

        # Oyun döngüsü
        running = True
        while running:
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Ateş etme
                if not game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullets.append({"x": player_x + 12, "y": player_y})

                # Enter tuşuna basıldığında oyunu yeniden başlat
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_over:
                    game_loop()  # Yeni oyun başlat

                # Z tuşuna basıldığında pencereyi kapat
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    running = False

            # Oyuncu hareketi (WASD tuşları ile)
            if not game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] and player_x > 0:  # A tuşu ile sola hareket
                    player_x -= player_speed
                if keys[pygame.K_d] and player_x < WIDTH - 30:  # D tuşu ile sağa hareket
                    player_x += player_speed
                if keys[pygame.K_w] and player_y > 0:  # W tuşu ile yukarı hareket
                    player_y -= player_speed
                if keys[pygame.K_s] and player_y < HEIGHT - 30:  # S tuşu ile aşağı hareket
                    player_y += player_speed

            # Mermileri hareket ettir
            for bullet in bullets[:]:
                bullet["y"] -= bullet_speed
                if bullet["y"] < 0:
                    bullets.remove(bullet)

            # Düşmanları hareket ettir ve çarpışma kontrolü
            for enemy in enemies[:]:
                enemy["y"] += enemy["speed"]
                if enemy["y"] > HEIGHT:
                    enemy["x"] = random.randint(0, WIDTH - 30)
                    enemy["y"] = random.randint(-100, -40)
                    enemy["speed"] = random.randint(1, 3)

                # Mermi ve düşman çarpışması
                for bullet in bullets[:]:
                    if enemy["x"] < bullet["x"] < enemy["x"] + 30 and enemy["y"] < bullet["y"] < enemy["y"] + 40:
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 1
                        break

                # Oyuncu ve düşman çarpışması
                if enemy["x"] < player_x < enemy["x"] + 30 and enemy["y"] + 40 > player_y:
                    game_over = True

            # Yeni düşman oluştur
            while len(enemies) < enemy_count:
                enemies.append({"x": random.randint(0, WIDTH - 30), "y": random.randint(-100, -40), "speed": random.randint(1, 3)})

            # Oyuncu roketini çiz
            if not game_over:
                draw_rocket(player_x, player_y)

            # Mermileri çiz
            for bullet in bullets:
                pygame.draw.rect(screen, YELLOW, (bullet["x"], bullet["y"], 5, 8))

            # Düşman roketlerini profesyonel şekilde çiz
            for enemy in enemies:
                draw_enemy_rocket(enemy["x"], enemy["y"])

            # Skor ekrana yazdır
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            # Game Over mesajı
            if game_over:
                game_over_text = font.render("GAME OVER", True, RED)
                screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                restart_text = font.render("Press ENTER to Restart", True, WHITE)
                screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 20))

            pygame.display.flip()
            clock.tick(FPS)

    # İlk oyun başlatma
    game_loop()

    # Pygame'i kapat
    pygame.quit()
space_warriors()