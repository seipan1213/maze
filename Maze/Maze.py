#!/usr/bin/env python
# coding: utf-8

# 

# 

# In[23]:


# 迷路の自動生成
import sys
import random

class Maze:
    _width = 0 # 迷路の横幅
    _height = 0 # 迷路の縦幅
    
    _data = [0][0] # 生成した迷路のデータ
    
    _startPath = [] # 進行した地点のポイントを保有するリスト
    _endPath = [] # 穴掘りの処理が終了したポイントを保有するリスト

    _movePath = [] # プレイヤーが移動したパス（スタートからゴールまでのパス）を保有するリスト
    
    _isCreated = False # 迷路生成が終わっているかどうか
    
    _playerPoint = None # プレイヤーの現在座標
    
    _startPoint = None # 迷路のスタート地点
    _goalPoint = None # 迷路のゴール地点
    
    ### 定数 ###
    PATH = 0
    WALL = 1
    PLAYER = 2
    START = 3
    GOAL = 4
    
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    ### 定数（終わり） ###
    
    # コンストラクタ
    def __init__(self, width, height):
        # 迷路生成が可能な値かどうかの判定を行う
        if (
            width < 5 or width % 2 == 0 or
            height < 5 or  height % 2 == 0
        ):
            sys.stderr.write("横・縦の値はそれぞれ5以上の奇数を入力してください")
            return
        
        self._width = width
        self._height = height
    
    # マップ生成（初期化）
    def create(self):
        self._isCreated = False
        
        # 指定したサイズのマップを生成して、初期値としてWALL（1）を代入する
        self._data = [[Maze.WALL for w in range(0, self._width)] for h in range(0, self._height)]
        
    # マップを掘り進める
    def dig(self, x, y):
        self._data[y][x] = Maze.PATH
        
        while True:
            digDirections = []
        
            # 掘ることが出来る方向を判定してリストに格納する
            if y - 2 > 0 and self._data[y-2][x] == Maze.WALL:
                digDirections.append(Maze.UP)
                
            if y + 2 < self._height - 1 and self._data[y+2][x] == Maze.WALL:
                digDirections.append(Maze.DOWN)
                
            if x - 2 > 0 and self._data[y][x-2] == Maze.WALL:
                digDirections.append(Maze.LEFT)
                
            if x + 2 < self._width - 1 and self._data[y][x+2] == Maze.WALL:
                digDirections.append(Maze.RIGHT)
            
            # どこにも掘ることができなくなった場合はループを終了する
            if len(digDirections) == 0:
                wallCount = 0
                if y - 1 >= 0 and self._data[y -1][x] == Maze.WALL:
                    wallCount += 1
                if y + 1 <= self._height - 1 and self._data[y+1][x] == Maze.WALL:
                    wallCount += 1
                if x - 1 >= 0 and self._data[y][x-1] == Maze.WALL:
                    wallCount += 1
                if x + 1 <= self._width - 1 and self._data[y][x+1] == Maze.WALL:
                    wallCount += 1
                
                # 行き止まり（前後左右を見て3点が壁）だった場合に候補として判定
                if wallCount == 3:
                    self._endPath.append([x, y]) # 掘り終わった位置を保存
                break
                
            # 掘る方向をランダム選択する
            direction = digDirections[random.randint(0, len(digDirections) - 1)]
            
            # 指定方向に掘り進める
            if direction == Maze.UP:
                self._data[y-1][x] = Maze.PATH
                self._data[y-2][x] = Maze.PATH
                y -= 2
            elif direction == Maze.DOWN:
                self._data[y+1][x] = Maze.PATH
                self._data[y+2][x] = Maze.PATH
                y += 2
            elif direction == Maze.LEFT:
                self._data[y][x-1] = Maze.PATH
                self._data[y][x-2] = Maze.PATH
                x -= 2
            elif direction == Maze.RIGHT:
                self._data[y][x+1] = Maze.PATH
                self._data[y][x+2] = Maze.PATH
                x += 2
               
            # 現在位置をリストに追加する
            self._startPath.append([x, y])
            
            #self.draw()
            
        # 次に掘り進める位置を判定する（掘り進めることが出来なかった場合は終了する）
        pathLen = len(self._startPath)
        if pathLen > 0:
            path = self._startPath.pop(random.randint(0, pathLen - 1))
            newX = path[0]
            newY = path[1]
            
            # 再帰処理として自身（dig）を呼び出す
            self.dig(newX, newY)
        else:
            self._isCreated = True
        
        
    # プレイヤーの配置
    def setPlayer(self, x, y):
        if (
            self._isCreated and
            x > 0 and x < self._width - 1 and y > 0 and y < self._height and
            self._data[y][x] == self.PATH
        ):
            self._playerPoint = [x, y]
            self._movePath.append([x, y])
           
    # プレイヤーを移動させる
    def movePlayer(self, direction):
        if self._playerPoint != None:
            x = self._playerPoint[0]
            y = self._playerPoint[1]
            
            prevX = x
            prevY = y

            if direction == self.UP and y > 0 and self._data[y-1][x] == self.PATH:
                y -= 1
            elif direction == self.DOWN and y < len(self._data) - 1 and self._data[y+1][x] == self.PATH:
                y += 1
            elif direction == self.LEFT and x > 0 and self._data[y][x-1] == self.PATH:
                x -= 1
            elif direction == self.RIGHT and x < len(self._data[0]) - 1 and self._data[y][x+1] == self.PATH:
                x += 1

            # 引き返している際は現在いるパスを消してから値を入れる                
            if self.movePathContains(x, y) == True:
                mp = self.getFromMovePath(prevX,  prevY)
                if mp != None:
                    self._movePath.remove(mp)
            else:
                self._movePath.append([x, y])

            self._playerPoint = [x, y]

    # _movePathが指定した値を保有しているかどうかを調べる
    def movePathContains(self, x, y):
        for mp in self._movePath:
            if mp[0] == x and mp[1] == y:
                return True
        return False

    # _movePathが保有している要素を検索して返す
    def getFromMovePath(self, x, y):
        for mp in self._movePath:
            if mp[0] == x and mp[1] == y:
                return mp
        return None
            
    # スタート位置を指定する
    def setStartPoint(self, x, y):
        if(
            self._isCreated and
            x > 0 and x < self._width - 1 and y > 0 and y < self._height and
            self._data[y][x] == Maze.PATH
        ):
            self._startPoint = [x, y]
            
    # ゴール位置を指定する
    def setGoalPoint(self, x, y):
        if(
            self._isCreated and
            x > 0 and x < self._width -1 and y > 0 and y < self._height and
            self._data[y][x] == Maze.PATH
        ):
            self._goalPoint = [x, y]
            
    # _endPathからランダムの位置を取得する
    def getRandomEndPath(self):
        result = [-1, -1]
        
        pathLen = len(self._endPath)
        if pathLen > 0:
            result = self._endPath[random.randint(0, pathLen - 1)]
            #result = self._endPath.pop(random.randint(0, pathLen - 1))
            
        return result

    # プレイヤーがゴール地点にいるかどうかの判定を行う
    def isPlayerOnGoalPoint(self):
        return (
            self._playerPoint[0] == self._goalPoint[0] and
            self._playerPoint[1] == self._goalPoint[1]
        )

     # プレイヤーをマニュアル操作する
    def palyManualy(self):
        step = 0

        while True:
            i = input("移動方向を入力してください(上:w, 下:s, 左:a, 右:d) : ")
            
            if i == "w":
                self.movePlayer(Maze.UP)
            elif i == "s":
                self.movePlayer(Maze.DOWN)
            elif i == "a":
                self.movePlayer(Maze.LEFT)
            elif i == "d":
                self.movePlayer(Maze.RIGHT)

            self.draw()

            step += 1

            # ゴール地点に到着したらループを終了する
            if self.isPlayerOnGoalPoint() == True:
                  break;

        message = "Clear Maze (Step:{})".format(step)
        print(message)

    # ランダム制御でプレイヤーを操作する
    def playAuto01(self):
        step = 0

        while True:
            x = self._playerPoint[0]
            y = self._playerPoint[1]

            movableList = []

            if y - 1 > 0 and self._data[y - 1][x] == Maze.PATH:
                movableList.append(Maze.UP)
            if y + 1 < self._height and  self._data[y + 1][x] == Maze.PATH:
                movableList.append(Maze.DOWN)
            if x - 1 > 0 and self._data[y][x-1] == Maze.PATH:
                movableList.append(Maze.LEFT)
            if x + 1 < self._width and self._data[y][x + 1] == Maze.PATH:
                movableList.append(Maze.RIGHT)

            if len(movableList) > 0:
                  moveDirection = movableList[random.randint(0, len(movableList) - 1)]
              #moveDirection = movableList[0]
            else:
                  break

            self.movePlayer(moveDirection)
            #self.movePlayer(random.randint(0, 3))

            step += 1

            # ゴール地点に到着したらループを終了する
            if self.isPlayerOnGoalPoint() == True:
                break;

        self.draw()
        message = "Clear Maze (Step:{})".format(step)
        print(message)
            
    # 迷路をビジュアライズして描画する
    def draw(self):
        if self._isCreated == False:
            return
        
        playerX = -1
        playerY = -1
        if self._playerPoint != None:
            playerX = self._playerPoint[0]
            playerY = self._playerPoint[1]

        m = ""
        for h in range(0, self._height):
            for w in range(0, self._width):
                mp = self.getFromMovePath(w, h)

                if playerX == w and playerY == h:
                    m += "☆"
                elif self._startPoint[0] == w and self._startPoint[1] == h:
                    m += "Ｓ"
                elif self._goalPoint[0] == w and self._goalPoint[1] == h:
                    m += "Ｇ"
                elif mp != None and mp[0] == w and mp[1] == h:
                    m += "＊"
                elif self._data[h][w] == Maze.WALL:
                    m += "■"
                elif self._data[h][w] == Maze.PATH:
                    m += "□"
            
            m += "\n" # 列の処理が終わったら改行コードを入れる
            
        print(m)
# 迷路をテキスト化したものを取得する
    def getMazeText(self):
        if self._isCreated == False:
            return
        
        playerX = -1
        playerY = -1
        if self._playerPoint != None:
            playerX = self._playerPoint[0]
            playerY = self._playerPoint[1]
            
        m = ""
        for h in range(0, self._height):
            for w in range(0, self._width):
                mp = self.getFromMovePath(w, h)

                if playerX == w and playerY == h:
                    m += "☆"
                elif self._startPoint[0] == w and self._startPoint[1] == h:
                    m += "Ｓ"
                elif self._goalPoint[0] == w and self._goalPoint[1] == h:
                    m += "Ｇ"
                elif mp != None and mp[0] == w and mp[1] == h:
                    m += "＊"
                elif self._data[h][w] == Maze.WALL:
                    m += "■"
                elif self._data[h][w] == Maze.PATH:
                    m += "□"
            
            m += "\n" # 列の処理が終わったら改行コードを入れる
            
            
        # 生成したテキストをリターンする
        return m
    
    score=0
    prescore=0
    nowscore=0
    px=1
    py=1
    cnt=0
    op=[]
    cl=[]
    opcl=[]
    ar2=[[] for i in range(4)]
    def Afind(self,x,h):
        #print("わからん")
        #self.px=self._playerPoint[0]           
        #self.py=self._playerPoint[1]

        self.op.append(0,self.px,self.py)
        opcl=[[0 for i in range(x)]for i in range(y)]
        self.headache(nowscore,px,py) 
        
    def headache(self,ns,spx,spy):
        saiki(self,ns,spx,spy)
        while len(self.op)==0:
            self.op.sort()
            if self.op[0][1]==self._goalPoint[0] and self.op[0][2]==self._goalPoint[1]:
                self.cl.append(self._goalPoint[0],self._goalPoint[1])
                print(self.cl)
                break
            saiki(ns,self.op[0][1],self.op[0][2])
            
    def saiki(self,ns,spx,spy):
        if self._data[spx+1][spy]== Maze.PATH and not self.opcl[spx+1][spy]==0 and self._data[spx-1][spy]== Maze.PATH and not self.opcl[spx-1][spy]==0 and self._data[spx][spy+1]== Maze.PATH and not self.opcl[spx][spy+1]==0 and self._data[spx][spy-1]== Maze.PATH and not self.opcl[spx][spy-1]==0:
            self.opcl[spx][spy]=2
            self.cl.append(spx,spy)
            self.op.pop(0)
            return
        if self._data[spx+1][spy]== Maze.PATH and self.opcl[spx+1][spy]==0:
            self.opcl[spx+1][spy]=1
            self.op.append(Pres(spx+1,spy)+ns,spx+1,spy)
        if self._data[spx-1][spy]== Maze.PATH and self.opcl[spx-1][spy]==0:
            self.opcl[spx-1][spy]=1
            self.op.append(Pres(spx-1,spy)+ns,spx-1,spy)
        if self._data[spx][spy+1]== Maze.PATH and self.opcl[spx][spy+1]==0:
            self.opcl[spx][spy+1] = 1
            self.op.append(Pres(spx,spy+1)+ns,spx,spy+1)
        if self._data[spx][spy-1]== Maze.PATH and self.opcl[spx][spy-1]==0:
            self.opcl[spx][spy-1] = 1
            self.op.append(Pres(spx,spy-1)+ns,spx,spy-1)
        opcl[spx][spy]=2
        self.cl.append(spx,spy)
        self.op.pop(0)
        return
    
    def Pres(spx,spy):
        presocre= self._goalPoint[0]-spx+self._goalPoint[1]-spy
        return  presocre
            


# In[ ]:




