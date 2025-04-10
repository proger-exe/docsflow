from AtlantSDK.misc.memory import MemoryStorage

class StateSystem:
    def __init__(self):
        self.state = ""
        self.memory = MemoryStorage()

    def get_state(self):
        return self.state 
    
    def set_state(self, state: str):
        self.state = state

    def update_memory(self, key: str, what):
        self.memory.set(key, what)
    
    def get_memory(self, key: str):
        self.memory.get(key)
    