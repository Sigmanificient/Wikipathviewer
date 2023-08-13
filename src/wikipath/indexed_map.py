from typing import Dict, List, Generic, TypeVar, Optional

T = TypeVar('T')


class IndexedMap(Generic[T]):

    def __init__(self):
        self.__map: Dict[T, int] = {}
        self.__indices: List[T] = []
        self.__last_id = -1

    def add(self, item: T) -> int:
        self.__last_id += 1
        self.__indices.append(item)
        self.__map[item] = self.__last_id
        return self.__last_id

    def get_id(self, item: T) -> int:
        return self.__map.get(item, -1)

    def get_name(self, idx: int) -> Optional[T]:
        if idx < 0 or idx > self.__last_id:
            return None

        return self.__indices[idx]
    
    def __len__(self) -> int:
        return self.__last_id

    def __contains__(self, item: str):
        return item in self.__map