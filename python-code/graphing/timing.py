import json, time
from time import strftime
import os.path
import os
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from openpyxl import load_workbook

def save_time(my_time, type):
    save_date = time.strftime("%m-%d-%Y")
    path_to_json = "./graphing/"
    cwd = os.getcwd()
    excel_file = pd.read_excel('./graphing/timing.xlsx', sheet_name=type, index=None)
    update_flag = 0

    for i, row in excel_file.iterrows():
        if row['Date'] == save_date:
            # print("Previous runtime found for " + type)
            prev_time = row['Best Runtime']
            my_time = check_best_time(my_time, prev_time)
            excel_file.at[i,'Best Runtime'] = my_time
            update_flag = 1
            break
        else:
            continue

    if(update_flag == 0):
        print("Adding new runtime for " + type + " on " + save_date + " to spreadsheet...")
        sample_cell = [{'Date':save_date,'Best Runtime':my_time}]
        new_cell = pd.DataFrame(sample_cell)
        append_df_to_excel('./graphing/timing.xlsx', new_cell, type)

def check_best_time(new, prev):
    if(new < prev):
        print("New best runtime found! Updating spreadsheet...")
        return new
    else:
        # print("Previous runtime was better, tossing out new time...")
        return prev

def append_df_to_excel(filename, df, sheet_name, startrow=None, truncate_sheet=False, **to_excel_kwargs):
    if 'engine' in to_excel_kwargs:
        to_excel_kwargs.pop('engine')

    writer = pd.ExcelWriter(filename, engine='openpyxl')

    try:
        FileNotFoundError
    except NameError:
        FileNotFoundError = IOError

    try:
        # try to open an existing workbook
        writer.book = load_workbook(filename)

        # get the last row in the existing Excel sheet if it was not specified explicitly
        if startrow is None and sheet_name in writer.book.sheetnames:
            startrow = writer.book[sheet_name].max_row

        # truncate sheet
        if truncate_sheet and sheet_name in writer.book.sheetnames:
            idx = writer.book.sheetnames.index(sheet_name)
            writer.book.remove(writer.book.worksheets[idx])
            writer.book.create_sheet(sheet_name, idx)

        # copy existing sheets
        writer.sheets = {ws.title:ws for ws in writer.book.worksheets}
    except FileNotFoundError:
        pass

    if startrow is None:
        startrow = 0

    # write and save
    df.to_excel(writer, sheet_name, startrow=startrow, header=None, index=None, **to_excel_kwargs)
    writer.save()

def main():
    data = []
    print(data)

if __name__ == '__main__':
    main()
