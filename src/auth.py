# The auth handler for our app; responsible for handling user auth actions

def login_user(student_id):
  # Ensure student_id is the correct format
  # If valid, generate an OTP and send it to the user's email
  # If invalid, return an error response
  return

def validate_otp(student_id, otp):
  # Validate the OTP sent to the user's email
  # If valid, log the user in and return a success response
  # If invalid, return an error response
  return

def get_user_info(student_id):
  # Retrieve user information based on the student_id
  # Return user details if found, else return an error response
  return

def edit_user_info(student_id, new_info):
  # Update user information based on the student_id and new_info provided
  # Return a success response if updated, else return an error response
  return