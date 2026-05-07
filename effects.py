import pygame
import random
import math
from config import LARGURA, ALTURA, BRANCO, QUANTIDADE_ESTRELAS, QUANTIDADE_ESTRELAS_PISCANTES
from assets import fundo_jogo, explosoes

# ============================================
# ESTRELAS DO FUNDO (MOVIMENTO VERTICAL)
# ============================================

estrelas = []
for _ in range(QUANTIDADE_ESTRELAS):
    x = random.randint(0, LARGURA)
    y = random.randint(0, ALTURA)
    velocidade = random.randint(1, 2)
    estrelas.append([x, y, velocidade])

# ============================================
# ESTRELAS PISCANTES (PARA TELA DE FIM)
# ============================================

estrelas_piscantes = []
for _ in range(QUANTIDADE_ESTRELAS_PISCANTES):
    x = random.randint(0, LARGURA)
    y = random.randint(0, ALTURA)
    tamanho = random.choice([1, 2, 3])
    velocidade_piscar = random.uniform(0.02, 0.08)
    fase = random.uniform(0, math.pi * 2)
    estrelas_piscantes.append([x, y, tamanho, velocidade_piscar, fase])


# ============================================
# FUNÇÕES DE EFEITOS
# ============================================

def desenhar_estrelas_moveis(tela):
    for estrela in estrelas:
        pygame.draw.circle(tela, BRANCO, (estrela[0], estrela[1]), 2)


def atualizar_estrelas_moveis(pausado=False):
    for estrela in estrelas:
        if not pausado:
            estrela[1] += estrela[2]

        if estrela[1] > ALTURA:
            estrela[0] = random.randint(0, LARGURA)
            estrela[1] = 0


def desenhar_estrelas_piscantes(tela, tempo):
    for estrela in estrelas_piscantes:
        brilho = (math.sin(tempo * estrela[3] + estrela[4]) + 1) / 2
        intensidade = int(100 + brilho * 155)
        cor = (intensidade, intensidade, intensidade)
        pygame.draw.circle(tela, cor, (estrela[0], estrela[1]), estrela[2])


def animar_explosao(tela):
    for frame in explosoes:
        tela.blit(fundo_jogo, (0, 0))

        # Redesenha as estrelas
        for estrela in estrelas:
            pygame.draw.circle(tela, BRANCO, (estrela[0], estrela[1]), 2)

        # A posição será passada como argumento quando chamar
        pygame.display.update()
        pygame.time.delay(80)


def animar_explosao_com_posicao(tela, x, y):
    for frame in explosoes:
        tela.blit(fundo_jogo, (0, 0))

        for estrela in estrelas:
            pygame.draw.circle(tela, BRANCO, (estrela[0], estrela[1]), 2)

        tela.blit(frame, (x - 30, y - 30))
        pygame.display.update()
        pygame.time.delay(80)