import pygame
from config import LARGURA, ALTURA

# ============================================
# INICIALIZAÇÃO DOS MIXERS
# ============================================

pygame.mixer.init()

# ============================================
# CARREGAMENTO DOS SONS
# ============================================

som_nave = pygame.mixer.Sound("sons/nave.wav")
som_explosao = pygame.mixer.Sound("sons/explosao.wav")
som_vitoria = pygame.mixer.Sound("sons/vitoria.mp3")

som_nave.set_volume(0.3)
som_explosao.set_volume(0.5)
som_vitoria.set_volume(0.5)

# ============================================
# CARREGAMENTO DAS IMAGENS DE FUNDO
# ============================================

menu_bg = pygame.image.load("imagens/menu_1.png")
menu_bg = pygame.transform.scale(menu_bg, (LARGURA, ALTURA))

fundo_jogo = pygame.image.load("imagens/fundo_jogo.jpg")
fundo_jogo = pygame.transform.scale(fundo_jogo, (LARGURA, ALTURA))

# ============================================
# CARREGAMENTO DOS SPRITES
# ============================================

nave_img = pygame.image.load("imagens/nave.png")
nave_img = pygame.transform.scale(nave_img, (80, 80))
nave_mask = pygame.mask.from_surface(nave_img)

asteroide_img = pygame.image.load("imagens/asteroide.png")
asteroide_img = pygame.transform.scale(asteroide_img, (60, 60))
asteroide_mask = pygame.mask.from_surface(asteroide_img)

# ============================================
# ANIMAÇÃO DE EXPLOSÃO
# ============================================

explosoes = []
for i in range(1, 5):
    img = pygame.image.load(f"imagens/explosao{i}.png")
    img = pygame.transform.scale(img, (120, 120))
    explosoes.append(img)