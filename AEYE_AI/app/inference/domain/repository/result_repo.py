from abc import ABCMeta, abstractmethod

from inference.domain.infer_result import InferenceResult


class IInferenceResultRepository(metaclass=ABCMeta):
    
    @abstractmethod
    def save(self, result : InferenceResult):
        raise NotImplementedError
    
    @abstractmethod
    def search_by_job_id(self, job_id : int):
        raise NotImplementedError