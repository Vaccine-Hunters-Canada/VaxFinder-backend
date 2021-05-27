from pathlib import Path
from re import findall
from typing import Union

# For file or directory locations
Location = Union[str, Path]


def read_content_from_file(filepath: Location) -> str:
    with open(filepath) as file:
        content = file.read()
    return content


def get_number_in_str(string: str) -> int:
    numbers_only_regex = r"\d+"

    numbers = findall(numbers_only_regex, string)

    assert len(numbers) == 1, f"{string}"

    return int(numbers[0])
