import pygame, sys
from pygame.locals import *

def beforeStart(SCREEN, color, fpsClock, FPS, WINWIDTH, WINHEIGHT):
    text = ''
    check_empty = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                check_empty = False
                if event.key == K_a:
                    text += 'a'
                if event.key == K_b:
                    text += 'b'
                if event.key == K_c:
                    text += 'c'
                if event.key == K_d:
                    text += 'd'
                if event.key == K_e:
                    text += 'e'
                if event.key == K_f:
                    text += 'f'
                if event.key == K_g:
                    text += 'g'
                if event.key == K_h:
                    text += 'h'
                if event.key == K_i:
                    text += 'i'
                if event.key == K_j:
                    text += 'j'
                if event.key == K_k:
                    text += 'k'
                if event.key == K_l:
                    text += 'l'
                if event.key == K_m:
                    text += 'm'
                if event.key == K_n:
                    text += 'n'
                if event.key == K_o:
                    text += 'o'
                if event.key == K_p:
                    text += 'p'
                if event.key == K_q:
                    text += 'q'
                if event.key == K_r:
                    text += 'r'
                if event.key == K_s:
                    text += 's'
                if event.key == K_t:
                    text += 't'
                if event.key == K_u:
                    text += 'u'
                if event.key == K_v:
                    text += 'v'
                if event.key == K_w:
                    text += 'w'
                if event.key == K_x:
                    text += 'x'
                if event.key == K_y:
                    text += 'y'
                if event.key == K_z:
                    text += 'z'
                if event.key == K_0:
                    text += '0'
                if event.key == K_1:
                    text += '1'
                if event.key == K_2:
                    text += '2'
                if event.key == K_3:
                    text += '3'
                if event.key == K_4:
                    text += '4'
                if event.key == K_5:
                    text += '5'
                if event.key == K_6:
                    text += '6'
                if event.key == K_7:
                    text += '7'
                if event.key == K_8:
                    text += '8'
                if event.key == K_9:
                    text += '9'
                if event.key == K_SPACE:
                    text += ' '
                if event.key == K_BACKSPACE:
                    text = text[:-1]
                if event.key == K_RETURN:
                    if text == '':
                        check_empty = True
                    else:
                        return str(text)

        back = pygame.image.load('image/back3.jpg')
        back = pygame.transform.scale(back, (WINWIDTH, WINHEIGHT))
        SCREEN.blit(back, (0, 0))

        font = pygame.font.SysFont('consolas', 30)
        surface = font.render('What is your name?', True, color)
        size = surface.get_size()
        posx = (WINWIDTH - size[0])/2
        posy = (WINHEIGHT - size[1])/2 - WINHEIGHT/5
        SCREEN.blit(surface, (posx, posy))

        text = text.casefold()
        text = text.capitalize()
        font = pygame.font.SysFont('consolas', 40)
        surface = font.render("{}".format(text), True, (255,   0,   0))
        size = surface.get_size()
        posx = (WINWIDTH - size[0]) / 2
        posy = (WINHEIGHT - size[1]) / 2
        SCREEN.blit(surface, (posx, posy))

        if check_empty == True:
            font = pygame.font.SysFont('consolas', 30)
            surface = font.render('Your name is empty', True, (255, 0, 0))
            size = surface.get_size()
            posx = (WINWIDTH - size[0]) / 2
            posy = (WINHEIGHT - size[1]) / 2 + WINHEIGHT / 5
            SCREEN.blit(surface, (posx, posy))

            font = pygame.font.SysFont('consolas', 10)
            surface = font.render('Press a letter to hide this messenge', True, (255, 0, 0))
            size = surface.get_size()
            posx = (WINWIDTH - size[0]) / 2
            posy = (WINHEIGHT - size[1]) / 2 + WINHEIGHT / 5 + size[1] * 3
            SCREEN.blit(surface, (posx, posy))

        pygame.display.update()
        fpsClock.tick(FPS)