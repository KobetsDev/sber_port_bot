
import xlsxwriter
from utils.mongo.user_class import User


async def create_table(file_path: str, participants: list[int] | list[dict]):
    '''Создаём Excel таблицу с переданными участниками или пользователями'''
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 30)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 10)
    worksheet.set_column('D:D', 15)
    if isinstance(participants[0], int):
        for index, user in enumerate(participants):
            user_info = await User(user).get_info()
            worksheet.write(f'A{index+1}', f"{user_info.get('last_name')} {user_info.get('first_name')} {user_info.get('patronymic')}")
            worksheet.write(f'B{index+1}', user_info.get('faculty'))
            worksheet.write(f'C{index+1}', user_info.get('group'))
            worksheet.write(f'D{index+1}', user_info.get('phone_number'))
    else:
        for index, user_info in enumerate(participants):
            worksheet.write(f'A{index+1}', f"{user_info.get('last_name')} {user_info.get('first_name')} {user_info.get('patronymic')}")
            worksheet.write(f'B{index+1}', user_info.get('faculty'))
            worksheet.write(f'C{index+1}', user_info.get('group'))
            worksheet.write(f'D{index+1}', user_info.get('phone_number'))
    workbook.close()
    return True
