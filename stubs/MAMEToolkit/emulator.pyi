from typing import Any

class Action:
    address: str
    port: str
    def __init__(self, address: str, port: str) -> None: ...

class Address:
    def __init__(self, address: str, data_type: str) -> None: ...

class Emulator:
    def __init__(
        self,
        env_id: str,
        roms_path: str,
        game_name: str,
        memory_addresses: dict[str, Address],
        *,
        frame_ratio: int = ...,
        render: bool = ...,
        throttle: bool = ...,
        frame_skip: int = ...,
        sound: bool = ...,
        debug: bool = ...,
        binary_path: str | None = ...,
    ) -> None: ...
    def step(self, actions: list[int]) -> dict[str, Any]: ...
    def close(self) -> None: ...
