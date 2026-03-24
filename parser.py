import asyncio
from httpx import AsyncClient
from config import pages_to_parse, is_letter
from utils import get_link, result_to_excel
from lxml import html
from responder import get_letter

async def parse_url(client, url):
    response = await client.get(url)
    return response


async def parse_inside_vacancy(client, url):
    page_content = await parse_url(client, url)
    tree = html.fromstring(page_content)
    desc_el = tree.xpath('//div[@data-qa="vacancy-description"]')
    description = desc_el[0].text_content().strip() if desc_el else ''
    skills = tree.xpath('//li[@data-qa="skills-element"]//div[contains(@class, "magritte-tag__label")]/text()')
    return description, skills


async def parse_content(client, page_content: str) -> list[dict]:
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
        link = f'https://hh.ru/vacancy/{vacancy_id}'
        description, skills = await parse_inside_vacancy(client, vacancy_id)
        result.append({
            'id': vacancy_id,
            'link': link,
            'title': title,
            'salary': salary,
            'description': description,
            'skills': skills
        })
    return result


async def process_page(client,  url, page_number):
    page_url = url + f'&page={page_number}'
    page = await parse_url(client, page_url)
    page_vacancies = await parse_content(client, page)
    return page_vacancies


async def parser():
    url = await get_link()
    async with AsyncClient() as client:
        tasks = [asyncio.create_task(process_page(client, url, page)) for page in range(pages_to_parse)]
        result = await asyncio.gather(*tasks)
        vacancy_list = []
        for item in result:
            if is_letter:
                letter = await get_letter(item['description'], item['skills'])
                item['letter'] = letter
            else:
                item['letter'] = ''
            vacancy_list += item
        await result_to_excel(vacancy_list)

