import gspread
from google.oauth2.service_account import Credentials
import os
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "service_account.json")

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
client = gspread.authorize(creds)

sheet = client.open("SITogether")
user_sheet = sheet.worksheet("users")
otp_sheet = sheet.worksheet("otp")

def get_header_values(sheet):
    headers = sheet.row_values(1)
    return headers

def column_name_exists(worksheet, column_name):
    headers = get_header_values(worksheet)
    if column_name not in headers:
        return False
    else:
        return True

def get_row_number_by_column_name(worksheet, column_name, value):
    headers = get_header_values(sheet=worksheet)
    if column_name not in headers:
        return {"success": False, "error": f"Column name {column_name} not found"}
    col_index = headers.index(column_name) + 1
    col_values = worksheet.col_values(col_index)

    try:
      row_number = col_values.index(value) + 1
      return {"success": True, "row": row_number}
    except ValueError:
        return {"success": False, "error": f'Value {value} not found in column'}

def get_cell_value(worksheet, row_number, column_name):
    headers = get_header_values()
    if not column_name_exists(worksheet=worksheet, column_name=column_name):
        return {"success": False, "error": f"Column {column_name} doesn't exist"}

    col_index = headers.index(column_name) + 1
    value = worksheet.cell(row_number, col_index).value
    return {"success": True, "value": value}

def get_row_value(worksheet, row_number):
    headers = get_header_values(worksheet)
    row_values = worksheet.row_values(row_number)

    row_values += [""] * (len(headers) - len(row_values))

    return dict(zip(headers, row_values))

# ---OTP Functions---
def upload_otp(student_id, otp):
    try:
      current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      row = [student_id, otp, current_datetime]
      otp_sheet.append_row(row)
      return 200
    except Exception as e:
        print(f"An error occured when creating otp: {e}")
        return 500

def check_otp(student_id):
    try:
      user = otp_sheet.find(student_id)
      print(user.row)
      if user is None:
          return 404
      return user
    except Exception as e:
        print(f"An error occured when checking otp: {e}")
        return 500

def delete_otp(row_number):
    print(f"Deleting otp row {row_number}")
    try:
      res = otp_sheet.delete_rows(row_number)
      print(res)
      return 200
    except Exception as e:
        print(f"Error deleting otp row {row_number}")
        return 500



# ---User Functions---
async def get_user(student_id):
    try:
        user = await user_sheet.find(student_id)
        return user
    except gspread.exceptions.CellNotFound:
        return None

def add_user(**fields):
    """
    fields: any combination of column_name=value, e.g.
        add_user(student_id="676767", name="Alice", bio="hi")
    """
    if "student_id" not in fields or "name" not in fields:
        return 400
    try:
        headers = user_sheet.row_values(1)  # actual column order in the sheet
        row = [fields.get(h, "") for h in headers]  # build row matching sheet's real column order
        user_sheet.append_row(row)
        return 200
    except Exception as e:
        return 500

def update_user(student_details):
    try:
        student_id = student_details.get("student_id")
        original_user = get_user(student_id)
        if original_user is not None:
            for key, value in student_details.items():
                if key != "student_id":
                    user_sheet.update_cell(original_user.row, original_user.col + list(student_details.keys()).index(key), value)
            return 200  # User updated successfully
        else:
            print(f"User with student_id {student_id} not found.")
            return 404  # User not found
    except gspread.exceptions.APIError as e:
        print(f"API error while updating user: {e}")
        return 500  # API error
    except gspread.exceptions.CellNotFound:
        print(f"Cell not found while updating user with student_id {student_id}.")
        return 404  # User not found
    except gspread.exceptions.WorksheetNotFound:
        print(f"Worksheet not found while updating user with student_id {student_id}.")
        return 404  # User not found
    except gspread.exceptions.RequestError as e:
        print(f"Request error while updating user: {e}")
        return 500  # Request error
    except Exception as e:
        print(f"Error updating user: {e}")
    return 500