import pygame

pygame.init()

# --- 基準となるウィンドウサイズ ---
BASE_W, BASE_H = 256, 240

screen = pygame.display.set_mode((BASE_W*2, BASE_H*2), pygame.RESIZABLE)
clock = pygame.time.Clock()

# -------------------------
# 背景
# -------------------------
bg = pygame.image.load("background.png").convert()
bg_x = 0
SCROLL_SPEED = 6

last_switch = pygame.time.get_ticks()
current_frame = 0

# --- キャラの状態 ---
state = "run"  # "idle" or "run" or "jump_up" or "jump_down"
ANIMATION_SWITCH_TIME = 200 * 3 // SCROLL_SPEED

# ジャンプ物理
GRAVITY = 0.5
JUMP_POWER = -11
JUMP_CUT = -2
jump_hold = False
vy = 0
y_offset = 0

# --- 元画像 ---
raw_frames = {
    "idle": [
        pygame.image.load("idle0.png").convert_alpha(),
        pygame.image.load("idle1.png").convert_alpha(),
    ],
    "run": [
        pygame.image.load("run0.png").convert_alpha(),
        pygame.image.load("run1.png").convert_alpha(),
        pygame.image.load("run2.png").convert_alpha(),
        pygame.image.load("run3.png").convert_alpha(),
    ],
    "jump_up": [
        pygame.image.load("jump_up0.png").convert_alpha(),
        pygame.image.load("jump_up1.png").convert_alpha(),
    ],
    "jump_down": [
        pygame.image.load("jump_down0.png").convert_alpha(),
        pygame.image.load("jump_down1.png").convert_alpha(),
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

        # マウスクリックでジャンプ開始
        if event.type == pygame.MOUSEBUTTONDOWN:
            if y_offset == 0:      # 地面にいる
                vy = JUMP_POWER    # ジャンプの初速
                jump_hold = True   # ジャンプクリック中
                state = "jump_up"  # 上昇中のモーション
                current_frame = 0  # アニメーションのフレームを初期化

        if event.type == pygame.MOUSEBUTTONUP:
            jump_hold = False

    # --- 現在のウィンドウサイズ ---
    win_w, win_h = screen.get_size()

    # --- ウィンドウサイズからスケールを計算 ---
    scale_x = win_w / BASE_W
    scale_y = win_h / BASE_H
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

    # -------------------------
    # ジャンプ物理処理
    # -------------------------
    if y_offset != 0 or vy != 0:
        # 重力
        vy += GRAVITY

        # ジャンプカット
        if not jump_hold and vy < JUMP_CUT:
            vy = JUMP_CUT

        y_offset += vy

        # 状態切り替え
        if vy < 0:
            state = "jump_up"
        else:
            state = "jump_down"

        # 着地
        if y_offset > 0:
            y_offset = 0
            vy = 0
            state = "run"

    # --- 現在の状態のフレームを参照 ---
    frames = scaled_frames[state]

    # -------------------------
    # 背景スクロール
    # -------------------------
    if bg_x <= -win_w:
        bg_x = 0

    bg_scaled = pygame.transform.scale(bg, (win_w, win_h))

    screen.blit(bg_scaled, (bg_x, 0))
    screen.blit(bg_scaled, (bg_x + win_w, 0))

    bg_x -= SCROLL_SPEED

    # -------------------------
    # アニメーション
    # -------------------------
    now = pygame.time.get_ticks()
    if now - last_switch >= ANIMATION_SWITCH_TIME:
        current_frame = (current_frame + 1) % len(frames)
        last_switch = now

    img = frames[current_frame]

    # --- 左下あたりに描画 ---
    x = (win_w - img.get_width()) // 5
    base_y = (177 * SCALE) - img.get_height()

    y = base_y + y_offset  # ジャンプ反映

    screen.blit(img, (x, y))

    # 画面を更新
    pygame.display.flip()

    # 待ち時間
    clock.tick(60)

pygame.quit()
