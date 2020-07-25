from typing import Optional

from dataclasses import dataclass


@dataclass
class LinkAllModel:
    app_label: str
    model_name: str
    verbose_name: Optional[str] = None
    url_method: Optional[str] = None
    is_show_url_in_select: bool = True
    
    def __post_init__(self):
        self.app_label = self.app_label.lower()
        self.model_name = self.model_name.lower()
