from abc import ABCMeta, abstractmethod

from inference.domain.request import Request


class IRequestRepository(metaclass=ABCMeta):
    
    @abstractmethod
    def save(self, request : Request):
        raise NotImplementedError
    
    @abstractmethod
    def search_by_job_id(self, job_id : int):
        raise NotImplementedError