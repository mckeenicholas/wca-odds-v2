from typing import Dict, TypedDict


class EventFormat(TypedDict):
    num_attempts: int
    default_format: str


event_formats: Dict[str, EventFormat] = {
    "333": {"num_attempts": 5, "default_format": "a"},
    "222": {"num_attempts": 5, "default_format": "a"},
    "444": {"num_attempts": 5, "default_format": "a"},
    "555": {"num_attempts": 5, "default_format": "a"},
    "666": {"num_attempts": 3, "default_format": "m"},
    "777": {"num_attempts": 3, "default_format": "m"},
    "sq1": {"num_attempts": 5, "default_format": "a"},
    "clock": {"num_attempts": 5, "default_format": "a"},
    "333oh": {"num_attempts": 5, "default_format": "a"},
    "pyram": {"num_attempts": 5, "default_format": "a"},
    "skewb": {"num_attempts": 5, "default_format": "a"},
    "333fm": {"num_attempts": 3, "default_format": "m"},
    "333bf": {"num_attempts": 3, "default_format": "b"},
    "444bf": {"num_attempts": 3, "default_format": "b"},
    "555bf": {"num_attempts": 3, "default_format": "b"},
}
