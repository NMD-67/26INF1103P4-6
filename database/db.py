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

def get_row_numbers_by_column_name(worksheet, column_name, value):
    """
    Used to get all the rows where the column value matches the given value
    """
    headers = get_header_values(sheet=worksheet)
    if column_name not in headers:
        return {"success": False, "error": f"Column name {column_name} not found"}
    col_index = headers.index(column_name) + 1
    col_values = worksheet.col_values(col_index)

    matching_rows = [
        i + 1 for i, v in enumerate(col_values)
        if v == value and i != 0
    ]

    try:
      return {"success": True, "rows": matching_rows}
    except ValueError:
        return {"success": False, "error": f'Value {value} not found in column'}

def get_cell_value(worksheet, row_number, column_name):
    headers = get_header_values()
    if not column_name_exists(worksheet=worksheet, column_name=column_name):
        return {"success": False, "error": f"Column {column_name} doesn't exist"}

    col_index = headers.index(column_name) + 1
    value = worksheet.cell(row_number, col_index).value
    return {"success": True, "value": value}

def delete_row(worksheet: gspread.Worksheet, row_number):
    print(f'Deleting row {row_number} from {worksheet}')
    try:
        worksheet.delete_rows(row_number)
        return 200
    except Exception as e:
        print(f'An error occured deleting row: {e}')
        

def get_row_values(worksheet, row_numbers):
  """
  Returns an array of row value arrays
  """
  values = []
  for row_number in row_numbers:
    headers = get_header_values(worksheet)
    row_values = worksheet.row_values(row_number)

    row_values += [""] * (len(headers) - len(row_values))

    print(row_values)
    values.append(dict(zip(headers, row_values)))

  return values

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

def get_otp(student_id):
    try:
      user_row_number = get_row_numbers_by_column_name(otp_sheet, "student_id", student_id)
      print(f"User row number: {user_row_number}")
      if not user_row_number["success"]:
          return 500
      user_row = get_row_values(otp_sheet, user_row_number["rows"])
      if user_row is None or len(user_row) < 1:
          return 404
      print(user_row)
      return {"row_numbers": user_row_number["rows"], "otp": user_row[0]["otp"]}
    except Exception as e:
        print(f"An error occured when checking otp: {e}")
        return 500

def delete_otp(row_numbers):
  try:  
    print(f'Delting otp {row_numbers}')
    i = 0
    for row_number in row_numbers:
      print(f"Deleting otp row {row_number}")
      res = otp_sheet.delete_rows(row_number - i)
      i += 1
      print(res)
    return 200
  except Exception as e:
      print(f"Error deleting otp row {row_number}: {e}")
      return 500



# ---User Functions---
def get_user(student_id):
    print(f'Getting user: {student_id}')
    try:
        user = user_sheet.find(student_id)
        user_rows = get_row_values(user_sheet, [user.row])

        if len(user_rows) < 1:
            return {"success": False, "error": "User not found!", "status": 404}

        user = user_rows[0]
        return {"success": True, "user": user}
    except gspread.exceptions.CellNotFound:
        return {"success": False, "error": "User not found!"}

def add_user(**fields):
    """
    fields: any combination of column_name=value, e.g.
        add_user(student_id="676767", name="Alice", bio="hi")
    """
    if "student_id" not in fields:
        return 400
    try:
        headers = user_sheet.row_values(1)  # actual column order in the sheet
        row = [fields.get(h, "") for h in headers]  # build row matching sheet's real column order
        user_sheet.append_row(row)
        return 201
    except Exception as e:
        return 500

def update_user(student_details):
    try:
        student_id = student_details.get("student_id")
        print(f'Updating user: {student_details}')
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

def delete_user(student_id):
    try:  
      print(f"Deleting student {student_id}")
      row_number = get_row_numbers_by_column_name(user_sheet, "student_id", student_id)

      res = otp_sheet.delete_rows(row_number[0])
      print(res)
      return 200
    except Exception as e:
        print(f"Error deleting otp row {row_number}: {e}")
        return 500

# get_otp("2603197")
#get_row_values(otp_sheet, 2)
# get_user("2603197")