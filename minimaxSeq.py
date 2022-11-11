import chess
import random
import math
# import chess.svg
# from IPython.display import SVG
import time


start_time = time.time()

inf = math.inf

pawntable = [
 0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,
 0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  5,  5,  0,-20,-40,
-30,  5, 10, 15, 15, 10,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 10, 15, 15, 10,  0,-30,
-40,-20,  0,  0,  0,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bishopstable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

rookstable = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  5,  5,  5,  5,  5,  0,-10,
  0,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

kingstable = [
 20, 30, 10,  0,  0, 10, 30, 20,
 20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]
pieces = [None,pawntable, knightstable, bishopstable, rookstable, queenstable, kingstable]    
points = [0,100,320,330,500,900,20000]
test = ['pawntable', 'knightstable', 'bishopstable', 'rookstable', 'queenstable', 'kingstable']

def checkGameState(board):
    if board.is_checkmate():
        if board.turn:
            return -99999
        else:
            return 99999
    elif board.is_stalemate():
        return 0

    elif board.is_insufficient_material():
        return 0
    
    elif board.is_seventyfive_moves():
        return -999999

    elif board.is_fivefold_repetition():
        return -999999
    else:
        return False

def sumPiecePosition(board, piece, color):
    pieceTable = pieces[piece]
    sumPieces = 0
    for pos in board.pieces(piece, color):


        if color == chess.BLACK:
            pos = chess.square_mirror(pos)

        # print(piece, chess.square_name(pos), pieceTable[pos])
        sumPieces += pieceTable[pos]
    # print(piece, sumPieces)
    return sumPieces

def scoreSum(board, piece, color):
    return len(board.pieces(piece, color)) * points[piece]


def evaluateBoard(board, maxColor):
    boardValue = 0
    scorePieceWhite = 0
    scorePieceBlack = 0
    piecesWeight = 0
    gameState = checkGameState(board)
    if gameState:
        return gameState
    
    for piece in range(1,7):
        piecePos1 = sumPiecePosition(board, piece, chess.WHITE)
        piecePos2 = sumPiecePosition(board, piece, chess.BLACK)
        piecesWeight += piecePos1 - piecePos2
        scorePieceWhite += scoreSum(board, piece, chess.WHITE)
        scorePieceBlack += scoreSum(board, piece, chess.BLACK)
        # print(piecePos1,scorePiece1, piecePos2,scorePiece2)
        
    boardValue = (scorePieceWhite - scorePieceBlack) + piecesWeight
    if maxColor:    
        return boardValue
    else:
        return -boardValue


def minimax(board, depth, maxPlayer, maxColor, alpha, beta):
    if depth == 0 or board.outcome() != None:
        return evaluateBoard(board, maxColor), None

    bestMove = None

    if maxPlayer:
        # bestScore = -inf

        for move in board.legal_moves: 
            
            board.push(move)
            score = minimax(board, depth-1, False, maxColor, alpha, beta)[0]
            board.pop()
            # print('MAX:')
            # print('prof: ',depth, move, score)
            
            if score >= beta: #corte
                return beta, bestMove
            
            if score > alpha:
                alpha = score
                bestMove = move
                
        return alpha, bestMove
    
    else:
        for move in board.legal_moves:
            
            board.push(move)
            score = minimax(board, depth-1, True, maxColor, alpha, beta)[0]
            board.pop()
            
            # print('MIN:')
            # print('prof: ',depth, move, score)
            
            if score <= alpha: #corte
                return alpha, bestMove

            if score < beta:
                beta = score
                bestMove = move

        return beta, bestMove

def randomMove(board):
    return random.choice(list(board.legal_moves))

def porradaDeBot(board, depth):
    whiteScore = 0
    blackScore = 0

    print(board)

    while board.outcome() == None:
        'brancas'
        move = minimax(board, depth, True, chess.WHITE, -inf, inf)[1]
        if board.outcome() != None:
            # print(board.outcome())
            break
        board.push(move)
        # print("\n WHITE:", move, "\n",board)
        

        'pretas'
        # move = minimax(board, depth, True, chess.BLACK, -inf, inf)[1]
        if board.outcome() != None:
            # print(board.outcome())
            break
        move = randomMove(board)
        board.push(move)
        # print("\n BLACK", move, "\n",board)
    print(board, "\n")
    print(board.outcome())        

if __name__ == "__main__":  
    board = chess.Board()

    # move = minimax(board, 3, True, chess.WHITE, -inf, inf)[1]
    # print(move)
    # board.push(move)
    # board.push(chess.Move.from_uci("d7d5"))
    # move = minimax(board, 3, True, chess.WHITE, -inf, inf)[1]
    # print(move)
    # board.push(move)
    # board.push(chess.Move.from_uci("e7e6"))
    # move = minimax(board, 3, True, chess.WHITE, -inf, inf)[1]
    # print(move)
    # board.push(move)


    porradaDeBot(board, 5)
    print("--- %s seconds ---" % (time.time() - start_time))