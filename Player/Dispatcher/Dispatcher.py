# coding=utf-8
import sys
import time
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
else:
    import queue as queue
import threading


class Dispatcher:
    list_template = []  # [(instr_type, hz, velocity(0-127), start_time, duration_tick),]
    list_instruments = []

    # music_template: "instr_type hz velocity(0-127) start_time end_time, ..."
    # eg. "0 65.408 100 0 100, 0 65.408 100 0 50, 0 65.408 100 0 100"
    def __init__(self, music_template):
        self.list_template = Dispatcher.parse_template(music_template)
        pass

    @staticmethod
    def parse_template(music_template):
        list_template = []
        _notes = music_template.replace('  ', ' ').replace(' ,', ',').replace(', ', ',').split(',')
        for str_note in _notes:
            _values = str_note.split(' ')
            if len(_values) != 5:
                continue
            v_instr_type = int(_values[0])
            v_hz = float(_values[1])
            v_velocity = int(_values[2])
            v_start_time = int(_values[3])
            duration_tick = int(_values[4])

            list_template.append((v_instr_type, v_hz, v_velocity, v_start_time, duration_tick))

        list_template.sort(key=lambda k: k[3])  # sort by start_time
        return list_template

    # 插入乐器
    def add_musical_instrument(self, instrument):
        self.list_instruments.append(instrument)

    def _thread_instr_loop(self, instrment, queue):
        while True:
            hertz, duration_seconds = queue.get(block=True)
            print("play(%f, %f)" % (hertz, duration_seconds))
            instrment.play(hertz, duration_seconds)

    def _init_instr(self):
        # 一类设备对应一条任务queue
        # 一个设备对应一条thread
        dict_kinds = {}
        for instr in self.list_instruments:
            instr_id = instr.get_id()
            if instr_id not in dict_kinds:
                dict_kinds[instr_id] = {'queue': queue.Queue(maxsize=-1), 'instrs': [instr]}
            else:
                dict_kinds[instr_id]['instrs'].append(instr)
            threading.Thread(target=self._thread_instr_loop,
                             args=(instr, dict_kinds[instr_id]['queue']),
                             name='instr-%d' % instr_id).start()
        return dict_kinds

    # 开始演奏
    def start(self):
        dict_kinds = self._init_instr()
        last_rtick = 0

        for tu_note in self.list_template:
            instr_id = tu_note[0]
            hz = tu_note[1]
            rtick = tu_note[3]
            duration_tick = tu_note[4]
            time.sleep((rtick-last_rtick) / 1000.0)
            # print("sleep(%f)" % ((rtick-last_rtick)/1000.0))
            dict_kinds[instr_id]['queue'].put((hz, duration_tick/1000.0))
            last_rtick = rtick
        pass
