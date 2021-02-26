import numpy as np

#normalize polling to decimals between 0 (none) and 1 (all)
def normalizePolling(polling):
  return np.array(polling/np.sum(polling))

#calculate standard deviation for a sample proportion
def calcSTDEV(x, sample):
  return np.sqrt(((1-x)*x)/sample)

#generate randomized iteration
def randomizedIteration(polling, sample):
  results = []
  for x in polling:
    stdev = calcSTDEV(x, sample)
    num = np.random.normal(x,stdev)
    while num < 0 or num > 1:
      num = np.random.normal(x,stdev)
    results.append(num)
  results = np.array(results)
  return np.array(results/np.sum(results))

#figure out the winner of a plurality (FPTP) election from results
def runPlurality(results):
  return np.argmax(results)

def runIRV(partyList, prefList, pointerList, results):
  partySums = np.array(len(partyList))
  while(np.count_nonzero(~np.isnan(partySums)) != len(results) - 1):
    index = np.nanargmin(partySums)
    for i in range(len(prefList)):
      if (pointerList[i] < len(prefList[i])) and (prefList[i][pointerList[i]] == partyList[index]):
        pointerList[i] += 1
        if(pointerList[i] < len(prefList[i])):
          newIndex = np.where(partyList == prefList[i][pointerList[i]])
          partySums[newIndex] += results[i]
        partySums[index] -= results[i]
    if(partySums[index] == 0):
      partySums[index] = np.isnan
    else:
      raise ValueError
  return np.where(partySums != np.isnan)

#run num iterations of a pluraity election
def runIterations(polling, num, sample):
  normalized = normalizePolling(polling)
  winList = np.zeros(len(polling))
  for i in range(num):
    results = randomizedIteration(normalized, sample)
    winner = runPlurality(results)
    winList[winner] += 1
  return winList

#read data from a file
def readFromFile(filename):
  data = []
  with open(filename) as infile:
      lines = infile.readlines()
      n = int(lines[0][0])
      for i in range(n):
        names = lines[3*i+1].split(',')
        names[-1] = names[-1][:-1]
        polls = list(map(int,lines[3*i+2][:-1].split(',')))
        num = int(lines[3*i+3])
        data.append([np.array(names), np.array(polls), num])
  return data

#print results of election simulation
def printResults(names, results):
  nameLength = len(max(names, key=len))
  total = np.sum(results)
  for i in range(len(results)):
    s = "{:<" + str(nameLength) + "} {:>6.1%}"
    print(s.format(names[i],int(results[i])/total))
  print()

#actually run election simulation given data from file
def runElections(npData, num):
  for el in npData:
    printResults(el[0], runIterations(el[1], num, el[2]))