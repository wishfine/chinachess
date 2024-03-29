import pygame
import time
import constants
from button import Button
import pieces
import socket
import threading
import sys
from tkinter import * #python标准Tk Gui工具包接口
import socket  #网络通信
import asyncio #异步IO
import time #格式化日期和时间
import sys  #内置模块，提供与python解释器和运行环境相关的功能
import threading #多线程
import json, types,string #types--包含常见的数据类型 json--解析json格式 string--字符串操作
from struct import * #支持python与C结构体之间转换
from ctypes import * #外部库，提供与C兼容的数据类型，并允许调用DLL或共享库中的函数



g_qipan = [None]*50
g_count = 0


class MainGame():
    window = None
    Start_X = constants.Start_X
    Start_Y = constants.Start_Y
    Line_Span = constants.Line_Span
    Max_X = Start_X + 8 * Line_Span
    Max_Y = Start_Y + 9 * Line_Span
    from_x = 0
    from_y = 0
    to_x = 0
    to_y = 0
    clickx=-1
    clicky=-1

    player1Color = constants.player1Color
    player2Color = constants.player2Color
    Putdownflag = player1Color


    piecesSelected = None

    button_go = None
    piecesList = []

    def __init__(self, sock):
        self.sock = sock
        self.need_redraw = False  # 添加一个标志来指示是否需要重新绘制界面



    def start_game(self):
        MainGame.window = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])
        pygame.display.set_caption("server")
        self.piecesInit()

        while True:
            time.sleep(0.1)
            # 获取事件
            MainGame.window.fill(constants.BG_COLOR)
            self.drawChessboard()
            self.piecesDisplay()

            self.Computerplay()
            self.getEvent()

            self.VictoryOrDefeat()
            if self.need_redraw == True:
                self.redraw_game_window()
                self.need_redraw = False

            pygame.display.update()
            pygame.display.flip()

    def redraw_game_window(self):
        print('sdsd')
        # 包含绘制棋盘和棋子的逻辑
        self.piecesDisplay()
    def drawChessboard(self):
        mid_end_y = MainGame.Start_Y + 4 * MainGame.Line_Span
        min_start_y = MainGame.Start_Y + 5 * MainGame.Line_Span
        for i in range(0, 9):
            x = MainGame.Start_X + i * MainGame.Line_Span
            if i == 0 or i == 8:
                y = MainGame.Start_Y + i * MainGame.Line_Span
                pygame.draw.line(MainGame.window, constants.BLACK, [x, MainGame.Start_Y], [x, MainGame.Max_Y], 1)
            else:
                pygame.draw.line(MainGame.window, constants.BLACK, [x, MainGame.Start_Y], [x, mid_end_y], 1)
                pygame.draw.line(MainGame.window, constants.BLACK, [x, min_start_y], [x, MainGame.Max_Y], 1)

        for i in range(0, 10):
            x = MainGame.Start_X + i * MainGame.Line_Span
            y = MainGame.Start_Y + i * MainGame.Line_Span
            pygame.draw.line(MainGame.window, constants.BLACK, [MainGame.Start_X, y], [MainGame.Max_X, y], 1)

        speed_dial_start_x = MainGame.Start_X + 3 * MainGame.Line_Span
        speed_dial_end_x = MainGame.Start_X + 5 * MainGame.Line_Span
        speed_dial_y1 = MainGame.Start_Y + 0 * MainGame.Line_Span
        speed_dial_y2 = MainGame.Start_Y + 2 * MainGame.Line_Span
        speed_dial_y3 = MainGame.Start_Y + 7 * MainGame.Line_Span
        speed_dial_y4 = MainGame.Start_Y + 9 * MainGame.Line_Span

        pygame.draw.line(MainGame.window, constants.BLACK, [speed_dial_start_x, speed_dial_y1],
                         [speed_dial_end_x, speed_dial_y2], 1)
        pygame.draw.line(MainGame.window, constants.BLACK, [speed_dial_start_x, speed_dial_y2],
                         [speed_dial_end_x, speed_dial_y1], 1)
        pygame.draw.line(MainGame.window, constants.BLACK, [speed_dial_start_x, speed_dial_y3],
                         [speed_dial_end_x, speed_dial_y4], 1)
        pygame.draw.line(MainGame.window, constants.BLACK, [speed_dial_start_x, speed_dial_y4],
                         [speed_dial_end_x, speed_dial_y3], 1)

    def piecesInit(self):
        MainGame.piecesList.append(pieces.Rooks(MainGame.player2Color, 0, 0))
        MainGame.piecesList.append(pieces.Rooks(MainGame.player2Color, 8, 0))
        MainGame.piecesList.append(pieces.Elephants(MainGame.player2Color, 2, 0))
        MainGame.piecesList.append(pieces.Elephants(MainGame.player2Color, 6, 0))
        MainGame.piecesList.append(pieces.King(MainGame.player2Color, 4, 0))
        MainGame.piecesList.append(pieces.Knighs(MainGame.player2Color, 1, 0))
        MainGame.piecesList.append(pieces.Knighs(MainGame.player2Color, 7, 0))
        MainGame.piecesList.append(pieces.Cannons(MainGame.player2Color, 1, 2))
        MainGame.piecesList.append(pieces.Cannons(MainGame.player2Color, 7, 2))
        MainGame.piecesList.append(pieces.Mandarins(MainGame.player2Color, 3, 0))
        MainGame.piecesList.append(pieces.Mandarins(MainGame.player2Color, 5, 0))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player2Color, 0, 3))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player2Color, 2, 3))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player2Color, 4, 3))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player2Color, 6, 3))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player2Color, 8, 3))

        MainGame.piecesList.append(pieces.Rooks(MainGame.player1Color, 0, 9))
        MainGame.piecesList.append(pieces.Rooks(MainGame.player1Color, 8, 9))
        MainGame.piecesList.append(pieces.Elephants(MainGame.player1Color, 2, 9))
        MainGame.piecesList.append(pieces.Elephants(MainGame.player1Color, 6, 9))
        MainGame.piecesList.append(pieces.King(MainGame.player1Color, 4, 9))
        MainGame.piecesList.append(pieces.Knighs(MainGame.player1Color, 1, 9))
        MainGame.piecesList.append(pieces.Knighs(MainGame.player1Color, 7, 9))
        MainGame.piecesList.append(pieces.Cannons(MainGame.player1Color, 1, 7))
        MainGame.piecesList.append(pieces.Cannons(MainGame.player1Color, 7, 7))
        MainGame.piecesList.append(pieces.Mandarins(MainGame.player1Color, 3, 9))
        MainGame.piecesList.append(pieces.Mandarins(MainGame.player1Color, 5, 9))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player1Color, 0, 6))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player1Color, 2, 6))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player1Color, 4, 6))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player1Color, 6, 6))
        MainGame.piecesList.append(pieces.Pawns(MainGame.player1Color, 8, 6))

    def piecesDisplay(self):
        for item in MainGame.piecesList:
            item.displaypieces(MainGame.window)

    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 获取鼠标位置
                pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = pos[0], pos[1]

                # 确保点击在棋盘内
                if mouse_x > MainGame.Start_X - MainGame.Line_Span / 2 and mouse_x < MainGame.Max_X + MainGame.Line_Span / 2 and mouse_y > MainGame.Start_Y - MainGame.Line_Span / 2 and mouse_y < MainGame.Max_Y + MainGame.Line_Span / 2:
                    click_x = round((mouse_x - MainGame.Start_X) / MainGame.Line_Span)
                    click_y = round((mouse_y - MainGame.Start_Y) / MainGame.Line_Span)

                    # 如果是第一位玩家的轮次
                    if MainGame.Putdownflag == MainGame.player1Color:
                        self.handlePlayerClick(MainGame.player1Color, click_x, click_y)


    def handlePlayerClick(self, playerColor, x, y):
        # 查找玩家点击位置的棋子
        clicked_piece = None
        for piece in MainGame.piecesList:
            if piece.x == x and piece.y == y and piece.player == playerColor:
                clicked_piece = piece
                break

        # 如果玩家之前已选择一个棋子
        if MainGame.piecesSelected:
            # 检查选中的棋子是否可以移动到新位置
            arr = pieces.listPiecestoArr(MainGame.piecesList)
            if MainGame.piecesSelected.canmove(arr, x, y):
                # 移动棋子并清空选择
                self.PiecesMove(MainGame.piecesSelected, x, y)
                MainGame.piecesSelected = None

            else:
                # 如果不能移动，则取消选择
                MainGame.piecesSelected = None
        else:
            MainGame.piecesSelected = clicked_piece

    def PutdownPieces(self, t, x, y):
        selectfilter = list(filter(lambda cm: cm.x == x and cm.y == y and cm.player == MainGame.player1Color,
                                   MainGame.piecesList))
        if len(selectfilter):
            MainGame.piecesSelected = selectfilter[0]
            return

        if MainGame.piecesSelected:
            arr = pieces.listPiecestoArr(MainGame.piecesList)
            if MainGame.piecesSelected.canmove(arr, x, y):
                self.PiecesMove(MainGame.piecesSelected, x, y)
                MainGame.Putdownflag = MainGame.player2Color
        else:
            fi = filter(lambda p: p.x == x and p.y == y, MainGame.piecesList)
            listfi = list(fi)
            if len(listfi) != 0:
                MainGame.piecesSelected = listfi[0]

    def PiecesMove(self, pieces, x, y):
        for item in MainGame.piecesList:
            if item.x == x and item.y == y:
                item.x = None
                item.y = None
        pieces.x = x
        pieces.y = y
        for item in MainGame.piecesList:
            self.send_move_to_client(self.Putdownflag)

    def send_move_to_client(self,Putdownflag):
        """将玩家的移动发送到服务器"""
        for item in MainGame.piecesList:
            msg = [{'player': item.player, 'x': item.x, 'y': item.y}]

            jmsg = json.dumps(msg)
            jmsg_len = len(jmsg)
            pack_msg = pack("l", jmsg_len)

            self.sock.send(pack_msg)
            self.sock.send(bytes(jmsg, 'utf-8'))
        print('cdcd')
        for item in MainGame.piecesList:
            print(item,item.player,item.x,item.y)

    def Computerplay(self):
        if MainGame.Putdownflag == MainGame.player2Color:
            return

    def VictoryOrDefeat(self):
        txt = ""
        result = [MainGame.player1Color, MainGame.player2Color]
        for item in MainGame.piecesList:
            if type(item) == pieces.King:
                if item.player == MainGame.player1Color and item.y == None:
                    txt = "lose"
                    MainGame.Putdownflag = constants.overColor
                if item.player == MainGame.player2Color and item.y == None:
                    txt = "win"
                    MainGame.Putdownflag = constants.overColor

        MainGame.window.blit(self.getTextSuface("%s" % txt), (constants.SCREEN_WIDTH - 100, 200))


    def getTextSuface(self, text):
        pygame.font.init()
        # print(pygame.font.get_fonts())
        font = pygame.font.SysFont('server', 18)
        txt = font.render(text, True, constants.TEXT_COLOR)
        return txt

    def endGame(self):
        print("exit")
        exit()


def net_recv(s, req_len):
    ret_data = b""
    rec_len = 0
    while True:
        data = s.recv(req_len)
        rec_len += len(data)
        ret_data += data
        if rec_len >= req_len:
            break
    return ret_data

def server_listen(s):
    while True:
        for item in MainGame.piecesList:
            data_len = unpack("l", net_recv(s, 4))
            print('data_len:', data_len)
            data = net_recv(s, data_len[0])
            qizi_info = json.loads(data.decode('utf-8'))

            item.player = qizi_info[0]['player']
            item.x = qizi_info[0]['x']
            item.y = qizi_info[0]['y']
        '''for item in MainGame.piecesList:
            print(item,item.player,item.x,item.y)'''
        MainGame.need_redraw = True


def task_func(c, addr, i):
    global g_qipan

    print('in task_func')
    print('连接地址：', addr)
    c.send(bytes('欢迎链接！', encoding='utf-8'))



    # 创建MainGame实例时传递socket
    game = MainGame(c)
    game.start_game()


if __name__ == '__main__':
    s = socket.socket()  # 创建 socket 对象
    # host = socket.gethostname()  # 获取本地主机名

    host = "127.0.0.1"  # 获取本地主机名
    port = 12345  # 设置端口
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s.bind((host, port))  # 绑定端口
    print(host)

    s.listen(5)  # 等待客户端连

    print("waitting for connection...")
    while True:
        c, addr = s.accept()  # 建立客户端连接。

        thread = threading.Thread(target=task_func, args=(c, addr, g_count,))
        thread.start()
        thread = threading.Thread(target=server_listen, args=(c,))
        thread.start()

        g_count += 1

