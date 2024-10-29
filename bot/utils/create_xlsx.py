
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
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 15)
    worksheet.set_column('H:H', 15)
    worksheet.set_column('I:I', 15)
    worksheet.set_column('J:J', 15)
    worksheet.set_column('K:K', 15)
    worksheet.set_column('L:L', 15)

    for index, user_info in enumerate(participants):
        worksheet.write(f'A{index+1}', user_info.get('last_name'))
        worksheet.write(f'B{index+1}', user_info.get('first_name'))
        worksheet.write(f'C{index+1}', user_info.get('patronymic'))
        worksheet.write(f'D{index+1}', user_info.get('email'))
        worksheet.write(f'E{index+1}', user_info.get('university'))
        worksheet.write(f'F{index+1}', user_info.get('faculty'))
        worksheet.write(f'G{index+1}', user_info.get('course'))
        worksheet.write(f'H{index+1}', user_info.get('phone_number'))
        worksheet.write(f'I{index+1}', user_info.get('block1'))
        worksheet.write(f'J{index+1}', user_info.get('block2'))
        worksheet.write(f'K{index+1}', user_info.get('block3'))
        worksheet.write(f'L{index+1}', user_info.get('block4'))
    workbook.close()
    return True
