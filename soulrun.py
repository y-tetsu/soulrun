import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

running = True
while running:
    # 画面を更新する処理
    clock.tick(60)
