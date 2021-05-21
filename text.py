import arcade


letter = []
for i in range(67):
    texture = arcade.load_texture('Letters/fonts2.png', x=(i*90) + 15, y=0, height=320, width=80)
    letter.append(texture)

LETTERS = tuple(letter)

LETTER_CODE = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
    "K": 10,
    "L": 11,
    "M": 12,
    "N": 13,
    "O": 14,
    "P": 15,
    "Q": 16,
    "R": 17,
    "S": 18,
    "T": 19,
    "U": 20,
    "V": 21,
    "W": 22,
    "X": 23,
    "Y": 24,
    "Z": 25,
    "a": 26,
    "b": 27,
    "c": 28,
    "d": 29,
    "e": 30,
    "f": 31,
    "g": 32,
    "h": 33,
    "i": 34,
    "j": 35,
    "k": 36,
    "l": 37,
    "m": 38,
    "n": 39,
    "o": 40,
    "p": 41,
    "q": 42,
    "r": 43,
    "s": 44,
    "t": 45,
    "u": 46,
    "v": 47,
    "w": 48,
    "x": 49,
    "y": 50,
    "z": 51,
    "1": 52,
    "2": 53,
    "3": 54,
    "4": 55,
    "5": 56,
    "6": 57,
    "7": 58,
    "8": 59,
    "9": 60,
    "0": 61,
    '.': 62,
    "?": 63,
    ",": 64,
    "!": 65,
    ":": 66,
#    " ": 67
}
LETTER_SIZE = 60


def gen_letter_list(string: str = None, s_x: float = 0, s_y: float = 0, scale: float = 1, gap: int = 10):
    """
    :param string: The actual string that is being converted
    :param s_x: The center x position of the first letter
    :param s_y: The center y position of the first letter
    :param scale: The scale of the sprite going from 0.1 to 1
    :param gap: The gap between the letters that is affected by scale
    :return: It returns a SpriteList with all of the letter as Sprites
    """
    letter_list = arcade.SpriteList()
    for index, char in enumerate(string):
        if char != " ":
            texture = LETTERS[LETTER_CODE[char]]
            cur_letter = arcade.Sprite(scale=scale,
                                       center_x=s_x + (((gap + LETTER_SIZE) * scale) * index),
                                       center_y=s_y)
            cur_letter.texture = texture
            letter_list.append(cur_letter)
    return letter_list


class Conversation:
    def __init__(self):
        self.texted = 0
        self.happy = "happy"
        self.annoyed = "annoyed"
        self.angry = "angry"
        self.chatt = [self.happy, self.annoyed, self.angry]
