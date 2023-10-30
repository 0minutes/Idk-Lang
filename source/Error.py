class Error:
    def __init__(self, details: str) -> None:
        self.details: str = details
  
    def ThrowError(self, message, location: tuple[list[str, int, int]]):
        return f'[{self.details}] {location[0]}:{location[1]}:{location[2]} -> {message}'

class UnfinishedStringErr(Error):
    def __init__(self, details: str) -> None:
        super().__init__(details)

class UnknownValError(Error):
    def __init__(self, details: str) -> None:
        super().__init__(details)