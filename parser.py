import asyncio
from httpx import AsyncClient
from config import pages_to_parse
from utils import get_link, result_to_excel
from lxml import html


async def parse_url(client, url):
    response = await client.get(url)
    return response


async def parse_content(page_content: str) -> list[dict]:
    tree = html.fromstring(page_content)
    result = []
    for card in tree.xpath('//div[contains(@class, "vacancy-card--")]'):
        vacancy_id = card.get('id', '')
        title_link = card.xpath('.//a[@data-qa="serp-item__title"]')
        if not title_link:
            continue
        title = title_link[0].xpath('.//span[@data-qa="serp-item__title-text"]/text()')
        title = title[0].strip() if title else ''
        salary_el = card.xpath(
            './/span[contains(@class, "compensation-labels--")]/span[contains(@class, "magritte-text_typography-label-1")]/text()')
        salary = salary_el[0].strip() if salary_el else ''
        result.append({
            'id': vacancy_id,
            'link': f'https://hh.ru/vacancy/{vacancy_id}',
            'title': title,
            'salary': salary,
        })
    return result


async def process_page(client,  url, page_number):
    page_url = url + f'&page={page_number}'
    page = await parse_url(client, page_url)
    page_vacancies = await parse_content(page)
#обработка внутренности страницы
    return page_vacancies


async def parser():
    url = await get_link()
    async with AsyncClient() as client:
        tasks = [asyncio.create_task(process_page(client, url, page)) for page in range(pages_to_parse)]
        result = await asyncio.gather(*tasks)
        vacancy_list = []
        for item in result:
            vacancy_list += item


        await result_to_excel(vacancy_list)
