import pygame

pygame.init()

# --- 基準となるウィンドウサイズ ---
BASE_W, BASE_H = 400, 300

screen = pygame.display.set_mode((BASE_W, BASE_H), pygame.RESIZABLE)
clock = pygame.time.Clock()

last_switch = pygame.time.get_ticks()
current_frame = 0

# --- キャラの状態 ---
state = "idle"  # "idle" or "jump"

# --- 元画像 ---
raw_frames = {
    "idle": [
        pygame.image.load("idle0.png").convert_alpha(),
        pygame.image.load("idle1.png").convert_alpha(),
    ],
    "jump": [
        pygame.image.load("jump0.png").convert_alpha(),
        pygame.image.load("jump1.png").convert_alpha(),
    ]
}

# --- スケール済み画像キャッシュ ---
scaled_frames = {}
prev_scale = None  # スケール変更検出用

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ★ マウス操作で状態を切り替える
        if event.type == pygame.MOUSEBUTTONDOWN:
            state = "jump"
            current_frame = 0
            last_switch = pygame.time.get_ticks()

        if event.type == pygame.MOUSEBUTTONUP:
            state = "idle"
            current_frame = 0
            last_switch = pygame.time.get_ticks()

    # --- 現在のウィンドウサイズ ---
    win_w, win_h = screen.get_size()

    # --- ウィンドウサイズからスケールを計算 ---
    scale_x = win_w / BASE_W * 10
    scale_y = win_h / BASE_H * 10
    SCALE = min(scale_x, scale_y)  # 縦横比を維持

    # --- スケールが変わったときだけ再生成 ---
    if SCALE != prev_scale:
        scaled_frames.clear()

        for key, imgs in raw_frames.items():
            scaled_list = []
            for img in imgs:
                w, h = img.get_size()
                scaled = pygame.transform.scale(
                    img,
                    (int(w * SCALE), int(h * SCALE))
                )
                scaled_list.append(scaled)
            scaled_frames[key] = scaled_list

        prev_scale = SCALE
        current_frame = 0
        last_switch = pygame.time.get_ticks()

    # --- 現在の状態のフレームを参照 ---
    frames = scaled_frames[state]

    # --- 画面をクリア ---
    screen.fill((0, 0, 0))

    # --- アニメーション更新 ---
    now = pygame.time.get_ticks()
    if now - last_switch >= 200:
        current_frame = (current_frame + 1) % len(frames)
        last_switch = now

    img = frames[current_frame]

    # --- 中央に描画 ---
    x = (win_w - img.get_width()) // 2
    y = (win_h - img.get_height()) // 2
    screen.blit(img, (x, y))

    # 画面を更新
    pygame.display.flip()

    # 待ち時間
    clock.tick(60)

pygame.quit()
