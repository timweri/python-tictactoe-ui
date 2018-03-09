from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class TicTacToeGame(Widget):
    P1 = 'X'
    P2 = 'O'
    PAT_HOR = [[(0, 0), (0, 1), (0, 2)],
               [(1, 0), (1, 1), (1, 2)],
               [(2, 0), (2, 1), (2, 2)]]
    PAT_VERT = [[(0, 0), (1, 0), (2, 0)],
                [(0, 1), (1, 1), (2, 1)],
                [(0, 2), (1, 2), (2, 2)]]
    PAT_DIAG = [[(0, 0), (1, 1), (2, 2)],
                [(2, 0), (1, 1), (0, 2)]]
    def __init__(self, **kwargs):
        super(TicTacToeGame, self).__init__(**kwargs)
        self.board_state = [[0,0,0],[0,0,0],[0,0,0]]
        self.turn = 1

        self.board = GridLayout(cols=3, rows=3, width=self.width, height=self.height*0.9)
        self.buttons = [[-1,-1,-1],[-1,-1,-1],[-1,-1,-1]]
        for i in range(0,3):
            for j in range(0,3):
                self.buttons[i][j] = Button(id='button' + str(i) + str(j), text='', background_color=(1,0,0,1), font_size=70)
                self.buttons[i][j].bind(on_press=self.grid_callback)
                self.board.add_widget(self.buttons[i][j])
        self.add_widget(self.board, index=0)
        self.bind(size=self.update_board)

        self.box = BoxLayout(orientation='vertical', padding=(10))
        self.dismiss_btn = Button(id='dismiss_btn', text='Dismiss', size_hint=(None,None), size=(self.box.width,self.box.height*0.3), pos_hint={'center_x':.5,'center_y':1})
        self.dismiss_btn.bind(on_press=self.dismiss_callback)
        self.announce_lbl = Label(text='Test', font_size=40)
        self.box.add_widget(self.announce_lbl)
        self.box.add_widget(self.dismiss_btn)

        self.popup = Popup(title='Winner', content=self.box, size_hint=(None,None), size=(400,400), auto_dismiss=False)

        self.ids['new_button'].bind(on_press=self.new_game)

    def update_board(self, instance, value):
        self.board.size = (self.width, self.height*0.9)

    def dismiss_callback(self, instance):
        self.popup.dismiss()

    def reset_board_gridlayout(self):
        for i in range(0,3):
            for j in range(0,3):
                self.buttons[i][j].text = ''

    def new_game(self, instance):
        self.board_state = [[0,0,0],[0,0,0],[0,0,0]]
        self.turn = 1
        self.reset_board_gridlayout()

    # return 0: no one wins
    # return 1: player 1 (X) wins
    # return 2: player 2 (O) wins
    def check_win(self):
        for pats in self.PAT_HOR + self.PAT_VERT + self.PAT_DIAG:
            triple = list(map(lambda x: self.board_state[x[0]][x[1]], pats))
            if (triple[0] == triple[1]) and (triple[1] == triple[2]) and (triple[0] != 0):
                if triple[0] == 1:
                    return 1
                elif triple[1] == 2:
                    return 2
                else:
                    raise ValueError('Unrecognized symbol.')
        for i in range(0,3):
            for j in range(0,3):
                if self.board_state[i][j] == 0:
                    return 0
        return 3

    def win(self, player):
        if player in [1,2]:
            print('Player ', player, ' wins!')
            self.announce_lbl.text='Player ' + str(player)+ ' wins!!!'
        elif player == 3:
            print('Draw!')
            self.announce_lbl.text='Draw!!!'
        else:
            raise ValueError('Unexpected result value.')
        self.popup.open()
        self.new_game(0)

    def move(self, coor):
        x, y = coor
        if self.buttons[x][y].text != '':
            return -1
        if (self.turn == 1):
            self.buttons[x][y].text = self.P1
            self.board_state[x][y] = 1
            self.turn = 2
            win = self.check_win()
            if win:
                self.win(win)

        elif self.turn == 2:
            self.buttons[x][y].text = self.P2
            self.board_state[x][y] = 2
            self.turn = 1
            win = self.check_win()
            if win:
                self.win(win)
        else:
            raise ValueError('Invalid player flag.')

    def grid_callback(self, instance):
        coor = (int(instance.id[6]), int(instance.id[7]))
        self.move(coor)

class TicTacToeApp(App):
    def build(self):
        return TicTacToeGame()

if __name__ == '__main__':
    TicTacToeApp().run()


