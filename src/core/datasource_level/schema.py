from __future__ import annotations
from typing import Any, TypeVar, Dict
from abc import abstractmethod

from core.executable_level_1.schema import Input, Output, Config


class DatasourceConfig(Config):
    ...


class DatasourceAction(Input):
    @abstractmethod
    def execute(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        ...


class DatasourceData(Output):
    ...

DatasourceConfigType = TypeVar('DatasourceConfigType', bound=DatasourceConfig, contravariant=True)
DatasourceActionType = TypeVar('DatasourceActionType', bound=DatasourceAction)
DatasourceDataType = TypeVar('DatasourceDataType', bound=DatasourceData)