import Utils

magnet = Utils.Magnet()

inp = input()

if (inp == 'on') or (inp == '1'):
    magnet.on()
else:
    magnet.off()
