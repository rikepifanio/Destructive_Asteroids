"""
Interface do usuário: menus, botões, telas
"""

import pygame
import sys
from config import LARGURA, ALTURA, BRANCO, AZUL, VERDE, VERMELHO, DOURADO, FPS_MENU
from config import COR_RANK_C, COR_RANK_B, COR_RANK_A, COR_RANK_S
from assets import menu_bg, som_vitoria
from game_data import game_data
from effects import desenhar_estrelas_piscantes


# ============================================
# FUNÇÕES AUXILIARES DE UI
# ============================================

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
    if score < 500:
        return "C", COR_RANK_C
    elif score < 1000:
        return "B", COR_RANK_B
    elif score < 1500:
        return "A", COR_RANK_A
    else:
        return "S", COR_RANK_S


# ============================================
# TELAS DO JOGO
# ============================================

def menu(tela, clock, fonte_padrao):
    """Tela principal do jogo"""
    while True:
        tela.blit(menu_bg, (0, 0))

        if botao(tela, fonte_padrao, "JOGAR", 300, 450, 200, 50, VERDE, (0, 200, 0)):
            return "jogo"

        if botao(tela, fonte_padrao, "SAIR", 300, 520, 200, 50, VERMELHO, (200, 0, 0)):
            fechar_jogo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fechar_jogo()

        pygame.display.update()
        clock.tick(FPS_MENU)


def tela_fim(tela, clock, fonte_padrao, msg):
    """Tela de fim de jogo (vitória ou derrota)"""
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