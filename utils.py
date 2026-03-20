from config import search, employment_forms, work_formats, items_on_page
import pandas as pd

async def get_link():
    employment_part = ''.join(f'&employment_form={i}' for i in employment_forms)
    work_format_part = ''.join(f'&work_format={i}' for i in work_formats)
    link = f'https://hh.ru/search/vacancy?text={search.replace(' ', '+')}&salary=&ored_clusters=true&experience=between1And3{employment_part}{work_format_part}&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&items_on_page={items_on_page}'
    return link


async def result_to_excel(data):
    df = pd.DataFrame(data)
    df.to_excel('vacancies.xlsx', index=False)
