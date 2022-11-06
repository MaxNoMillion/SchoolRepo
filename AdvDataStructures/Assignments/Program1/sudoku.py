# Provide your information as the values of these variables:
myName = 'Steen, Andrew'
myTechID = '10268080'
myTechEmail = 'ams128' #only your email id omit @latech.edu
###########################################################

import sys

from hashSet import HashSet


def getColumn(matrix, colIndex):
  col = []
  for rowIndex in range(9):
    col.append(matrix[rowIndex][colIndex])
    
  return col

def getSquare(matrix, rowIndex, colIndex):
  square = []
  for i in range(rowIndex, rowIndex+3): 
    for j in range(colIndex,colIndex+3):
        square.append(matrix[i][j])
        
  return square

def getGroups(matrix):
  groups = []
  # get rows
  for i in range(9):
    groups.append(list(matrix[i]))
  # get columns
  for i in range(9):
    groups.append(getColumn(matrix,i))
  # get squares
  # squares are processed left-right, up-down
  for i in range(0,9,3): 
    for j in range(0,9,3):
      groups.append(getSquare(matrix,i,j))     

  return groups

def cardinality(x):
  return len(x)

def rule1(group):
  changed = False
  cardList = []
  for elem in group:
    cardList.append(len(elem))

  #print(cardList)
  temp = []
  
  for elem in group:
    if cardList.count(len(elem)) == len(elem):
      temp = elem

  for elem in group:
    if len(temp) > len(elem):
      for item in temp:
        elem.discard(item)
        changed = True
        
  return changed
  
def rule2(group):
  changed = False

  for elem in group:
    if len(elem) == 1:
      for item in elem:
        for otherElem in group:
          if elem != otherElem and item in otherElem:
            otherElem.discard(item)
            changed = True
  return changed

def reduceGroup(group):
  changed = False 
  # this sorts the sets from smallest to largest based cardinality
  group.sort(key=cardinality)
  changed = rule2(group)
  changed = rule1(group)
  
  return changed

def reduceGroups(groups):
  changed = False
  for group in groups:
    if reduceGroup(group):
      changed = True
      
  return changed

def reduce(matrix):
    changed = True
    groups = getGroups(matrix)
        
    while changed:
        changed = reduceGroups(groups)
        
    for rowElem in range(9):
      print("|")
      for colElem in range(9):
        print("|", end = "")
        for item in matrix[rowElem][colElem]:
          print(f"{item} ", end = "")
    
def printMatrix(matrix):
  for i in range(9):
    for j in range(9):
      if len(matrix[i][j]) != 1:
        sys.stdout.write("x ")
      else:
        for k in matrix[i][j]:
          sys.stdout.write(str(k) + " ")

    sys.stdout.write("\n")

def main():
  file = open(sys.argv[1], "r")
  matrix = []

  for line in file:
    lst = line.split()
    row = []

    for val in lst:
      if val == 'x':
        s = HashSet(range(1,10))
      else:
        s = HashSet([eval(val)])
      row.append(s)

    matrix.append(row)

  print("Solving this puzzle:")
  printMatrix(matrix)

  reduce(matrix)  

  print()
  print("Solution:")
  printMatrix(matrix)
  
main()
