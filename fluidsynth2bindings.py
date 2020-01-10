# A set of Python ctypes bindings fir the bits of FluidSynth
# needed by EasyABC

from ctypes import CDLL, c_int, c_double, c_char_p, c_void_p

LIB = './libfluidsynth.2.1.2.dylib'

try:
    fluidsynth = CDLL(LIB)
except ImportError:
    raise ImportError("Couldn't find the FluidSynth library in the program directory.")

# parameter and return types
fluidsynth.new_fluid_settings.restype = c_void_p

fluidsynth.fluid_settings_setnum.argtypes = [c_void_p, c_char_p, c_double]
fluidsynth.fluid_settings_setint.argtypes = [c_void_p, c_char_p, c_int]
fluidsynth.fluid_settings_setstr.argtypes = [c_void_p, c_char_p, c_char_p]

fluidsynth.delete_fluid_settings.argtypes = [c_void_p]

fluidsynth.new_fluid_synth.argtypes = [c_void_p]
fluidsynth.new_fluid_synth.restype = c_void_p

fluidsynth.fluid_synth_sfload.argtypes = [c_void_p, c_char_p, c_int]
fluidsynth.fluid_synth_sfload.restype = c_int

fluidsynth.fluid_synth_program_select.argtypes = [c_void_p, c_int, c_int, c_int, c_int]
fluidsynth.fluid_synth_program_select.restype = c_int

fluidsynth.delete_fluid_synth.argtypes = [c_void_p]

fluidsynth.new_fluid_audio_driver.argtypes = [c_void_p, c_void_p]
fluidsynth.new_fluid_audio_driver.restype = c_void_p

fluidsynth.delete_fluid_audio_driver.argtypes = [c_void_p]

fluidsynth.new_fluid_player.argtypes = [c_void_p]
fluidsynth.new_fluid_player.restype = c_void_p

fluidsynth.fluid_player_add.argtypes = [c_void_p, c_char_p]

fluidsynth.fluid_player_join.argtypes = [c_void_p]

fluidsynth.fluid_player_play.argtypes = [c_void_p]

fluidsynth.fluid_player_stop.argtypes = [c_void_p]

fluidsynth.fluid_player_get_status.argtypes = [c_void_p]
fluidsynth.fluid_player_get_status.restype = c_int

fluidsynth.fluid_player_get_total_ticks.argtypes = [c_void_p]
fluidsynth.fluid_player_get_total_ticks.restype = c_int

fluidsynth.fluid_player_get_current_tick.argtypes = [c_void_p]
fluidsynth.fluid_player_get_current_tick.restype = c_int

fluidsynth.fluid_player_seek.argtypes = [c_void_p, c_int]
fluidsynth.fluid_player_seek.restype = c_int

fluidsynth.fluid_player_get_bpm.argtypes = [c_void_p]
fluidsynth.fluid_player_get_bpm.restype = c_int

fluidsynth.fluid_player_set_bpm.argtypes = [c_void_p, c_int]
fluidsynth.fluid_player_set_bpm.restype = c_int

fluidsynth.delete_fluid_player.argtypes = [c_void_p]

