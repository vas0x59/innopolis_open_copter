import Utils

magnet = Utils.Magnet()

inp = raw_input()
# input()
if (inp == 'on') or (inp == '1'):
    magnet.on()
else:
    magnet.off()
