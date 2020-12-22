import copy
class Kill: 
    def __init__(self, AIplay, high, width):
        self.AIplay = AIplay     # AI持方
        self.oppoPlay = 3 - AIplay

        self.high =  high    # 棋盘长度(纵的)
        self.width = width      # 棋盘宽度 # y向右，x向下
        self.AIPlace = []  # AI已落子的位置
        self.oppoPlace = [] # 对手已落子的位置
        self.killingdepth = 8
    
    def UpdateBoardInformation(self, board):
        # 可能可以做一些时间上的优化
        for i in range(self.high):
            for j in range(self.width):
                if board[i][j] != 0:
                    if board[i][j] == self.AIplay:
                        self.AIPlace.append((i,j))
                    else:
                        self.oppoPlace.append((i,j))
    
    def lines(self, board, x, y, dir, play, Oppo):
        line = [0 for i in range(9)]
        temp_x = x + (-5 * dir[0])
        temp_y = y + (-5 * dir[1])
        for i in range(9):
            temp_x += dir[0]
            temp_y += dir[1]
            if (temp_x < 0 or temp_x >= self.high or temp_y < 0 or temp_y >= self.width):
                line[i] = Oppo
            else:
                line[i] = board[temp_x][temp_y]
        return line
    
    def interested_move(self, board, player_color, AIPlace, oppoPlace):
        # 用来返回感兴趣的点
        value = {}
        player_Five = []
        oppo_Five = []
        player_four = []
        oppo_four = []
        player_blockedfours = []
        player_threes = []
        oppo_blockedfours = []

        
        for i in range(self.high):
            for j in range(self.width):
                if (board[i][j] == 0) and (((i > 0) and (j > 0) and (board[i-1][j-1] != 0)) or \
                                            ((i > 0) and (j < self.high - 1) and (board[i-1][j+1] != 0)) or \
                                            ((i < self.high - 1) and (j > 0) and (board[i+1][j-1] != 0)) or \
                                            ((i < self.high - 1) and (j < self.high - 1) and (board[i+1][j+1] != 0)) or \
                                            ((j > 0) and (board[i][j-1] != 0)) or \
                                            ((i > 0) and (board[i-1][j] != 0)) or \
                                            ((i < self.high - 1) and (board[i+1][j] != 0)) or \
                                            ((j < self.high - 1) and (board[i][j+1] != 0))): 
                    step_player_feature = self.feature(board, player_color, AIPlace, oppoPlace, [(i, j)])
                    step_oppo_feature = self.feature(board, 3-player_color, AIPlace, oppoPlace, [(i, j)])
                    if step_oppo_feature['FIVE'] > 0:
                        oppo_Five.append((i,j))
                    elif step_player_feature['FIVE'] > 0:
                        player_Five.append((i,j))
                    elif step_oppo_feature['FOUR'] > 0:
                        oppo_four.append((i,j))
                    elif step_player_feature['FOUR'] > 0:
                        player_four.append((i,j))

                    elif step_player_feature['SFOUR'] > 0:
                        player_blockedfours.append((i,j))
                    elif step_oppo_feature['SFOUR'] > 0:
                        oppo_blockedfours.append((i,j))

                    elif step_player_feature['THREE'] > 0:
                        player_threes.append((i,j)) 
        
        return oppo_Five, player_Five, oppo_four, player_four, player_blockedfours, oppo_blockedfours, player_threes

    def Killing(self, board, player):
        oppo_player = 3 - player
        self.UpdateBoardInformation(board)
        oppo_Five, player_Five, oppo_four, player_four, player_blockedfours, oppo_blockedfours, player_threes = self.interested_move(board, player, self.AIPlace, self.oppoPlace)
        if player_Five:
            return player_Five
        elif oppo_Five:
            return oppo_Five
        elif player_four:
            return player_four
        elif not(player_blockedfours or player_threes):
            return None
        else:
            if oppo_four or oppo_blockedfours:
                Thread = player_blockedfours
            else:
                Thread = player_blockedfours + player_threes
            if Thread == []:
                return None
            for chess in Thread:
                Flag = True
                new_board = copy.deepcopy(board)
                new_board[chess[0]][chess[1]] = player
                # 在此地落子并更新feature
                AIplace = self.AIPlace + [chess]
                oppo_Five, player_Five, oppo_four, player_four, player_blockedfours, oppo_blockedfours, player_threes = self.interested_move(new_board, oppo_player, AIplace, self.oppoPlace)
                # answer chess
                if player_Five:
                    break
                else:
                    if oppo_Five:
                        answer = oppo_Five
                    elif player_four:
                        Flag = False
                        break
                    elif oppo_four:
                        answer = oppo_four
                for answer_chess in answer:
                    if not(Flag):
                        break
                    new_new_board = copy.deepcopy(new_board)
                    new_new_board[answer_chess[0]][answer_chess[1]] = oppo_player
                    oppo_place = self.oppoPlace + [answer_chess]
                    Feedback = self.simulation(new_new_board, player, AIplace, oppo_place, 1)
                    if not(Feedback):
                        Flag = False
                        break
                if Flag:
                    return [chess]
    
    def simulation(self, board, player, AIPlace, oppoPlace, depth):
        if depth > self.killingdepth:
            return False
        oppo_Five, player_Five, oppo_four, player_four, player_blockedfours, oppo_blockedfours, player_threes = self.interested_move(board, player, AIPlace, oppoPlace)
        oppo_player = 3 - player 
        if player_Five or (not(oppo_four) and player_four):
            return True
        if oppo_Five or (not(player_four or player_blockedfours) and oppo_four):
            return False
        if oppo_four or oppo_blockedfours:
            Thread = player_blockedfours
        else:
            Thread = player_blockedfours + player_threes
        if Thread == []:
            return False
        for chess in Thread:
            Flag = True
            new_board = copy.deepcopy(board)
            new_board[chess[0]][chess[1]] = player
            new_AIPlace = AIPlace + [chess]
            oppo_Five, player_Five, oppo_four, player_four, player_blockedfours, oppo_blockedfours, player_threes = self.interested_move(new_board, oppo_player, new_AIPlace, oppoPlace)
            # answer chess
            if player_Five or (player_four and not(oppo_Five)) or (player_threes and (not(oppo_four)) and not(oppo_Five) and not(oppo_blockedfours)):
                return False
            if oppo_Five:
                answer = oppo_Five
            elif oppo_four:
                answer = oppo_four
            for answer_chess in answer:
                new_new_board = copy.deepcopy(new_board)
                new_new_board[answer_chess[0]][answer_chess[1]] = oppo_player
                new_oppo_place = oppoPlace + [answer_chess]
                if not(self.simulation(new_new_board, player, new_AIPlace, new_oppo_place, depth + 1)):
                    Flag = False
                    break
            if Flag:
                return True
        return False   
                
    def take_one(self,dic):
        for key,value in dic.items():
            if dic[key] == 1:
                return key 
            
    def feature(self, board, player, AIPlace, oppoPlace, step = None):
        # step 参数拿来做每一步的评估，在 interested 函数中先做一个大致的排序
        board = board
        length = self.high
        width = self.width
        Directionset = [(0,1),(1,0),(1,1),(1,-1)]
        AIFeature = AIPlace
        OppoFeature = oppoPlace
        countList = ['FIVE','FOUR','SFOUR','THREE','STHREE','TWO','STWO']
        count = dict.fromkeys(countList, 0)
        if player == self.AIplay:
            operation_feature = copy.deepcopy(AIFeature)
        else:
            operation_feature = copy.deepcopy(OppoFeature)
        
        if step:
            operation_feature = step
        
        oppo = 3 - player
        # 参数 player ：现在下棋的人
        # oppo : 你的对手的颜色
        # 这里好像可以独立出来一个函数(我确实这么做了)

        for direction in Directionset:
            #for features in operation_AIfeature:
            feature_dict = dict.fromkeys(operation_feature,1)
            while not(all(value == 0 for value in feature_dict.values())):
                chess = self.take_one(feature_dict)
                lines = self.lines(board, chess[0], chess[1], direction, player, oppo)
                m_range = 1
                left = 4
                right = 4
                while left > 0:
                    if lines[left-1] != player:
                        break
                    left -= 1
                while right < 8:
                    if lines[right+1] != player:
                        break
                    right += 1
                left_oppo = left
                right_oppo = right
                while left_oppo > 0:
                    if lines[left_oppo-1] == oppo:
                        left_oppo -= 1
                        break
                    left_oppo -= 1
                while right_oppo < 8:
                    if lines[right_oppo+1] == oppo:
                        right_oppo += 1
                        break
                    right_oppo += 1
                               
                if right_oppo - left_oppo < 5:
                    feature_dict[chess] = 0
                    continue # 这一列没有研究价值
                else:
                    chess_range = right_oppo - left_oppo
                for i in range(left, right+1):
                    location = (chess[0] + (i-4) * direction[0], chess[1] + (i-4) * direction[1])
                    feature_dict[location] = 0
                    
                m_range = right - left + 1 
                if m_range >= 5:
                    count['FIVE'] += 1
                # Live Four : XMMMMX 
                # Chong Four : XMMMMP, PMMMMX
                if m_range == 4:
                    left_empty = right_empty = False
                    if lines[left-1] == 0:
                        left_empty = True			
                    if lines[right+1] == 0:
                        right_empty = True
                    if left_empty and right_empty:
                        count['FOUR'] += 1
                    elif left_empty or right_empty:
                        count['SFOUR'] += 1
                    # Chong Four : MXMMM, MMMXM, the two types can both exist
                    # Live Three : XMMMXX, XXMMMX
                    # Sleep Three : PMMMX, XMMMP, PXMMMXP
                if m_range == 3:
                    left_empty = right_empty = False
                    left_four = right_four = False
                    if lines[left-1] == 0:
                        if lines[left-2] == player:
                            location = (chess[0] - (6-left) * direction[0], chess[1] - (6-left) * direction[1])
                            feature_dict[location] = 0  
                            count['SFOUR'] += 1
                            left_four = True
                        left_empty = True
                        
                    if lines[right+1] == 0:
                        if lines[right+2] == player:  
                            location = (chess[0] + (right-2) * direction[0], chess[1] + (right-2) * direction[1])
                            feature_dict[location] = 0                                  
                            count['SFOUR'] += 1
                            left_four = True
                        right_empty = True                        
                    if left_four or right_four:
                        pass
                    elif left_empty and right_empty:
                        if chess_range > 5: # XMMMXX, XXMMMX
                            count['THREE'] += 1
                        else: # PXMMMXP
                            count['STHREE'] += 1
                    elif left_empty or right_empty: # PMMMX, XMMMP
                        count['STHREE'] += 1
                if m_range == 2:
                    left_empty = right_empty = False
                    left_three = right_three = False
                    if lines[left - 1] == 0:
                        if lines[left - 2] == player:
                            location = (chess[0] - (6-left) * direction[0], chess[1] - (6-left) * direction[1])
                            feature_dict[location] = 0  
                            if lines[left - 3] == 0:
                                if lines[right + 1] == 0:
                                    count['THREE'] += 1
                                else:
                                    count['STHREE'] += 1
                            elif lines[left - 3] == oppo:
                                if lines[right + 1] == 0:
                                    count['STHREE'] += 1
                                    left_three = True
                        left_empty = True
                    
                    if lines[right + 1] == 0:
                        if lines[right + 2] == player:
                            if lines[right + 3] == player:
                                location = (chess[0] + (right-2) * direction[0], chess[1] + (right-2) * direction[1])
                                feature_dict[location] = 0   
                                location = (chess[0] + (right-1) * direction[0], chess[1] + (right-1) * direction[1])
                                feature_dict[location] = 0
                                count['SFOUR'] += 1
                                right_three = True
                            elif lines[right + 3] == 0:
                                if left_empty:
                                    count['THREE'] += 1
                                else:
                                    count['STHREE'] += 1
                                right_three = True
                            elif left_empty:
                                count['STHREE'] += 1
                                right_three = True
                        
                        right_empty = True
                        
                    if left_three or right_three:
                        pass
                    elif left_empty and right_empty:
                        count['TWO'] += 1
                    elif left_empty or right_empty:
                        count['STWO'] += 1
                
                if m_range == 1:
                    left_empty = right_empty = False
                    if lines[left - 1] == 0:
                        if lines[left-2] == player:
                            if lines[left-3] == 0:
                                if lines[right + 1] == oppo:
                                    count['STWO'] += 1
                        left_empty = True
                    
                    if lines[right + 1] == 0:
                        if lines[right + 2] == player:
                            if lines[right + 3] == 0:
                                if left_empty:
                                    count['TWO'] += 1
                                else:
                                    count['STWO'] += 1
                        elif lines[right+2] == 0:
                            if (lines[right+3] == player) and (lines[right + 4] == 0):
                                count['TWO'] += 1                        
        return count

if __name__ == "__main__":
    axis  = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    axis  = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]    
    
    boar1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [2, 0, 0, 0, 0, 0, 2, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [1, 2, 2, 0, 0, 0, 2, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    kill = Kill( 1, 20, 20) 
    action = kill.Killing(boar1, 1)
    print(action)