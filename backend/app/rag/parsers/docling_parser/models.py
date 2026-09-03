from dataclasses import dataclass
from typing import List


@dataclass
class DocumentElement:
    element_index: int
    type: str
    markdown: str
    pages: List[int]


@dataclass
class NormalizedDocument:
    elements: List[DocumentElement]