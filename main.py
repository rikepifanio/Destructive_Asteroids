import pygame
import random
import sys

pygame.init()

menu_bg = pygame.image.load("imagens/menu_1.png")
menu_bg = pygame.transform.scale(menu_bg, (800, 600))

def botao(texto, x, y, largura, altura, cor, cor_hover):
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()

    if x < mouse[0] < x + largura and y < mouse[1] < y + altura:
        pygame.draw.rect(tela, cor_hover, (x, y, largura, altura))

        if clique[0] == 1:
            pygame.time.delay(150)
            pygame.event.clear()
            return True
    else:
        pygame.draw.rect(tela, cor, (x, y, largura, altura))

    txt = fonte.render(texto, True, (255, 255, 255))
    tela.blit(txt, (x + 20, y + 10))

    return False

# Tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Desvie dos Inimigos")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Jogador
jogador = pygame.Rect(350, 500, 50, 50)
vel_jogador = 5

# Inimigos
inimigos = []
vel_inimigo = 10

# Tempo
clock = pygame.time.Clock()
tempo_vitoria = 20

fonte = pygame.font.SysFont(None, 36)

def texto(msg, x, y):
    img = fonte.render(msg, True, BRANCO)
    tela.blit(img, (x, y))

def menu():
    while True:
        tela.blit(menu_bg, (0, 0))

        if botao("JOGAR", 300, 450, 200, 50, (0, 128, 0), (0, 200, 0)):
            return "jogo"

        if botao("SAIR", 300, 520, 200, 50, (128, 0, 0), (200, 0, 0)):
            pygame.quit()
            sys.exit()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def tela_fim(msg):
    while True:
        tela.fill(PRETO)

        texto(msg, 320, 250)

        if botao("Menu", 150, 320, 120, 50, (0, 0, 128), (0, 0, 200)):
            pygame.event.clear()
            return "menu"

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def jogo():
    jogador = pygame.Rect(350, 500, 50, 50)
    inimigos = []
    start = pygame.time.get_ticks()

    while True:
        clock.tick(60)
        tela.fill(PRETO)

        tempo = (pygame.time.get_ticks() - start) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jogador.x -= vel_jogador
        if teclas[pygame.K_RIGHT]:
            jogador.x += vel_jogador
        # Limitar jogador na tela
        if jogador.x < 0:
            jogador.x = 0

        if jogador.x > LARGURA - jogador.width:
            jogador.x = LARGURA - jogador.width

        if random.randint(1, 30) == 1:
            inimigos.append(pygame.Rect(random.randint(0, 750), 0, 50, 50))

        for inimigo in inimigos:
            inimigo.y += vel_inimigo

            if inimigo.colliderect(jogador):
                return "fim"

        if tempo >= tempo_vitoria:
            return "vitoria"

        pygame.draw.rect(tela, AZUL, jogador)

        for inimigo in inimigos:
            pygame.draw.rect(tela, VERMELHO, inimigo)

        texto(f"Tempo: {int(tempo)}", 10, 10)

        pygame.display.update()

estado = "menu"

while True:
    if estado == "menu":
        estado = menu()

    elif estado == "jogo":
        estado = jogo()

    elif estado == "fim":
        estado = tela_fim("Voce perdeu!")

    elif estado == "vitoria":
        estado = tela_fim("Voce venceu!")