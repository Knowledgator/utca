from core.executable_level_1.executable import Executable
from core.datasource_level.schema import (
    DatasourceActionType, DatasourceDataType, DatasourceConfigType
)

class Datasource(Executable[DatasourceConfigType, DatasourceActionType, DatasourceDataType]):
    ...