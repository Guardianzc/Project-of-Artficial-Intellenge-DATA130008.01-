from my_AI_AlphaBeta import *

def board_v():
    def whether_XOY(x):
        if x == 1:
            return('O  ')
        elif x == 2:
            return('X  ')
        else:
            return('=  ')
    st = ['{:>3s}'.format(str(i)) for i in range(len(board[0]))]
    st = ''.join(st)
    print(' '+st)
    c = 0
    for i,row in enumerate(board):
        st_list = map(whether_XOY,row)
        st = '{:>2} '.format(str(i))+''.join(st_list)
        print(st)

def local_start():
    
    while 1:
        print('——现在开始和我的sbAI下棋——输入exit退出————')
        x,y = input("到你了, 输入x y坐标，不想玩就输exit exit，傻逼:").split()
        print()
        if x == 'exit':
            print('操你妈，傻逼')
            return None
        try:
            brain_opponents(int(x), int(y))
        except ValueError or IndexError:
            print('超出范围了！！！！我把你妈操蹦起来')
            continue
        break
    return 0

if __name__ == '__main__':
    pp.width = int(input("棋盘宽度:"))
    pp.height = int(input("棋盘高度:"))
    
    board_v()         
    while local_start()!=None:
        board_v()
        brain_turn()
        board_v()
        Board_instance = Board(1,2,pp.height,pp.width)
        print(Board_instance.get_value(board,1))


        