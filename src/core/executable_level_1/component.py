from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from core.executable_level_1.pipeline import ExecutionSchema  # Forward declaration for type checking

class Component:
    def __ror__(self, comp: Union['ExecutionSchema', 'Component']) -> 'ExecutionSchema':
        from core.executable_level_1.pipeline import ExecutionSchema
        if isinstance(comp, ExecutionSchema):
            comp.add(self)
            return comp
        else:
            return ExecutionSchema(self)


