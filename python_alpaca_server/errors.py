from .response import CommonRequest


class AlpacaError(Exception):
    def __init__(
        self,
        error_number: int,
        error_message: str,
        client_transaction_id: int,
        client_id: int,
        server_transaction_id: int,
    ):
        self.error_number = error_number
        self.error_message = error_message
        self.client_transaction_id = client_transaction_id
        self.client_id = client_id
        self.server_transaction_id = server_transaction_id

        super().__init__(f"{error_number} - {error_message}")


class NotImplementedError(AlpacaError):
    def __init__(self, req: CommonRequest):
        super().__init__(
            0x400, "not implemented", req.ClientTransactionID, req.ClientID, 0
        )


class InvalidValueError(AlpacaError):
    def __init__(self):
        super().__init__(0x401, "invlaid value")


class ValueNotSetError(AlpacaError):
    def __init__(self):
        super().__init__(0x402, "value not set")


class NotConnectedError(AlpacaError):
    def __init__(self):
        super().__init__(0x407, "not connected")


class InvalidWhileParkedError(AlpacaError):
    def __init__(self):
        super().__init__(0x408, "invalid while parked")


class InvalidWhileSlavedError(AlpacaError):
    def __init__(self):
        super().__init__(0x409, "invalid while slaved")


class InvalidOperationError(AlpacaError):
    def __init__(self):
        super().__init__(0x40B, "invalid operation")


class ActionNotImplemented(AlpacaError):
    def __init__(self):
        super().__init__(0x40C, "action not implemented")
