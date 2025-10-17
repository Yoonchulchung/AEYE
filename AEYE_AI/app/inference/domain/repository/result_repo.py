from abc import abstractmethod, ABCMeta

from inference.domain.result import Result

class IResultRepository(metaclass=ABCMeta):
    
    @abstractmethod
    def save(self, result : Result):
        raise NotImplementedError
    
    @abstractmethod
    def search_by_job_id(self, job_id : int):
        raise NotImplementedError