import xlwt
from decimal import Decimal
import traceback


def file(cat, period, name_):
    # name = (str(binascii.hexlify(os.urandom(20)))[2:42]) + ".xls"
    name = str(name_) + ".xls"
    wb = xlwt.Workbook()
    ws = wb.add_sheet('expenses')
    ws.write_merge(1, 1, 1, 4, 'покупки за ' + period)
    ws.write(2, 1, '№')  # строка столбец
    ws.write(2, 2, 'количество')
    ws.write(2, 3, 'коммент')
    ws.write(2, 4, "дата")
    i = 4
    for c in cat:
        ws.write(i, 1, c['id_expenses'])
        ws.write(i, 2, c['pay'])
        ws.write(i, 3, c['comment'])
        ws.write(i, 4, str(c['date']))
        i += 2
    wb.save('temps/{}'.format(name))
    return 'temps/{}'.format(name)
