class ClientAlreadyExistsError(Exception):
    pass


class InvalidDueDateError(Exception):
    pass


class InvalidAmountError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class CreatePaymentError(Exception):
    pass