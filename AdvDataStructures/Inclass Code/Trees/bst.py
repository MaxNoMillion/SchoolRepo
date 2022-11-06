
class BinarySearchTree:
  class __Node:
    def __init__(self, val, left = None, right = None):
      self.val = val
      self.left = left
      self.right = right

    def getVal(self):
      return self.val
    def setVal(self, newVal):
      self.val = newVal

    def getLeft(self):
      return self.left
    def getRight(self):
      return self.right

    def setLeft(self, newLeft):
      self.left = newLeft
    def setRight(self, newRight):
      self.right = newRight

    def __iter__(self):
      if self.left != None:
        for elem in self.left:
          yield elem

      yield self.val

      if self.right != None:
        for elem in self.right:
          yield elem

  def __init__(self):
    self.root = None

  def insert(self, val):
    self.root = BinarySearchTree.__insert(self.root, val)

  def __insert(root, val):
    if root == None:
      return BinarySearchTree.__Node(val)

    if val < root.getVal():
      root.setLeft(BinarySearchTree.__insert(root.getLeft(), val))

    else:
      root.setRight(BinarySearchTree.__insert(root.getRight(), val))

    return root

  def delete(self, val):
    self.root = BinarySearchTree.__delete(self.root, val)
  
  def __delete(root, val):
    if root == None:
      return None

    elif val < root.getVal():
      root.setLeft(BinarySearchTree.__delete(root.getLeft(), val))

    elif val > root.getVal():
      root.setRight(BinarySearchTree.__delete(root.getRight(), val))

    else:
      if root.getLeft() == None:
        temp = root.getRight()
        root = None
        return temp
      
      elif root.getRight() == None:
        temp = root.getLeft()
        root = None
        return temp

      temp = BinarySearchTree.__getInorderPredecessor(root.getLeft())

      root.setVal(temp.getVal())

      root.setLeft(BinarySearchTree.__delete(root.getLeft(), temp.getVal()))

    return root

  def __getInorderPredecessor(root):
    current = root

    while (current.getRight() != None):
      current = current.getRight()
    return current

  def __iter__(self):
    if self.root != None:
      return iter(self.root)
    else:
      return iter([])

def main():

  s = input("Enter a list of values: ")
  lst = s.split()

  tree = BinarySearchTree()

  for item in lst:
    tree.insert(int(item))

  for item in tree:
    print(item)

  d = input("\nEnter a value to delete: ")
  tree.delete(int(d))

  for item in tree:
    print(item)

main()



      

