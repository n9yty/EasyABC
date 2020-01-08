#!/usr/bin/env python3

import faulthandler  # pip install faulthandler
faulthandler.enable()

import fluidsynth as F

fs = F.Synth(bsize=2048)

driver_name = F.onLinux and 'pulseaudio' or 'dsound'
fs.start(driver_name)

sfid = fs.sfload('GeneralUser_GS_v1.471.sf2')

fs.program_select(0, sfid, 0, 0)

p = F.Player(fs)

p.set_gain(0.7)

p.add('0101_speed-the-plough.midi')
p.load()

p.play(0)
