# This file is based on
# https://github.com/dilsonpereira/Minimum-Cost-Perfect-Matching

# This is a binary heap for pairs of the type (Decimal key, int satellite)
# It is assumed that satellites are unique integers
# This is the case with graph algorithms, in which satellites are vertex or edge indices

from decimal import Decimal

class BinaryHeap:
    def __init__(self):
        self.key: dict[int, Decimal] = {}  # Given the satellite, this is its key
        self.pos: dict[int, int] = {}  # Given the satellite, this is its position in the heap
        self.satellite: list[int] = [0]  # This is the heap!
        self.size: int = 0  # Number of elements in the heap
    
    # Inserts (key k, satellite s) in the heap
    def insert(self, k: Decimal, s: int) -> None:
        # If satellite is already in the heap
        if s in self.pos:
            raise ValueError('Error: satellite already in heap')
    
        self.satellite.append(0)
        self.size += 1
        i = self.size
        while i // 2 > 0 and self.key[self.satellite[i // 2]] > k:
            self.satellite[i] = self.satellite[i // 2]
            self.pos[self.satellite[i]] = i
            i //= 2
        self.satellite[i] = s
        self.pos[s] = i
        self.key[s] = k
    
    # Deletes the element with minimum key and returns its satellite information
    def delete_min(self) -> int:
        if self.size == 0:
            raise IndexError('Error: empty heap')
    
        min = self.satellite[1]
        slast = self.satellite[self.size]
        self.size -= 1
    
        child = 2
        i = 1
        while child  <= self.size:
            if child < self.size and self.key[self.satellite[child]] > self.key[self.satellite[child + 1]]:
                child += 1
    
            if self.key[slast] > self.key[self.satellite[child]]:
                self.satellite[i] = self.satellite[child]
                self.pos[self.satellite[child]] = i
            else:
                break
            i = child
            child *= 2
        self.satellite[i] = slast
        self.pos[slast] = i
    
        del self.key[min]
        del self.pos[min]
        del self.satellite[-1]

        return min
    
    # Changes the key of the element with satellite s
    def change_key(self, k: Decimal, s: int) -> None:
        self.remove(s)
        self.insert(k, s)
    
    # Removes the element with satellite s
    def remove(self, s: int) -> None:
        i = self.pos[s]
        while i // 2 > 0:
            self.satellite[i] = self.satellite[i // 2]
            self.pos[self.satellite[i]] = i
            i //= 2
        self.satellite[1] = s
        self.pos[s] = 1
    
        self.delete_min()

    # Returns the number of elements in the heap
    def __len__(self) -> int:
        return self.size
    
    # Resets the structure
    def clear(self) -> None:
        self.key.clear()
        self.pos.clear()
        self.satellite.clear()
        self.satellite.append(0)
        self.size = 0

    ## 指定されたサテライトがこのヒープに含まれているときTrueを返す。
    #  @param satellite サテライト。
    #  @return 指定されたサテライトがこのヒープに含まれているときTrue。
    def contains_satellite(self, satellite: int) -> bool:
        return satellite in self.key
