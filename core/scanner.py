import asyncio

async def scan_port(ip, port, timeout=1):
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False


async def scan_ports(ip, ports):
    results = {}

    tasks = []
    for port in ports:
        tasks.append(asyncio.create_task(scan_port(ip, port)))

    statuses = await asyncio.gather(*tasks)

    for p, st in zip(ports, statuses):
        results[p] = st

    return results



