#!/usr/bin/env python2
# coding=utf-8
import sys
import midi
import argparse
from Common.Common import *
from Common.MIDI import *
from Modules.TuneAnalyzer import *

INSTR_NORMAL = 0
INSTR_PERCUSSION = 1


# return: boolean
def __piano_solo(track):
    has_instr = False
    for event in track:
        if event.statusmsg != 0xC0:
            continue

        # channel 10(id:9) is Percussion
        if event.channel == 9:
            return False

        has_instr = True

        if is_piano(event.value) is False:
            return False

    return has_instr


def __get_number_for_valid_tracks(partten):
    number = 0
    for track in partten:
        for event in track:
            if event.name != 'Program Change' and event.name != 'pitch On':
                continue
            number += 1
            break
    return number


# return: list_paths
def find_midi_by_single_track(midi_dir):
    list_paths = []
    list_sub_path = get_subs(midi_dir, '*.mid')
    file_count_of_single_track = 0
    cache_group = 'single_track'
    index = 0
    for sub_path in list_sub_path:
        index += 1
        midi_path = midi_dir + sub_path[1:]
        if index % 10 == 0:
            print('cur: %d' % index)
            print('total files single track : %d' % file_count_of_single_track)
        try:
            is_single = read_cache(cache_group, sub_path)
            # is_single = None
            if is_single is None:
                pattern = midi.read_midifile(midi_path)
                track_num = __get_number_for_valid_tracks(pattern)
                if track_num == 1:
                    write_cache(cache_group, sub_path, 'true')
                    is_single = 'true'
                else:
                    write_cache(cache_group, sub_path, 'false')
                    is_single = 'false'
            if is_single == 'true':
                file_count_of_single_track += 1
                list_paths.append(midi_path)
        except Exception, e:
            print("exception: " + midi_path)
            if (str(e).find('Bad header in MIDI file.') != -1) or (str(e).find('Bad track header in MIDI') != -1):
                os.remove(midi_path)
            print(e)
            # raise e

    return list_paths


def find_midi_by_piano_solo(midi_dir):
    list_solo_paths = []
    # piano solo only
    list_paths = find_midi_by_single_track(midi_dir)
    # list_paths.sort(reverse=True)
    cache_group = 'piano_solo_only'
    for midi_path in list_paths:
        try:
            is_piano_solo = read_cache(cache_group, midi_path)
            # is_piano_solo = None
            if is_piano_solo is None:
                pattern = midi.read_midifile(midi_path)
                track = None
                for track in pattern:
                    for event in track:
                        if event.name == 'Program Change' or event.name == 'pitch On':
                            break
                if __piano_solo(track):
                    write_cache(cache_group, midi_path, 'true')
                    is_piano_solo = 'true'
                else:
                    write_cache(cache_group, midi_path, 'false')
                    is_piano_solo = 'false'

            if is_piano_solo == 'false':
                continue

            # Here is piano solo
            print('piano solo: ' + midi_path)
            list_solo_paths.append(midi_path)
        except Exception, e:
            print("exception: " + midi_path)
            print(e)
    return list_solo_paths


def __get_min_pitch(track):
    min_pitch = 0xFF
    for event in track:
        if event.statusmsg != 0x90:
            continue
        if min_pitch > event.pitch:
            min_pitch = event.pitch
    if min_pitch == 0xFF:
        return -1
    return min_pitch


def _has_pitch(track):
    for event in track:
        if event.statusmsg == 0x90:
            return True
    return False


"""
# return: {_1_16_index: [pitch,..], }
def gen_feature(track, resolution, pitch_diff):
    # print(123)
    _1_16_tick = resolution / 4  # 十六分音符分到的tick数
    dict_feature = {}
    # TODO：目前还未遇到pattern.resolution（division）为负数情况，可能是py-midi自动做了处理，以后确认
    cur_tick_total = 0
    for event in track:
        if event.tick != 0 and event.tick < _1_16_tick:
            return None  # 表明当前粒度已经小与十六分音符, 暂不支持。
        cur_tick_total += event.tick
        # MIDI中0x90表示按下键盘, 0x80表示松开, 但实际上0x80不一定被使用. 而通常使用0x90加上力度为0来表示某个音符的终结.
        if event.statusmsg != 0x90:
            continue
        if event.velocity == 0:
            continue

        index = cur_tick_total / _1_16_tick
        if dict_feature.has_key(index) is False:
            dict_feature[index] = [event.pitch]
        else:
            dict_feature[index].append(event.pitch + pitch_diff)
    return dict_feature
"""


def __calc_tick_multiple(pattern, to_tick):
    return float(to_tick) / float(pattern.resolution)


# return: diff, scale_id
def __calc_pitch_diff(pattern, to_pitch):
    scale_id = -1
    min_pitch_aligned = -1
    for track in pattern:
        if _has_pitch(track) is False:
            continue

        min_pitch = __get_min_pitch(track)
        if min_pitch == 41:
            print(123)
        is_major, tmp_scale_id = get_tune_with_track(track)
        if is_major is None:
            if scale_id != -1:
                is_major = 0
                tmp_scale_id = scale_id
            else:
                return None, None  # failed
        is_major = is_major == 0
        if is_major is False:
            return None, None  # not supported minor

        if scale_id != -1 and scale_id != tmp_scale_id:
            assert False, "The scales are not equels."  # 多个音轨之间的调号居然不同？？
            # return None, None  # d
        scale_id = tmp_scale_id

        # int(min_pitch / 12)*12 算出所处音阶组开头位置
        #  + scale_id 加上音阶id.   最终得出目标pitch.
        tmp_min_pitch_aligned = int(min_pitch / 12)*12 + scale_id
        if min_pitch_aligned == -1 or min_pitch_aligned > tmp_min_pitch_aligned:
            min_pitch_aligned = tmp_min_pitch_aligned
    return to_pitch - min_pitch_aligned, scale_id
    # return None, None


# return: [(instr_type, velocity, begin_tick, duration_tick), ...]
def gen_feature(track, pitch_diff, tick_multiple):
    list_feature = []
    # TODO：目前还未遇到pattern.resolution（division）为负数情况，可能是py-midi自动做了处理，以后确认
    events_num = len(track)
    cur_instr = INSTR_NORMAL
    for i in range(events_num):
        event = track[i]
        # key down
        if event.statusmsg == 0x90 or event.statusmsg == 0x80:
            if event.statusmsg == 0x90 and event.velocity > 0:
                pitch = event.pitch
                begin_tick = event.tick * tick_multiple
                # find key up
                duration_tick = 0
                for _i in range(i, events_num):
                    _event = track[_i]
                    # MIDI中0x90表示按下键盘, 0x80表示松开, 但实际上0x80不一定被使用. 而通常使用0x90加上力度为0来表示某个音符的终结.
                    if (_event.statusmsg == 0x80 and _event.pitch == pitch) or \
                       (_event.statusmsg == 0x90 and _event.velocity == 0 and _event.pitch == pitch):
                        duration_tick = (_event.tick-event.tick) * tick_multiple
                        break
                if event.pitch + pitch_diff < 36:
                    print(123)
                list_feature.append((cur_instr,
                                     pitch_2_hz(event.pitch + pitch_diff),  # 直接转为对应频率
                                     event.velocity,
                                     int(begin_tick),
                                     int(duration_tick)))
        # change instr
        elif event.statusmsg == 0xC0:
            # channel 10(id:9) is Percussion
            if event.channel == 9:
                cur_instr = INSTR_PERCUSSION
            else:
                cur_instr = INSTR_NORMAL

    return list_feature


def feature_2_str(list_feature):
    str_feature = ''
    for tu_note in list_feature:
        str_feature += '%d %.3f %d %d %d, ' % (tu_note[0], tu_note[1], tu_note[2], tu_note[3], tu_note[4])
    return str_feature


# 将调号转为pitch
# tune: 'C#2'
def  tune_2_pitch(tune):
    tune = tune.lower()
    assert len(tune) <= 3
    prefix_len = 1
    if (len(tune) >= 2) and (ord('c') <= ord(tune[0])) and (ord(tune[0]) <= ord('z')):
        pass
    else:
        return None  # invalid

    if '#b'.find(tune[1]) != -1:
        prefix_len = 2  # eg.  C#2
    relative_note = tune[:prefix_len]
    group = int(tune[prefix_len:])
    relative_note_id = id_with_note(relative_note)  # eg. 'C#'
    # C0 == 0x0C(midi.pitch)
    # C2 == 0x24
    # i = 0
    # tmp = 12
    # while i <= group:
    #     tmp *= 2
    #     i += 1
    pitch = 0xC + group*12 + relative_note_id
    return pitch


# 将pitch值直接转为声音频率
def pitch_2_hz(pitch):
    pitch -= 0xC
    # C - B
    C0_hertz = [16.352, 17.324, 18.354, 19.445, 20.602, 21.827, 23.125, 24.500, 25.957, 27.500, 29.135, 30.868]
    group = int(pitch / 12)
    relative_note = pitch % 12
    # 八度之间频率以一倍的关系递增
    i = 0
    frequency = C0_hertz[relative_note]
    while i <= group:
        frequency *= 2
        i += 1
    return frequency


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Generator.py', description='%(prog)s eg.  [-t c3] [-s 5] a.mid')
    parser.add_argument('-t', '-tune', action='store', dest='tune',
                        help='Adjust the music to the tune.  eg. c3')
    parser.add_argument('-s', '-speed', action='store', dest='speed', type=int,
                        help='Adjust the music to the speed.  eg. 0 to 9')
    parser.add_argument('-f', '-midi_file', action='store', dest='midi_file', help='Midi file path.')
    args = parser.parse_args()

    # -f
    midi_path = args.midi_file
    if args.midi_file is None:
        parser.print_help()
        exit(0)
    if os.path.exists(args.midi_file) is False:
        print("[err] does not exist: %s" % args.midi_file)
        exit(0)

    # -t
    pitch = -1  # default
    if args.tune:
        pitch = tune_2_pitch(args.tune)
        if pitch is None:
            print('[err] the tune is invalid: "%s",  eg. C3' % args.tune)
            exit(0)
        print('[info] args.tune: %s (pitch %d)' % (args.tune, pitch))

    # -s
    tick = 240  # default
    if (0 <= args.speed) and (args.speed <= 9):
        min_tick = 100
        tick = min_tick * (10-args.speed)  # 0 slow  -  9 fast
        print('[info] args.speed: %d (tick %d)' % (args.speed, tick))
    else:
        print('[err] the speed is invalid: %d,  eg. 0 to 9' % args.speed)
        exit(0)

    # open midi
    pattern = None
    try:
        pattern = midi.read_midifile(midi_path)
        pattern.make_ticks_abs()
        print('[info] the midi\'s resolution(tick): %d' % pattern.resolution)
    except Exception, e:
        print("[err] exception: " + midi_path)
        print("[err] :" + str(e))
        exit(0)

    # 得到曲子调号, 并算出至C2的距离差(统一features的调号)
    pitch_diff = 0
    if pitch != -1:
        pitch_diff, scale_id = __calc_pitch_diff(pattern, pitch)
        if pitch_diff is None:
            print('[err] get pitch diff err: %s' % midi_path)
            exit(0)
        print('[info] %s to %s: %d pitch diff, %s' % (note_with_id(scale_id), args.tune, pitch_diff, midi_path))

    # 算出至tick的距离差(统一features的速度)
    tick_multiple = __calc_tick_multiple(pattern, tick)
    track = None
    list_feature = []
    for track in pattern:
        if _has_pitch(track) is False:
            continue
        list_feature += gen_feature(track, pitch_diff, tick_multiple)

    if list_feature is None:
        print('gen_feature() not support: %s' % midi_path)
        exit(0)

    str_feature = feature_2_str(list_feature)
    print('feature: %s' % str_feature)
