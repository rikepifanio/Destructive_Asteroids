import pygame
import random
from config import LARGURA, ALTURA, FPS, VELOCIDADE_JOGADOR, PONTOS_POR_VITORIA, DOURADO
from assets import fundo_jogo, nave_img, nave_mask, asteroide_img, asteroide_mask
from assets import som_nave, som_explosao, som_vitoria
from effects import desenhar_estrelas_moveis, atualizar_estrelas_moveis, animar_explosao_com_posicao
from game_data import game_data, atualizar_score, atualizar_tempo, perder_vida, resetar_vidas
from ui import desenhar_texto, desenhar_vidas


def jogo(tela, clock, fonte_padrao):
    jogador = pygame.Rect(350, 500, 80, 80)
    inimigos = []
    tempo_inicial = pygame.time.get_ticks()
    pausado = False

    # Tempo de invencibilidade após perder vida (frames)
    invencivel = False
    tempo_invencivel = 0
    duracao_invencivel = 60  # 1 segundo (60 frames)

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

        if pausado:
            # Overlay escuro cobrindo toda a tela
            overlay = pygame.Surface((LARGURA, ALTURA))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            tela.blit(overlay, (0, 0))

            # Painel semi-transparente da pausa
            painel_pause = pygame.Surface((400, 250))
            painel_pause.set_alpha(200)
            painel_pause.fill((20, 20, 40))  # Azul escuro
            painel_x = (LARGURA - 400) // 2
            painel_y = (ALTURA - 250) // 2

            tela.blit(painel_pause, (painel_x, painel_y))

            # Borda dourada do painel
            pygame.draw.rect(tela, DOURADO, (painel_x, painel_y, 400, 250), width=3, border_radius=15)

            # Texto "PAUSADO" estilizado
            fonte_pause = pygame.font.SysFont("Arial", 55, bold=True)

            # Efeito de sombra no texto
            texto_sombra = fonte_pause.render("PAUSADO", True, (0, 0, 0))
            texto_principal = fonte_pause.render("PAUSADO", True, DOURADO)

            texto_x = (LARGURA - texto_principal.get_width()) // 2
            tela.blit(texto_sombra, (texto_x + 3, painel_y + 53))
            tela.blit(texto_principal, (texto_x, painel_y + 50))

            # Instrução para continuar
            fonte_inst = pygame.font.SysFont("Arial", 24)
            continuar_texto = fonte_inst.render("Pressione ESC para continuar", True, (200, 200, 200))
            continuar_x = (LARGURA - continuar_texto.get_width()) // 2
            tela.blit(continuar_texto, (continuar_x, painel_y + 130))

            # Instrução para voltar ao menu
            fonte_menu = pygame.font.SysFont("Arial", 18)
            menu_texto = fonte_menu.render("ou pressione M para voltar ao menu", True, (150, 150, 150))
            menu_x = (LARGURA - menu_texto.get_width()) // 2
            tela.blit(menu_texto, (menu_x, painel_y + 175))

            # Verifica se pressionou M para voltar ao menu
            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_m:
                        som_nave.stop()
                        pygame.event.clear()
                        return "menu"

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

            # Verifica colisão (apenas se não estiver invencível)
            if not invencivel:
                offset = (inimigo.x - jogador.x, inimigo.y - jogador.y)

                if nave_mask.overlap(asteroide_mask, offset):
                    # Perdeu uma vida
                    if perder_vida():
                        # Ainda tem vidas - fica invencível temporariamente
                        som_explosao.play()
                        animar_explosao_com_posicao(tela, jogador.x, jogador.y)
                        invencivel = True
                        tempo_invencivel = duracao_invencivel

                        # Remove o asteroide que colidiu
                        inimigos.remove(inimigo)

                        # Pisca a nave para indicar invencibilidade
                        continue
                    else:
                        # Sem vidas - GAME OVER
                        som_nave.stop()
                        som_explosao.play()
                        animar_explosao_com_posicao(tela, jogador.x, jogador.y)
                        pygame.event.clear()
                        return "fim"

        # Gerencia o tempo de invencibilidade
        if invencivel:
            tempo_invencivel -= 1
            if tempo_invencivel <= 0:
                invencivel = False

            # Efeito de piscar quando invencível
            if (tempo_invencivel // 5) % 2 == 0:  # Pisca a cada 5 frames
                tela.blit(nave_img, (jogador.x, jogador.y))
        else:
            # Desenha nave normalmente
            tela.blit(nave_img, (jogador.x, jogador.y))

        # Desenha asteroides
        for inimigo in inimigos:
            tela.blit(asteroide_img, (inimigo.x, inimigo.y))

        # Mostra pontuação e vidas
        desenhar_texto(tela, fonte_padrao, f"Score: {game_data['score']}", 10, 40)
        desenhar_vidas(tela, game_data["vidas"])

        pygame.display.update()