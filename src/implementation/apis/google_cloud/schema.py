from typing import Any, Dict, Union, Optional

from pydantic import PrivateAttr, BaseModel

from core.datasource_level.schema import DatasourceConfig

class GoogleCloudClientConfig(BaseModel):
    credentials: Union[Dict[str, Any], str, None]
    scopes: list[str]


class GoogleCloudDatasourceServiceConfig(DatasourceConfig):
    _service: Optional[Any] = PrivateAttr()

    def set_service(self, service: Any) -> None:
        self._service = service

    
    @property
    def service(self) -> Any:
        return self._service