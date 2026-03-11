import numpy as np

class Action:
    port: str
    field: str
    def __init__(self, port: str, field: str) -> None: ...
    def get_lua_string(self) -> str: ...

class Address:
    address: str
    mode: str
    def __init__(self, address: str, mode: str) -> None: ...
    def get_lua_string(self) -> str: ...

class Emulator:
    def __init__(
        self,
        env_id: str,
        roms_path: str,
        game_id: str,
        memory_addresses: dict[str, Address],
        frame_ratio: int = ...,
        render: bool = ...,
        throttle: bool = ...,
        frame_skip: int = ...,
        sound: bool = ...,
        debug: bool = ...,
        binary_path: str | None = ...,
    ) -> None: ...
    def step(self, actions: list[Action]) -> dict[str, np.ndarray]: ...
    def close(self) -> None: ...
