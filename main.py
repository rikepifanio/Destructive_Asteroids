import pygame
import random
import sys

pygame.init()

menu_bg = pygame.image.load("imagens/menu_1.png")
menu_bg = pygame.transform.scale(menu_bg, (800, 600))

nave_img = pygame.image.load("imagens/nave.png")
nave_img = pygame.transform.scale(nave_img, (64, 64))
nave_mask = pygame.mask.from_surface(nave_img)

asteroide_img = pygame.image.load("imagens/asteroide.png")
asteroide_img = pygame.transform.scale(asteroide_img, (50, 50))
asteroide_mask = pygame.mask.from_surface(asteroide_img)

estado = "menu"

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
pygame.display.set_caption("Destructive Ateroids")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

# Tempo
clock = pygame.time.Clock()
tempo_vitoria = 20

fonte = pygame.font.SysFont(None, 36)

def fechar_jogo() -> NoReturn:
    pygame.quit()
    sys.exit()

def texto(msg, x, y):
    img = fonte.render(msg, True, BRANCO)
    tela.blit(img, (x, y))

def menu():
    while True:
        tela.blit(menu_bg, (0, 0))

        if botao("JOGAR", 300, 450, 200, 50, (0, 128, 0), (0, 200, 0)):
            return "jogo"

        if botao("SAIR", 300, 520, 200, 50, (128, 0, 0), (200, 0, 0)):
            fechar_jogo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fechar_jogo()

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
                fechar_jogo()

        pygame.display.update()

def jogo():
    jogador = pygame.Rect(350, 500, 50, 50)
    vel_jogador = 5
    inimigos = []
    vel_inimigo = 10
    start = pygame.time.get_ticks()

    while True:
        clock.tick(60)
        tela.fill(PRETO)

        tempo = (pygame.time.get_ticks() - start) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fechar_jogo()

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
            inimigos.append(pygame.Rect(random.randint(0, LARGURA - 50), 0, 50, 50))

        for inimigo in inimigos:
            inimigo.y += vel_inimigo
            # Hitbox
            offset = (inimigo.x - jogador.x, inimigo.y - jogador.y)

            if nave_mask.overlap(asteroide_mask, offset):
                return "fim"

        if tempo >= tempo_vitoria:
            return "vitoria"

        tela.blit(nave_img, (jogador.x, jogador.y))

        for inimigo in inimigos:
            tela.blit(asteroide_img, (inimigo.x, inimigo.y))
        # Temporizador do Game
        texto(f"Tempo: {int(tempo)}", 10, 10)

        pygame.display.update()

while True:
    if estado == "menu":
        estado = menu()

    elif estado == "jogo":
        estado = jogo()

    elif estado == "fim":
        estado = tela_fim("Voce perdeu!")

    elif estado == "vitoria":
        estado = tela_fim("Voce venceu!")