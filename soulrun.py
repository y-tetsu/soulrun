import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

last_switch = pygame.time.get_ticks()
current_frame = 0
frames = [
    pygame.image.load("frame0.png").convert_alpha(),
    pygame.image.load("frame1.png").convert_alpha(),
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 画面をクリア
    screen.fill((0, 0, 0))

    # キャラを表示
    now = pygame.time.get_ticks()
    if now - last_switch >= 200:
        current_frame = (current_frame + 1) % len(frames)
        last_switch = now
    screen.blit(frames[current_frame], (135, 95))

    # 画面を更新
    pygame.display.flip()

    # 待ち時間
    clock.tick(60)

pygame.quit()
