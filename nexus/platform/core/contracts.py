from dataclasses import dataclass

@dataclass(frozen=True)
class ServiceContract:
    name: str
    version: str
    capabilities: tuple[str, ...] = ()

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities
