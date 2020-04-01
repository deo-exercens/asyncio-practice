from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:
    ''' 메시지 '''
    seqno: int
    contents: str
    dt: datetime
