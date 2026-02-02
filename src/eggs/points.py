"""
Peso Principal: Vitória/Progresso (ex: +1000).
Peso Secundário: Material/Peças (ex: +100 por peça).
Peso Terciário: Estrutura/Cadeia (ex: +10 por conexão, -5 por isolada).
"""

UNCHAINED = 1
COLUMNS = 1
THREAT = 1
PIECE_WEIGHT = 1

# row 0
B56_00 = 0 + COLUMNS
B56_01 = 0
B56_02 = 0
B56_03 = 0
B56_04 = 0 + COLUMNS

# row 1
B56_10 = 0.1 + COLUMNS
B56_11 = 0.1
B56_12 = 0.1
B56_13 = 0.1
B56_14 = 0.1 + COLUMNS

# row 2
B56_20 = 0.15 + COLUMNS
B56_21 = 0.15
B56_22 = 0.15
B56_23 = 0.15
B56_24 = 0.15 + COLUMNS

# row 3
B56_30 = 0.2 + COLUMNS
B56_31 = 0.2
B56_32 = 0.2
B56_33 = 0.2
B56_34 = 0.2 + COLUMNS

# row 4
B56_40 = 0.3 + COLUMNS
B56_41 = 0.3
B56_42 = 0.3
B56_43 = 0.3
B56_44 = 0.3 + COLUMNS

# row 5
B56_50 = 0.4 + COLUMNS
B56_51 = 0.4
B56_52 = 0.4
B56_53 = 0.4
B56_54 = 0.4 + COLUMNS

WHITE_56_BOARD = [
    [B56_00, B56_01, B56_02, B56_03, B56_04],
    [B56_10, B56_11, B56_12, B56_13, B56_14],
    [B56_20, B56_21, B56_22, B56_23, B56_24],
    [B56_30, B56_31, B56_32, B56_33, B56_34],
    [B56_40, B56_41, B56_42, B56_43, B56_44],
    [B56_50, B56_51, B56_52, B56_53, B56_54]
]
BLACK_56_BOARD = WHITE_56_BOARD[::-1]