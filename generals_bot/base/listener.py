from abc import ABC, abstractmethod

from socketio import AsyncClient


class BaseListener(ABC):
    @property
    @abstractmethod
    def _sio(self) -> AsyncClient:
        pass

    @_sio.setter
    def _sio(self, sio: AsyncClient):
        pass
