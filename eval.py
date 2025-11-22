import chess

class Evaluator:
    def __init__(self, board: chess.Board):
        self.board = board

    def piece_evaluation(self, board: chess.Board) -> int:
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        evaluation = 0
        for piece_type in piece_values:
            evaluation += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
            evaluation -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
        
        piece_square_tables = {
            chess.PAWN: [
                0, 0, 0, 0, 0, 0, 0, 0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5, 5, 10, 25, 25, 10, 5, 5,
                0, 0, 0, 20, 20, 0, 0, 0,
                5, -5, -10, 0, 0, -10, -5, 5,
                5, 10, 10, -20, -20, 10, 10, 5,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
            chess.KNIGHT: [
                -50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50
            ],
            chess.BISHOP: [
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -10, -10, -10, -10, -10, -20
            ],
            chess.ROOK: [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 10, 10, 10, 10, 10, 10, 5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                0, 0, 0, 5, 5, 0, 0, 0
            ],
            chess.QUEEN: [
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -5, 0, 5, 5, 5, 5, 0, -5,
                0, 0, 5, 5, 5, 5, 0, -5,
                -10, 5, 5, 5, 5, 5, 0, -10,
                -10, 0, 5, 0, 0, 0, 0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ],
            chess.KING: [
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                20, 20, 0, 0, 0, 0, 20, 20,
                20, 30, 10, 0, 0, 10, 30, 20
            ]
        }
        return evaluation, piece_square_tables
    
    def opening_book(self, board: chess.Board) -> int:
        opening_book = {
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": 0,
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1": 20,
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1": 20,
        }
        fen = board.fen()
        return opening_book.get(fen, None)
    
    def opening_evaluation(self, board: chess.Board) -> int:
        opening_score = self.opening_book(board)
        if opening_score is not None:
            return opening_score
        return 0
    
    def middle_game_evaluation(self, board: chess.Board, piece_square_tables) -> int:
        evaluation = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                pst = piece_square_tables[piece.piece_type]
                if piece.color == chess.WHITE:
                    evaluation += pst[square]
                else:
                    evaluation -= pst[chess.square_mirror(square)]
        return evaluation
    
    def bishop_pair_activation(self, board: chess.Board) -> int:
        white_bishops = len(board.pieces(chess.BISHOP, chess.WHITE))
        black_bishops = len(board.pieces(chess.BISHOP, chess.BLACK))
        activation = 0
        if white_bishops >= 2:
            activation += 30
        if black_bishops >= 2:
            activation -= 30
        return activation
    
    def knight_pairs_activation(self, board: chess.Board) -> int:
        white_knights = len(board.pieces(chess.KNIGHT, chess.WHITE))
        black_knights = len(board.pieces(chess.KNIGHT, chess.BLACK))
        activation = 0
        if white_knights >= 2:
            activation += 20
        if black_knights >= 2:
            activation -= 20
        return activation
    
    def castling_rights_evaluation(self, board: chess.Board) -> int:
        evaluation = 0
        if board.has_kingside_castling_rights(chess.WHITE):
            evaluation += 10
        if board.has_queenside_castling_rights(chess.WHITE):
            evaluation += 10
        if board.has_kingside_castling_rights(chess.BLACK):
            evaluation -= 10
        if board.has_queenside_castling_rights(chess.BLACK):
            evaluation -= 10
        return evaluation
    
    def king_safety_evaluation(self, board: chess.Board) -> int:
        evaluation = 0
        white_king_square = board.king(chess.WHITE)
        black_king_square = board.king(chess.BLACK)
        if white_king_square:
            white_king_file = chess.square_file(white_king_square)
            if white_king_file in [0, 7]:
                evaluation -= 10
        if black_king_square:
            black_king_file = chess.square_file(black_king_square)
            if black_king_file in [0, 7]:
                evaluation += 10
        return evaluation
    
    def trading_phase_evaluation(self, board: chess.Board) -> int:
        evaluation = 0
        total_material = sum([
            len(board.pieces(piece_type, chess.WHITE)) + len(board.pieces(piece_type, chess.BLACK))
            for piece_type in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        ])
        if total_material <= 10:
            evaluation += 20
        return evaluation
    
    def queen_activation(self, board: chess.Board) -> int:
        evaluation = 0
        white_queen_square = board.king(chess.WHITE)
        black_queen_square = board.king(chess.BLACK)
        if white_queen_square:
            white_queen_rank = chess.square_rank(white_queen_square)
            if white_queen_rank >= 4:
                evaluation += 10
        if black_queen_square:
            black_queen_rank = chess.square_rank(black_queen_square)
            if black_queen_rank <= 3:
                evaluation -= 10
        return evaluation
    
    def random_move_reduction(self, board: chess.Board) -> int:
        import random
        evaluation = 0
        if random.random() < 0.05:
            evaluation += random.randint(-10, 10)
        return evaluation
    
    def endgame_evaluation(self, board: chess.Board) -> int:
        evaluation = 0
        white_king_square = board.king(chess.WHITE)
        black_king_square = board.king(chess.BLACK)
        if white_king_square:
            white_king_rank = chess.square_rank(white_king_square)
            evaluation += (7 - white_king_rank) * 10
        if black_king_square:
            black_king_rank = chess.square_rank(black_king_square)
            evaluation -= black_king_rank * 10
        return evaluation
    
    def evaluate_board(self) -> int:
        opening_score = self.opening_evaluation(self.board)
        if opening_score != 0:
            return opening_score
        
        evaluation, piece_square_tables = self.piece_evaluation(self.board)
        evaluation += self.middle_game_evaluation(self.board, piece_square_tables)
        evaluation += self.bishop_pair_activation(self.board)
        evaluation += self.knight_pairs_activation(self.board)
        evaluation += self.castling_rights_evaluation(self.board)
        evaluation += self.king_safety_evaluation(self.board)
        evaluation += self.trading_phase_evaluation(self.board)
        evaluation += self.queen_activation(self.board)
        evaluation += self.random_move_reduction(self.board)
        evaluation += self.endgame_evaluation(self.board)
        
        return evaluation
    
