
class Trie:
  def __init__(self):
    self.start = None

  class TrieNode:
    def __init__(self, item, next = None, follows = None):
      self.item = item
      self.next = next
      self.follows = follows

  def __insert(node, key):
    if len(key) == 0:
      return None

    if node == None:
      return Trie.TrieNode(key[0], None, Trie.__insert(None, key[1:]))
    
    if key[0] == node.item[0]:
      node.follows = Trie.__insert(node.follows, key[1:])
      return node

    node.next = Trie.__insert(node.next, key)
    return node

  def insert(self, key):
    self.start = Trie.__insert(self.start, key + "$")

  def __str(node, indent):
    if node == None:
      return ""
    return f"\n{indent}{str(node.item)}{Trie.__str(node.follows, indent + ' ')}{Trie.__str(node.next, indent)}"

  def __str__(self):
    return Trie.__str(self.start, "")


def main():
  words = ["cow", "cat", "rat", "rabbits", "dog"]

  trie = Trie()

  for word in words:
    trie.insert(word)

  print(trie)

main()
