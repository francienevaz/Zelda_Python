# Arquivo de configurações do jogo - settings.py

# Configurações de janela e renderização
WIDTH = 1280          # Largura da janela do jogo
HEIGHT = 720          # Altura da janela do jogo
FPS = 60              # Quadros por segundo (frame rate)
TILE_SIZE = 64         # Tamanho de cada tile em pixels

# Configurações de Interface do Usuário (UI)
BAR_HEIGHT = 20                # Altura das barras de status
HEALTH_BAR_WIDTH = 200         # Largura da barra de vida
ENERGY_BAR_WIDTH = 140         # Largura da barra de energia
ITEM_BOX_SIZE = 80             # Tamanho dos slots de itens
UI_FONT = '../graphics/font/joystix.ttf'  # Fonte utilizada na UI
UI_FONT_SIZE = 18              # Tamanho base da fonte
UI_SMALL_FONT_SIZE = 12         # Tamanho da fonte menor

# Cores gerais
WATER_COLOR = '#71ddee'        # Cor da água
UI_BG_COLOR = '#222222'        # Cor de fundo da UI
UI_BORDER_COLOR = '#111111'    # Cor das bordas da UI
TEXT_COLOR = '#EEEEEE'         # Cor do texto

#Volume de áudio
VOLUME_MUSIC = 0.5
VOLUME_SFX = 0.7

# Cores específicas da UI
UI_BORDER_COLOR_ACTIVE = 'gold' # Cor da borda quando ativa/selecionada

# Dados das armas disponíveis no jogo
weapon_data = {
    'sword': {
        'cooldown': 100,       # Tempo de recarga em ms
        'damage': 15,          # Dano base
        'graphic': '../graphics/weapons/sword/full.png'  # Imagem da arma
    },
    'lance': {
        'cooldown': 400,
        'damage': 30,
        'graphic': '../graphics/weapons/lance/full.png'
    },
    'axe': {
        'cooldown': 300,
        'damage': 20,
        'graphic': '../graphics/weapons/axe/full.png'
    },
    'rapier': {
        'cooldown': 50,
        'damage': 8,
        'graphic': '../graphics/weapons/rapier/full.png'
    },
    'sai': {
        'cooldown': 80,
        'damage': 10,
        'graphic': '../graphics/weapons/sai/full.png'
    },
}

# Dados das magias disponíveis
magic_data = {
    'flame': {
        'strength': 5,         # Poder da magia
        'cost': 20,            # Custo de energia
        'graphic': '../graphics/particles/flame/fire.png'  # Efeito visual
    },
    'heal': {
        'strength': 20,
        'cost': 10,
        'graphic': '../graphics/particles/heal/heal.png'
    }
}

# Dados dos inimigos
monster_data = {
    'squid': {
        'health': 100,         # Vida máxima
        'exp': 100,            # Experiência concedida ao derrotar
        'damage': 20,          # Dano causado
        'attack_type': 'slash', # Tipo de ataque
        'attack_sound': '../audio/attack/slash.wav',  # Som do ataque
        'speed': 3,            # Velocidade de movimento
        'resistance': 3,       # Resistência a knockback/empurrão
        'attack_radius': 80,   # Alcance do ataque
        'notice_radius': 360   # Alcance de detecção do jogador
    },
    'raccoon': {
        'health': 300,
        'exp': 250,
        'damage': 40,
        'attack_type': 'claw',
        'attack_sound': '../audio/attack/claw.wav',
        'speed': 2,
        'resistance': 3,
        'attack_radius': 120,
        'notice_radius': 400
    },
    'spirit': {
        'health': 100,
        'exp': 110,
        'damage': 8,
        'attack_type': 'thunder',
        'attack_sound': '../audio/attack/fireball.wav',
        'speed': 4,
        'resistance': 3,
        'attack_radius': 60,
        'notice_radius': 350
    },
    'bamboo': {
        'health': 70,
        'exp': 120,
        'damage': 6,
        'attack_type': 'leaf_attack',
        'attack_sound': '../audio/attack/slash.wav',
        'speed': 3,
        'resistance': 3,
        'attack_radius': 50,
        'notice_radius': 300
    }
}