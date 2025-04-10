class MemoryStorage:
    def __init__(self):
        self.memory = {}

    def set(self, key: str, value):
        self.memory[key] = value 
    
    def get(self, key: str):
        return self.memory.get(key)

    def get_all_with_prefix(self, prefix: str):
        res = []
        for sector in self.memory:
            if prefix in sector:
                res.append((sector, self.memory[sector]))

        return res