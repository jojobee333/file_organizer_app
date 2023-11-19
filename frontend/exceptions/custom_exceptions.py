class InvalidEntryException(Exception):
    def __init__(self, message, additional_data=None):
        super().__init__(message)
        self.additional_data = additional_data