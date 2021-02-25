import plurality as p

NUM = 10000

print("Color Parties Example")
p.runElection(p.readFromFile('data/colors.txt'), NUM)
print("NYC Mayoral Election")
p.runElection(p.readFromFile('data/nycmayor.txt'), NUM)