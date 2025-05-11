from datetime import datetime
from enum import Enum
from typing import Any, List, Optional, Tuple

import numpy as np

DATA_TYPE = np.dtype(
    [
        ("datetime", "datetime64[ns]"),
        ("open", "f8"),
        ("high", "f8"),
        ("low", "f8"),
        ("close", "f8"),
        ("volume", "f8"),
    ]
)


class CandlestickPhase(Enum):
    OPEN = 1
    CLOSE = 2


class Data:

    def __init__(self, data: np.ndarray[Any, np.dtype[Any]]):
        self.__data = data
        self.__current_data_index = 0
        self.__candlestick_phase = CandlestickPhase.OPEN

    def __getitem__(self, index: int) -> Any:
        return self.__data[index]

    def __len__(self) -> int:
        return len(self.__data)

    def __iter__(self):
        return iter(self.__data)

    def set_candlestick_phase(self, phase: CandlestickPhase) -> None:
        self.__candlestick_phase = phase

    def get_candlestick_phase(self) -> CandlestickPhase:
        return self.__candlestick_phase

    def increment_data_index(self) -> None:
        self.__current_data_index += 1

    def get_data(self, key: Optional[str] = None) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data[key] if key else self.__data

    def get_current_data_index(self) -> int:
        return self.__current_data_index

    def get_current_data(self, key: str) -> float:
        return self.__data[self.__current_data_index][key]

    def get_current_price(self) -> float:
        return self.__data[self.__current_data_index][
            "open" if self.__candlestick_phase == CandlestickPhase.OPEN else "close"
        ]

    def get_current_low_price(self) -> float:
        return (
            self.__data[self.__current_data_index]["low"]
            if self.__candlestick_phase == CandlestickPhase.CLOSE
            else self.__data[self.__current_data_index]["open"]
        )

    def get_current_high_price(self) -> float:
        return (
            self.__data[self.__current_data_index]["high"]
            if self.__candlestick_phase == CandlestickPhase.CLOSE
            else self.__data[self.__current_data_index]["open"]
        )

    def get_current_numpy_datetime(self) -> np.datetime64:
        return self.__data[self.__current_data_index]["datetime"]

    def get_current_datatime(self) -> datetime:
        return (
            self.__data[self.__current_data_index]["datetime"]
            .astype("M8[ms]")
            .astype(datetime)
        )

    @property
    def datetime(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data["datetime"]

    @property
    def open(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data["open"]

    @property
    def low(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data["low"]

    @property
    def high(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data["high"]

    @property
    def close(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data["close"]

    @property
    def volume(self) -> np.ndarray[Any, np.dtype[Any]]:
        return self.__data["volume"]

    @staticmethod
    def from_array(
        data: List[
            Tuple[
                Any,
                Optional[float],
                Optional[float],
                Optional[float],
                Optional[float],
                Optional[float],
            ]
        ],
    ) -> "Data":
        data_array = np.array(
            data,
            dtype=DATA_TYPE,
        )
        return Data(data_array)

    @staticmethod
    def from_csv(
        file_path: str,
        delimiter: str = ",",
    ) -> "Data":
        data_np = np.genfromtxt(
            file_path,
            delimiter=delimiter,
            skip_header=1,
            dtype=DATA_TYPE,
            usecols=(0, 1, 2, 3, 4, 5),
        )
        return Data(data_np)
