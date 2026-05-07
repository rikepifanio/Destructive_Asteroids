import pygame
import random
from config import LARGURA, ALTURA, FPS, VELOCIDADE_JOGADOR, PONTOS_POR_VITORIA
from assets import fundo_jogo, nave_img, nave_mask, asteroide_img, asteroide_mask
from assets import som_nave, som_explosao, som_vitoria
from effects import desenhar_estrelas_moveis, atualizar_estrelas_moveis, animar_explosao_com_posicao
from game_data import game_data, atualizar_score, atualizar_tempo
from ui import desenhar_texto


def jogo(tela, clock, fonte_padrao):
    jogador = pygame.Rect(350, 500, 80, 80)
    inimigos = []
    tempo_inicial = pygame.time.get_ticks()
    pausado = False

    som_nave.play(-1)

    while True:
        clock.tick(FPS)
        tela.blit(fundo_jogo, (0, 0))

        # Desenha estrelas
        desenhar_estrelas_moveis(tela)

        # Atualiza estrelas
        atualizar_estrelas_moveis(pausado)

        # Atualiza dados do jogo
        tempo_atual = (pygame.time.get_ticks() - tempo_inicial) / 1000
        score_atual = int(tempo_atual * 10)

        atualizar_tempo(tempo_atual)
        atualizar_score(score_atual)

        # Verifica vitória
        if game_data["score"] >= PONTOS_POR_VITORIA:
            som_nave.stop()
            som_vitoria.play()
            return "vitoria"

        velocidade_asteroides = 8 + (game_data["score"] // 100)

        # Processa eventos
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pausado = not pausado
                if pausado:
                    pygame.mixer.pause()
                else:
                    pygame.mixer.unpause()

            if evento.type == pygame.QUIT:
                pygame.quit()
                return "quit"

        # Tela de pausa
        if pausado:
            overlay = pygame.Surface((LARGURA, ALTURA))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            tela.blit(overlay, (0, 0))

            desenhar_texto(tela, fonte_padrao, "PAUSADO", 320, 250, (255, 255, 255), 36, True)
            desenhar_texto(tela, fonte_padrao, "ESC para continuar", 250, 300, (255, 255, 255), 24)

            pygame.display.update()
            continue

        # Movimento do jogador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jogador.x -= VELOCIDADE_JOGADOR
        if teclas[pygame.K_RIGHT]:
            jogador.x += VELOCIDADE_JOGADOR

        # Limita jogador na tela
        jogador.x = max(0, min(jogador.x, LARGURA - jogador.width))

        # Spawn de asteroides
        taxa_spawn = max(8, 30 - (game_data["score"] // 100))
        if random.randint(1, taxa_spawn) == 1:
            inimigos.append(pygame.Rect(random.randint(0, LARGURA - 60), 0, 50, 50))

        # Atualiza e verifica colisões dos inimigos
        for inimigo in inimigos[:]:
            inimigo.y += velocidade_asteroides

            # Remove inimigos que saíram da tela
            if inimigo.y > ALTURA:
                inimigos.remove(inimigo)
                continue

            # Verifica colisão
            offset = (inimigo.x - jogador.x, inimigo.y - jogador.y)

            if nave_mask.overlap(asteroide_mask, offset):
                som_nave.stop()
                som_explosao.play()
                animar_explosao_com_posicao(tela, jogador.x, jogador.y)
                pygame.event.clear()
                return "fim"

        # Desenha elementos na tela
        tela.blit(nave_img, (jogador.x, jogador.y))

        for inimigo in inimigos:
            tela.blit(asteroide_img, (inimigo.x, inimigo.y))

        # Mostra pontuação
        desenhar_texto(tela, fonte_padrao, f"Score: {game_data['score']}", 10, 40)

        pygame.display.update()