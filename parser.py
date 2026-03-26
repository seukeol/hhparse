import asyncio
from httpx import AsyncClient
from config import pages_to_parse, is_letter
from utils import get_link, result_to_excel
from lxml import html
from responder import get_letter
import random


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://hh.ru/',
    'Connection': 'keep-alive',
}

sem = asyncio.Semaphore(4)


async def parse_url(client, url, retries=3):
    for attempt in range(retries):
        response = await client.get(url, follow_redirects=False)
        if response.status_code == 302:
            wait = random.randint(10, 30)
            print(f"302 на {url}, ждём {wait}с (попытка {attempt + 1}/{retries})")
            await asyncio.sleep(wait)
            continue
        if response.status_code != 200:
            print(f"Статус {response.status_code} на {url}")
        return response.text
    print(f"Не удалось получить {url} после {retries} попыток")
    return ''


async def parse_inside_vacancy(client, url):
    async with sem:
        rand_sleep = random.randint(3, 8)
        await asyncio.sleep(rand_sleep)
        page_content = await parse_url(client, url)
    if not page_content:
        return '', ''
    try:
        tree = html.fromstring(page_content)
    except Exception as e:
        print(e)
        return '', ''
    desc_el = tree.xpath('//div[@data-qa="vacancy-description"]')
    description = desc_el[0].text_content().strip() if desc_el else ''
    skills = tree.xpath('//li[@data-qa="skills-element"]//div[contains(@class, "magritte-tag__label")]/text()')
    return description, skills


async def parse_content(client, page_content) -> list[dict]:
    tree = html.fromstring(page_content)
    result = []
    for card in tree.xpath('//div[contains(@class, "vacancy-card--")]'):
        vacancy_id = card.get('id', '')
        title_link = card.xpath('.//a[@data-qa="serp-item__title"]')
        if not title_link:
            continue
        title = title_link[0].xpath('.//span[@data-qa="serp-item__title-text"]/text()')
        title = title[0].strip() if title else ''
        if title.lower().__contains__('преподаватель'):
            continue
        salary_el = card.xpath(
            './/span[contains(@class, "compensation-labels--")]/span[contains(@class, "magritte-text_typography-label-1")]/text()')
        salary = salary_el[0].strip() if salary_el else ''
        link = f'https://hh.ru/vacancy/{vacancy_id}'
        description, skills = await parse_inside_vacancy(client, link)
        result.append({
            'id': vacancy_id,
            'link': link,
            'title': title,
            'salary': salary,
            'description': description,
            'skills': skills,
            'letter': '',
            'responded': 0
        })
    return result


async def process_page(client, url, page_number):
    async with sem:
        rand_sleep = random.randint(3, 8)
        await asyncio.sleep(rand_sleep)
        page_url = url + f'&page={page_number}'
        page = await parse_url(client, page_url)
    if not page:
        return []
    return await parse_content(client, page)


async def parser():
    url = await get_link()
    async with AsyncClient(headers=HEADERS, follow_redirects=True, timeout=60.0) as client:
        await client.get('https://hh.ru/')
        await asyncio.sleep(random.randint(2, 4))
        tasks = [asyncio.create_task(process_page(client, url, page)) for page in range(pages_to_parse)]
        result = await asyncio.gather(*tasks)
        vacancy_list = []
        for item in result:
            vacancy_list += item
        await result_to_excel(vacancy_list)