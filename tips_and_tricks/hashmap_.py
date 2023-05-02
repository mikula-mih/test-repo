
""" Implementing HashMaps in Python """
# Memory index access takes constant time and hashing takes constant time.
# Hence, the search complexity of a hash map is also constant time,
# that is, O(1).

class HashTable:

    # create empty bucket list of given size
    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        return [[] for _ in range(self.size)]

    # Insert values into hash map
    def set_val(self, key, val):
        # Get the index from the key
        # using hash function
        hashed_key = hash(key) % self.size

        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            # check if the bucket has same key as
            # the key to be inserted
            if record_key == key:
                found_key = True
                break

        # If the bucket has same key as the key to be inserted,
        # Update the key vakue
        # Otherwise apppend the new key-value pair to the bucket
        if found_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))

    # Return searched value with specific key
    def get_val(self, key):
        # Get the index from the key using
        # hash function
        hashed_key = hash(key) % self.size

        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record

            # check if the bucket has same key as
            # the key being searched
            if record_key == key:
                found_key = True
                break

        # If the bucket has same key as the key being searched,
        # Return the value found
        # Otherwise indicate there was no record found
        if found_key:
            return record_val
        else:
            return "No record found"

    # Remove a value with specific key
    def delete_val(self, key):

        # Get the index from the key using
        # hash function
        hashed_key = hash(key) % self.size

        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record

            # check if the bucket has same key as
            # the key to be deleted
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket.pop(index)
        return

    # To print the items of hash map
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashMap:
    def __init__(self):
        self.store = [None for _ in range(16)]
    def get(self, key):
        index = hash(key) & 15
        if self.store[index] is None:
            return None
        n = self.store[index]
        while True:
            if n.key == key:
                return n.value
            else:
                if n.next:
                    n = n.next
                else:
                    return None
    def put(self, key, value):
        nd = Node(key, value)
        index = hash(key) & 15
        n = self.store[index]
        if n is None:
            self.store[index] = nd
        else:
            if n.key == key:
                n.value = value
            else:
                while n.next:
                    if n.key == key:
                        n.value = value
                        return
                    else:
                        n = n.next
                n.next = nd

class HashMap_v2:
    def __init__(self):
        self.size = 64
        self.map = [None] * self.size

    def _get_hash(self, key):
        hash = 0

        for char in str(key):
            hash += ord(char)
        return hash % self.size

    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
                else:
                    self.map[key_hash].append(list([key_value]))
                    return True

    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    def delete(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None :
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    def print(self):

        print('---Phonebook---')
        for item in self.map:
            if item is not None:
                print(str(item))




def main_HashMap():
    hm = HashMap()
    hm.put("1", "sachin")
    hm.put("2", "sehwag")
    hm.put("3", "ganguly")
    hm.put("4", "srinath")
    hm.put("5", "kumble")
    hm.put("6", "dhoni")
    hm.put("7", "kohli")
    hm.put("8", "pandya")
    hm.put("9", "rohit")
    hm.put("10", "dhawan")
    hm.put("11", "shastri")
    hm.put("12", "manjarekar")
    hm.put("13", "gupta")
    hm.put("14", "agarkar")
    hm.put("15", "nehra")
    hm.put("16", "gawaskar")
    hm.put("17", "vengsarkar")
    print(hm.get("1"))
    print(hm.get("2"))
    print(hm.get("3"))
    print(hm.get("4"))
    print(hm.get("5"))
    print(hm.get("6"))
    print(hm.get("7"))
    print(hm.get("8"))
    print(hm.get("9"))
    print(hm.get("10"))
    print(hm.get("11"))
    print(hm.get("12"))
    print(hm.get("13"))
    print(hm.get("14"))
    print(hm.get("15"))
    print(hm.get("16"))
    print(hm.get("17"))

def main_HashTable():
    hash_table = HashTable(50)

    # insert some values
    hash_table.set_val('gfg@example.com', 'some value')
    print(hash_table)
    print()

    hash_table.set_val('portal@example.com', 'some other value')
    print(hash_table)
    print()

    # search/access a record with key
    print(hash_table.get_val('portal@example.com'))
    print()

    # delete or remove a value
    hash_table.delete_val('portal@example.com')
    print(hash_table)

if __name__ == "__main__":
    main_HashMap()
    main_HashTable()
    h = HashMap_v2()
    h.print()
