class FeatureFlags:
    def __init__(self, **flags: bool):
        self._flags = dict(flags)

    def enabled(self, name: str, default: bool = False) -> bool:
        return self._flags.get(name, default)

    def set(self, name: str, enabled: bool) -> None:
        self._flags[name] = enabled
