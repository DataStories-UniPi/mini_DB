class Bucket:
    def __init__(self, max_bucket_size):
        self.data = []
        self.max_bucket_size = max_bucket_size

    def insert(self, data):
        self.data.append(data)
        if len(self.data) > self.max_bucket_size:
            return True
        return False

    def delete(self, data):
        self.data.remove(data)

# Define a hash function for the data
def hash_function(key, max_bucket_size):
    return jenkinsHash(key) % max_bucket_size

# Jenkins hash function
def jenkinsHash(key):
    data = bytearray(key.encode())
    length = len(data)
    hash = 0
    for i in range(length):
        hash += data[i]
        hash += (hash << 10)
        hash ^= (hash >> 6)
    hash += (hash << 3)
    hash ^= (hash >> 11)
    hash += (hash << 15)
    return hash & 0xffffffff

class ExtendibleHashIndex:
    def __init__(self, max_bucket_size):
        self.buckets = {}
        self.max_bucket_size = max_bucket_size

    def insert(self, data):
        key, idx = data
        hash_value = hash_function(key, self.max_bucket_size)
        if hash_value not in self.buckets:
            self.buckets[hash_value] = Bucket(self.max_bucket_size) # Create a new bucket
        if self.buckets[hash_value].insert(data):
            self.split_bucket(hash_value)

    def delete(self, data):
        key, idx = data
        hash_value = hash_function(key, self.max_bucket_size)
        if hash_value in self.buckets:
            self.buckets[hash_value].delete(data)

    def split_bucket(self, hash_value):
        original_bucket = self.buckets[hash_value]
        new_bucket_1 = Bucket(self.max_bucket_size)
        new_bucket_2 = Bucket(self.max_bucket_size)

        for data in original_bucket.data:
            key, idx = data
            new_hash_value = hash_function(key, self.max_bucket_size * 2)
            if new_hash_value & 1:
                new_bucket_1.insert(data)
            else:
                new_bucket_2.insert(data)

        self.buckets[hash_value] = new_bucket_1
        self.buckets[hash_value + self.max_bucket_size] = new_bucket_2

    def find(self, key):
        hash_value = hash_function(key, self.max_bucket_size)
        if hash_value in self.buckets:
            bucket = self.buckets[hash_value]
            for data in bucket.data:
                if data[0] == key:
                    return data[1]
        return None