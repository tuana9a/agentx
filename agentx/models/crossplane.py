from __future__ import annotations

import crossplane

from pydantic import BaseModel
from typing import List, Optional


class DirectiveEntry(BaseModel):
    directive: Optional[str]
    line: Optional[int] = None
    args: Optional[List[str]] = []
    block: Optional[List[DirectiveEntry]] = None


class ParsedEntry(BaseModel):
    file: Optional[str] = None
    status: Optional[str] = None
    errors: Optional[List] = []
    parsed: List[DirectiveEntry] = []

    def build(self):
        return crossplane.build(self.dict()["parsed"], indent=2)

    def save(self):
        if not self.file:
            return
        with open(self.file, "w", encoding="utf-8") as f:
            content = self.build()
            f.write(content)