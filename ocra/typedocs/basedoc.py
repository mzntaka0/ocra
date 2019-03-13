# -*- coding: utf-8 -*-
"""
"""
from abc import abstractmethod, ABCMeta


class Basedoc(object, metaclass=ABCMeta):
    """

    Args:
    """

    @abstractmethod
    def read_lines(self):
        """
        This method have to have the features below.
            - load document from document_Path
            - recognize each lines
            - get words in each lines and coordinate from docs
            - return list which includs words and coordinate of each lines

        Input
        ----------
            - document_Path (Path): document Path
        """
        pass
