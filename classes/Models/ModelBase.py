class ModelBase:
    __created_at: str
    __updated_at: str

    def __init__(self, data: dict):
        self.__created_at = data['created_at']
        self.__updated_at = data['updated_at']

    @property
    def created_at(self):
        """Get the created_at of model."""
        return self.__created_at

    @property
    def updated_at(self):
        """Get the updated_at of model."""
        return self.__updated_at
