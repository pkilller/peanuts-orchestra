# coding=utf-8

from Common.Scale import *

g_scales = [
    scale_major_with_id(0),  # major
    scale_major_with_id(1),
    scale_major_with_id(2),
    scale_major_with_id(3),
    scale_major_with_id(4),
    scale_major_with_id(5),
    scale_major_with_id(6),
    scale_major_with_id(7),
    scale_major_with_id(8),
    scale_major_with_id(9),
    scale_major_with_id(10),
    scale_major_with_id(11),
    # ============================================
    scale_minor_with_id(0),  # minor
    scale_minor_with_id(1),
    scale_minor_with_id(2),
    scale_minor_with_id(3),
    scale_minor_with_id(4),
    scale_minor_with_id(5),
    scale_minor_with_id(6),
    scale_minor_with_id(7),
    scale_minor_with_id(8),
    scale_minor_with_id(9),
    scale_minor_with_id(10),
    scale_minor_with_id(11),
]


# 以音符id来分组调号, 以便快速索引
g_fast_table = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[], 10:[], 11:[]}  # {note_id: [scale_index,], }


# init g_fast_table
scale_index = 0
for dict_scale in g_scales:
    for note_id in dict_scale:
        g_fast_table[note_id].append(scale_index)
    scale_index += 1


# 识别出track的调号
# return: (0.major or 1.minor, scale_id)    eg.  (0, 1('C#'))
def get_tune_with_track(track):
    dict_hit_scale_cache = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}, 10: {}, 11: {},
                            12: {}, 13: {}, 14: {}, 15: {}, 16: {}, 17: {}, 18: {}, 19: {}, 20: {}, 21: {},
                            22: {}, 23: {}}
    index_best_match = -1
    count_max_match = 0
    for event in track:
        if event.statusmsg != 0x90:  # key down
            continue

        # 记录命中音阶的音符,
        note_id = event.pitch % 12
        for scale_index in g_fast_table[note_id]:
            dict_hit_scale_cache[scale_index][note_id] = None
            if len(dict_hit_scale_cache[scale_index]) == 7:
                # 命中了全部的音符数, 表明已判定成功
                if scale_index <= 11:
                    # is major
                    return 0, scale_index
                else:
                    # is minor
                    return 1, scale_index - 12
            else:
                # 命中了部分, 记录, 用于兜底
                cur_match = len(dict_hit_scale_cache[scale_index])
                if count_max_match < cur_match:
                    count_max_match = cur_match
                    index_best_match = scale_index

    # 若命中数低于5个音符(全部命中为7), 认为失败
    if count_max_match < 5:
        return None, None

    if index_best_match <= 11:
        return 0, index_best_match
    else:
        return 1, index_best_match - 12
