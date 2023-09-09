from __future__ import annotations
from typing import Any


class VariableTypeModifier:
    def __init__(self, var: Any) -> None:
        self.var = var
        self.status = False
    
    def cast_int(self) -> VariableTypeModifier:
        if self.status:
            return self
        try:
            self.var = int(self.var)
            self.status = True
        except Exception:
            pass
        return self

    def cast_float(self) -> VariableTypeModifier:
        if self.status:
            return self
        try:
            self.var = float(self.var)
            self.status = True
        except Exception:
            pass
        return self
   
    def get(self) -> Any:
        return self.var
