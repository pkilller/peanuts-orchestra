# coding=utf-8

from MusicalInstrument.Abstract_MusicalInstrument import Abstract_Stepper


class StepperSHT42C100801(Abstract_Stepper):
    dict_diff_info = {}

    def __init__(self, io_a1, io_a2, io_b1, io_b2):
        Abstract_Stepper.__init__(self, 0, "SHT-42C100801-01", "", io_a1, io_a2, io_b1, io_b2)
        StepperSHT42C100801.init_diff_info()

    def get_delay(self, hertz):
        bak_hertz = hertz
        hertz = int(hertz)
        if hertz not in StepperSHT42C100801.dict_diff_info:
            print("Not found diff: %f(%d). %s" % (hertz, bak_hertz, self.get_name()))
            return 1 / hertz
        diff = StepperSHT42C100801.dict_diff_info[hertz]
        return 1 / (hertz + diff)

    @staticmethod
    def init_diff_info():
        if len(StepperSHT42C100801.dict_diff_info) > 0:
            return

        DIFF_INFO_TEMPLATE = {
          "61.736": 0,
          "69.296": 0,
          "329.632": 12.0,
          "58.27": 0,
          "41.204": 0,
          "155.56": 3.0,
          "880.0": 94.0,
          "116.54": 0,
          "932.32": 108.0,
          "43.654": 0,
          "65.408": 0,
          "830.624": 85.0,
          "523.264": 32.0,
          "311.12": 12.0,
          "185.0": 5.0,
          "246.944": 7.0,
          "32.704": 0,
          "196.0": 5.0,
          "98.0": 0,
          "784.0": 76.0,
          "130.816": 0,
          "73.416": 0,
          "1046.528": 125.0,
          "220.0": 6.0,
          "38.89": 0,
          "587.328": 42.0,
          "164.816": 4.0,
          "440.0": 23.0,
          "55.0": 0,
          "82.408": 0,
          "49.0": 0,
          "370.0": 16.0,
          "146.832": 0,
          "207.656": 5.0,
          "277.184": 9.0,
          "392.0": 19.0,
          "987.776": 120.0,
          "415.312": 20.0,
          "554.368": 37.0,
          "46.25": 0,
          "77.78": 0,
          "34.648": 0,
          "493.888": 30.0,
          "698.464": 58.0,
          "349.232": 14.0,
          "659.264": 50.0,
          "92.5": 0,
          "233.08": 7.0,
          "174.616": 4.0,
          "466.16": 26.0,
          "138.592": 0,
          "103.828": 0,
          "740.0": 67.0,
          "87.308": 0,
          "123.472": 0,
          "36.708": 0,
          "110.0": 0,
          "293.664": 10.0,
          "622.24": 48.0,
          "51.914": 0,
          "261.632": 8.0
        }

        for str_hertz in DIFF_INFO_TEMPLATE:
            hertz = int(float(str_hertz))
            diff_value = DIFF_INFO_TEMPLATE[str_hertz]
            print("init_diff: %d: %f" % (hertz, diff_value))
            StepperSHT42C100801.dict_diff_info[hertz] = diff_value
            StepperSHT42C100801.dict_diff_info[hertz - 1] = diff_value
            StepperSHT42C100801.dict_diff_info[hertz + 1] = diff_value
            StepperSHT42C100801.dict_diff_info[hertz - 2] = diff_value
            StepperSHT42C100801.dict_diff_info[hertz + 2] = diff_value
