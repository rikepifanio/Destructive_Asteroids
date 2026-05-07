# ============================================
# DICIONÁRIO PRINCIPAL DE DADOS
# ============================================

game_data = {
    "score": 0,
    "tempo": 0,
    "estado": "menu"
}

def reset_game_data():
    """Reseta os dados do jogo para uma nova partida"""
    game_data["score"] = 0
    game_data["tempo"] = 0
    game_data["estado"] = "menu"

def atualizar_score(valor):
    """Atualiza a pontuação"""
    game_data["score"] = valor

def atualizar_tempo(valor):
    """Atualiza o tempo"""
    game_data["tempo"] = valor