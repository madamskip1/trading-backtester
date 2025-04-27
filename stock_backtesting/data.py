from datetime import datetime
from typing import Any, Optional

import numpy as np

DATA_TYPE = np.dtype(
    [
        ("datetime", "datetime64[ns]"),
        ("open", "f8"),
        ("min", "f8"),
        ("max", "f8"),
        ("close", "f8"),
    ]
)


class Data:

    def __init__(self, data: np.ndarray[Any, np.dtype[Any]]):
        self.__data = data
        self.__current_data_index = 0

    def __getitem__(self, index: int) -> Any:
        return self.__data[index]

    def increment_data_index(self) -> None:
        self.__current_data_index += 1

    def get_data(self, key: Optional[str] = None) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data[key] if key else self.__data

    def get_current_data_index(self) -> int:
        return self.__current_data_index

    def get_current_data(self, key: str) -> float:
        return self.__data[self.__current_data_index][key]

    def get_current_datatime(self) -> datetime:
        return (
            self.__data[self.__current_data_index]["datetime"]
            .astype("M8[ms]")
            .astype(datetime)
        )

    @property
    def open(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data["open"]

    @property
    def min(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data["min"]

    @property
    def max(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data["max"]

    @property
    def close(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data["close"]
