from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, ListProperty, DictProperty
from kivy.lang.builder import Builder

from reversi import Reversi

WIDTH = HEIGHT = 8

class Cell(Button):
    coord = DictProperty({'x':0, 'y':0})

class ReversiGrid(GridLayout):
    cells = ListProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for y in range(HEIGHT):
            self.cells.append([])
            for x in range(WIDTH):
                new_button = Cell()
                new_button.coord['x'], new_button.coord['y'] = x, y
                new_button.bind(on_release = App.get_running_app().on_cell_release)
                self.add_widget(new_button)
                self.cells[y].append(new_button)

    def toggle_cell(self, x, y):
        self.cells[y][x].disabled = not self.cells[y][x].disabled
    
    def color_cell(self, x, y, color):
        self.cells[y][x].background_color = color
    

class ReversiApp(App):
    grid = ObjectProperty()
    reversi = ObjectProperty(Reversi())
    def build(self):
        kv = Builder.load_file('reversi.kv')
        self.grid = kv.ids.reversi_grid
        self.update_grid()
                    #self.grid.toggle_cell(x, y)
        return kv

    def update_grid(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if color := self.reversi.get_cell_color(x, y):
                    self.grid.color_cell(x, y, color)

    def update_score(self):
        self.root.ids.red_text.text = f'Red: {self.reversi.count("red")}'
        self.root.ids.blue_text.text = f'Blue: {self.reversi.count("blue")}'
        self.root.ids.turn_text.color = self.reversi.get_turn_color()
        self.root.ids.turn_text.text = f'{self.reversi.get_turn_color()} turn'.capitalize()
        
    def end_game(self):        
        red = self.reversi.count('red')
        blue = self.reversi.count('blue')
        turn_text = self.root.ids.turn_text

        if red > blue:
            turn_text.color = 'red'
            turn_text.text = 'Red Wins!'
        elif blue > red:
            turn_text.color = 'blue'
            turn_text.text = 'Blue Wins!'
        else:
            turn_text.color = 'white'
            turn_text.text = 'Draw!'

    def on_cell_release(self, instance):
        if self.reversi.valid_move(**instance.coord):
            self.reversi.move(**instance.coord)
            self.update_grid()
            self.update_score()

        if self.reversi.all_cells_filled():
            self.end_game()

if __name__ == '__main__':
    ReversiApp().run()