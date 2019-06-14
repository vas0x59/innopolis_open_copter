import Utils

magnet = Utils.Magnet()

inp = raw_input()
# input()
if (inp == 'on') or (inp == '1'):
    magnet.on()
    print "MAGNET ON"
else:
    magnet.off()
    print "MAGNET OFF"
