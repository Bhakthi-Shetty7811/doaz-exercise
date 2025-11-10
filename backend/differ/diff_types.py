from typing import TypedDict, List, Optional

class Entity(TypedDict):
    id: str
    type: str
    text: str
    numeric_value: float
    unit: str
    tolerance: str
    bbox_px: List[int]

class Change(TypedDict):
    change_id: str
    type: str
    entity_ref_before: Optional[str]
    entity_ref_after: Optional[str]
    before: Optional[dict]
    after: Optional[dict]
    similarity: float
