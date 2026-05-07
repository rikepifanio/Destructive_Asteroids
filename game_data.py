# ============================================
# DICIONÁRIO PRINCIPAL DE DADOS
# ============================================

game_data = {
    "score": 0,
    "tempo": 0,
    "vidas": 3,  # ← NOVO: sistema de vidas
    "estado": "menu"
}

def reset_game_data():
    """Reseta os dados do jogo para uma nova partida"""
    game_data["score"] = 0
    game_data["tempo"] = 0
    game_data["vidas"] = 3  # ← NOVO: reseta vidas
    game_data["estado"] = "menu"

def atualizar_score(valor):
    """Atualiza a pontuação"""
    game_data["score"] = valor

def atualizar_tempo(valor):
    """Atualiza o tempo"""
    game_data["tempo"] = valor

def perder_vida():
    """Remove uma vida e retorna se ainda está vivo"""
    game_data["vidas"] -= 1
    return game_data["vidas"] > 0

def resetar_vidas():
    """Reseta as vidas para 3"""
    game_data["vidas"] = 3