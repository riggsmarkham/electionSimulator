import plurality as p

NUM = 10000

# print("Color Parties Example")
# p.runFPTPElections(p.readFromFile('data/colors.txt'), NUM)
# print("NYC Mayoral Election")
# p.runFPTPElections(p.readFromFile('data/nycmayor.txt'), NUM)
p.runRCVElections(p.readFromFile('data/rankedpreferences.txt'), NUM)