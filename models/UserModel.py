from dataclasses import dataclass

@dataclass
class User:
   first_name: str
   last_name: str
   email: str
   id: int = None