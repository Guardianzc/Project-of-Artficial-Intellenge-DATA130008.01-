import pisqpipe as pp
import random
import copy
from Board import Board
import time
MAXDEPTH = 3
SEARCH_R = 1
class node:
    def __init__(self,value,x,y):
        self.value = value
        self.action = (x,y)
def AlphaBetaSearch(board,t):
    depth = 1
    alpha = node(-float('inf'),None,None)
    beta = node(float('inf'),None,None)
    node_action= MaxValue(board,alpha,beta,depth,t)
    # print(node_action.value)
    return node_action.action
def score(board,piecetype):
    '''
    对于 出现一端被堵，但已经有四颗连着了，必须堵另一端
    对于 三连珠 两端无堵 必堵任意一端 
    基于以上两点，有以下基本得分
    对于白子(type = 1)来说 白子连的越多 白子得分越高
    对于黑子(type = 2)来说 黑子连得越多 白子得分越低
    '''
    Board_instance = Board(1,2,pp.height,pp.width)
    if piecetype == 2:
        return -Board_instance.get_value(board,piecetype)
    else:
        return Board_instance.get_value(board,piecetype)
def getPiecePlace(board,piecetype):
    return [(i,j) for (i,row) in enumerate(board) for (j,piece) in enumerate(row) if piece == piecetype]
def checkWetheredge(x,y):
    width = pp.width
    height = pp.height
    w_search_start = min(SEARCH_R,x)
    w_search_end = min(SEARCH_R,width-(x+1))
    h_search_start = min(SEARCH_R,y)
    h_search_end = min(SEARCH_R,height-(y+1))
    return [(i,j) for i in range(x-w_search_start,x+w_search_end+1) for j in range(y-h_search_start,y+h_search_end+1)]
def CheckWhichToGo(board,piecetype):
    '''
    输入一个棋盘，找出 piecetype类型的棋子能下的地方
    返回一个保存所有（x,y）点的队列
    '''
    ToGoQueue = []
    my_place = getPiecePlace(board,piecetype)#找出我方棋子所在的地方
    # if my_place!=[]:#如果对方开局
    for x,y in my_place:
        for i,j in checkWetheredge(x,y):
            if board[i][j] == 0:
                ToGoQueue.append((i,j))
    # else:
    #     ToGoQueue = CheckWhichToGo(board,3-piecetype)
    return ToGoQueue
def MaxValue(board,alpha,beta,depth,t):
    piecetype = 1
    # if time.time()-t>13:
    #     return alpha
    if depth>MAXDEPTH or time.time()-t>10:
        return node(score(board,piecetype),None,None)
    else:
        v = node(-float('inf'),None,None)
        # queue = CheckWhichToGo(board,piecetype)#找出可落子的地方
        # queue = queue+CheckWhichToGo(board,3-piecetype)#找出对方棋子附近可以落子的地方
        Board_instance = Board(1,2,pp.height,pp.width)
        queue = Board_instance.interested_move(board, 1)
        for x,y in queue:
            board_next = copy.deepcopy(board)
            board_next[x][y] = piecetype
            next_v = MinValue(board_next,alpha,beta,depth+1,t)
            if v.value<next_v.value:
                v = node(next_v.value,x,y)
            # v = node(max(v.value,next_v.value),x,y)
            # print(x,y,next_v.value)
            if v.value > beta.value:
                return v
            if v.value >alpha.value:
                alpha = v
        return v
def MinValue(board,alpha,beta,depth,t):
    piecetype = 2
    # if time.time()-t>13:
    #     return beta
    if depth>MAXDEPTH or time.time()-t>10:
        return node(score(board,piecetype),None,None)
    else:
        v = node(float('inf'),None,None)
        # queue = CheckWhichToGo(board,piecetype)
        # queue = queue+CheckWhichToGo(board,3-piecetype)
        Board_instance = Board(1,2,pp.height,pp.width)
        queue = Board_instance.interested_move(board, 2)
        for x,y in queue:
            board_next = copy.deepcopy(board)
            board_next[x][y] = piecetype
            next_v = MaxValue(board_next,alpha,beta,depth+1,t)
            if v.value>next_v.value:
                v = node(next_v.value,x,y)
            if v.value < alpha.value:
                return v
            if v.value < beta.value:
                beta = v
        return v

    
