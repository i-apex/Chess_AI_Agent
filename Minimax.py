import gym
import gym_chess
import chess
import chess.svg
import random
import os
import sys

# Log all stdout to a file
sys.stdout = open('game_log.txt', 'w', encoding='utf-8')

previous_moves = []

def evaluate_board(board):
    piece_values = {
        chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
        chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
    }
    eval = 0
    for piece_type in piece_values:
        eval += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        eval -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

    # Center control bonus
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    for square in center_squares:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.WHITE:
                eval += 0.5
            else:
                eval -= 0.5

    # Mobility bonus
    eval += 0.1 * len(list(board.legal_moves)) if board.turn == chess.WHITE else -0.1 * len(list(board.legal_moves))

    return eval


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval


def get_best_move(board, depth):
    best_move = None
    max_eval = float('-inf')
    move_scores = []

    for move in board.legal_moves:
        if len(previous_moves) >= 2 and move == previous_moves[-2]:
            continue  # avoid repeating the same move sequence

        board.push(move)
        eval = minimax(board, depth - 1, float('-inf'), float('inf'), False)
        board.pop()
        move_scores.append((move, eval))

        if eval > max_eval:
            max_eval = eval
            best_move = move

    # Slight randomization for similar evals
    top_moves = [m for m, e in move_scores if abs(e - max_eval) < 0.2]
    if top_moves:
        best_move = random.choice(top_moves)

    return best_move, max_eval


def save_board_svg(board, move_number):
    svg = chess.svg.board(board=board, size=500)
    filepath = f"frames/board_{move_number:03d}.svg"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)

# --- Main Logic ---

if not os.path.exists("frames"):
    os.makedirs("frames")

env = gym.make('Chess-v0')
state = env.reset()
done = False
move_number = 0

print("Initial Board:\n")
print(env.render(mode='unicode'))

while not done:
    board = env._board
    save_board_svg(board, move_number)
    print(env.render(mode='unicode'))

    if board.turn == chess.WHITE:
        move, evaluation = get_best_move(board, depth=3)
    else:
        move = random.choice(list(board.legal_moves))
        evaluation = evaluate_board(board)

    print("\nMove played:", move.uci())
    print("Evaluation:", evaluation)
    print("Move by:", "White" if board.turn == chess.WHITE else "Black")

    previous_moves.append(move)
    if len(previous_moves) > 5:
        previous_moves.pop(0)

    state, reward, done, info = env.step(move)
    move_number += 1

# Save final board state
save_board_svg(env._board, move_number)
print("\nGame over!")
print(env.render(mode='unicode'))