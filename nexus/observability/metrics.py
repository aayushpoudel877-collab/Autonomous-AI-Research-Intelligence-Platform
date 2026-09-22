from dataclasses import dataclass
@dataclass
class Counter:
    value:int=0
    def inc(self,amount:int=1): self.value+=amount
