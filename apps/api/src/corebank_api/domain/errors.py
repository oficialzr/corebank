class TransferError(Exception):
    pass


class SourceAccountNotFoundError(TransferError):
    pass


class DestinationAccountNotFoundError(TransferError):
    pass


class SameAccountTransferError(TransferError):
    pass


class CurrencyMismatchError(TransferError):
    pass


class InsufficientFundsError(TransferError):
    pass


class UserError(Exception):
    pass


class EmailAlreadyRegisteredError(UserError):
    pass


class InvalidCredentialsError(UserError):
    pass
