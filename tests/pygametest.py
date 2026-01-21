import pygame
import sys
from eggs.board import Board, WHITE, BLACK, EMPTY_SQUARE
from eggs.game_controller import GameController
from eggs.pieces import Egg

# --- CONFIGURAÇÕES VISUAIS ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 720  # 600 largura / 5 colunas = 120px por casa. 120 * 6 linhas = 720.
ROWS = 6
COLS = 5
CELL_SIZE = SCREEN_WIDTH // COLS

# Cores (RGB)
COLOR_BG_LIGHT = (238, 238, 210) # Cor creme (casa clara)
COLOR_BG_DARK = (118, 150, 86)   # Cor verde musgo (casa escura)
COLOR_WHITE_EGG = (240, 240, 240)
COLOR_BLACK_EGG = (40, 40, 40)
COLOR_HIGHLIGHT = (100, 200, 100, 150) # Verde transparente para movimentos legais
COLOR_SELECTED = (255, 215, 0)         # Dourado para peça selecionada
COLOR_LINE = (0, 0, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Egg Game - Teste Lógico")
    clock = pygame.time.Clock()

    # --- INICIALIZAÇÃO DO JOGO ---
    board = Board(length=COLS, height=ROWS)
    board.start()
    controller = GameController(board)

    # Variáveis de Estado da UI
    selected_piece: Egg | None = None
    valid_moves_for_selected: list = [] # Lista de objetos Move

    def get_row_col_from_mouse(pos):
        x, y = pos
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        return row, col

    running = True
    while running:
        # 1. EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Verifica se apertou Z e se o CTRL está segurado
                if event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    controller.undo_move()
                    # Importante: Limpar a seleção visual para não bugar o desenho
                    selected_piece = None
                    valid_moves_for_selected = []

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Clique esquerdo
                    row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                    
                    # Verifica se clicou dentro do tabuleiro
                    if 0 <= row < ROWS and 0 <= col < COLS:
                        clicked_item = board.query_square((row, col))
                        
                        # LOGICA DE CLIQUE
                        move_made = False
                        
                        # Se já temos uma peça selecionada, tentamos mover
                        if selected_piece:
                            # Procura se o clique corresponde ao destino de algum movimento válido
                            chosen_move = None
                            for move in valid_moves_for_selected:
                                # move.path[-1] é o quadrado final ((row, col))
                                if move.path[-1] == (row, col):
                                    chosen_move = move
                                    break
                            
                            if chosen_move:
                                print(f"Movendo peça {selected_piece.position} para {(row, col)}")
                                success = controller.make_move(chosen_move)
                                if success:
                                    selected_piece = None
                                    valid_moves_for_selected = []
                                    move_made = True
                            
                            # Se clicou na mesma peça ou em outra coisa inválida, apenas desseleciona
                            # (A menos que tenha clicado em OUTRA peça sua, aí trocamos a seleção abaixo)
                            if not move_made and clicked_item != controller.group_turn:
                                selected_piece = None
                                valid_moves_for_selected = []

                        # Se não moveu, verificamos se quer selecionar uma peça nova
                        if not move_made:
                            item_at_square = board[row, col]
                            # Só seleciona se for um Ovo e for a vez do grupo dele
                            if isinstance(item_at_square, Egg) and item_at_square.group == controller.group_turn:
                                selected_piece = item_at_square
                                valid_moves_for_selected = controller.get_legal_moves(selected_piece)
                                print(f"Selecionada: {selected_piece} em {selected_piece.position}. Opções: {len(valid_moves_for_selected)}")

        # 2. DESENHO (DRAW)
        screen.fill(COLOR_BG_LIGHT)

        # A. Desenhar Tabuleiro
        for row in range(ROWS):
            for col in range(COLS):
                # Xadrez simples
                if (row + col) % 2 != 0:
                    pygame.draw.rect(screen, COLOR_BG_DARK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # B. Highlights (Movimentos Possíveis)
        if selected_piece and valid_moves_for_selected:
            # Desenha quadrado na peça selecionada
            py, px = selected_piece.position
            rect = pygame.Rect(px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, COLOR_SELECTED, rect, 5) # Borda grossa

            # Desenha bolinhas nos destinos
            for move in valid_moves_for_selected:
                target_r, target_c = move.path[-1]
                center_x = target_c * CELL_SIZE + CELL_SIZE // 2
                center_y = target_r * CELL_SIZE + CELL_SIZE // 2
                # Círculo translúcido (simulação)
                pygame.draw.circle(screen, (100, 255, 100), (center_x, center_y), 15)

        # C. Desenhar Peças
        for row in range(ROWS):
            for col in range(COLS):
                item = board[row, col]
                if isinstance(item, Egg):
                    center_x = col * CELL_SIZE + CELL_SIZE // 2
                    center_y = row * CELL_SIZE + CELL_SIZE // 2
                    radius = CELL_SIZE // 2 - 15 # Margem
                    
                    color = COLOR_WHITE_EGG if item.group == WHITE else COLOR_BLACK_EGG
                    
                    # Corpo da peça
                    pygame.draw.circle(screen, color, (center_x, center_y), radius)
                    # Borda da peça para contraste
                    pygame.draw.circle(screen, COLOR_LINE, (center_x, center_y), radius, 2)

        # D. Texto de Turno (Opcional, mas útil)
        # Se quiser adicionar fontes, descomente abaixo:
        # font = pygame.font.SysFont('Arial', 30)
        # text = font.render(f"Vez do: {'Branco' if controller.group_turn == 1 else 'Preto'}", True, (0,0,0))
        # screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()