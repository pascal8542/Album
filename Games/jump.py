import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Multi Ball Paddle Game")

clock = pygame.time.Clock()

# Paddle
paddle_width = 100
paddle_height = 15
paddle_vel = 7

# Ball
ball_radius = 10
base_speed = 5

# Score & Highscore
score = 0
highscore = 0
first_hit = True
game_over = False

# Spawn Flags
spawn_2_balls = False
spawn_3_balls = False

balls = []


def create_ball():
    return {
        "x": paddle_x + paddle_width // 2,
        "y": paddle_y - ball_radius,
        "vx": base_speed,
        "vy": -base_speed
    }


def increase_speed(ball):
    if ball["vx"] > 0:
        ball["vx"] += 0.3
    else:
        ball["vx"] -= 0.3

    if ball["vy"] > 0:
        ball["vy"] += 0.3
    else:
        ball["vy"] -= 0.3


def reset_game():
    global paddle_x, paddle_y, balls, score, first_hit, game_over
    global spawn_2_balls, spawn_3_balls

    paddle_x = 200
    paddle_y = 450

    balls = [create_ball()]

    score = 0
    first_hit = True
    game_over = False

    spawn_2_balls = False
    spawn_3_balls = False


# Startwerte
paddle_x = 200
paddle_y = 450

balls = [create_ball()]

highscore = 0

run = True

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # Restart
    if game_over and keys[pygame.K_r]:
        reset_game()

    if not game_over:

        # Paddle
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_vel
        if keys[pygame.K_RIGHT] and paddle_x < 500 - paddle_width:
            paddle_x += paddle_vel

        # neue Bälle
        if score >= 5 and not spawn_2_balls:
            balls.append(create_ball())
            spawn_2_balls = True

        if score >= 15 and not spawn_3_balls:
            balls.append(create_ball())
            spawn_3_balls = True

        # Ball Logik
        for ball in balls[:]:

            ball["x"] += ball["vx"]
            ball["y"] += ball["vy"]

            # Wände
            if ball["x"] <= ball_radius or ball["x"] >= 500 - ball_radius:
                ball["vx"] *= -1

            if ball["y"] <= ball_radius:
                ball["vy"] *= -1

            # Paddle
            if (paddle_y <= ball["y"] + ball_radius <= paddle_y + paddle_height and
                paddle_x <= ball["x"] <= paddle_x + paddle_width):

                ball["vy"] *= -1
                increase_speed(ball)

                if not first_hit:
                    score += 1
                else:
                    first_hit = False

            # unten → Ball weg
            if ball["y"] >= 500:
                balls.remove(ball)

        # Game Over
        if len(balls) == 0:
            game_over = True

            # 🏆 Highscore Update
            if score > highscore:
                highscore = score

    # DRAW
    win.fill((0, 0, 0))

    # Paddle
    pygame.draw.rect(
        win, (0, 255, 0),
        (paddle_x, paddle_y, paddle_width, paddle_height)
    )

    # Bälle
    for ball in balls:
        pygame.draw.circle(
            win, (255, 0, 0),
            (int(ball["x"]), int(ball["y"])),
            ball_radius
        )

    # Score + Highscore
    font = pygame.font.SysFont(None, 40)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    high_text = font.render(f"Highscore: {highscore}", True, (255, 255, 0))

    win.blit(score_text, (10, 10))
    win.blit(high_text, (10, 40))

    # Game Over Text
    if game_over:
        text = font.render("GAME OVER - Press Y", True, (255, 255, 255))
        win.blit(text, (80, 220))

    pygame.display.flip()

pygame.quit()