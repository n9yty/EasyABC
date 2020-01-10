#!/usr/bin/env python3

import faulthandler

import fluidsynth2player as F

faulthandler.enable()

player = F.FluidSynth2Player('GeneralUser_GS_v1.471.sf2')
player.Load('0101_speed-the-plough.midi')

print('Unit is MIDI tick:', player.unit_is_midi_tick)
print('Total length:', player.Length())

print('Playing')
player.Play()
print('is_playing, is_paused:', player.is_playing, player.is_paused)

input('Press return to pause')

player.Pause()
print('is_playing, is_paused, tell:', player.is_playing, player.is_paused, player.Tell())
print('Total length', player.Length())

input('Press return to continue')

player.Play()
print('is_playing, is_paused:', player.is_playing, player.is_paused)

input('Press return to stop')

player.Stop()

input('Press return to restart at the beginning')

player.Play()

input('Press return to load and play a new tune')

player.Load('0102_morpeth-rant.midi')
player.Play()

input('Press return to quit')

player.Stop()
player.dispose()
