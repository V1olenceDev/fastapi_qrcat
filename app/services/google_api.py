from datetime import datetime

from aiogoogle import Aiogoogle


FORMAT = "%Y/%m/%d %H:%M:%S"
TABLE_HEADER = [
    ['Отчет от', datetime.now().strftime(FORMAT)],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


def create_spreadsheet_body(title: str, locale: str = 'ru_RU', row_count: int = 100, column_count: int = 11) -> dict:
    """Создание тела запроса для создания таблицы."""
    return {
        'properties': {'title': title, 'locale': locale},
        'sheets': [{'properties': {'sheetType': 'GRID', 'sheetId': 0, 'title': 'Лист1',
                                   'gridProperties': {'rowCount': row_count, 'columnCount': column_count}}}]
    }


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создание таблицы в Google Sheets."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = create_spreadsheet_body(f'Отчет на {now_date_time}')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body))
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str, wrapper_services: Aiogoogle, email: str) -> None:
    """Установка прав доступа к таблице для пользователя."""
    permissions_body = {'type': 'user', 'role': 'writer', 'emailAddress': email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields="id"))


async def spreadsheets_update_value(
        spreadsheetid: str, projects: list, wrapper_services: Aiogoogle) -> None:
    """Обновление значений в таблице."""
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = TABLE_HEADER.copy()  # Создаем копию заголовка таблицы
    for res in projects:
        new_row = [res['name'], str(res['delta']), res['description']]
        table_values.append(new_row)

    # Проверяем, что данные поместятся в созданную таблицу
    max_rows = 100  # Максимальное количество строк в таблице
    max_columns = 11  # Максимальное количество столбцов в таблице
    if len(table_values) > max_rows:
        raise ValueError(f"Слишком много строк данных ({len(table_values)}), максимальное количество: {max_rows}")

    for row in table_values:
        if len(row) > max_columns:
            raise ValueError(f"Слишком много столбцов данных ({len(row)}), максимальное количество: {max_columns}")

    update_body = {'majorDimension': 'ROWS', 'values': table_values}
    range_ = f'A1:E{len(table_values)}'  # Используем R-нотацию для указания диапазона
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=range_,
            valueInputOption='USER_ENTERED',
            json=update_body))
