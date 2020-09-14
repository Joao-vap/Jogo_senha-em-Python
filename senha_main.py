import pygame
from pygame import display, event
from pygame import image, transform
import os
import random
from time import sleep

DIM_TELA_Y = 512
DIM_TELA_X = 1024
DIM_INICIAR = [256, 64]
DIM_INST = [138, 50]
BOTOES = [x for x in os.listdir('cores') if x[-3:].lower() == 'png']

rodando = True
injogo = True

# definindo a senha

senha = []

for n in range(4):
    x = random.randint(1, 6)
    senha.append(x)

# iniciando a tela para o jogo

pygame.init()
display.set_caption("Senha")
tela = display.set_mode((DIM_TELA_X, DIM_TELA_Y))
inicial = transform.scale(image.load('Tela_inicial/Fundoinicial.png'), (DIM_TELA_X, DIM_TELA_Y))
botao_init = transform.scale(image.load('Tela_inicial/iniciar.png'), DIM_INICIAR)
botao_inst = transform.scale(image.load('Tela_inicial/instrucoes.png'), DIM_INST)

coord_init = [(DIM_TELA_X / 2) - 128, (DIM_TELA_Y / 2) + 34]
coord_inst = [30, 450]
coord_voltar = coord_inst

tela.blit(inicial, (0, 0))
tela.blit(botao_init, coord_init)
tela.blit(botao_inst, coord_inst)


def checar_iniciar(x, y):
    if coord_init[0] < x < (coord_init[0] + DIM_INICIAR[0]):
        if coord_init[1] < y < (coord_init[1] + DIM_INICIAR[1]):
            return True
    else:
        return False


def checar_inst(x, y):
    if coord_inst[0] < x < (coord_inst[0] + DIM_INST[0]):
        if coord_init[1] < y < (coord_inst[1] + DIM_INST[1]):
            return True
    else:
        return False


def checar_voltar(x, y):
    if coord_inst[0] < x < (coord_inst[0] + DIM_INST[0]):
        if coord_init[1] < y < (coord_inst[1] + DIM_INST[1]):
            return True
    else:
        return False


def checar_respostas(localidade):

    vetorsenha = [0, 0, 0, 0, 0, 0]
    acertos = []

    for w in senha:
        vetorsenha[w - 1] += 1

    for numero in range(4):
        if len(localidade[rodada]) < 4:
            for amenos in range(4 - len(localidade[rodada])):
                localidade[rodada].append(0)

    for n in range(4):
        if localidade[rodada][n] == senha[n]:
            acertos.append(1)
            vetorsenha[localidade[rodada][n] - 1] = vetorsenha[localidade[rodada][n] - 1] - 1

    for m in range(4):
        for x in range(4):
            if localidade[rodada][m] == senha[x] and vetorsenha[localidade[rodada][m] - 1] != 0 and localidade[rodada][m] != senha[m]:
                acertos.append(0)
                vetorsenha[localidade[rodada][m] - 1] = vetorsenha[localidade[rodada][m] - 1] - 1
                break

    zeros = len(acertos) - sum(acertos)
    s = sum(acertos)

    return [zeros, s]


def atualizar_telas_certos(n):

    acertos = transform.scale(image.load('acertos/' + str(n[0]) + str(n[1]) + '.png'), (50, 50))
    tela.blit(acertos, (50 + (rodada * 86), 330))
    display.flip()


def partytime():

    felps = transform.scale(image.load('acertos/felipe.png'), (120, 60))
    for x in range(20):
            for z in range(15):
                tela.blit(felps, (x * 95, 40 * z))
                display.flip()

    sleep(3)

    setup_tabuleiro()


def setup_tabuleiro():

    tela_jogo = transform.scale(image.load('Tela_inicial/tela_jogo.png'), (DIM_TELA_X, DIM_TELA_Y))
    tela.blit(tela_jogo, (0, 0))

    lista = ['testar.png', 'apagar.png', 'Voltar_inst.png']
    for botao in BOTOES:
        lista.append(botao)

    contador_botoes = [320, 420]
    indices = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    i = 1
    index = 0
    outros = False

    for item in lista:
        if 0 == (i % 4):
            outros = True
            contador_botoes = [0, 435]
            i = 1
        if outros:
            bot = transform.scale(image.load('cores/' + item), (40, 40))
            contador_botoes[0] = contador_botoes[0] + 50
            tela.blit(bot, (contador_botoes[0], contador_botoes[1]))
            indices[index] = [[contador_botoes[0], contador_botoes[0] + 40],
                              [contador_botoes[1], contador_botoes[1] + 40]]
            i = 1
        else:
            botao = transform.scale(image.load('Tela_inicial/' + item), (150, 60))
            contador_botoes[0] = contador_botoes[0] + 160
            tela.blit(botao, (contador_botoes[0], contador_botoes[1]))
            indices[index] = [[contador_botoes[0], contador_botoes[0] + 150],
                              [contador_botoes[1], contador_botoes[1] + 60]]
            i += 1

        index += 1

    display.flip()

def mostrar():

    Aurelio = ['verde', 'roxo', 'amarelo', 'azul', 'vermelho', 'cinza']

    apag = transform.scale(image.load('Tela_inicial/Apagar.png'), (50, 250))
    tela.blit(apag, (930, 40))
    display.flip()

    for n in range(len(senha)):
        correto = transform.scale(image.load('cores/' + Aurelio[senha[n]-1] + '.png'), (40, 40))
        tela.blit(correto, (930, 50 + (65 * n)))
        display.flip()

    sleep(3)

    setup_tabuleiro()

# loop principal

while rodando:

    evento_rodada = event.get()

    for e in evento_rodada:
        if e.type == pygame.QUIT:
            rodando = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if checar_iniciar(mouse_x, mouse_y):
                jogando = True

                tela_jogo = transform.scale(image.load('Tela_inicial/tela_jogo.png'), (DIM_TELA_X, DIM_TELA_Y))
                tela.blit(tela_jogo, (0, 0))

                lista = ['testar.png', 'apagar.png', 'Voltar_inst.png']
                for botao in BOTOES:
                    lista.append(botao)

                contador_botoes = [320, 420]
                indices = [0, 0, 0, 0, 0, 0, 0, 0, 0]

                i = 1
                index = 0
                outros = False

                for item in lista:
                    if 0 == (i % 4):
                        outros = True
                        contador_botoes = [0, 435]
                        i = 1
                    if outros:
                        bot = transform.scale(image.load('cores/' + item), (40, 40))
                        contador_botoes[0] = contador_botoes[0] + 50
                        tela.blit(bot, (contador_botoes[0], contador_botoes[1]))
                        indices[index] = [[contador_botoes[0], contador_botoes[0] + 40],
                                          [contador_botoes[1], contador_botoes[1] + 40]]
                        i = 1
                    else:
                        botao = transform.scale(image.load('Tela_inicial/' + item), (150, 60))
                        contador_botoes[0] = contador_botoes[0] + 160
                        tela.blit(botao, (contador_botoes[0], contador_botoes[1]))
                        indices[index] = [[contador_botoes[0], contador_botoes[0] + 150],
                                          [contador_botoes[1], contador_botoes[1] + 60]]
                        i += 1

                    index += 1

                display.flip()

                while jogando:

                    localidade = []

                    for i in range(10):
                        l = [0]
                        localidade.append(l)

                    out = False

                    for rodada in range(10):

                        localidade[rodada] = []

                        if out:
                            break

                        ciclo = True

                        while ciclo:

                            evento_rodada = event.get()

                            for e in evento_rodada:
                                if e.type == pygame.QUIT:
                                    rodando = False
                                    jogando = False
                                    injogo = False
                                    ciclo = False
                                    out = True
                                    break

                                if e.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_x, mouse_y = pygame.mouse.get_pos()

                                    qual = 1
                                    for item in indices:
                                        if item[0][0] < mouse_x < item[0][1]:
                                            if item[1][0] < mouse_y < item[1][1]:
                                                if qual == 1:
                                                    ciclo = False
                                                    break

                                                elif qual == 2:
                                                    apag = transform.scale(image.load('Tela_inicial/Apagar.png'), (30, 240))
                                                    tela.blit(apag, (60 + (rodada * 86), 50))
                                                    localidade[rodada].append(1)
                                                    display.flip()
                                                    localidade[rodada] = []

                                                elif qual == 3:
                                                    jogando = False
                                                    ciclo = False
                                                    out = True
                                                    break

                                                elif qual == 4:
                                                    if len(localidade[rodada]) < 4:
                                                        ver = transform.scale(image.load('cores/verde.png'), (30, 30))
                                                        tela.blit(ver, (60 + (rodada * 86), 50 + (len(localidade[rodada]) * 65)))
                                                        localidade[rodada].append(1)
                                                        display.flip()

                                                elif qual == 5:
                                                    if len(localidade[rodada]) < 4:
                                                        ver = transform.scale(image.load('cores/roxo.png'), (30, 30))
                                                        tela.blit(ver, (60 + (rodada * 86), 50 + (len(localidade[rodada]) * 65)))
                                                        localidade[rodada].append(2)
                                                        display.flip()

                                                elif qual == 6:
                                                    if len(localidade[rodada]) < 4:
                                                        ver = transform.scale(image.load('cores/amarelo.png'), (30, 30))
                                                        tela.blit(ver, (60 + (rodada * 86), 50 + (len(localidade[rodada]) * 65)))
                                                        localidade[rodada].append(3)
                                                        display.flip()

                                                elif qual == 7:
                                                    if len(localidade[rodada]) < 4:
                                                        ver = transform.scale(image.load('cores/azul.png'), (30, 30))
                                                        tela.blit(ver, (60 + (rodada * 86), 50 + (len(localidade[rodada]) * 65)))
                                                        localidade[rodada].append(4)
                                                        display.flip()

                                                elif qual == 8:
                                                    if len(localidade[rodada]) < 4:
                                                        ver = transform.scale(image.load('cores/vermelho.png'), (30, 30))
                                                        tela.blit(ver, (60 + (rodada * 86), 50 + (len(localidade[rodada]) * 65)))
                                                        localidade[rodada].append(5)
                                                        display.flip()

                                                else:
                                                    if len(localidade[rodada]) < 4:
                                                        ver = transform.scale(image.load('cores/cinza.png'), (30, 30))
                                                        tela.blit(ver, (60 + (rodada * 86), 50 + (len(localidade[rodada]) * 65)))
                                                        localidade[rodada].append(6)
                                                        display.flip()
                                        qual += 1

                        if not ciclo:
                            n = checar_respostas(localidade)
                            atualizar_telas_certos(n)

                        if len(localidade[rodada]) < 4:
                            ciclo = True

                        if n[1] == 4:
                            partytime()
                            break

                    if rodada == 9:
                        mostrar()

                display.flip()

                if rodando:
                    tela.blit(inicial, (0, 0))
                    tela.blit(botao_init, coord_init)
                    tela.blit(botao_inst, coord_inst)

            if checar_inst(mouse_x, mouse_y) and injogo:

                instrucao = True

                inst_texto = transform.scale(image.load('Tela_inicial/instrucoes_texto.png'), (DIM_TELA_X, DIM_TELA_Y))
                voltar_bot = transform.scale(image.load('Tela_inicial/Voltar_inst.png'), DIM_INST)
                tela.blit(inst_texto, (0, 0))
                tela.blit(voltar_bot, coord_voltar)
                display.flip()

                while instrucao:

                    evento_rodada = event.get()

                    for e in evento_rodada:
                        if e.type == pygame.QUIT:
                            instrucao = False
                            rodando = False

                        if e.type == pygame.MOUSEBUTTONDOWN:
                            mouse_x, mouse_y = pygame.mouse.get_pos()

                            if checar_voltar(mouse_x, mouse_y):
                                instrucao = False

                    tela.blit(inicial, (0, 0))
                    tela.blit(botao_init, coord_init)
                    tela.blit(botao_inst, coord_inst)

    display.flip()

print('Obrigado por jogar!')