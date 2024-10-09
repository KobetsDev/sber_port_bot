import calendar
from datetime import datetime

from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup)
from aiogram.utils.callback_data import CallbackData

# setting callback_data prefix and parts
calendar_callback = CallbackData('dialog_calendar', 'act', 'year', 'month', 'day', 'time')
ignore_callback = calendar_callback.new("IGNORE", -1, -1, -1, -1)  # for buttons with no answer


class DialogCalendar:
    months = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]
    time_mass = [
        "06-00", "06-30", "07-00", "07-30", "08-00", "08-30",
        "09-00", "09-30", "10-00", "10-30", "11-00", "11-30",
        "12-00", "12-30", "13-00", "13-30", "14-00", "14-30",
        "15-00", "15-30", "16-00", "16-30", "17-00", "17-30",
        "18-00", "18-30", "19-00", "19-30", "20-00", "20-30",
    ]

    def __init__(self, year: int = datetime.now().year, month: int = datetime.now().month):
        self.year = year
        self.month = month

    async def start_calendar(
        self,
        year: int = datetime.now().year
    ) -> InlineKeyboardMarkup:
        inline_kb = InlineKeyboardMarkup(row_width=5)
        # first row - years
        inline_kb.row()
        for value in range(year - 2, year + 3):
            inline_kb.insert(InlineKeyboardButton(
                value,
                callback_data=calendar_callback.new("SET-YEAR", value, -1, -1, -1)
            ))
        # nav buttons
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            '<<',
            callback_data=calendar_callback.new("PREV-YEARS", year, -1, -1, -1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            '>>',
            callback_data=calendar_callback.new("NEXT-YEARS", year, -1, -1, -1)
        ))

        return inline_kb

    async def _get_month_kb(self, year: int):
        inline_kb = InlineKeyboardMarkup(row_width=7)
        # first row with year button
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
        inline_kb.insert(InlineKeyboardButton(
            year,
            callback_data=calendar_callback.new("START", year, -1, -1, -1)
        ))
        inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
        # two rows with 6 months buttons
        inline_kb.row()
        for month in self.months[0:6]:
            inline_kb.insert(InlineKeyboardButton(
                month,
                callback_data=calendar_callback.new("SET-MONTH", year, self.months.index(month) + 1, -1, -1)
            ))
        inline_kb.row()
        for month in self.months[6:12]:
            inline_kb.insert(InlineKeyboardButton(
                month,
                callback_data=calendar_callback.new("SET-MONTH", year, self.months.index(month) + 1, -1, -1)
            ))
        return inline_kb

    async def _get_days_kb(self, year: int, month: int):
        inline_kb = InlineKeyboardMarkup(row_width=7)
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            year,
            callback_data=calendar_callback.new("START", year, -1, -1, -1)
        ))
        inline_kb.insert(InlineKeyboardButton(
            self.months[month - 1],
            callback_data=calendar_callback.new("SET-YEAR", year, -1, -1, -1)
        ))
        inline_kb.row()
        for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
            inline_kb.insert(InlineKeyboardButton(day, callback_data=ignore_callback))

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            inline_kb.row()
            for day in week:
                if (day == 0):
                    inline_kb.insert(InlineKeyboardButton(" ", callback_data=ignore_callback))
                    continue
                inline_kb.insert(InlineKeyboardButton(
                    str(day), callback_data=calendar_callback.new("SET-DAY", year, month, day, -1)
                ))
        return inline_kb

    async def _get_time_kb(self, year: int, month: int, day: int):
        inline_kb = InlineKeyboardMarkup(row_width=5)

        inline_kb.row()
        for time in self.time_mass:
            # print(time)
            inline_kb.insert(InlineKeyboardButton(time,
                                                  callback_data=calendar_callback.new("SET-TIME", year, month, day, time))
                             )
        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> tuple:
        return_data = (False, None)
        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
        if data['act'] == "SET-YEAR":
            await query.message.edit_reply_markup(await self._get_month_kb(int(data['year'])))
        if data['act'] == "PREV-YEARS":
            new_year = int(data['year']) - 5
            await query.message.edit_reply_markup(await self.start_calendar(new_year))
        if data['act'] == "NEXT-YEARS":
            new_year = int(data['year']) + 5
            await query.message.edit_reply_markup(await self.start_calendar(new_year))
        if data['act'] == "START":
            await query.message.edit_reply_markup(await self.start_calendar(int(data['year'])))
        if data['act'] == "SET-MONTH":
            await query.message.edit_reply_markup(await self._get_days_kb(int(data['year']), int(data['month'])))
        if data['act'] == "SET-DAY":
            await query.message.edit_reply_markup(await self._get_time_kb(
                int(data['year']), int(data['month']), int(data['day'])
            )
            )
        if data['act'] == "SET-TIME":
            await query.message.delete_reply_markup()   # removing inline keyboard
            return_data = True, datetime(
                int(data['year']),
                int(data['month']),
                int(data['day']),
                int(data['time'].split('-')[0]),  # hours
                int(data['time'].split('-')[1]),  # minutes
            )
        return return_data
