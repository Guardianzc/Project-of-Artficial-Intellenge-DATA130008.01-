import copy
class Board: 
    def __init__(self, AIplay, oppoPlay, high, width):
        self.AIplay = AIplay     # AI持方
        self.oppoPlay = 3 - AIplay
        self.AIscoreBoard = {}
        self.oppoScoreBoard = {}
        self.length =  high    # 棋盘长度(纵的)
        self.width = width      # 棋盘宽度 # y向右，x向下
        self.AIPlace = []  # AI已落子的位置
        self.oppoPlace = [] # 对手已落子的位置
    
    def UpdateBoardInformation(self, board):
        # 可能可以做一些时间上的优化
        for i in range(self.length):
            for j in range(self.width):
                if board[i][j] != 0:
                    if board[i][j] == self.AIplay:
                        self.AIPlace.append((i,j))
                    else:
                        self.oppoPlace.append((i,j))
    '''    
    def FeatureExactor(self, player):
        # 计算当前的棋形
        features = []
        if player == 'AI':
            queue = self.AIPlace
        else:
            queue = self.oppoPlace
        
        while queue:
            one_queue = [] # 标记其中的一个棋形
            searchlist = []
            searchlist = queue.pop(0)
            while searchlist: # 不断搜索一个棋形的队列
                search_node = searchlist.pop(0)
                one_queue.append(search_node)
                for node in queue:
                    if (abs(node[0] - search_node[0]) <= 1) and (abs(node[1] - search_node[1]) <= 1):
                        searchlist.append(node)
                        queue.remove(node)
                    if (abs(node[0] - search_node[0]) == 2) and (abs(node[1] - search_node[1]) == 2) and (board[(node[0] - search_node[0])/2][(node[1] - search_node[1])/2]) != (3-player):
                        searchlist.append(node)
                        queue.remove(node)   
                    if (abs(node[0] - search_node[0]) == 1) and (abs(node[1] - search_node[1]) == 2) and ((board[node[0]][(node[1] + search_node[1])/2]) != (3-player)) and ((board[search_node[0]][(node[1] + search[1])/2]) != (3-player)):
                        searchlist.append(node)
                        queue.remove(node)
                    if (abs(node[0] - search_node[0]) == 2) and (abs(node[1] - search_node[1]) == 1) and ((board[(node[0] + search_node[0])/2][node[1]]) != (3-player)) and ((board[(node[0] + search_node[0])/2][search[1]]) != (3-player)):
                        searchlist.append(node)
                        queue.remove(node)
                if queue = []:
                    one_queue += searchlist
                    searchlist = []
            features.append(one_queue)
        return features
    '''
    def lines(self, board, x, y, dir, play, Oppo):
        line = [0 for i in range(9)]
        temp_x = x + (-5 * dir[0])
        temp_y = y + (-5 * dir[1])
        for i in range(9):
            temp_x += dir[0]
            temp_y += dir[1]
            if (temp_x < 0 or temp_x >= self.length or temp_y < 0 or temp_y >= self.width):
                line[i] = Oppo
            else:
                line[i] = board[temp_x][temp_y]
        return line

    def take_one(self,dic):
        for key,value in dic.items():
            if dic[key] == 1:
                return key 
        
    def feature(self, board, player, step = None):
        # step 参数拿来做每一步的评估，在 interested 函数中先做一个大致的排序
        board = board
        length = self.length
        width = self.width
        Directionset = [(0,1),(1,0),(1,1),(1,-1)]
        AIFeature = self.AIPlace
        OppoFeature = self.oppoPlace
        countList = ['FIVE','FOUR','SFOUR','THREE','STHREE','TWO','STWO']
        count = dict.fromkeys(countList, 0)
        if player == self.AIplay:
            operation_feature = copy.deepcopy(AIFeature)
        else:
            operation_feature = copy.deepcopy(OppoFeature)
        
        if step:
            operation_feature = [step]
        
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
    
        
    
    def interested_move(self, board, player_color):
        # 用来返回感兴趣的点
        value = {}
        Five = []
        player_four = []
        oppo_four = []
        player_blockedfours = []
        oppo_blockedfours = []
        threes = []
        twos = []
        neighbors = []
        for i in range(self.length):
            for j in range(self.width):
                if (board[i][j] == 0) and (((i > 0) and (j > 0) and (board[i-1][j-1] != 0)) or \
                                            ((i > 0) and (j < self.length - 1) and (board[i-1][j+1] != 0)) or \
                                            ((i < self.length - 1) and (j > 0) and (board[i+1][j-1] != 0)) or \
                                            ((i < self.length - 1) and (j < self.length - 1) and (board[i+1][j+1] != 0)) or \
                                            ((j > 0) and (board[i][j-1] != 0)) or \
                                            ((i > 0) and (board[i-1][j] != 0)) or \
                                            ((i < self.length - 1) and (board[i+1][j] != 0)) or \
                                            ((j < self.length - 1) and (board[i][j+1] != 0))): 
                    step_player_feature = self.feature(board, player_color, (i, j))
                    step_oppo_feature = self.feature(board, 3-player_color, (i, j))
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
    
    def get_value(self, board, player):
        self.UpdateBoardInformation(board)
        player = player
        oppo_player = 3 - player
        player_count = self.feature(board, player)
        oppo_count = self.feature(board, oppo_player)
        if player_count['FIVE'] > 0:
            return 10000
        if oppo_count['FIVE'] > 0:
            return -9950
        if player_count['SFOUR'] >= 2:
            player_count['FOUR'] += 1
        
        if player_count['FOUR'] > 0:
            return 9500
        if player_count['SFOUR'] > 0:
            return 9250
        if oppo_count['FOUR'] > 0:
            return -9450
        if oppo_count['SFOUR'] > 0:
            return -9250
        if oppo_count['THREE'] > 0 and player_count['SFOUR'] == 0:
            return -9000 
        if player_count['THREE'] > 1 and oppo_count['THREE'] == 0 and oppo_count['STHREE'] == 0:
            return 9250
        if player_count['SFOUR'] > 0 and player_count['THREE'] > 0:
            return 9250
        player_score = 0
        if player_count['THREE'] > 1:
            player_score += 5000
        elif player_count['THREE'] > 0:
            player_score += 1000
        if oppo_count['THREE'] > 1:
            player_score -= 7000
        elif oppo_count['THREE'] > 0:
            player_score -= 5000
        if player_count['STHREE'] > 0:
            player_score += player_count['STHREE'] * 500
        if oppo_count['STHREE'] > 0:
            player_score -= player_count['STHREE'] * 600
        if player_count['TWO'] > 0:
            player_score += player_count['TWO'] * 100
        if oppo_count['TWO'] > 0:
            player_score -= oppo_count['TWO'] * 150
        if player_count['STWO'] > 0:
            player_score += player_count['STWO'] * 50
        if oppo_count['STWO'] > 0:
            player_score -= oppo_count['STWO'] * 75
        
        return player_score
          
        
        
        
        
        
empty_board=[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
if __name__ == "__main__":
    axis  = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]    
    board1= [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 2, 0, 1, 0, 0, 2, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 1, 2, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    AIplay = 1
    oppoPlay = 2
    length = 20
    width = 20
    board = Board(AIplay, oppoPlay, length, width)
    counts = board.get_value(board1, AIplay)                        
    print(counts)                        
                              
                                                      
                    
                        
                                                                   
                        
            
            
            
        
        
        