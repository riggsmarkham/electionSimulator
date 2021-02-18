from numpy import random
from math import sqrt

NUM = 10000

#normalize polling to decimals between 0 (none) and 1 (all)
def normalizePolling(polling):
  total = sum(polling)
  newPolling = []
  for x in polling:
    newPolling.append(x/total)
  return newPolling

#calculate standard deviation from sample size
def calcSTDEV(sample):
  return 1/sqrt(sample)

#generate randomized iteration
def randomizedIteration(polling, stdev):
  results = []
  for x in polling:
    num = random.normal(x,stdev)
    while num < 0 or num > 1:
      num = random.normal(x,stdev)
    results.append(num)
  newTotal = sum(results)
  for i in range(len(results)):
    results[i] /= newTotal
  return results

#figure out the winner of a plurality (FPTP) election from results
def runPlurality(results):
  maxIndex = -1;
  maxValue = 0.0;
  for i in range(len(results)):
    if results[i] > maxValue:
      maxIndex = i
      maxValue = results[i]
  return maxIndex

#run num iterations of a pluraity election
def runIterations(polling, num, sample):
  stdev = calcSTDEV(sample)
  normalized = normalizePolling(polling)
  winList = [0 for i in range(len(polling))]
  for i in range(num):
    results = randomizedIteration(normalized, stdev)
    winner = runPlurality(results)
    winList[winner] += 1
  return winList

#print results of simulated elections
def printResults(names, results):
  nameLength = max(len(x) for x in names)
  #numLength = max(len(str(x)) for x in results)
  total = sum(results)
  for i in range(len(results)):
    # s = "{:<" + str(nameLength) + "} {:>" + str(numLength) + "n} {:.2%}"
    # print(s.format(names[i],results[i],results[i]/total))
    s = "{:<" + str(nameLength) + "} {:>6.1%}"
    print(s.format(names[i],results[i]/total))
  print()

#read data from file to run simulation
def readFromFile(filename, num):
  file = open(filename, 'r')
  n = int(file.readline())
  for i in range(n):
    names = file.readline().split(',')
    names[-1] = names[-1][:-1]
    polling = [int(x) for x in file.readline().split(',')]
    sample = int(file.readline())
    printResults(names, runIterations(polling, num, sample))
  file.close()

print("Color Parties Example")
readFromFile('data/colors.txt', NUM)
print("NYC Mayoral Election")
readFromFile('data/nycmayor.txt',NUM)