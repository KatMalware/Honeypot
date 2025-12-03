import asyncio
import importlib

class ServiceListener:
    def __init__(self, bind='0.0.0.0', port=2222, service_name='ssh'):
        self.bind = bind
        self.port = port
        self.service_name = service_name

    async def handle(self, reader, writer):
        handler_module = importlib.import_module(f"services.{self.service_name}")
        handler = getattr(handler_module, "handle_connection")
        await handler(reader, writer)

    async def start(self):
        server = await asyncio.start_server(self.handle, self.bind, self.port)
        print(f"[+] {self.service_name} running on {self.bind}:{self.port}")
        async with server:
            await server.serve_forever()



