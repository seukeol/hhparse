from config import search, employment_forms, work_formats, items_on_page, excluded_words
import pandas as pd
import os


async def get_link():
    employment_part = ''.join(f'&employment_form={i}' for i in employment_forms)
    work_format_part = ''.join(f'&work_format={i}' for i in work_formats)
    excluded_part = '&excluded_text='.join(f'{i}%2C+' for i in excluded_words)
    link = f'https://hh.ru/search/vacancy?text={search.replace(' ', '+')}{excluded_part}&salary=&ored_clusters=true&experience=between1And3{employment_part}{work_format_part}&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&items_on_page={items_on_page}'
    return link


async def result_to_excel(data):
    new_df = pd.DataFrame(data)
    file_path = 'vacancies.xlsx'
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path, engine="openpyxl")
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        first_col = combined_df.columns[0]
        combined_df = combined_df.drop_duplicates(subset=first_col, keep='first')
    else:
        combined_df = new_df
    combined_df.to_excel(file_path, index=False)
