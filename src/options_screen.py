from screen import Screen
from asset_manager import AssetManager
from drawable import Drawable
from button import Button
from slider import Slider
from number_label import NumberLabel
from toggle_button import ToggleButton

class OptionsScreen(Screen):
    
    def __init__(self, asset_manager : AssetManager, game) -> None:
        super().__init__()
        self.add_element(Drawable(asset_manager.get_text()['options'], 571, 122)) # the TETRIS logo
        self.add_element(Button(483, 109, asset_manager.get_buttons()['back'], game.change_screen, 'title'))
        self.add_element(Drawable(asset_manager.get_small_frame(), 1020, 250))
        self.add_element(Drawable(asset_manager.get_small_frame(), 1020, 360))
        self.sound_percent_label = NumberLabel(asset_manager, 1063, 260, True, False, True, 3)
        self.music_percent_label = NumberLabel(asset_manager, 1063, 370, True, False, True, 3)
        self.add_element(Slider(605, 277, self.update_sound))
        self.add_element(Slider(605, 389, self.update_music))
        self.add_element(self.music_percent_label)
        self.add_element(self.sound_percent_label)
        self.add_element(ToggleButton(520, 252, asset_manager.get_sound_icons(), self.test))
        self.add_element(ToggleButton(520, 364, asset_manager.get_music_icons(), self.test))
        self.game = game
    
    def test(self, boolean):
        print(f'SET TO {boolean}')
    
    def update_music(self, value):
        percent = int(value*100)
        self.music_percent_label.set_value(percent)
        # game.update_music_volume or something

    def update_sound(self, value):
        percent = int(value*100)
        self.sound_percent_label.set_value(percent)
        # update sound

