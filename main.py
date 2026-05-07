import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

# SOM
som_nave = pygame.mixer.Sound("sons/nave.wav")
som_explosao = pygame.mixer.Sound("sons/explosao.wav")
som_nave.set_volume(0.3)
som_explosao.set_volume(0.5)

# BACKGROUND / FUNDO DO JOGO
menu_bg = pygame.image.load("imagens/menu_1.png")
menu_bg = pygame.transform.scale(menu_bg, (800, 600))
fundo_jogo = pygame.image.load("imagens/fundo_jogo.jpg")
fundo_jogo = pygame.transform.scale(fundo_jogo, (800, 600))

# ASSETS E MASCARA DA NAVE / ASTEROIDE / EXPLOSAO
nave_img = pygame.image.load("imagens/nave.png")
nave_img = pygame.transform.scale(nave_img, (80, 80))
nave_mask = pygame.mask.from_surface(nave_img)

asteroide_img = pygame.image.load("imagens/asteroide.png")
asteroide_img = pygame.transform.scale(asteroide_img, (60, 60))
asteroide_mask = pygame.mask.from_surface(asteroide_img)

explosoes = [
    pygame.image.load("imagens/explosao1.png"),
    pygame.image.load("imagens/explosao2.png"),
    pygame.image.load("imagens/explosao3.png"),
    pygame.image.load("imagens/explosao4.png")
]

# Ajustar tamanho
for i in range(len(explosoes)):
    explosoes[i] = pygame.transform.scale(explosoes[i], (120, 120))

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

# Estrelas do fundo
estrelas = []

for i in range(40):
    x = random.randint(0, LARGURA)
    y = random.randint(0, ALTURA)

    velocidade = random.randint(1, 2)

    estrelas.append([x, y, velocidade])

# Tempo
clock = pygame.time.Clock()

fonte = pygame.font.SysFont(None, 36)

def fechar_jogo():
    pygame.quit()
    sys.exit()

def texto(msg, x, y):
    img = fonte.render(msg, True, BRANCO)
    tela.blit(img, (x, y))

def animar_explosao(x, y):
    for frame in explosoes:

        tela.blit(fundo_jogo, (0, 0))

        #Desenhar Estrelas
        for estrela in estrelas:
            pygame.draw.circle(tela, BRANCO, (estrela[0], estrela[1]), 2)

        #Desenhar explosao
        tela.blit(frame, (x - 30, y - 30))

        pygame.display.update()

        pygame.time.delay(80)

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
    jogador = pygame.Rect(350, 500, 80, 80)
    vel_jogador = 5
    inimigos = []
    start = pygame.time.get_ticks()
    score = 0
    pausado = False
    som_nave.play(-1)

    while True:
        clock.tick(60)
        tela.blit(fundo_jogo, (0, 0))
        # Desenhar estrelas
        for estrela in estrelas:
            pygame.draw.circle(tela, BRANCO, (estrela[0], estrela[1]), 2)

            if not pausado:
                estrela[1] += estrela[2]

            # Resetar estrela
            if estrela[1] > ALTURA:
                estrela[0] = random.randint(0, LARGURA)
                estrela[1] = 0

        tempo = (pygame.time.get_ticks() - start) / 1000
        score = int(tempo * 10)
        velocidade_atual = 8 + (score // 100)

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pausado = not pausado
                    if pausado:
                        pygame.mixer.pause()
                    else:
                        pygame.mixer.unpause()
            if evento.type == pygame.QUIT:
                fechar_jogo()

        if pausado:
            overlay = pygame.Surface((LARGURA, ALTURA))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))

            tela.blit(overlay, (0, 0))

            texto("PAUSADO", 320, 250)
            texto("ESC para continuar", 250, 300)

            pygame.display.update()
            continue

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

        spawn_rate = max(8, 30 - (score // 100))

        if random.randint(1, spawn_rate) == 1:
            inimigos.append(pygame.Rect(random.randint(0, LARGURA - 60), 0, 50, 50))

        for inimigo in inimigos:
            inimigo.y += velocidade_atual
            # Hitbox
            offset = (inimigo.x - jogador.x, inimigo.y - jogador.y)

            if nave_mask.overlap(asteroide_mask, offset):
                som_nave.stop()
                som_explosao.play()
                animar_explosao(jogador.x, jogador.y)
                return "fim"

        tela.blit(nave_img, (jogador.x, jogador.y))

        for inimigo in inimigos:
            tela.blit(asteroide_img, (inimigo.x, inimigo.y))
        # Contador de Score
        texto(f"Score: {score}", 10, 40)

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