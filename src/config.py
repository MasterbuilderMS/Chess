import pygame
import os
from sound import Sound
from theme import Theme, Color


class Config:
    def __init__(self):
        self.themes = []  # list of themes
        self._add_themes()
        self.idx = 0  # current theme
        self.font = pygame.font.SysFont("monospace", 18, bold=True)
        self.move_sound = Sound(os.path.join("assets/sounds/move.wav"))
        self.capture_sound = Sound(os.path.join("assets/sounds/capture.wav"))

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)

    def _add_themes(self):
        green = Theme(
            Color("#EAEBC8", "#779A58"),
            Color("#F4F774", "#ACC333"),
            Color("#C86464", "#C84646"),
        )

        brown = Theme(
            Color("#EBD1A6", "#A57550"),
            Color("#F5EA64", "#D1B93B"),
            Color("#C86464", "#C84646"),
        )

        blue = Theme(
            Color("#E5E4C8", "#3C5F87"),
            Color("#7BBBE3", "#2B77BF"),
            Color("#C86464", "#C84646"),
        )

        gray = Theme(
            Color("#787776", "#565554"),
            Color("#637E8F", "#526680"),
            Color("#C86464", "#C84646"),
        )
        self.themes = [green, blue, brown, gray]

    @property
    def theme(self):
        return self.themes[self.idx]
