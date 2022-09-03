#coding=utf-8
import time
from MusicalInstrument.Abstract_MusicalInstrument import Abstract_Stepper


class StepperSHT01832(Abstract_Stepper):
    dict_diff_info = {}

    def __init__(self, io_a1, io_a2, io_b1, io_b2):
        Abstract_Stepper.__init__(self, 0, "SHT-42C1-Y13-01832", "", io_a1, io_a2, io_b1, io_b2)
        StepperSHT01832.init_diff_info()
        pass

    def get_delay(self, hertz):
        hertz = int(hertz)
        if hertz not in StepperSHT01832.dict_diff_info:
            print("Not found diff: %f. %s" % (hertz, self.get_name()))
            return 1 / hertz
        diff = StepperSHT01832.dict_diff_info[hertz]
        return 1 / (hertz + diff)

    @staticmethod
    def init_diff_info():
        if len(StepperSHT01832.dict_diff_info) > 0:
            return

        DIFF_INFO_TEMPLATE = {
            "69.296": 0.5,
            "740.0": 67.0,
            "110.0": 1.6,
            "261.632": 8.0,
            "466.16": 25.0,
            "311.12": 12.0,
            "55.0": 0,
            "196.0": 4.5,
            "329.632": 13.0,
            "116.54": 2.0,
            "61.736": 0,
            "830.624": 88.0,
            "932.32": 113.0,
            "36.708": 0,
            "49.0": 0,
            "370.0": 16.0,
            "32.704": 0,
            "138.592": 2.5,
            "87.308": 0.8,
            "51.914": 0,
            "58.27": 0,
            "77.78": 1.0,
            "174.616": 3.5,
            "34.648": 0,
            "392.0": 18.0,
            "220.0": 5.5,
            "123.472": 2.0,
            "207.656": 5.0,
            "587.328": 41.0,
            "440.0": 23.0,
            "415.312": 20.0,
            "82.408": 0.5,
            "880.0": 100.0,
            "92.5": 1.0,
            "293.664": 10.0,
            "523.264": 33.0,
            "73.416": 0.5,
            "246.944": 7.0,
            "43.654": 0,
            "164.816": 3.0,
            "987.776": 135.0,
            "185.0": 4.0,
            "277.184": 9.0,
            "46.25": 0,
            "146.832": 3.2,
            "98.0": 1.0,
            "622.24": 48.0,
            "554.368": 37.0,
            "233.08": 6.0,
            "103.828": 1.0,
            "784.0": 77.0,
            "349.232": 14.0,
            "65.408": 0.5,
            "493.888": 29.0,
            "41.204": 0,
            "155.56": 3.0,
            "659.264": 52.0,
            "698.464": 59.0,
            "130.816": 2.0,
            "38.89": 0
        }

        for str_hertz in DIFF_INFO_TEMPLATE:
            hertz = int(float(str_hertz))
            StepperSHT01832.dict_diff_info[hertz] = DIFF_INFO_TEMPLATE[str_hertz]
            StepperSHT01832.dict_diff_info[hertz - 1] = DIFF_INFO_TEMPLATE[str_hertz]
            StepperSHT01832.dict_diff_info[hertz + 1] = DIFF_INFO_TEMPLATE[str_hertz]
            StepperSHT01832.dict_diff_info[hertz - 2] = DIFF_INFO_TEMPLATE[str_hertz]
            StepperSHT01832.dict_diff_info[hertz + 2] = DIFF_INFO_TEMPLATE[str_hertz]
