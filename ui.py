import pygame
import sys
from config import LARGURA, ALTURA, BRANCO, AZUL, VERDE, VERMELHO, DOURADO, FPS_MENU
from config import COR_RANK_C, COR_RANK_B, COR_RANK_A, COR_RANK_S
from assets import menu_bg, som_vitoria
from game_data import game_data
from effects import desenhar_estrelas_piscantes

def fechar_jogo():
    """Fecha o jogo completamente"""
    pygame.quit()
    sys.exit()


def desenhar_texto(tela, fonte_padrao, texto, x, y, cor=BRANCO, tamanho=36, negrito=False):
    """Desenha texto na tela"""
    fonte = pygame.font.SysFont(None, tamanho, bold=negrito)
    img = fonte.render(texto, True, cor)
    tela.blit(img, (x, y))


def botao(tela, fonte_padrao, texto, x, y, largura, altura, cor_normal, cor_hover):
    """Cria um botão interativo"""
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, largura, altura)

    if rect.collidepoint(mouse):
        pygame.draw.rect(tela, cor_hover, rect, border_radius=10)
        if clique[0]:
            pygame.time.delay(150)
            pygame.event.clear()
            return True
    else:
        pygame.draw.rect(tela, cor_normal, rect, border_radius=10)

    pygame.draw.rect(tela, BRANCO, rect, width=2, border_radius=10)

    texto_surface = fonte_padrao.render(texto, True, BRANCO)
    texto_x = x + (largura - texto_surface.get_width()) // 2
    texto_y = y + (altura - texto_surface.get_height()) // 2
    tela.blit(texto_surface, (texto_x, texto_y))

    return False


def obter_rank(score):
    """Retorna o rank baseado na pontuação"""
    if score < 150:
        return "C", COR_RANK_C
    elif score < 300:
        return "B", COR_RANK_B
    elif score < 450:
        return "A", COR_RANK_A
    else:
        return "S", COR_RANK_S

def menu(tela, clock, fonte_padrao):
    """Tela principal do jogo com botões estilizados (painel semi-transparente)"""

    # Cria uma superfície semi-transparente para o painel dos botões
    painel_botoes = pygame.Surface((260, 130))
    painel_botoes.set_alpha(180)  # Semi-transparente
    painel_botoes.fill((0, 0, 0))  # Preto

    while True:
        # Desenha o fundo do menu (imagem da galáxia com asteroide)
        tela.blit(menu_bg, (0, 0))

        # Centraliza o painel na tela
        painel_x = (LARGURA - 260) // 2
        painel_y = ALTURA - 180  # 420 (ALTURA=600, 600-180=420)

        # Desenha o painel atrás dos botões
        tela.blit(painel_botoes, (painel_x, painel_y))

        # Borda dourada do painel
        pygame.draw.rect(tela, DOURADO, (painel_x, painel_y, 260, 130), width=2, border_radius=15)

        mouse = pygame.mouse.get_pos()
        botao_jogar = pygame.Rect(painel_x + 30, painel_y + 20, 200, 40)

        if botao_jogar.collidepoint(mouse):
            # Efeito de brilho externo no hover
            pygame.draw.rect(tela, (0, 100, 0), botao_jogar.inflate(6, 6), border_radius=8)
            pygame.draw.rect(tela, VERDE, botao_jogar, border_radius=8)

            # Texto com brilho
            texto_botao = fonte_padrao.render("JOGAR", True, BRANCO)

            if pygame.mouse.get_pressed()[0]:
                pygame.time.delay(150)
                pygame.event.clear()
                return "jogo"
        else:
            pygame.draw.rect(tela, (0, 80, 0), botao_jogar, border_radius=8)
            texto_botao = fonte_padrao.render("JOGAR", True, (200, 200, 200))

        # Borda dourada do botão
        pygame.draw.rect(tela, DOURADO, botao_jogar, width=2, border_radius=8)

        # Centraliza texto do botão
        texto_x = botao_jogar.x + (botao_jogar.width - texto_botao.get_width()) // 2
        texto_y = botao_jogar.y + (botao_jogar.height - texto_botao.get_height()) // 2
        tela.blit(texto_botao, (texto_x, texto_y))

        botao_sair = pygame.Rect(painel_x + 30, painel_y + 70, 200, 40)

        if botao_sair.collidepoint(mouse):
            # Efeito de brilho externo no hover
            pygame.draw.rect(tela, (100, 0, 0), botao_sair.inflate(6, 6), border_radius=8)
            pygame.draw.rect(tela, VERMELHO, botao_sair, border_radius=8)
            texto_sair = fonte_padrao.render("SAIR", True, BRANCO)

            if pygame.mouse.get_pressed()[0]:
                pygame.time.delay(150)
                pygame.event.clear()
                fechar_jogo()
        else:
            pygame.draw.rect(tela, (80, 0, 0), botao_sair, border_radius=8)
            texto_sair = fonte_padrao.render("SAIR", True, (200, 200, 200))

        # Borda dourada do botão
        pygame.draw.rect(tela, DOURADO, botao_sair, width=2, border_radius=8)

        # Centraliza texto do botão
        texto_x = botao_sair.x + (botao_sair.width - texto_sair.get_width()) // 2
        texto_y = botao_sair.y + (botao_sair.height - texto_sair.get_height()) // 2
        tela.blit(texto_sair, (texto_x, texto_y))

        fonte_inst = pygame.font.SysFont("Arial", 14)
        instrucoes = fonte_inst.render("← →  mover nave  |  ESC  pausar", True, (200, 200, 200))
        inst_x = (LARGURA - instrucoes.get_width()) // 2
        inst_bg = pygame.Surface((instrucoes.get_width() + 20, 20))
        inst_bg.set_alpha(150)
        inst_bg.fill((0, 0, 0))
        tela.blit(inst_bg, (inst_x - 10, ALTURA - 30))
        tela.blit(instrucoes, (inst_x, ALTURA - 30))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fechar_jogo()

        pygame.display.update()
        clock.tick(FPS_MENU)

def tela_fim(tela, clock, fonte_padrao, msg):
    score = game_data["score"]
    tempo = game_data["tempo"]

    if msg == "Voce venceu!":
        som_vitoria.play()

    rank, cor_rank = obter_rank(score)
    contador_piscar = 0

    while True:
        contador_piscar += 0.05
        tela.fill((0, 0, 0))

        # Fundo com estrelas piscantes
        desenhar_estrelas_piscantes(tela, contador_piscar)

        # Caixa de informações semi-transparente
        overlay = pygame.Surface((500, 350))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 40))
        tela.blit(overlay, (150, 150))
        pygame.draw.rect(tela, BRANCO, (150, 150, 500, 350), width=3, border_radius=15)

        # Título
        titulo = "MISSION COMPLETE" if msg == "Voce venceu!" else "GAME OVER"
        fonte_titulo = pygame.font.SysFont(None, 55, bold=True)
        titulo_img = fonte_titulo.render(titulo, True, DOURADO)
        titulo_x = (LARGURA - titulo_img.get_width()) // 2
        tela.blit(titulo_img, (titulo_x, 180))

        # Score
        fonte_info = pygame.font.SysFont(None, 32)
        score_texto = fonte_info.render(f"SCORE: {score}", True, BRANCO)
        score_x = (LARGURA - score_texto.get_width()) // 2
        tela.blit(score_texto, (score_x, 270))

        # Tempo
        tempo_texto = fonte_info.render(f"TEMPO: {int(tempo)}s", True, BRANCO)
        tempo_x = (LARGURA - tempo_texto.get_width()) // 2
        tela.blit(tempo_texto, (tempo_x, 320))

        # Rank
        fonte_rank = pygame.font.SysFont(None, 48, bold=True)
        rank_texto = fonte_rank.render(f"RANK {rank}", True, cor_rank)
        rank_x = (LARGURA - rank_texto.get_width()) // 2
        tela.blit(rank_texto, (rank_x, 380))

        # Botão menu
        if botao(tela, fonte_padrao, "MENU", 300, 450, 200, 55, AZUL, (0, 100, 200)):
            pygame.event.clear()
            return "menu"

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fechar_jogo()

        pygame.display.update()
        clock.tick(FPS_MENU)

def desenhar_vidas(tela, vidas):
    coracao_texto = "❤️ " * vidas
    fonte_vidas = pygame.font.SysFont("segoeuiemoji", 30)  # Fonte que suporta emoji

    try:
        # Tenta usar emoji
        img_vidas = fonte_vidas.render(coracao_texto, True, VERMELHO)
    except:
        # Fallback: usa texto simples se emoji não funcionar
        fonte_vidas = pygame.font.SysFont(None, 30)
        img_vidas = fonte_vidas.render(f"Vidas: {vidas}", True, VERMELHO)

    tela.blit(img_vidas, (10, 80))