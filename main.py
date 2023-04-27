import pygame
image_path ='/data/data/com.danya.myapp/files/app/'
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 350) )#flags=pygame.NOFRAME
pygame.display.set_caption('IZZATI LETYAT')
icon = pygame.image.load('images/icon.png').convert_alpha()

pygame.display.set_icon(icon)

bg = pygame.image.load('images/SpritesIt/backgraudn.png').convert()
walk_right = [
    pygame.image.load('images/SpritesIT/Right/a.png').convert_alpha(),
    pygame.image.load('images/SpritesIT/Right/b.png').convert_alpha(),
    pygame.image.load('images/SpritesIT/Right/c.png').convert_alpha(),
    pygame.image.load('images/SpritesIT/Right/d.png').convert_alpha(),
]
walk_left = [
    pygame.image.load('images/SpritesIT/Left/a.png').convert_alpha(),
    pygame.image.load('images/SpritesIT/Left/b.png').convert_alpha(),
    pygame.image.load('images/SpritesIT/Left/c.png').convert_alpha(),
    pygame.image.load('images/SpritesIT/Left/d.png').convert_alpha(),
]

moai = pygame.image.load('images/SpritesIT/moai.png').convert_alpha()
moai_list_in_game = []


player_anim_count = 0
bg_x = 0

player_speed = 7
player_x = 150
player_y = 250

is_jump = False
jump_count = 10
gameplay = True
bg_sound = pygame.mixer.Sound('Sounds/bg.mp3')
bg_sound.play()

moai_timer = pygame.USEREVENT + 1
pygame.time.set_timer(moai_timer, 4000)

label = pygame.font.Font('fonts/RubikIso-Regular.ttf', 40)
lose_label = label.render('Вы проиграли!', False, (193, 196, 199))
restart_label = label.render('Играть занова', True, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(170, 200))

bullets_left = 5
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []

running = True
while running:


    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x+618, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if moai_list_in_game:
            for (i, el) in enumerate(moai_list_in_game):
                screen.blit(moai, el)
                el.x -= 10

                if el.x < -10:
                    moai_list_in_game.pop()


                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_d] and player_x < 200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
                is_jump = True
        else:
            if jump_count >= -10:
                if jump_count > 0:
                    player_y -= (jump_count**2) / 2
                else:
                    player_y += (jump_count**2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 10



        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -618:
            bg_x = 0


        if bullets:
            for(i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 20

                if el.x > 640:
                    bullets.pop(i)

                if moai_list_in_game:
                    for (index, moai1) in enumerate(moai_list_in_game):
                        if el.colliderect(moai1):
                            moai_list_in_game.pop(index)
                            bullets.pop(i)

    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label,(170, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            moai_list_in_game.clear()
            bullets.clear()



    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == moai_timer:
            moai_list_in_game.append(moai.get_rect(topleft=(620, 250)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_w and bullets_left> 0:
            bullets.append(bullet.get_rect(topleft=(player_x+10, player_y)))
            bullets_left -=1


    clock.tick(15)
