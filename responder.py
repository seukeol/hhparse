from config import openai_api_key
from openai import OpenAI
from playwright.async_api import async_playwright, Playwright
import pandas as pd
import asyncio

async def get_letter(text, skills):
    client = OpenAI(
        api_key=openai_api_key,
        base_url="https://api.proxyapi.ru/openai/v1",
    )
    prompt = f"""
    Привет. Ты - профессиональный помощник сейчас я пришлю тебе текст вакансии, а ты будешь писать сопроводительное. Пиши очень коротко, по человечески, не очень официально (привет, вместо здравствуйте итп). Старайся избегать списков, банальных для нейронок конструкций, чтобы не было понятно, что это нейросеть. Старайся избегать сложных метафор и речевых оборотов. Так же не используй длинное тире, вместо него ставь дефиз. Не злоупотребляй скобками (были ответы, где нейросеть писала задачу и в скобках библиотеку, это можно, но если так все письмо - это выглядит странно). Иногда можешь игнорировать знаки препинания, вроде кавычек (пример: "под ключ" в контексте проекта можно писать без них, т.к. это уже достаточно устоявшееся выражение). Начинай строго с "Привет!", заканчивай строго "Буду рад пообщаться :)" Я джун, это важно понимать, НО НЕ ПИСАТЬ ОБ ЭТОМ. любой навык, который есть и в вакансии, и в моем резюме - надо упомянуть. Не обязательно говорить что именно я делал, но и не запрещено. смотри по ситуации, но обязательно хотя бы просто упомяни"
===========================================================================
Вот мой опыт работы:

Самозанятость.


Python-разработчик
Январь 2025 — сейчас (1 год и 3 месяца)

Выполнял коммерческие заказы по backend-разработке и автоматизации для различных клиентов.

Чем занимался:
- Разработка backend-сервисов на Python
- Создание Telegram-ботов различной сложности (aiogram)
- Интеграция с внешними API и платёжными системами
- Разработка парсеров и систем автоматического сбора данных
- Построение асинхронных решений на базе asyncio
- Проектирование архитектуры под задачи клиента
- Оптимизация производительности и устойчивости сервисов
- Деплой и контейнеризация проектов (Docker)
- Поддержка и доработка существующих решений

Основной стек:
Python 3.12, asyncio, aiohttp, httpx, aiogram, SQLAlchemy, PostgreSQL, SQLite, Docker

Результаты:
- Реализовано 15+ коммерческих проектов
- Автоматизированы бизнес-процессы клиентов
- Разработаны Telegram-боты с интеграцией внешних сервисов
- Реализованы системы парсинга и обработки больших объёмов данных
- Обеспечена стабильная работа сервисов под нагрузкой
- Повышена скорость обработки запросов и отклика систем


ООО "ТСЕ"
Менеджер по автоматизации
Март 2025 — Январь 2026 (11 месяцев)

Разрабатывал различные инструменты для автоматизации работы.

Чем занимался:
- Проектирование и разработка production-сервисов на Python
- Интеграция с внешними REST API, проектирование устойчивых механизмов обработки ошибок и ретраев
- Выявление и своевременное устранение багов
- Системы логирования, мониторинга и алертов
- Построение ETL-процессов и аналитических систем
- Поддержка и развитие существующих инструментов
- Самостоятельная декомпозиция бизнес-требований > ТЗ > архитектура > реализация
- Выявление и устранение багов, оптимизация производительности

Основной используемый стек: python 3.13, aiohttp, httpx, playwright, asyncio, aiogram, SQL (SQLAlchemy, PostgresSQL, SQLite), Docker


Результаты:
- Автоматизированы около 80% рутинной работы.
- Разработаны несколько многоуровневых систем аналитики данных.
- Спроектированы и реализованы 2 уникальных внутренних решения (которых вообще нет на рынке).
- Освобождено до 70 человеко-часов в месяц за счёт автоматизации.
- Снижено количество ошибок, связанных с человеческим фактором.
- Повышена скорость обработки данных и формирования аналитической отчётности.


=============================================================================
Вот мои навыки:
Python
FastAPI
Flask
REST API
asyncio
SQL
SQLite
SQLAlchemy
Docker
HTTPX
Python 3
API
gRPC
MySQL
PostgreSQL
Kubernetes
Redis
RabbitMQ
Apache Kafka
Git
Pytest
playwright
Celery
Linux
Bash
aiohttp
Микросервисная архитектура
Рефакторинг кода
Jupyter Notebook
NoSQL
=====================================================================
вот блок "обо мне":
Разработчик на Python с опытом проектирования API и серверной логики. Работал с FastAPI, асинхронным стеком (asyncio), интеграциями с внешними сервисами и реляционными базами данных.

Имею практический опыт:
- разработки и поддержки REST API
- построения асинхронных сервисов
- интеграции с внешними API
- парсинга данных и автоматизации бизнес-процессов


Активно применял и применяю в коммерческих проектах: Python 3.12+, FastAPI, Flask, asyncio, aiohttp, httpx, SQL (SQLAlchemy, PostgreSQL, SQLite), Alembic, Docker, Docker Compose, Git.

Изучал отдельно (+применял в пет проектах): Redis, Kafka, RabbitMQ, Celery, Kubernetes.

Дополнительно:
PyTest (API-тестирование), Playwright / Selenium (парсинг и end to end / UI-тесты), работа с REST API, асинхронная обработка задач, парсинг и обработка данных.

Быстро погружаюсь в новые проекты, самостоятельно довожу задачи до результата и ответственно подхожу к срокам.

Для связи:
tg @seukeolcode
email seukeolttyl@gmail.com
=============================================================================
Вот текст вакансии: {text}
============================================================================
Вот отдельно указанные теги вакансии: {skills}
    """

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {"role": "system", "content": '''Ты - эксперт по трудоустройству в IT сфере.'''},
            {"role": "user", "content": prompt}
        ]
    )

    return response.output[0].content[0].text


async def check_login(page):
    await page.wait_for_load_state("domcontentloaded", timeout=60000)
    count = await page.locator('a.supernova-button[data-qa="login"]').count()
    is_present = count > 0
    return not is_present


async def login(page):
    await page.locator('a.supernova-button[data-qa="login"]').click()
    await page.locator('[data-qa="submit-button"]').click()
    phone_number = input('Введите номер телефона (без +7): ')
    await page.wait_for_selector('input[data-qa="magritte-phone-input-national-number-input"]')
    await page.locator('input[data-qa="magritte-phone-input-national-number-input"]').fill(phone_number)
    await page.locator('button[data-qa="submit-button"]').click()

    await page.wait_for_selector('[data-qa="magritte-pincode-input-digit-0"]')
    await asyncio.sleep(30)
    return True


async def respond(page, url, message):
    try:
        await page.goto(url)
        await page.wait_for_load_state(
            'domcontentloaded',
            timeout=30000
        )
    except Exception as e:
        print('load_error', e)
        await asyncio.sleep(5)
        return False

    try:
        already_responded = page.locator('[data-qa="vacancy-response-link-top-again"]')
        await already_responded.wait_for(state="visible", timeout=3000)
        print('already_responded')
        return True
    except Exception:
        pass

    try:
        await page.locator('[data-qa="vacancy-response-link-top"]').first.click(timeout=3000)
    except Exception as e:
        print('response_error', e)
        return False

    try:
        relocation = page.locator('[data-qa="relocation-warning-confirm"]')
        await relocation.wait_for(state="visible", timeout=3000)
        await relocation.click(timeout=3000)
    except Exception:
        pass

    try:
        await page.wait_for_selector('[data-qa="add-cover-letter"]', timeout=3000)
        await page.locator('[data-qa="add-cover-letter"]').click(timeout=3000)
    except Exception as e:
        print('add_cover_letter_error', e)

    try:
        textarea = page.locator('[data-qa="vacancy-response-popup-form-letter-input"]')
        await textarea.wait_for(state="visible", timeout=3000)
        await textarea.click(timeout=3000)
        await textarea.fill(message)
    except Exception as e:
        print('type_letter_error', e)
        return False

    try:
        await page.locator('[data-qa="vacancy-response-submit-popup"]').click(timeout=3000)
    except Exception as e:
        print('click_respond_error', e)
        return False

    return True


async def responder():
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch(headless=False)
        page = await browser.new_page()
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.0.0 Safari/537.36",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Referer": "https://hh.ru/"
        })
        await page.goto("https://hh.ru", timeout=60000)
        is_logged_in = await check_login(page)
        if not is_logged_in:
            await login(page)
        df = pd.read_excel('vacancies.xlsx')
        for i, row in df.iterrows():
            if row['responded'] == 0 and row['letter']:
                is_responded = await respond(page, row['link'], row['letter'])
                if is_responded:
                    df.loc[i, 'responded'] = 1

        df.to_excel('vacancies.xlsx', index=False)
        await browser.close()