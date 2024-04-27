from pygame import Surface
from screen import Screen
from asset_manager import AssetManager
from drawable import Drawable
from button import Button
from number_label import NumberLabel

class GameOverScreen(Screen):
    def __init__(self, asset_manager : AssetManager, game) -> None:
        super().__init__()
        self.game = game
        self.add_element(Drawable(asset_manager.get_text()['game_over'], 570, 200))
        self.add_element(Drawable(asset_manager.get_text()['score'], 500, 768))
        self.score_label = NumberLabel(asset_manager, 500, 800, False, True, True, 6)
        self.add_element(self.score_label) # score
        self.add_element(Button(720, 400, asset_manager.get_buttons()['again'], self.play_again))
        self.add_element(Button(720, 650, asset_manager.get_buttons()['menu'], self.game.change_screen, 'title'))
    
    def set_score(self, score):
        self.score_label.set_value(score)

    def play_again(self):
        self.game.get_screen('play').reset_game()
        self.game.change_screen('play')
        