#!/usr/bin/env python3
# coding=utf-8
import os
import json
import threading
from MusicalInstrument.StepperSHT42C100801 import Stepper09

g_hertz = 500
g_diff = 0
g_stepper = None
C0_HERTZ = [16.352, 17.324, 18.354, 19.445, 20.602, 21.827, 23.125, 24.500, 25.957, 27.500, 29.135, 30.868]
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
g_program_path = os.path.dirname(os.path.abspath(__file__))


def _new_thread():
    global g_hertz
    global g_diff
    global g_stepper
    while True:
        g_stepper.play(g_hertz+g_diff, 0.5)
    pass


# return: 'C#'
# id: 1
def note_with_id(id):
    global NOTES
    return NOTES[id]


def read_diff_with_name(stepper_name):
    try:
        with open('%s/diff_info/%s.json' % (g_program_path, stepper_name), 'r') as f:
            return json.load(fp=f)
    except Exception as e:
        return {}
    pass


def write_diff_with_name(stepper_name, dict_diff):
    try:
        with open('%s/diff_info/%s.json' % (g_program_path, stepper_name), 'w+') as f:
            return json.dump(dict_diff, fp=f, indent=2)
    except Exception as e:
        return False
    pass


def add_diff_with_name(stepper_name, hertz, diff):
    dict_diff = read_diff_with_name(stepper_name)
    if dict_diff is None:
        return False
    dict_diff[hertz] = diff
    return write_diff_with_name(stepper_name, dict_diff)


if __name__ == '__main__':
    global g_hertz
    global g_diff
    global g_stepper
    global C0_HERTZ

    # input stepper name
    stepper_name = input("* Please input the stepper name: ")
    if not stepper_name:
        print("[Error] Invalid name~")
        exit(-2)
    stepper_name = stepper_name.strip()
    print("[Stepper Name]: " + stepper_name)

    # input gpio number
    gpio_numbers = input("* Please input the gpio number by GPIO.BOARD (eg: 5 10 11 12): ")
    list_gpio_numbers = []
    if gpio_numbers:
        _tmp = gpio_numbers.split(' ')
        if len(_tmp) == 4:
            list_gpio_numbers = [int(_tmp[0]), int(_tmp[1]), int(_tmp[2]), int(_tmp[3])]
    if len(list_gpio_numbers) == 0:
        print("[Error] Invalid gpio number~")
        exit(-2)
    print("[GPIO Numbers]: A:%d B:%d C:%d D:%d" % (list_gpio_numbers[0],
                                                   list_gpio_numbers[1],
                                                   list_gpio_numbers[2],
                                                   list_gpio_numbers[3]))
    STEPPER0_A1 = list_gpio_numbers[0]
    STEPPER0_A2 = list_gpio_numbers[1]
    STEPPER0_B1 = list_gpio_numbers[2]
    STEPPER0_B2 = list_gpio_numbers[3]
    g_stepper = Stepper09(STEPPER0_A1, STEPPER0_A2, STEPPER0_B1, STEPPER0_B2)
    threading.Thread(target=_new_thread).start()

    is_new = True
    note_index = 12
    note_descript = ""
    while int(note_index/12) <= 6:  # max: B6
        if is_new:
            _note_name = note_with_id(note_index % 12)
            _hertz = C0_HERTZ[note_index % 12]
            for i in range(int(note_index / 12)):
                _hertz *= 2
            note_descript = "%s%d(%.3fHz)" % (_note_name, int(note_index/12), _hertz)

            print("[New Hertz] %s of C1(32.703Hz)-B6(1975.5Hz)" % note_descript)
            g_hertz = _hertz
            is_new = False
            note_index += 1
        else:
            str_diff = input("* Input diff value of hertz: ")
            if str_diff == '':
                is_new = True
                print("[Got Diff] Diff:%.3fHz of %s\n\n" % (g_diff, note_descript))
                if add_diff_with_name(stepper_name, g_hertz, g_diff) is False:
                    print("[Error]Save the diff failed~")
                g_diff = 0
            else:
                g_diff = float(str_diff)

        # print("base:%fHz + diff:%fHz = %fHz" % (g_hertz, g_diff, g_hertz + g_diff))
    print('The "%s" is done.')
    pass

