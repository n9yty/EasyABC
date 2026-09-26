#rm reference.txt generalmidi.txt abcm2ps_osx abc2midi_osx abc2abc_osx
#rm -fr dist/EasyABC.app
python setup.py py2app
#cp -r reference.txt generalmidi.txt img locale sound dist/EasyABC.app/Contents/Resources
#cp -r bin/abcm2ps bin/abc2midi bin/abc2abc dist/EasyABC.app/Contents/Resources/bin
for file in `ls -1 locale/`; do 
   mkdir "dist/EasyABC.app/Contents/Resources/$file.lproj" 
done
mkdir "dist/EasyABC.app/Contents/Resources/English.lproj"   

#FAU 20240103: there shall be no executable within Resources folder. Need to move them to Helpers or MacOS

mkdir dist/EasyABC.app/Contents/Helpers
cp bin/* dist/EasyABC.app/Contents/Helpers

# The above fails because there are dirs in bin for the mac architectures, so ensure we exit with 0
exit 0
