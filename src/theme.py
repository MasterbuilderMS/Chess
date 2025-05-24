from dataclasses import dataclass


@dataclass
class Color:
    light: str
    dark: str


@dataclass
class Theme:
    bg: Color
    trace: Color
    moves: Color
