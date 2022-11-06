# imports 
import random


# Node class
class Node:
  def __init__(self, data = 0, link = 0):    # initializing
    self.data = data
    self.link = link

  # getters and setters
  def getData(self):
    return self.data

  def setData(self, data):
    self.data = data

  def getLink(self):
    return self.link

  def setLink(self, link):
    self.link = link


class List:
  def __init__(self):
    self.head = Node()
    self.tail = Node()
    self.curr = Node()

  def IsEmpty(self):
    return self.head == None
  
  def IsFull(self):
    MAX_SIZE = 100
    return self.head == MAX_SIZE

  def First(self):
    self.curr = self.head

  def Last(self):
    self.curr = self.tail

  def SetPos(self, pos):
    if (not self.IsEmpty() and pos >= 0 and pos < self.GetSize()):
      self.curr = self.head
      for i in range(0, pos):
        self.curr = self.curr.getLink()
  
  def Prev(self):
    if (not self.IsEmpty() and self.curr != self.head):
      inc = self.head
      while (inc.getLink() != self.curr):
        inc = inc.getLink()
      self.curr = inc
    
  def Next(self):
    if (not self.IsEmpty() and self.curr != self.tail):
      self.curr = self.curr.getLink()
  
  def GetPos(self):
    if (self.IsEmpty()):
      return -1
    else:
      pos = -1
      temp = self.head
      while (temp != self.curr.getLink()):
        temp = temp.getLink()
        pos += 1
      return pos

  def GetValue(self):
    if (self.IsEmpty()):
      return -1
    else:
      return self.curr.getData()
  
  def GetSize(self):
    if (self.IsEmpty()):
      return 0
    else:
      size = 1
      temp = self.head
      while (temp != self.tail):
        temp = temp.getLink()
        size += 1
      return size
  
  def InsertBefore(self, data):
    if (self.IsEmpty() or self.IsFull()):
      self.InsertAfter(data)
    elif (self.head == self.curr):
      temp = Node()
      temp.setData(self.head)
      self.head = temp
      self.curr = temp
    else:
      inc = self.head
      temp = Node()
      temp.setData()
      while(inc.getLink() != self.curr):
        inc = inc.getLink()
      inc.setLink(temp)
      temp.setLink(self.curr)
      self.curr = temp

  def InsertAfter(self, data):
    temp = Node()

    if (not self.IsFull()):
      if (not self.IsEmpty()):
        self.head = Node()
        self.head.setData(data)
        self.curr = self.head
        self.tail = self.head
      elif (self.curr == self.tail):
        temp = Node()
        temp.setData(data)
        self.curr.setLink(temp)
        self.tail = temp
        self.curr = temp
      else:
        temp = Node()
        temp.setData(data)
        temp.setLink(self.curr.getLink())
        self.curr.setLink(temp)
        self.curr = temp
  
  def Remove(self):
    if (not self.IsEmpty()):
      if (self.curr == self.tail and self.GetSize() != 1):
        self.Prev()
        self.tail = self.curr
        self.curr.setLink(None)
      elif (self.curr == self.head):
        self.head = self.head.getLink()
        self.curr = self.head
      else:
        self.Prev()
        self.curr.setLink(self.curr.getLink().getLink())
        self.curr = self.curr.getLink()
  
  def Replace(self, data):
    if (not self.IsEmpty()):
      self.curr.setData(data)

  # def __str__(self):
  #   if (self.IsEmpty()):
  #     return "None"
  #   else:
  #     temp = self.head
  #     result = ""
  #     while (temp != self.tail.getLink()):
  #       result += str(temp.getData()) + " "
  #       temp = temp.getLink()
  #     return result

def toString(self):
  if (self.IsEmpty()):
    return "None"
  else:
    temp = self.head
    result = ""
    while (temp != self.tail.getLink()):
      print(result)
      result += str(temp.getData()) + " "
      temp = temp.getLink()
    return result

##################
#####  MAIN  #####
##################

listSize = int(input("Please, enter the number of nodes: "))

myList = List()

for i in range(listSize):
  myList.InsertAfter(random.randint(0, 100))

print("Unsorted list: " + toString(myList))
print("Head data: " + str(myList.head.getData()))
print("Tail data: " + str(myList.tail.getData()))
print(myList.head.getLink().getData())
