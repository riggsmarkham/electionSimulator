import plurality as p

NUM = 10000

print("Color Parties Example")
p.runElections(p.readFromFile('data/colors.txt'), NUM)
print("NYC Mayoral Election")
p.runElections(p.readFromFile('data/nycmayor.txt'), NUM)