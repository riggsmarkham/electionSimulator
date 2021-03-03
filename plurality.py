import numpy as np
from itertools import permutations

EPSILON = 10e-10

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

def constructPrefList(partyList):
  return np.asarray(list(permutations(partyList)))

#figure out the winner of a ranked choice voting election
#that's a lot of goddamn inputs (pointerList should be internally created probably)
#what about upper thresholds? How about STV?
def runRCV(partyList, prefList, pointerList, results):
  partySums = np.zeros(len(partyList))
  #initially populate partySums
  for i in range(len(results)):
    index = np.where(partyList == prefList[i][0])
    partySums[index] += results[i]
  while(np.max(partySums) <= (np.sum(partySums)/2)):
    print("start max: " + str(np.max(partySums)))
    index = np.where(partySums == np.min(partySums[np.nonzero(partySums)]))
    print(index)
    for i in range(len(prefList)):
      if (pointerList[i] < len(prefList[i])) and (prefList[i][pointerList[i]] == partyList[index]):
        pointerList[i] += 1
        trying = True
        while(trying):
          if(pointerList[i] < len(prefList[i])):
            newIndex = np.where(partyList == prefList[i][pointerList[i]])
            if(partySums[newIndex] != 0):
              print("pre add:  " + str(partySums))
              partySums[newIndex] += results[i]
              print("post add: " + str(partySums))
              trying = False
            else:
              pointerList[i] += 1
          else:
            trying = False
        print("pre sub:  " + str(partySums))
        partySums[index] -= results[i]
        print("post sub: " + str(partySums))
    print("end:      " + str(partySums))
    if(np.absolute(partySums[index]) <= EPSILON):
      partySums[index] = 0
    else:
      print("error value: " + str(partySums[index]))
      raise ValueError("didn't reduce to zero")
    print("post reset: " + str(partySums))
    print("end max: " + str(np.max(partySums)))
    print("end sum: " + str(np.sum(partySums)))
  return np.argmax(partySums)

#run num iterations of a pluraity election
def runFPTPIterations(polling, num, sample):
  normalized = normalizePolling(polling)
  winList = np.zeros(len(polling))
  for i in range(num):
    results = randomizedIteration(normalized, sample)
    winner = runPlurality(results)
    winList[winner] += 1
  return winList

def runRCVIterations(polling, partyList, num, sample):
  normalized = normalizePolling(polling)
  winList = np.zeros(len(polling))
  prefList = constructPrefList(partyList)
  pointerList = np.zeros(len(prefList), dtype=int)
  for i in range(num):
    results = randomizedIteration(normalized, sample)
    winner = runRCV(partyList, prefList, pointerList, results)
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
        if(np.any(np.less(polls,0))):
          raise ValueError("negative input poll")
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
def runFPTPElections(npData, num):
  for el in npData:
    printResults(el[0], runFPTPIterations(el[1], num, el[2]))

def runRCVElections(npData, num):
  for el in npData:
    printResults(el[0], runRCVIterations(el[1], el[0], num, el[2]))