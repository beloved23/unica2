import xlwt
import xlrd
from datautils.helpers import get_attr
from datetime import datetime, date
from decimal import Decimal

STYLES = {'datetime': xlwt.easyxf(num_format_str='dd-mm-yyyy'),
          'decimal': xlwt.easyxf('font: bold on; pattern: pattern solid, fore-colour grey25', num_format_str='#,##0.00'),
          'default': xlwt.easyxf('alignment: wrap on',num_format_str='@'),
          'header': xlwt.easyxf('font: bold on; align: wrap off, horiz center;')}

def get_style(obj):
    if isinstance(obj, (datetime, date)): return STYLES['datetime']
    elif isinstance(obj, Decimal): return STYLES['decimal']
    else: return STYLES['default']

def export(qset, file_obj, include=None, exclude=['id']):
    '''
    file_obj can be a string or a file-like object (HttpResponse)
    '''
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sheet1')
    #field names
    field_names = filter(lambda x: x not in exclude, include or qset.model._meta.fields.get_all_field_names())
    #write headers
    for idx, fld_name in enumerate(field_names):
        ws.write(0, idx, fld_name.split('.')[-1].upper().replace('_',' '),
                STYLES['header'])
    #write rows
    for row, obj in enumerate(qset):
        for col, fld_name in enumerate(field_names):
            val = get_attr(obj, fld_name)
            style = get_style(val)
            #val, style = get_attr(obj, fld_name)
            ws.write(row+1, col, str(val), style)

    wb.save(file_obj)

def extract(file_content):
    '''
    Read the contents of an excel file

    Takes an open excel file
    Returns a list of dicts of {header: content}
    '''
    doc = xlrd.open_workbook(file_contents=file_content)
    sheet = doc.sheet_by_index(0)
    headers = [sheet.cell_value(0,i).upper() for i in range(sheet.ncols)]
    rows = []
    for row_idx in range(1, sheet.nrows):
        row = dict([(headers[col_idx], sheet.cell_value(row_idx, col_idx)) for col_idx in range(sheet.ncols)])
        rows.append(row)
    return rows

def export_list(object_list, file_obj, headers):
    '''
    Like export but for lists not querysets
    '''
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sheet1')
    #headers
    for idx, header in enumerate(headers):
        ws.write(0, idx, header.upper().replace('_', ' ').replace('.', ' '), STYLES['header'])
    #rows
    for row in range(len(object_list)):
        for col in range(len(headers)):
            val = object_list[row][col]
            if callable(val):
                val = val()
            ws.write(row+1, col, val, STYLES['default'])

    wb.save(file_obj)
