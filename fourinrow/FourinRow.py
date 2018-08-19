#coding:utf-8
import random, copy, sys, pygame
from pygame.locals import *

BOARDWIDTH = 7  # 棋子盘的宽度栏数
BOARDHEIGHT = 6 # 棋子盘的高度栏数
assert BOARDWIDTH >= 4 and BOARDHEIGHT >= 4, 'Board must be at least 4x4.'

#python assert断言是声明其布尔值必须为真的判定，如果发生异常就说明表达示为假。
#可以理解assert断言语句为raise-if-not，用来测试表示式，其返回值为假，就会触发异常。

DIFFICULTY = 2 # 难度系数，计算机能够考虑的移动级别
               #这里2表示，考虑对手走棋的7种可能性及如何应对对手的7种走法

SPACESIZE = 50 # 棋子的大小

FPS = 30 # 屏幕的更新频率，即30/s
WINDOWWIDTH = 640  # 游戏屏幕的宽度像素
WINDOWHEIGHT = 480 # 游戏屏幕的高度像素

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)#X边缘坐标量，即格子栏的最左边
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)#Y边缘坐标量，即格子栏的最上边
BRIGHTBLUE = (0, 50, 255)#蓝色
WHITE = (255, 255, 255)#白色

BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

RED = 'red'
BLACK = 'black'
EMPTY = None
HUMAN = 'human'
COMPUTER = 'computer'

#初始化pygame的各个模块
pygame.init()

#初始化了一个Clock对象
FPSCLOCK = pygame.time.Clock()

#创建游戏窗口
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

#游戏窗口标题
pygame.display.set_caption(u'four in row')

#Rect(left,top,width,height)用来定义位置和宽高
REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)


#这里创建的是窗口中左下角和右下角的棋子
BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE, SPACESIZE)

#载入红色棋子图片
REDTOKENIMG = pygame.image.load('4rowred.png')

#将红色棋子图片缩放为SPACESIZE
REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))

#载入黑色棋子图片
BLACKTOKENIMG = pygame.image.load('4rowblack.png')

#将黑色棋子图片缩放为SPACESIZE
BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))

#载入棋子面板图片
BOARDIMG = pygame.image.load('4rowboard.png')

#将棋子面板图片缩放为SPACESIZE
BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))

#载入人胜利时图片
HUMANWINNERIMG = pygame.image.load('4rowhumanwinner.png')

#载入AI胜时图片
COMPUTERWINNERIMG = pygame.image.load('4rowcomputerwinner.png')

#载入平局提示图片
TIEWINNERIMG = pygame.image.load('4rowtie.png')

#返回一个Rect实例
WINNERRECT = HUMANWINNERIMG.get_rect()

#游戏窗口中间位置坐标
WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

#载入操作提示图片
ARROWIMG = pygame.image.load('4rowarrow.png')

#返回一个Rect实例
ARROWRECT = ARROWIMG.get_rect()

#操作提示的左位置
ARROWRECT.left = REDPILERECT.right + 10

#将操作提示与下方红色棋子实例在纵向对齐
ARROWRECT.centery = REDPILERECT.centery

def drawBoard(board, extraToken=None):
    #DISPLAYSURF是我们的界面，在初始化变量模块中有定义
    DISPLAYSURF.fill(BGCOLOR)#将游戏窗口背景填充为蓝色
    spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE)
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            if board[x][y] == RED:#如果格子值为红色
                #则在游戏窗口的的spaceRect中画红色棋子
                DISPLAYSURF.blit(REDTOKENIMG, spaceRect)
            elif board[x][y] == BLACK:#否则画黑色棋子
                DISPLAYSURF.blit(BLACKTOKENIMG, spaceRect)

    # extraToken是包含了位置信息和颜色信息的变量
    # 用来显示指定的棋子
    if extraToken != None:
        if extraToken['color'] == RED:
            DISPLAYSURF.blit(REDTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))
        elif extraToken['color'] == BLACK:
            DISPLAYSURF.blit(BLACKTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))

    # 画棋子面板
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            DISPLAYSURF.blit(BOARDIMG, spaceRect)

    # 画游戏窗口中左下角和右下角的棋子
    DISPLAYSURF.blit(REDTOKENIMG, REDPILERECT)
    DISPLAYSURF.blit(BLACKTOKENIMG, BLACKPILERECT)

def getNewBoard():
    board = []
    for x in range(BOARDWIDTH):
        board.append([EMPTY] * BOARDHEIGHT)
        return board#返回board列表，其值为BOARDHEIGHT数量的None

def getPotentialMoves(board, tile, lookAhead):
    if lookAhead == 0 or isBoardFull(board):
        '''
         如果难度系数为0，或格子已满
         则返回列表值全为0，即此时适应度值和列的潜在移动值相等。
         此时AI将随机降落棋子，失去智能
        '''
        return [0] * BOARDWIDTH

    #确定对手棋子颜色
    if tile == RED:
        enemyTile = BLACK
    else:
        enemyTile = RED
    potentialMoves = [0] * BOARDWIDTH
    #初始一个潜在的移动列表，其数值全部为0
    for firstMove in range(BOARDWIDTH):
        #对每一栏进行遍历，将双方中的任一方的移动称为firstMove
        #则另外一方的移动就称为对手，counterMove
        #这里我们的firstMove为AI，对手为玩家
        dupeBoard = copy.deepcopy(board)
        #这里用深复制是为了让board和dupeBoard互不影响
        if not isValidMove(dupeBoard, firstMove):
            #如果在dupeBoard中黑色棋子移到firstMove栏无效
            continue
        #进行下一个firstMove
        makeMove(dupeBoard, tile, firstMove)
        #如果是有效的移动，则设置相应的格子颜色

        if isWinner(dupeBoard, tile):
            potentialMoves[firstMove] = 1
            #获胜的棋子自动获得一个很高的数值来表示其获胜的几率
            #数值越大，获胜的可能性越大，对手获胜的可能性越小
            break
        else:
            if isBoardFull(dupeBoard):
                #如果dupeBoard中没有空格，无法移动
                potentialMoves[firstMove] = 0
            else:
                for counterMove in range(BOARDWIDTH):
                    #考虑对手的移动
                    dupeBoard2 = copy.deepcopy(dupeBoard)
                    if not isValidMove(dupeBoard2, counterMove):
                        continue
                    makeMove(dupeBoard2, enemyTile, counterMove)
                    if isWinner(dupeBoard2, enemyTile):
                        potentialMoves[firstMove] = -1
                        #如果玩家获胜，则AI在此栏的值最低
                        break
                    else:
                        #递归调用getPotentialMoves
                        results = getPotentialMoves(dupeBoard2, tile, lookAhead - 1)
                        potentialMoves[firstMove] += (sum(results) / BOARDWIDTH) / BOARDWIDTH
    return potentialMoves

#玩家操作
def getHumanMove(board, isFirstMove):
    draggingToken = False
    tokenx, tokeny = None, None
    while True:
        #pygame.event.get()来处理所有事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and not draggingToken and REDPILERECT.collidepoint(event.pos):
                #如果事件类型为鼠标按下，notdraggingToken为True，鼠标点击的位置在REDPILERECT里面
                draggingToken = True
                tokenx, tokeny = event.pos
            elif event.type == MOUSEMOTION and draggingToken:#如果开始拖动了红色棋子
                tokenx, tokeny = event.pos #更新被拖拽的棋子位置
            elif event.type == MOUSEBUTTONUP and draggingToken:
                #如果鼠标松开，并且棋子被拖拽

                #如果棋子被拖拽在board的正上方
                if tokeny < YMARGIN and tokenx > XMARGIN and token < WINDOWWIDTH - XMARGIN:
                    column = int((tokenx - XMARGIN) / SPACESIZE)#根据棋子的x坐标确定棋子会落到的列(0,1...6)
                    if isValidMove(board, column):#如果棋子移动有效
                        '''
                         掉落在相应的空格子中，
                         这里只是显示一个掉落的效果
                         不用这个函数也能通过小面的代码实现棋子填充空格
                        '''
                        animateDroppingToken(board, column, RED)

                        #将空格中最下面的格子设为红色
                        board[column][getLowestEmptySpace(board, column)] = RED
                        drawBoard(board)#在落入的格子中画红色棋子
                        pygame.display.update()#窗口更新
                        return
                tokenx, tokeny = None, None
                draggingToken = False
        if tokenx != None and tokeny != None:#如果拖动了棋子，则显示拖动的棋子
            #并且通过调整x,y的坐标使拖动时，鼠标始终位于棋子的中心位置
            drawBoard(board, {'x':tokenx - int(SPACESIZE/2), 'y':tokeny - int(SPACESIZE/2), 'color':RED})
        else:
            #当为无效移动时，鼠标松开后，因为此时board中所有格子的值均为none
            #当调用drawBoard时，进行的操作是显示下面的两个棋子，相当于棋子回到开始拖动的地方
            drawBoard(board)

        if isFirstMove:
            DISPLAYSURF.blit(ARROWIMG, ARROWRECT)#AI先走，显示提示操作图片

        pygame.display.update()
        FPSCLOCK.tick()

#AI操作
#实现AI棋子自动移动并降落到相应位置的函数
def animateComputerMoving(board, column):
    x = BLACKPILERECT.left
    y = BLACKPILERECT.top
    speed = 1.0
    while y > (YMARGIN - SPACESIZE):#当y的值比较大，即棋子位于窗口下方时
        y -= int(speed) #y不断减小，即棋子不断上移
        speed += 0.5
        drawBoard(board, {'x':x, 'y':y, 'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()

    #当棋子上升到board顶端时
    y = YMARGIN - SPACESIZE #y重新赋值，此时棋子的最下边和board的最上边相切
    speed = 1.0

    while x > (XMARGIN + column * SPACESIZE): #当x值大于需要移到的列的x坐标时
        x -= int(speed)#x值不断减小，即左移
        speed += 0.5
        drawBoard(board, {'x':x, 'y':y, 'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()
    #黑色棋子降落到计算得到的空格
    animateDroppingToken(board, column, BLACK)

def getComputerMove(board):
    potentialMoves = getPotentialMoves(board, BLACK, DIFFICULTY)#潜在的移动，是一个含BOARDWIDTH个值的列表。。
    print potentialMoves
    bestMoves = []
    bestMoveFitness = max(potentialMoves)
    print bestMoveFitness
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveFitness and isValidMove(board, i):
            bestMoves.append(i) #列出所有可以移动到的列，该列表可能为空，可能只有一个值，也可能有多个值
    print bestMoves
    return random.choice(bestMoves)#从可以移动到的列中，随机选择一个座位移动到的目标

#棋子移动操作
def getLowestEmptySpace(board, column):
    #返回一列中最下面的空格
    for y in range(BOARDHEIGHT-1, -1, -1):
        if board[column][y] == EMPTY:
            return y
    return -1
def makeMove(board, player, column):
    lowest = getLowestEmptySpace(board, column) #返回一栏中
    if lowest != -1:
        board[column][lowest] = player
        '''
         将player(red/black)赋值给一栏中的最low的一个空格，因为棋子是落在一栏当中所有空格的最下面一个空格
        '''

def animateDroppingToken(board, column, color):
    x = XMARGIN + column * SPACESIZE #x坐标
    y = YMARGIN - SPACESIZE #y坐标
    dropSpeed = 1.0
    lowestEmptySpace = getLowestEmptySpace(board, column) #一列的空格当中最下面的一个空格

    while True:
        y += int(dropSpeed)
        dropSpeed += 0.5
        if int((y-YMARGIN)/SPACESIZE) >= lowestEmptySpace:#判断到达最下面的空格
            return
        drawBoard(board, {'x':x, 'y':y, 'color':color})#y不断变化，不断绘制红色棋子，形成不断降落的效果
        pygame.display.update()
        FPSCLOCK.tick()

def isValidMove(board, column):
    #判断棋子移动有效性
    if column < 0 or column >= (BOARDWIDTH) or board[column][0] != EMPTY:
        #如果列<0 或者 > BOARDWIDTH，或列中没有空格子
        return False
    return True

def isBoardFull(board):
    #如果格子中没有空余，则返回True
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == EMPTY:
                return False
    return True

#获胜条件判断
def isWinner(board, tile):
    #检查水平方向棋子情况
    for x in range(BOARDWIDTH - 3): #x的取值为0,1,2,3
        for y in range(BOARDHEIGHT): #遍历所有的行
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True

    #检查竖直方向棋子情况，与水平类似
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True

    #检查左倾斜方向棋子情况
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):#因为左倾斜连成四子时
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True

    #检查右倾斜方向棋子情况
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True
    return False

#程序运行
def main():
    isFirstGame = True

    while True: #使游戏一直能够运行下去
        runGame(isFirstGame)
        isFirstGame = False

def runGame(isFirstGame):
    if isFirstGame:
        #刚刚启动游戏第一局是，让AI先走第一步棋子，以便玩家可以观察到游戏是怎么玩的
        turn = COMPUTER
        showHelp = True

    else:
        #从第二局开始，随机分配
        if random.randint(0,1) == 0:
            turn = COMPUTER
        else:
            turn = HUMAN
        showHelp = False

if __name__ == '__main__':
    main()
