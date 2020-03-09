import pygame
import serial
import time

pygame.init()

HIGH = b'H'
LOW = b'L'
NOT_PRESSED = b'0'
PRESSED = b'1'

MAPPING_MORSE_TO_CHAR = {
    "._": "A",
    "_...": "B",
    "_._.": "C",
    "_..": "D",
    ".": "E",
    ".._.": "F",
    "__.": "G",
    "....": "H",
    "..": "I",
    ".___": "J",
    "_._": "K",
    "._..": "L",
    "__": "M",
    "_.": "N",
    "___": "O",
    ".__.": "P",
    "__._": "Q",
    "._.": "R",
    "...": "S",
    "_": "T",
    ".._": "U",
    "..._": "V",
    ".__": "W",
    "_.._": "X",
    "_.__": "Y",
    "__..": "Z",
    ".____": "1",
    "..___": "2",
    "...__": "3",
    "...._": "4",
    ".....": "5",
    "_....": "6",
    "__...": "7",
    "___..": "8",
    "____.": "9",
    "_____": "0"
}

MAPPING_CHAR_TO_MORSE = {
    "A": "._",
    "B": "_...",
    "C": "_._.",
    "D": "_..",
    "E": ".",
    "F": ".._.",
    "G": "__.",
    "H": "....",
    "I": "..",
    "J": ".___",
    "K": "_._",
    "L": "._..",
    "M": "__",
    "N": "_.",
    "O": "___",
    "P": ".__.",
    "Q": "__._",
    "R": "._.",
    "S": "...",
    "T": "_",
    "U": ".._",
    "V": "..._",
    "W": ".__",
    "X": "_.._",
    "Y": "_.__",
    "Z": "__..",
    "1": ".____",
    "2": "..___",
    "3": "...__",
    "4": "...._",
    "5": ".....",
    "6": "_....",
    "7": "__...",
    "8": "___..",
    "9": "____.",
    "0": "_____"
}


def play_music():
    print('Start Game ARDUINOI to GAME:')
    filename = "/home/salvador/arduino/0170.wav"
    son = pygame.mixer.Sound(filename)

    while True:
        msg = ser.read()
        if msg == b'1':
            son.play()
            time.sleep(5)


def led_on_off():
    print('Start Game PC to ARDUINOI :')
    while True:
        msg = input()
        if 'z' == msg:
            time.sleep(0.1)
            ser.write(HIGH)
            print(ser.readline())
        if 'a' == msg:
            time.sleep(0.1)
            ser.write(LOW)
            print(ser.readline())


def morse_arduino_to_pc():
    print('Start Game ARDUINOI to GAME:')
    delta = 0
    start_2 = time.time()
    last_char = NOT_PRESSED
    msg = ""
    status = False

    while True:
        current_char = ser.read()
        if last_char == NOT_PRESSED and current_char == PRESSED:
            start = time.time()
            last_char = current_char

        if current_char == PRESSED:
            end = time.time()
            delta = end - start

        if last_char == PRESSED and current_char == NOT_PRESSED:
            if delta > 0.2:
                print("_")
                msg += "_"
            else:
                print(".")
                msg += "."
            delta = 0
            last_char = current_char
            start_2 = time.time()
            status = True

        if last_char == NOT_PRESSED and current_char == NOT_PRESSED and status:
            end_2 = time.time()
            delta_2 = end_2 - start_2
            if delta_2 > 1:
                print(msg, " -> ", MAPPING_MORSE_TO_CHAR.get(msg))
                msg = ""
                status = False


def morse_pc_to_arduino():
    print('Start Game PC to ARDUINOI :')
    msg = input("Tappez votre text : ")
    msg = msg.upper()
    for char in msg:
        code_morse = MAPPING_CHAR_TO_MORSE.get(char)
        for code in code_morse:
            if '_' == code:
                print("-> point ", code)
                ser.write(HIGH)
                time.sleep(0.6)
            if '.' == code:
                print("-> tirez ", code)
                ser.write(HIGH)
                time.sleep(0.3)
            ser.write(LOW)
            time.sleep(0.1)


if __name__ == '__main__':
    print("Initialisation ...")
    ser = serial.Serial('/dev/ttyACM1', 9600)
    time.sleep(2)  # wait for the serial connection to initialize

    print('Start Game :')
    morse_arduino_to_pc()
    # morse_pc_to_arduino()
    # play_music()
    # led_on_off()
