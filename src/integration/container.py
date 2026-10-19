from typing import Callable, Any

class Container:
    def __init__(self):
        self._providers: dict[str, tuple[Callable[[], Any]], bool] = {}
        self._singleton: dict[str, Any] = {}

    def register(self, name: Any, provider: Callable[[], Any], is_singleton: bool = False) -> None:
        self._providers[name.__name__] = (provider, is_singleton)

    def resolve(self, name:Any) -> Any:
        if name.__name__ in self._singleton:
            return self._singleton[name.__name__]

        if name.__name__ not in self._providers:
            raise ValueError(f'No provider registered for {name.__name__}')

        provider, is_singleton = self._providers[name.__name__]
        instance = provider()

        if is_singleton:
            self._singleton[name.__name__] = instance

        return instance
