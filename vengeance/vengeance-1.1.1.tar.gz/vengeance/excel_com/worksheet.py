
from datetime import date
from datetime import datetime

# noinspection PyUnresolvedReferences
from pythoncom import com_error as pythoncom_error

from .excel_constants import *
from .workbook import excel_application_to_foreground

from ..excel_com.excel_address import col_letter
from ..excel_com.excel_address import col_number
from ..excel_com.excel_address import max_cols as excel_max_cols
from ..excel_com.excel_address import max_rows as excel_max_rows

from ..util.iter import iterator_to_list
from ..util.iter import modify_iteration_depth
from ..util.iter import is_exhaustable


def get_worksheet(wb,
                  ws,
                  *,
                  clear_filter=False,
                  activate=False):

    if is_worksheet_instance(ws):
        return ws

    if wb is None:
        raise AssertionError("Excel workbook has not been set, cannot retrieve worksheet: '{}'".format(ws))

    try:
        ws = wb.Sheets[ws]
    except pythoncom_error as e:
        raise NameError("'{}' worksheet not found in '{}'".format(ws, wb.Name)) from e

    # if chart that has been moved to its own worksheet, these calls will fail
    # if ws.__class__.__name__ != '_Worksheet':

    if clear_filter:
        clear_worksheet_filter(ws)

    if activate:
        ws.Visible = True
        excel_application_to_foreground(ws.Application)
        ws.Activate()

    return ws


def is_worksheet_instance(o):
    return o.__class__.__name__ in ('CDispatch', '_Worksheet')


def first_row(excel_range, default=1):

    search = range_find(excel_range,
                        what='*',
                        look_at=xlPart,
                        search_order=xlByRows,
                        search_direction=xlNext)

    if search:
        r = max(search.Row, default)
    else:
        r = default

    return int(r)


def last_row(excel_range, default=1):

    search = range_find(excel_range,
                        what='*',
                        look_at=xlPart,
                        search_order=xlByRows,
                        search_direction=xlPrevious)

    if search:
        r = max(search.Row, default)
    else:
        r = default

    return int(r)


def first_col(excel_range, default='A'):

    search = range_find(excel_range,
                        what='*',
                        look_at=xlPart,
                        search_order=xlByColumns,
                        search_direction=xlNext)

    if search:
        c = max(search.Column, col_number(default))
    else:
        c = default

    return col_letter(c)


def last_col(excel_range, default='A'):

    search = range_find(excel_range,
                        what='*',
                        look_at=xlPart,
                        search_order=xlByColumns,
                        search_direction=xlPrevious)

    if search:
        c = max(search.Column, col_number(default))
    else:
        c = default

    return col_letter(c)


def range_find(excel_range,
               what,
               after=None,
               look_in=xlValues,
               look_at=xlWhole,
               search_order=xlByRows,
               search_direction=xlPrevious,
               match_case=False):

    if after is None:
        if search_direction == xlNext:
            after = last_cell(excel_range)
        elif search_direction == xlPrevious:
            after = first_cell(excel_range)

    search = excel_range.Find(what,
                              after,
                              look_in,
                              look_at,
                              search_order,
                              search_direction,
                              match_case)

    return search


def first_cell(excel_range):
    return excel_range.Cells(1)


def last_cell(excel_range):
    """
    excel_range.Cells(excel_range.Cells.Count) is not always reliable
    and can cause an overflow error, but when excel_range.Address
    only provides row address, something like '$1:$20', this method must be used

    # '$1:$20' = excel_range.Address
    # excel_range.Parent.Rows(a)
    """
    try:
        a = excel_range.Address.split(':')[-1]
        return excel_range.Parent.Range(a)
    except pythoncom_error:
        return excel_range.Cells(excel_range.Cells.Count)


def is_filtered(ws):
    return (ws.AutoFilter is not None) and bool(ws.AutoFilter.FilterMode)


# noinspection PyProtectedMember
def clear_worksheet_filter(ws):
    if is_filtered(ws):
        ws._AutoFilter.ShowAllData()


def is_range_empty(excel_range):
    num_blank = excel_range.Application.WorksheetFunction.CountBlank(excel_range)
    num_cells = excel_range.Cells.Count

    return num_blank == num_cells


def activate_worksheet(ws):
    excel_application_to_foreground(ws.Application)

    ws.Parent.Activate()

    ws.Visible = True
    ws.Activate()


def write_to_excel_range(v, excel_range):
    m = validate_matrix_within_max_worksheet_dimensions(v)
    m = list(convert_python_types(m))

    num_cols = len(m[0])
    num_rows = len(m)
    excel_range_dest = excel_range.Resize(num_rows, num_cols)

    excel_range.Parent.Range(excel_range, excel_range_dest).Value = m


def escape_excel_range_errors(excel_range):
    m = excel_range.Value
    m = modify_iteration_depth(m, 2)
    m = [list(row) for row in m]

    try:
        range_errors = excel_range.SpecialCells(xlCellTypeFormulas, xlErrors)
        cell = first_cell(excel_range)
        r_0  = cell.Row
        c_0  = cell.Column

        for cell_error in range_errors:
            r = cell_error.Row    - r_0
            c = cell_error.Column - c_0
            m[r][c] = excel_errors.get(m[r][c], 'unknown error')

    except pythoncom_error:
        pass

    return m


def convert_python_types(m):
    """ convert python types so they are compatible with Excel

    for each row in matrix:
        for each value in row:
            convert datetime.date to datetime.datetime (pywintypes time?)
            convert non-primitives to repr()
    """
    # region {closure function}
    NoneType = type(None)

    def convert_excel_value(v):
        if isinstance(v, (NoneType, bool, int, float, str)):
            _v_ = v
        elif isinstance(v, date):
            _v_ = datetime(v.year, v.month, v.day)
        else:
            _v_ = repr(v)

        return _v_
    # endregion

    if is_exhaustable(m):
        # m = iterator_to_list(m)
        # m = modify_iteration_depth(m, depth=2)
        raise TypeError('matrix must be a list of lists, not a generator')

    max_cols = len(m[0])

    for i, row in enumerate(m):
        if (max_cols - len(row)) != 0:
            raise ValueError('cannot write to Excel worksheet, jagged columns at row {:,}\n\t'.format(i))

        yield tuple(convert_excel_value(v) for v in row)


def validate_matrix_within_max_worksheet_dimensions(v):
    """ ensure matrix fits within Excel's column and row maximum """
    m = iterator_to_list(v)
    m = modify_iteration_depth(m, depth=2)

    num_rows = len(m)
    num_cols = max(map(len, m))

    if num_rows > excel_max_rows:
        raise ValueError("number of rows in matrix ({:,}) exceeds Excel's row limit ({:,})"
                         .format(num_rows, excel_max_rows))

    if num_cols > excel_max_cols:
        raise ValueError("number of columns in matrix ({:,}) exceeds Excel's column limit({:,})"
                         "(did you mean to transpose this matrix first?)"
                         .format(num_cols, excel_max_cols))

    return m


def parse_range(excel_range):
    c_1 = first_cell(excel_range).Column
    c_1 = col_letter(c_1)

    c_2 = last_cell(excel_range).Column
    c_2 = col_letter(c_2)

    r_1 = first_cell(excel_range).Row
    r_2 = last_cell(excel_range).Row

    return c_1, r_1, c_2, r_2

