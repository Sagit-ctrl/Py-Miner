import pygame, sys, random
from pygame.locals import *
from inpt import beforeStart
from data import *

# Tạo sẵn các màu sắc
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
SILVER = (215, 215, 215)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
MAROON = (128, 0, 0)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
ORANGE = (255, 140, 0)
EMPTY = (0, 0, 0, 0)
# Thông số cơ bản của màn hình hiển thị
WIDTH = 25
HEIGHT = 25
BLANK = 2
NUM_X = 16
NUM_Y = 16
WINDOWHEIGHTADD = NUM_Y*HEIGHT + (NUM_Y + 1)*BLANK + 100
WINDOWWIDTH = NUM_X*WIDTH + (NUM_X + 1)*BLANK
WINDOWHEIGHT = NUM_Y*HEIGHT + (NUM_Y + 1)*BLANK
# Thông số cơ bản của game
NUM_MINE = 40

pygame.init()
FPS = 6
fpsClock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHTADD), SRCALPHA, pygame.RESIZABLE)
programIcon = pygame.image.load('image/mine.png')
pygame.display.set_icon(programIcon)
pygame.display.set_caption('Miner')

# Các hàm hiển thị
def color():
    x = random.randrange(0, 10)
    list_color = [BLACK, RED, GREEN, BLUE, YELLOW, MAGENTA, MAROON, PURPLE, TEAL, NAVY, ORANGE]
    color = list_color[x]
    return color

def display(font_size, status, font_color, X1, X2, Y1, Y2):
    status = str(status)
    font = pygame.font.SysFont('consolas', font_size)
    surface = font.render(status, True, font_color)
    size = surface.get_size()
    posx = (X1 - size[0]) / 2 + X2
    posy = (Y1 - size[1]) / 2 + Y2
    SCREEN.blit(surface, (posx, posy))
    return [posx, posy]

def displayImage(name_file, scaleX, scaleY, X1, X2, Y1, Y2, relative = False, posx = 0, posy = 0):
    surface = pygame.image.load('image/' + str(name_file))
    surface = pygame.transform.scale(surface, (scaleX, scaleY))
    size = surface.get_size()
    if relative:
        posx = posx
        posy = posy
    else:
        posx = (X1 - size[0]) / 2 + X2
        posy = (Y1 - size[0]) / 2 + Y2
    SCREEN.blit(surface, (posx, posy))
    return [posx, posy]

def choice_color(number):
    list_color = [RED, GREEN, BLUE, YELLOW, ORANGE]
    return list_color[number]


# Các hàm xử lý dữ liệu
def changeDatabase(name, point, time, realtime):
    insert_check = False
    data = readSqliteTable()
    print(data)
    endid = len(data) - 1
    if endid == 0:
        pass
    else:
        for i in range(endid):
            deleteSqliteRecord(i)

    for i in range(len(data)):
        if point > data[i][2] and not insert_check:
            data.insert(i, [0, name, point, time, realtime])
            insert_check = True
        elif point == data[i][2] and not insert_check:
            if realtime <= data[i][4] and not insert_check:
                data.insert(i, (0, name, point, time, realtime))
                insert_check = True

    print(data)
    for i in range(len(data)):
        InsertbyQueryPython(i, data[i][1], data[i][2], data[i][3], data[i][4])

def changeTime(realtime):
    second_after_process = int(realtime / 1000)
    minute = int(second_after_process / 60)
    second = second_after_process - minute * 60
    if minute < 10:
        if second < 10:
            time = '0' + str(minute) + ':' + '0' + str(second)
        else:
            time = '0' + str(minute) + ':' + str(second)
    else:
        if second < 10:
            time = str(minute) + ':' + '0' + str(second)
        else:
            time = str(minute) + ':' + str(second)
    return time

def randomPositionMine():
    # Tạo ra mìn
    position_mine = []
    quantity_mine = 0
    while quantity_mine < NUM_MINE:
        check = False
        x = random.randrange(0, NUM_X, 1)
        y = random.randrange(0, NUM_Y, 1)
        if len(position_mine) == 0:
            pass
        else:
            for i in range(len(position_mine)):
                if x == position_mine[i][0] and y == position_mine[i][1]:
                    check = True
                else:
                    pass
        if not check:
            position_mine.append([x, y])
        quantity_mine = len(position_mine)
    print(position_mine)
    return position_mine

def createNumber(position_mine):

    position_number = []
    # Tạo ra số
    for i in range(NUM_X):
        for j in range(NUM_Y):
            count = 0
            around = [[i - 1, j - 1], [i, j - 1], [i + 1, j - 1], [i - 1, j], [i + 1, j], [i - 1, j + 1], [i, j + 1],
                           [i + 1, j + 1]]
            for around in around:
                for mine in position_mine:
                    if around[0] == mine[0] and around[1] == mine[1]:
                        count += 1
            position_number.append([i, j, count])

    for number in position_number:
        for mine in position_mine:
            if number[0] == mine[0] and number[1] == mine[1]:
                number[2] = 9

    return position_number

def Position(position_number):
    position = position_number

    # Tạo ra cái gì đó
    for i in position:
        i.append(0)

    return position

def check_pos_mouse(pos):
    check_pos_position = False
    check_pos = []
    for i in range(NUM_X + 1):
        for j in range(NUM_Y + 1):
            x = BLANK * (i + 1) + WIDTH * i
            y = BLANK * (j + 1) + HEIGHT * j
            if x > pos[0] and y > pos[1] and check_pos_position == False:
                check_pos = [i - 1, j - 1]
                check_pos_position = True
    return check_pos

def check_lose(pos, position_mine):
    pos = check_pos_mouse(pos)
    for mine in position_mine:
        if pos[0] == mine[0] and pos[1] == mine[1]:
            return True

def check_win(coverList):
    count = 0
    for cover in coverList:
        if cover[3] == 0:
            count += 1
    if count == NUM_MINE:
        return True
    else:
        return False

# Các class chạy trong hàm GameRun()
class Board():

    def __init__(self):
        self.surface = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
        self.time = 0
        self.color = color()
        self.quantity = 0
        self.image_icon = str('smile.png')

    def draw(self):

        displayImage('back2.jpg', WINDOWWIDTH, 100, 0, 0, 0, 0, True, 0, WINDOWHEIGHT)
        self.surface.fill(BLACK)
        SCREEN.blit(self.surface, (0, 0))

        for i in range(NUM_X):
            for j in range(NUM_Y):
                color = WHITE
                x = BLANK * (i + 1) + WIDTH * i
                y = BLANK * (j + 1) + HEIGHT * j
                pygame.draw.rect(SCREEN, color, (x, y, WIDTH, HEIGHT))

        pos = display(HEIGHT, str(self.quantity), WHITE, WINDOWWIDTH / 2, 0, 100, WINDOWHEIGHT)
        displayImage('flag.jpg', WIDTH, HEIGHT, 0, 0, 0, 0, True, pos[0] - 40, pos[1])
        display(HEIGHT, str(self.time), WHITE, WINDOWWIDTH / 2, WINDOWWIDTH / 2, 100, WINDOWHEIGHT)
        displayImage(self.image_icon, WIDTH * 2, HEIGHT * 2, WINDOWWIDTH, 0, 100, WINDOWHEIGHT)
        pygame.draw.rect(SCREEN, self.color, pygame.Rect(WINDOWWIDTH / 4 - WIDTH * 7 / 4 - 20, 50 + WINDOWHEIGHT - HEIGHT / 10 * 11, WIDTH * 2 + 40, HEIGHT * 2), 2)

    def update(self, quantity, time, changeicon, color):
        self.color = color
        self.quantity = quantity
        self.time = changeTime(time)
        if changeicon == 1:
            self.image_icon = str('glass.png')
        elif changeicon == 2:
            self.image_icon = str('cry.png')

    def output(self):
        return self.time

class Mine():

    def __init__(self):
        self.position = []

    def start(self, position_mine):
        self.position = position_mine

    def draw(self):
        for i in range(len(self.position)):
            x = BLANK * (self.position[i][0] + 1) + WIDTH * self.position[i][0]
            y = BLANK * (self.position[i][1] + 1) + HEIGHT * self.position[i][1]
            displayImage('mine.png', WIDTH, HEIGHT, 0, 0, 0, 0, True, x, y)

    def output(self):
        return self.position

class Number():

    def __init__(self):
        self.position = []
        self.color = [BLACK, RED, BLUE, TEAL, MAGENTA, MAROON, PURPLE, GREEN, NAVY]
        self.font = pygame.font.SysFont('consolas', 22)
        self.surface = self.font.render('', True, RED)

    def start(self, position_number):
        self.position = position_number

    def draw(self):
        color_num = BLACK
        for i in range(len(self.position)):
            x = self.position[i][2]
            if x == 9:
                pass
            else:
                color_num = self.color[x]

            self.surface = self.font.render(str(self.position[i][2]), True, color_num)
            size = self.surface.get_size()
            x = BLANK * (self.position[i][0] + 1) + WIDTH * self.position[i][0] + (WIDTH - size[0])/2
            y = BLANK * (self.position[i][1] + 1) + HEIGHT * self.position[i][1] + (HEIGHT - size[1])/2
            if self.position[i][2] != 0 and self.position[i][2] != 9:
                SCREEN.blit(self.surface, (x, y))

    def output(self):
        return self.position

class CoverBoard():

    def __init__(self):
        self.cover = []
        self.check_pos = [None, None]
        self.endL = 0

    def start(self, position):
        self.cover = position

    def inpt(self, pos):
        self.check_pos = pos

    def draw(self):
        for cover in self.cover:
            if cover[3] == 1:
                pass
            else:
                color = YELLOW
                x = BLANK * (cover[0] + 1) + WIDTH * cover[0]
                y = BLANK * (cover[1] + 1) + HEIGHT * cover[1]
                # displayImage('block.png', WIDTH, HEIGHT, 0, 0, 0, 0, True, x, y)
                pygame.draw.rect(SCREEN, color, (x, y, WIDTH, HEIGHT))

    def update(self, process):
        if process == 1:
            for cover in self.cover:
                if cover[0] == self.check_pos[0] and cover[1] == self.check_pos[1]:
                    cover[3] = 1
            for cover in self.cover:
                if cover[3] == 1 and cover[2] == 0:
                    i = cover[0]
                    j = cover[1]
                    around = [[i-1, j-1], [i, j-1], [i+1, j-1], [i-1, j], [i+1, j], [i-1, j+1], [i, j+1], [i+1, j+1]]
                    for around in around:
                        for cover in self.cover:
                            if cover[0] == around[0] and cover[1] == around[1]:
                                    cover[3] = 1
        elif process == 2:
            for cover in self.cover:
                cover[3] = 1
        elif process == 3:
            for cover in self.cover:
                if cover[1] == self.endL:
                    cover[3] = 0
            self.endL += 1

    def output(self):
        return self.cover

    def end(self):
        return self.endL

class Mark():

    def __init__(self):
        self.position = []
        self.quantity = len(self.position)
        self.surface = pygame.image.load("image/flag.jpg")
        self.surface = pygame.transform.scale(self.surface, (WIDTH, HEIGHT))

    def draw(self):
        for i in range(len(self.position)):
            x = BLANK * (self.position[i][0] + 1) + WIDTH * self.position[i][0]
            y = BLANK * (self.position[i][1] + 1) + HEIGHT * self.position[i][1]
            SCREEN.blit(self.surface, (x, y))

    def update(self, pos):
        check_pos_position = False

        for i in range(NUM_X + 1):
            for j in range(NUM_Y + 1):
                x = BLANK * (i + 1) + WIDTH * i
                y = BLANK * (j + 1) + HEIGHT * j
                if x > pos[0] and y > pos[1] and check_pos_position == False:
                    if self.position.count([i - 1, j - 1]) > 0:
                        self.position.remove([i - 1, j - 1])
                        check_pos_position = True
                    else:
                        self.position.append([i - 1, j - 1])
                        check_pos_position = True

    def output(self):
        self.quantity = len(self.position)
        return self.quantity

# Các hàm xử lý chính ( các screen trong game ~ mỗi hàm là một màn hình)
def GameStart(name):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                return

        displayImage('back.png', WINDOWWIDTH + 300, WINDOWHEIGHTADD, 0, 0, 0, 0, True, 0, 0)
        display(100, 'MINER', color(), WINDOWWIDTH, 0, WINDOWHEIGHT, 0)
        display(30, 'Welcome to MINER,' + ' ' + str(name), color(), WINDOWWIDTH, 0, WINDOWHEIGHT, 100)
        display(20, 'Press anything to continue', RED, WINDOWWIDTH, 0, WINDOWHEIGHT, 200)

        pygame.display.update()
        fpsClock.tick(FPS)

def GameRun(board, mine, number, coverboard, mark):

    # Khởi tạo hệ thống
    randomBoard = randomPositionMine()
    mine.start(randomBoard)
    createNum = createNumber(mine.output())
    number.start(createNum)
    position = Position(number.output())
    coverboard.start(position)

    # Khởi tạo các giá trị boolen xác định trạng thái game
    pressSpace = False
    checkwin = False
    checklose = False
    checktime = False
    changeIcon = 0
    process_in_coverboard = 1
    starttime = 0

    # Vòng lặp game
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Chuột trái mở map
            elif event.type == MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
                if not checkwin and not checklose:
                    pos = pygame.mouse.get_pos()
                    coverboard.inpt(check_pos_mouse(pos))
                    checklose = check_lose(pos, randomBoard)
                    checktime = True
            # Chuột phải đánh dấu
            elif event.type == MOUSEBUTTONDOWN and event.button == BUTTON_RIGHT:
                if not checkwin and not checklose:
                    pos = pygame.mouse.get_pos()
                    mark.update(pos)
                    checktime = True
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if checkwin or checklose:
                        pressSpace = True
                # Khởi tạo lại thời gian
                if event.key == K_RETURN and checktime == False:
                    starttime = pygame.time.get_ticks()
                    checktime = True

        # Draw game
        time = pygame.time.get_ticks() - starttime
        board.update(mark.output(), time, changeIcon, color())
        board.draw()
        mine.draw()
        number.draw()
        coverboard.update(process_in_coverboard)
        coverboard.draw()
        if not checktime:
            display(20, 'Press "enter" to start', color(), WINDOWWIDTH, 0, WINDOWHEIGHT * 2, 10)

        # Kiểm tra điều kiện thắng
        if not checkwin and not checklose:
            mark.draw()
            checkwin = check_win(coverboard.output())
        else:
            if checkwin:
                display(80, 'You win', color(), WINDOWWIDTH, 0, WINDOWHEIGHT, 0)
                changeIcon = 1
            elif checklose:
                display(80, 'You lose', color(), WINDOWWIDTH, 0, WINDOWHEIGHT, 0)
                changeIcon = 2
            display(20, 'Press "space" to continnue', color(), WINDOWWIDTH, 0, WINDOWHEIGHT * 2, 10)

            if pressSpace == False:
                process_in_coverboard = 2
            else:
                process_in_coverboard = 3
                check = coverboard.end()
                if check == NUM_Y:
                    if checkwin == True:
                        return [NUM_MINE, str(board.output()), time]
                    else:
                        return [0, 0, 0]


        pygame.display.update()
        fpsClock.tick(FPS)

def GameEnd(name, point, time, realtime):
    list = []
    if point == 0 and realtime == 0:
        pass
    else:
        changeDatabase(name, point, time, realtime)

    data = readSqliteTable()
    for i in range(5):
        list.append(data[i])

    SCREEN.fill(WHITE)
    displayImage('back4.jpg', WINDOWWIDTH, WINDOWHEIGHTADD, 0, 0, 0, 0, True, 0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_a:
                    return 1
                elif event.key == K_q:
                    pygame.quit()
                    sys.exit()
                else:
                    return 0

        display(50, 'CONGTURALATION!', color(), WINDOWWIDTH, 0, WINDOWHEIGHTADD / 4, 0)

        sepWinX = WINDOWWIDTH / 4
        sepWinY = WINDOWHEIGHTADD / 32

        color_ = color()

        display(30, 'Rank', color_, sepWinX, 0, sepWinY, sepWinY * 8)
        for i in range(len(list)):
            status = i + 1
            display(30, status, choice_color(i), sepWinX, 0, sepWinY * 3, sepWinY * 8 + (i + 1) * 50)

        display(30, 'Name', color_, sepWinX, sepWinX, sepWinY, sepWinY * 8)
        for i in range(len(list)):
            status = str(list[i][1])
            display(30, status, choice_color(i), sepWinX, sepWinX, sepWinY * 3, sepWinY * 8 + (i + 1) * 50)

        display(30, 'Score', color_, sepWinX, sepWinX * 2, sepWinY, sepWinY * 8)
        for i in range(len(list)):
            status = str(list[i][2])
            display(30, status, choice_color(i), sepWinX, sepWinX * 2, sepWinY * 3, sepWinY * 8 + (i + 1) * 50)

        display(30, 'Time', color_, sepWinX, sepWinX * 3, sepWinY, sepWinY * 8)
        for i in range(len(list)):
            status = str(list[i][3])
            display(30, status, choice_color(i), sepWinX, sepWinX * 3, sepWinY * 3, sepWinY * 8 + (i + 1) * 50)

        display(20, 'Press "A" to play again', WHITE, WINDOWWIDTH, 0, 100, WINDOWHEIGHT - 40)
        display(20, 'Press anything to continue', WHITE, WINDOWWIDTH, 0, 100, WINDOWHEIGHT)

        pygame.display.update()
        fpsClock.tick(FPS)

def main():

    again = 0
    while True:
        # Khai báo tiền xử lý
        board = Board()
        mine = Mine()
        number = Number()
        coverboard = CoverBoard()
        mark = Mark()


        if again == 0:
            name = beforeStart(SCREEN, color(), fpsClock, 60, WINDOWWIDTH, WINDOWHEIGHTADD)
            GameStart(name)
        else:
            pass

        score = GameRun(board, mine, number, coverboard, mark)
        again = GameEnd(name, score[0], score[1], score[2])

if __name__ == '__main__':
    main()

