import configparser
from openpyxl import Workbook
import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo
import SQLHandler

config = configparser.ConfigParser()
config.read("configurations.ini")

table_name = config["Database Information"]["Table"]

def setup():
    workbook = Workbook()
    sheet = workbook.active
    server_connection = SQLHandler.create_server_connection()

    return workbook, sheet, server_connection

def add_headers(server_connection, sheet):
    headers = list()

    for header in SQLHandler.get_headers(server_connection):
        headers.append(header['Field'])

    sheet.append(headers)
    return len(headers)

def add_rows(server_connection, sheet):

    for row in SQLHandler.get_all(server_connection):
        info = list()
        for header in SQLHandler.get_headers(server_connection):
            info.append(row[header["Field"]])
        sheet.append(info)

def create_table(server_connection, header_count):
    row_count = SQLHandler.get_row_count(server_connection)[0]['COUNT(*)']

    table = Table(displayName=f"{table_name}", ref=f"A1:{openpyxl.utils.get_column_letter(header_count)}{row_count}")

    style = TableStyleInfo(name=f"{table_name}", showFirstColumn=True,
                        showLastColumn=False, showRowStripes=True, showColumnStripes=True)
    table.tableStyleInfo = style
    return table

def save_file(sheet, table, workbook):
    sheet.add_table(table)
    workbook.save(f"/Users/brunogomespascotto/Downloads/{Table}.xlsx")

if __name__ == "__main__":
    workbook, sheet, server_connection = setup()
    header_count = add_headers(server_connection, sheet)
    add_rows(server_connection, sheet)
    table = create_table(server_connection, header_count)
    save_file(sheet, table, workbook)