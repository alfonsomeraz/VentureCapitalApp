from pydantic import BaseModel
from typing import List
import datetime


class Deal(BaseModel):
  company: str
  interest: int
  industry: str
  location: str
  deal_stage: str
  deal_size: int
  lead_investor: str
  lead_investor_location: str
  investors: List[str]
  date_added: datetime.datetime