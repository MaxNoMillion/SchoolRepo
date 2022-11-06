
class AVLTree:
  def __init__(self, root = None):
    self.root = root
  
  class AVLNode:
    def __init__(self, item, balance, left = None, right = None):
      self.item = item
      self.right = right
      self.left = left
      self.balance = balance

    def getBalance(self):
      return self.balance
    def setBalance(self, balance):
      self.balance = balance
    
    def __repr__(self):
      return f"AVLNode({repr(self.item)}, balance = {repr(self.balance)}, \
                left = {repr(self.left)}, right = {repr(self.right)})"
    
    def __iter__(self):
      if self.left != None:
        for elem in self.left:
          yield elem
        
      yield self.item

      if self.right != None:
        for elem in self.right:
          yield elem

    # find leaves
    def _getLeaves(self):
      # empty tree
      if self == None:
        return
      
      # if no children -> print item

      # if left child -> go left

      # if right child -> go right


  def __repr__(self):
    return f"AVLTree({repr(self.root)})"
  
  def __iter__(self):
    return iter(self.root)

  def insert(self, item):
    def rotateRight(pivot):
      leftChild = pivot.left

      return leftChild

    def rotateLeft(pivot):
      rightChild = pivot.right

      return rightChild

    def __insert(root, item):
      if root == None:
        return AVLTree.AVLNode(item)
    
      if item < root.item:
        root.left = __insert(root.left, item)
      
        # CASE 1 and Case 2
        # update balance

        # Case 3
        if  root.getBalance() == -2:
          badChild = root.left

          # Subcase A - Single Rotation
            # must be right rotate
          
          # Subcase B - Double Rotation
            # rotate at badChild and rotate at pivot
            # based on where badGrandChild is

              # adjust the balances

              # if inserted at badGrandChild -> pivot, badChild balances = 0

              # if inserted item smaller than badGrandChild (left subtree)
                # pivot balance = 1, badChild balance = 0

              # if inserted item larger than badGrandChild (right subtree)
                # pivot balance = 0, badChild balance = -1
      
      elif item > root.item:
        root.right = __insert(root.right, item)

        # CASE 1 and Case 2
        # update balance

        # Case 3
        if  root.getBalance() == 2:
          badChild = root.right

          # Subcase A - Single Rotation
            # must be left rotate
          
          # Subcase B - Double Rotation
            # rotate at badChild and rotate at pivot
            # based on where badGrandChild is

              # adjust the balances

              # if inserted at badGrandChild -> pivot, badChild balances = 0

              # if inserted item smaller than badGrandChild (left subtree)
                # pivot balance = 0, badChild balance = 1

              # if inserted item larger than badGrandChild (right subtree)
                # pivot balance = -1, badChild balance = 0
      
      else:
        print(f"Inserting duplicate: {item}")
        raise Exception("Duplicate value")

      return root    

    self.pivotFound = False
    self.root = __insert(self.root, item)

  def __lookup(node, item):
    if node == None:
      return False
    
    # if reached node with lookup -> return True

    # if item larger than node item -> go right

    # if item smaller than node item -> go left

    return AVLTree.__lookup(node.left, item)

  # if item is in tree
  def __contains__(self, item):
    return AVLTree.__lookup(self, item)

  def leaves(self):
    self.root._getLeaves()

  
def main():
  tree = AVLTree()

  print(repr(tree.root))

main()


    

