from parser import parser


async def main():
    await parser()

if __name__ == '__main__':
    asyncio.run(main())