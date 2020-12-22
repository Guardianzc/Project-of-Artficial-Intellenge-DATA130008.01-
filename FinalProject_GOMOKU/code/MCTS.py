from random import choice
import copy
class MCTS:
    def __init__(self, board, AI, width, high):
        self.board = board
        self.width = width
        self.high = high
        
        self.player = AI 
        self.oppo_player = 3 - self.player
        
        self.Directionset = [(0,1),(1,0),(1,1),(1,-1)]
        self.simulation_time = 150
        
        self.AIPlace = []
        self.oppoPlace = []

    
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
    
    def line_detection(self, lines, player, direction, location):
        Four = []
        Three = []
        for i in range(9):
            if lines[i] == 0:
                count = 0
                iteration = 1
                while ((i + iteration) < 9) and (lines[i + iteration] == player):
                    count += 1
                    iteration += 1
                iteration = 1
                while (lines[i - iteration] == player) and ((i - iteration) >= 0):
                    count += 1
                    iteration += 1
                iteration = 1
                if count == 4:
                    Four.append((location[0] + (i - 4) * direction[0], location[1] + (i - 4) * direction[1]))
                if count == 3:
                    Three.append((location[0] + (i - 4) * direction[0], location[1] + (i - 4) * direction[1]))
        return Four, Three
        
    def Heuristic_Knowledge(self, current_board, player_step, oppo_step, player_color):
        oppo_color = 3 - player_color
        
        Oppo_Fourfeature = []
        Player_Fourfeature = []
        Oppo_Threefeature = []
        Player_Threefeature = []     
        
        
        for direction in self.Directionset:
            if oppo_step:
                oppo_feature = self.lines(current_board, oppo_step[0], oppo_step[1], direction, oppo_color, player_color)
                Four, Three = self.line_detection(oppo_feature, oppo_color, direction, oppo_step)
                Oppo_Fourfeature += Four
                Oppo_Threefeature += Three
            else:
                for i in range(self.high):
                    for j in range(self.width):
                        if current_board[i][j] == oppo_color:
                            oppo_feature = self.lines(current_board, i, j, direction, oppo_color, player_color)
                            Four, Three = self.line_detection(oppo_feature, oppo_color, direction, (i,j))
                            Oppo_Fourfeature += Four
                            Oppo_Threefeature += Three                            
                
            if player_step:
                player_feature = self.lines(current_board, player_step[0], player_step[1], direction, player_color, oppo_color)
                Four, Three = self.line_detection(player_feature, player_color, direction, player_step)
                Player_Fourfeature += Four
                Player_Threefeature+= Three
            else:
                for i in range(self.high):
                    for j in range(self.width):
                        if current_board[i][j] == player_color:
                            player_feature = self.lines(current_board, i, j, direction, player_color, oppo_color)
                            Four, Three = self.line_detection(player_feature, player_color, direction, (i,j))
                            Player_Fourfeature += Four
                            Player_Threefeature+= Three  
        
        Oppo_Fourfeature = list(set(Oppo_Fourfeature))
        Player_Fourfeature = list(set(Player_Fourfeature))
        Oppo_Threefeature = list(set(Oppo_Threefeature))
        Player_Threefeature = list(set(Player_Threefeature))
        return Oppo_Fourfeature, Player_Fourfeature, Oppo_Threefeature, Player_Threefeature

    def UpdateBoardInformation(self, board):
        # 可能可以做一些时间上的优化
        self.AIPlace = []
        self.oppoPlace = []
        for i in range(self.high):
            for j in range(self.width):
                if board[i][j] != 0:
                    if board[i][j] == self.player:
                        self.AIPlace.append((i,j))
                    else:
                        self.oppoPlace.append((i,j))
                        
    def take_one(self,dic):
        for key,value in dic.items():
            if dic[key] == 1:
                return key                       
              
    def feature(self, board, player, step = None):
        # step 参数拿来做每一步的评估，在 interested 函数中先做一个大致的排序
        board = board
        length = self.high
        width = self.width
        Directionset = [(0,1),(1,0),(1,1),(1,-1)]
        self.UpdateBoardInformation(board)
        AIFeature = self.AIPlace
        OppoFeature = self.oppoPlace
        countList = ['FIVE','FOUR','SFOUR','THREE','STHREE','TWO','STWO']
        count = dict.fromkeys(countList, 0)
        if player == self.player:
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
                '''
                while (0 <= left[0] <= width) and (0 <= left[1] <= length) and (board[left[0]][left[1]] == self.AIplay):
                    left[0] -= direction[0]
                    left[1] -= direction[1]                         
                    m_range += 1 
                    AI_feature_dict[left] = 0
                while (0 <= right[0] <= width) and (0 <= right[1] <= length) and (board[right[0]][right[1]] == self.AIplay):
                    right[0] += direction[0]
                    right[1] += direction[1]                         
                    m_range += 1 
                    AI_feature_dict[right] = 1
                '''
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
                        right_oppo+1
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
                if m_range == 5:
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
    
    def interested_move(self, board):
        # 用来返回感兴趣的点
        player_color = 1
        value = {}
        Five = []
        player_four = []
        oppo_four = []
        player_blockedfours = []
        oppo_blockedfours = []

        threes = []

        twos = []

        neighbors = []
        
        for i in range(self.high):
            for j in range(self.width):
                if (board[i][j] == 0) and (((i > 0) and (j > 0) and (board[i-1][j-1] != 0)) or \
                                            ((i > 0) and (j < self.high - 1) and (board[i-1][j+1] != 0)) or \
                                            ((i < self.high - 1) and (j > 0) and (board[i+1][j-1] != 0)) or \
                                            ((i < self.high - 1) and (j < self.high - 1) and (board[i+1][j-1] != 0)) or \
                                            ((j > 0) and (board[i][j-1] != 0)) or \
                                            ((i > 0) and (board[i-1][j] != 0)) or \
                                            ((i < self.high - 1) and (board[i+1][j] != 0)) or \
                                            ((j < self.high - 1) and (board[i][j+1] != 0))): 
                    step_player_feature = self.feature(board, player_color, [(i, j)])
                    step_oppo_feature = self.feature(board, 3-player_color, [(i, j)])
                    if step_oppo_feature['FIVE'] > 0:
                        Five.append((i,j))
                    elif step_player_feature['FIVE'] > 0:
                        Five.append((i,j))
                    elif step_oppo_feature['FOUR'] > 0:
                        oppo_four.append((i,j))
                    elif step_player_feature['FOUR'] > 0:
                        player_four.append((i,j))
                    elif step_oppo_feature['SFOUR'] > 0:
                        oppo_blockedfours.append((i,j))
                    elif step_player_feature['SFOUR'] > 0:
                        player_blockedfours.append((i,j))

                    elif step_oppo_feature['THREE'] > 0:
                        threes.append((i,j))
                    elif step_player_feature['THREE'] > 0:
                        threes.append((i,j)) 
                    elif step_oppo_feature['TWO'] > 1:
                        twos.append((i,j))
                    elif step_player_feature['TWO'] > 1:
                        twos.append((i,j))
                    else:
                        neighbors.append((i,j))
        
        if Five:
            return Five
        if player_four:
            return player_four         
        if oppo_four and not(player_blockedfours):
            return oppo_four
        if oppo_four and player_blockedfours:
            return oppo_four + player_blockedfours
        if threes:
            return threes
        if twos:
            return twos
        return neighbors
    
    def random_choice(self, action):
        return choice(action)
    
    def train(self):
        interested = self.interested_move(self.board)
        reward = {}
        for move in interested:
            reward[move] = 0
            simulation = 0
            while simulation < self.simulation_time:
                New_board = copy.deepcopy(self.board)
                New_board[move[0]][move[1]] = self.player
                reward[move] += self.Simulation(New_board, None, move, 3-self.player)
                simulation += 1
        return max(reward,key = reward.get)
                
    def Simulation(self, board, player_move, oppo_move, player_color):
        
        Oppo_Fourfeature, Player_Fourfeature, Oppo_Threefeature, Player_Threefeature = self.Heuristic_Knowledge(board, player_move, oppo_move, player_color)
        if Player_Fourfeature:
            return (self.player == player_color)
        elif len(Oppo_Fourfeature) > 1:
            return (self.player != player_color)
        else:
            if Oppo_Fourfeature:
                board[Oppo_Fourfeature[0][0]][Oppo_Fourfeature[0][1]] = player_color
                choice = (Oppo_Fourfeature[0][0], Oppo_Fourfeature[0][1])
            elif Player_Threefeature:
                choice = self.random_choice(Player_Threefeature)
                board[choice[0]][choice[1]] = player_color
            elif Oppo_Threefeature:
                choice = self.random_choice(Oppo_Threefeature)
                board[choice[0]][choice[1]] = player_color
            else:
                inte = self.ok_move(board)
                if not(inte):
                    return 0.5
                choice = self.random_choice(inte)
                board[choice[0]][choice[1]] = player_color                
        return self.Simulation(board, oppo_move, choice, 3-player_color)
    

    def ok_move(self, board):
        # 用来返回感兴趣的点
        player_color = 1


        neighbors = []
        
        for i in range(self.high):
            for j in range(self.width):
                if (board[i][j] == 0) and (((i > 0) and (j > 0) and (board[i-1][j-1] != 0)) or \
                                            ((i > 0) and (j < self.high - 1) and (board[i-1][j+1] != 0)) or \
                                            ((i < self.high - 1) and (j > 0) and (board[i+1][j-1] != 0)) or \
                                            ((i < self.high - 1) and (j < self.high - 1) and (board[i+1][j-1] != 0)) or \
                                            ((j > 0) and (board[i][j-1] != 0)) or \
                                            ((i > 0) and (board[i-1][j] != 0)) or \
                                            ((i < self.high - 1) and (board[i+1][j] != 0)) or \
                                            ((j < self.high - 1) and (board[i][j+1] != 0))): 
                    neighbors.append((i,j))
                    return neighbors
                    
                    
if __name__ == "__main__":
    axis  = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
    mcts = MCTS(boar1, 1, 20, 20) 
    action = mcts.train()
    print(action)
               
        
        
            
            
            
            
            
        
         
        
        
        