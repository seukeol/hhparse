from config import auto_respond, is_letter
from parser import parser
from responder import responder, get_letter
import asyncio
import pandas as pd

async def main():
    #await parser()

    if is_letter:
        df = pd.read_excel('vacancies.xlsx', engine="openpyxl")
        df['letter'] = df['letter'].astype(object)
        for idx, vacancy in df.iterrows():
            if pd.isna(vacancy['letter']):
                try:
                    letter = await get_letter(vacancy['description'], vacancy['skills'])
                    df.at[idx, 'letter'] = letter
                except Exception as e:
                    continue
        df.to_excel('vacancies.xlsx', index=False, engine="openpyxl")

    if auto_respond:
        await responder()


if __name__ == '__main__':
    asyncio.run(main())