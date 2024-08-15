import uuid
from pydantic import BaseModel, Field
from enum import IntEnum


class Text:
    def __init__(self, filepath:str, contents:str) -> None:
        self.filepath = filepath
        self.contents = contents
    
    
class CSV():
    def __init__(self, filepath:str, keys, contents) -> None:
        self.filepath = filepath
        self.keys = keys
        self.contents = contents
        
        
class DocIndex(BaseModel):
    doc_id: str = Field(default_factory=lambda: uuid.uuid4().hex)


class Document(DocIndex):
    content: str


class Operator(IntEnum):
    Eq = 0
    Ne = 1
    Gt = 2
    Ge = 3
    Lt = 4
    Le = 5
    In = 6
    Notin = 7
    And = 8
    Or = 9
    