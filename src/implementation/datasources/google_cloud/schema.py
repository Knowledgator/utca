from typing import Any, Dict, Union

from core.datasource_level.schema import DatasourceConfig

class GoogleCloudClientConfig(DatasourceConfig):
    credentials: Union[Dict[str, Any], str]
    scopes: list[str]