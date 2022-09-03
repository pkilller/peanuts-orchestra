#!/usr/bin/env python2
# coding=utf-8
"""
Attach to a MIDI device and send the contents of a MIDI file to it.
"""
import sys
import time
import midi
import midi.sequencer as sequencer

i = 0x3c


def show_track(obj):
    global i
    msg = 'name: %s, statusmsg: %x, ' % (obj.name, obj.statusmsg)
    """
    if obj.statusmsg == 0x90:
        obj.data[1] = i
        i += 1
        if i > 0x70:
            i = 0x3c
        print(123)

    """
    if hasattr(obj, 'tick') and hasattr(obj, 'velocity') and obj.velocity == 0:
        return
    if hasattr(obj, 'tick'):
        msg += 'tick: %d, ' % obj.tick

    if hasattr(obj, 'metacommand'):
        msg += 'metacommand: %d, ' % obj.metacommand

    if hasattr(obj, 'text'):
        msg += 'text: %s, ' % obj.text

    if hasattr(obj, 'pitch'):
        msg += 'pitch: %s, ' % obj.pitch
    print(msg)


def main():
    if len(sys.argv) != 4:
        print "Usage: {0} <client> <port> <file>".format(sys.argv[0])
        exit(2)

    client = sys.argv[1]
    port = sys.argv[2]
    filename = sys.argv[3]
    
    pattern = midi.read_midifile(filename)

    hardware = sequencer.SequencerHardware()

    if not client.isdigit:
        client = hardware.get_client(client)

    if not port.isdigit:
        port = hardware.get_port(port)

    seq = sequencer.SequencerWrite(sequencer_resolution=pattern.resolution)
    seq.subscribe_port(client, port)

    pattern.make_ticks_abs()
    events = []
    for track in pattern:
        for event in track:
            if event.statusmsg == 0xb0:
                pass
                # continue
            show_track(event)
            events.append(event)
    events.sort()
    seq.start_sequencer()
    for event in events:
        buf = seq.event_write(event, False, False, True)
        if buf is None:
            continue
        if buf < 1000:
            time.sleep(.5)
    while event.tick > seq.queue_get_tick_time():
        seq.drain()
        time.sleep(.5)

    print 'The end?'

main()


