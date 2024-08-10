import aiofiles
import asyncio

async def write_file(file_name, data):
    async with aiofiles.open(f"C:\\Users\\Path_Here", mode="a") as f:
        await f.write(f"{data}\n")