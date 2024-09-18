# python-alpaca-server

This is an easy to use Python server for ASCOM Alpaca. It can be run on any
system that running Python 3.12 or higher, including a Raspberry Pi. This allows
you to easily create new ASCOM Alpaca devices.

Nothing complicated here, just create a new class that implements your logic and
inherits from one of the base device classes.

Then start up a new `AlpacaServer`. The server automatically enables discovery
as well.

## Example

```python
from typing import List, override

from .app import AlpacaServer, Description
from .devices.safetymonitor import SafetyMonitor
from .errors import NotImplementedError
from .request import ActionRequest, CommandRequest, CommonRequest, PutConnectedRequest

# Inherit from the base SafetyMonitor class, and implement the methods.
class MySafetyMonitor(SafetyMonitor):
    def __init__(self, unique_id: str):
        super().__init__(unique_id)
        self._connected = False

    @override
    def put_action(self, req: ActionRequest) -> str:
        raise NotImplementedError(req)

    @override
    def put_command_blind(self, req: CommandRequest) -> None:
        raise NotImplementedError(req)

    @override
    def put_command_bool(self, req: CommandRequest) -> bool:
        raise NotImplementedError(req)

    @override
    def put_command_string(self, req: CommandRequest) -> str:
        raise NotImplementedError(req)

    @override
    def get_connected(self, req: CommonRequest) -> bool:
        return self._connected

    @override
    def put_connected(self, req: PutConnectedRequest) -> None:
        self._connected = req.Connected

    @override
    def get_description(self, req: CommonRequest) -> str:
        return "My Description"

    @override
    def get_driverinfo(self, req: CommonRequest) -> str:
        return "My Driver Info"

    @override
    def get_driverversion(self, req: CommonRequest) -> str:
        return "0.1.0"

    @override
    def get_interfaceversion(self, req: CommonRequest) -> int:
        return 1

    @override
    def get_name(self, req: CommonRequest) -> str:
        return "MySafetyMonitor"

    @override
    def get_supportedactions(self, req: CommonRequest) -> List[str]:
        return []

    @override
    def get_issafe(self, req: CommonRequest) -> bool:
        if not self._connected:
            return False

        # TODO: Check something to see if we are safe to observe. Return True if safe.
        return False


def get_server_description() -> Description:
    return Description(
        ServerName="MyServer",
        Manufacturer="MyManufacturer",
        ManufacturerVersion="0.1.0",
        Location="MyLocation",
    )


if __name__ == "__main__":
    import uvicorn

    port = 8000

    # Choose a unique ID to pass into MySafetyMonitor. This ID should stay the same
    # across server restarts.
    svr = AlpacaServer(get_server_description, [MySafetyMonitor("other")])

    # Create a FastAPI application we can attach to uvicorn or any other WSGI server.
    app = svr.create_app(port)

    try:
        uvicorn.run(app, host="0.0.0.0", port=port)
    except KeyboardInterrupt:
        pass
```
