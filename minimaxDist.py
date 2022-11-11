import chess
import random
import math
import time
import concurrent.futures


start_time = time.time()

inf = math.inf

maxDepth = 5

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


def minimax(board, depth, maxPlayer, maxColor, alpha, beta, firstMove):
    if depth == 0 or board.outcome() != None:
        return evaluateBoard(board, maxColor), None

    bestMove = None

    if maxPlayer:
        # bestScore = -inf
        if firstMove != None:
            board.push(firstMove)
            score = minimax(board, depth-1, False, maxColor, alpha, beta, None)[0]
            # print('MAX: ',depth, move, score)

            if score >= beta: #corte
                return beta, bestMove
            
            if score > alpha:
                alpha = score
                bestMove = firstMove
            
            # print('MAX: ',score, alpha)
            return alpha, bestMove
        else:
            for move in board.legal_moves: 
                
                board.push(move)
                score = minimax(board, depth-1, False, maxColor, alpha, beta, None)[0]
                board.pop()
                # print('MAX: ',depth, move, score)
                
                if score >= beta: #corte
                    return beta, bestMove
                
                if score > alpha:
                    alpha = score
                    bestMove = move
            # board.pop()
            return alpha, bestMove
    
    else:
        for move in board.legal_moves:
            # print(move)
            board.push(move)
            score = minimax(board, depth-1, True, maxColor, alpha, beta, None)[0]

            board.pop()
            
            # print('MIN:')
            # print('MIN: ',score, beta)
            
            if score <= alpha: #corte
                return alpha, bestMove

            if score < beta:
                beta = score
                bestMove = move

        return beta, bestMove

def randomMove(board):
    return random.choice(list(board.legal_moves))
            
def parallel(board,maxPlayer, maxColor, alpha, beta):
    bestMoves = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        for move in board.legal_moves:
            newBoard = board.copy()
            bestMoves.append(executor.submit(minimax, newBoard, maxDepth, maxPlayer, maxColor, alpha, beta, move))

        maior = -inf
        for task in concurrent.futures.as_completed(bestMoves):
            if task.result()[0] > maior:
                maior = task.result()[0]
                bestMove = task.result()[1]

    return bestMove

def porradaDeBot(board):
    # print(board)

    while board.outcome() == None:
        'brancas'
        # move = minimax(board, depth, True, chess.WHITE, -inf, inf)[1]
        move = parallel(board, True, chess.WHITE, -inf, inf)
        # print(move)
        if board.outcome() != None:
            # print(board.outcome())
            break
        # move = randomMove(board)
        board.push(move)
        # print("\n WHITE:", move, "\n",board)
        

        'pretas'
        # move = parallel(board, True, chess.BLACK, -inf, inf)[1]
        # move = minimax(board, depth, True, chess.BLACK, -inf, inf, None)[1]
        if board.outcome() != None:
            # print(board.outcome())
            break
        move = randomMove(board)
        board.push(move)
        # print("\n BLACK", move, "\n",board)
        
    # print(board.outcome())
    # print(board)
    return board.outcome()


if __name__ == "__main__":  
    board = chess.Board()

    
    num = 120
    winWhite = 0
    winBlack = 0
    RunTime = 0
    mediaTime = 0
    global_start_time = time.time()

    for i in range(num):
        start_time = time.time()
        result = porradaDeBot(board)
        RunTime += time.time() - start_time

        if result.winner:
            winWhite += 1
        else:
            winBlack += 1
    mediaTime = RunTime / num
    print("--- Tempo medio: %s seconds | Vitorias Brancas: %s | Vitorias pretas: %s---" %(mediaTime, winWhite, winBlack))
    print("--- Tempo total: %s seconds ---" % (time.time() - global_start_time))