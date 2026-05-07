import pygame
from config import LARGURA, ALTURA
from ui import menu, tela_fim
from game_logic import jogo
from game_data import reset_game_data

def main():
    # Inicialização do Pygame
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Destructive Asteroids")
    clock = pygame.time.Clock()
    fonte_padrao = pygame.font.SysFont(None, 36)

    estado = "menu"

    while True:
        if estado == "menu":
            reset_game_data()
            estado = menu(tela, clock, fonte_padrao)

        elif estado == "jogo":
            estado = jogo(tela, clock, fonte_padrao)

        elif estado == "fim":
            estado = tela_fim(tela, clock, fonte_padrao, "Voce perdeu!")

        elif estado == "vitoria":
            estado = tela_fim(tela, clock, fonte_padrao, "Voce venceu!")

        elif estado == "quit":
            break

if __name__ == "__main__":
    main()