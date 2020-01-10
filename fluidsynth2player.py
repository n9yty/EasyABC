# A EasyABC MIDI Player using the FluidSynth2 library

from ctypes import c_double, c_char_p
import os
import time

import faulthandler

from fluidsynth2bindings import fluidsynth as F
from midiplayer import MidiPlayer, EventHook


faulthandler.enable()


def b(s):
    return s.encode("latin-1")


class FluidSynth2Player(MidiPlayer):
    def __init__(self, sf2_path):
        super(MidiPlayer, self).__init__()

        self.OnAfterStop = EventHook()
        self.OnAfterLoad = EventHook()

        self.driver_name = 'coreaudio'

        self.pause_position = 0

        st = F.new_fluid_settings()
        F.fluid_settings_setnum(st, b'synth.gain', c_double(0.7))
        F.fluid_settings_setnum(st, b'synth.sample-rate', c_double(44100))
        F.fluid_settings_setint(st, b'audio.period-size', 2048)
        F.fluid_settings_setint(st, b'audio.periods', 2)
        F.fluid_settings_setstr(st, b'audio.driver', b(self.driver_name))
        self.settings = st

        self.synth = F.new_fluid_synth(st)
        self.sfid = F.fluid_synth_sfload(self.synth, c_char_p(b(sf2_path)), 0)
        F.fluid_synth_program_select(self.synth, 0, self.sfid, 0, 0)

        self.audio_driver = F.new_fluid_audio_driver(st, self.synth)
        if not self.audio_driver:   # API returns 0 on error (not None)
            self.audio_driver = None

        F.fluid_synth_program_select(self.synth, 0, self.sfid, 0, 0)

        self.player = F.new_fluid_player(self.synth)

    @property
    def is_playing(self):
        return F.fluid_player_get_status(self.player) == 1  # 0 = ready, 1 = playing, 2 = finished

    @property
    def is_paused(self):
        return self.pause_position > 0

    @property
    def supports_tempo_change_while_playing(self):
        return True

    @property
    def PlaybackRate(self):
        return F.fluid_player_get_bpm(self.player) / 100

    @PlaybackRate.setter
    def PlaybackRate(self, value):
        F.fluid_player_set_bpm(self.player, int(100 * value))

    @property
    def unit_is_midi_tick(self):
        return True

    def Play(self):
        self.Seek(self.pause_position)
        F.fluid_player_play(self.player)
        self.pause_position = 0

    def Stop(self):
        if self.is_playing:
            F.fluid_player_stop(self.player)
            self.pause_position = 0
            self.OnAfterStop.fire()

    def Pause(self):
        F.fluid_player_stop(self.player)
        self.pause_position = self.Tell()

    def Load(self, path):
        self.reset()
        if not os.path.exists(path):
            return False
        status = F.fluid_player_add(self.player, b(path))
        if status >= 0:
            # This is a spectacular hack - fluid_player_get_total_ticks()
            # only works once playback has started so we play the first
            # tenth of a second of the track (which seems to amount to the
            # first note) when the track is loaded. EasyABC seems to do
            # Load() immediately followed by Play() when you click play
            # on a new track so this *almost* works but there's slight
            # rhythm break
            F.fluid_player_play(self.player)
            time.sleep(0.1)
            F.fluid_player_stop(self.player)
            self.pause_position = self.Tell()
            self.OnAfterLoad.fire()
            return True
        return False

    def Length(self):
        # This tends to return 0 unless payback has already started
        return F.fluid_player_get_total_ticks(self.player)

    def Seek(self, pos_in_ticks):
        F.fluid_player_seek(self.player, pos_in_ticks)

    def Tell(self):
        return F.fluid_player_get_current_tick(self.player)

    def dispose(self):
        F.delete_fluid_player(self.player)
        if self.audio_driver is not None:
            F.delete_fluid_audio_driver(self.audio_driver)
        F.delete_fluid_synth(self.synth)
        F.delete_fluid_settings(self.settings)
        self.player = self.settings = self.synth = self.audio_driver = None

    def reset(self):              # the only way to empty the playlist ...
        F.delete_fluid_player(self.player)           # delete player
        self.player = F.new_fluid_player(self.synth)   # make a n
        self.pause_position = 0


class DummyMidiPlayer(MidiPlayer):
    def __init__(self):
        super(DummyMidiPlayer, self).__init__()
