from hashSets import HashSet


class HashMap:
  class __KVPair:
    def __init__(self, key, value):
      self.key = key
      self.value = value

    def __eq__(self, other):
      if type(self) != type(other):
        return False
      return self.key == other.key
    
    def getKey(self):
      return self.key

    def getValue(self):
      return self.value

    def __hash__(self):
      return hash(self.key)
    
  def __init__(self):
    self.hSet = HashSet()

  def __len__(self):
    return len(self.hSet)
  
  # items in object
  # key in HashMap
  def __contains__(self, item):
    return HashMap.__KVPair(item, None) in self.hSet

  def not_contains(self, item):
    return item not in self.hSet
  
  # HashMap[key] = value
  def __setitem__(self, key, value):
    self.hSet.add(HashMap.__KVPair(key, value))
  
  # HashMap[key]
  def __getitem__(self, key):
    if HashMap.__KVPair(key, None) in self.hSet:
      val = self.hSet[HashMap.__KVPair(key, None)].getValue()
      return val
    raise KeyError(f"Key {key} not in HashMap")
  
  def __iter__(self):
    for x in self.hSet:
      yield x.getKey()



