import gym
import gym_chess
import chess
import chess.svg
import random
import os
import sys

# Redirect all output to a log file
sys.stdout = open('ab_game_log.txt', 'w', encoding='utf-8')

# Global variable to count prunes
prune_count = 0

def evaluate_board(board):
    piece_values = {
        chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3.1,
        chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 0
    }

    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]

    eval = 0
    for piece_type in piece_values:
        eval += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
        eval -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]

    # Mobility
    eval += 0.1 * (len(list(board.legal_moves)) if board.turn == chess.WHITE else -len(list(board.legal_moves)))

    # Center control
    for square in center_squares:
        if board.piece_at(square):
            eval += 0.2 if board.piece_at(square).color == chess.WHITE else -0.2

    return eval

def alphabeta(board, depth, alpha, beta, maximizing_player):
    global prune_count

    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = alphabeta(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                prune_count += 1
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = alphabeta(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                prune_count += 1
                break
        return min_eval

def get_best_move_ab(board, depth, last_move=None):
    global prune_count
    prune_count = 0

    best_eval = float('-inf')
    best_moves = []

    legal_moves = list(board.legal_moves)
    random.shuffle(legal_moves)

    for move in legal_moves:
        # Avoid reversing the last move
        if last_move and move.to_square == last_move.from_square and move.from_square == last_move.to_square:
            continue

        board.push(move)
        eval = alphabeta(board, depth - 1, float('-inf'), float('inf'), False)
        board.pop()

        if eval > best_eval:
            best_eval = eval
            best_moves = [move]
        elif eval == best_eval:
            best_moves.append(move)

    best_move = random.choice(best_moves) if best_moves else random.choice(legal_moves)
    return best_move, best_eval, prune_count

def save_board_svg(board, move_number):
    svg = chess.svg.board(board=board, size=500)
    filepath = f"frames_ab/board_{move_number:03d}.svg"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)

# --- Main logic ---

if not os.path.exists("frames_ab"):
    os.makedirs("frames_ab")

env = gym.make('Chess-v0')
state = env.reset()
done = False
move_number = 0
last_white_move = None

print("Initial Board:\n")
print(env.render(mode='unicode'))

while not done:
    board = env._board
    save_board_svg(board, move_number)
    print(env.render(mode='unicode'))

    if board.turn == chess.WHITE:
        move, evaluation, prunes = get_best_move_ab(board, depth=3, last_move=last_white_move)
        last_white_move = move
    else:
        move = random.choice(list(board.legal_moves))
        evaluation = evaluate_board(board)
        prunes = 0

    print("\nMove played:", move.uci())
    print("Evaluation:", evaluation)
    print("Move by:", "White" if board.turn == chess.WHITE else "Black")
    print("Alpha-beta prunes this move:", prunes)

    state, reward, done, info = env.step(move)
    move_number += 1

# Final board
save_board_svg(env._board, move_number)
print("\nGame over!")
print(env.render(mode='unicode'))