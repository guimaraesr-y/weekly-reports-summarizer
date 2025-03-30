from abc import ABC


class AIAdapter(ABC):

    _api_key = None
    _model = None

    def generate_content(self, message: str):
        raise NotImplementedError
