import os
from db_utils import does_exists, delete_target, get_status


# Should be replaced with the real path to db
DB_PATH = r'/home/cluster/orelhaz/bin/rom_deshe/djangonautic/db.sqlite3'



# Happy case for adding query
def check_add_happy():
  code = os.system("python3 db_utils.py ADD romimo ABCDEFG RUNNING > /dev/null")
  if code != 0:
    print("1: TEST FAILED")
    return False
  ans = does_exists("romimo")
  if not ans:
    print("1: TEST FAILED")
    return False
  ans = delete_target("romimo")
  if not ans:
    print("1: TEST FAILED")
    return False
  print("1: TEST SUCCEED")
  return True

# Sad case for adding query - bad parameters are given
def check_add_bad():
  code = os.system("python3 db_utils.py romimo ABCDEFG RUNNING > /dev/null")
  if code == 0:
    print("2: TEST FAILED")
    return False
  print("2: TEST SUCCEED")
  return True

# Happy case for updating query
def check_update_happy():
  code = os.system("python3 db_utils.py ADD romimo ABCDEFG RUNNING > /dev/null")
  if code != 0:
    print("3: TEST FAILED")
    return False
  code = os.system("python3 db_utils.py UPDATE romimo some_log_msg RUNNING > /dev/null")
  if code != 0:
    print("3: TEST FAILED")
    return False
  ans = delete_target("romimo")
  if not ans:
    print("3: TEST FAILED")
    return False
  print("3: TEST SUCCEED")
  return True

# Sad case for updating query - target doesnt exists  
def check_update_sad():
  code = os.system("python3 db_utils.py UPDATE romimo_not_here some_log_msg RUNNING > /dev/null")
  if code == 0:
    print("4: TEST FAILED")
    return False
  print("4: TEST SUCCEED")
  return True

# Happy case for updating query - updating the status of the query
def check_update_status(status, test_num):
  code = os.system("python3 db_utils.py ADD romimo ABCDEFG RUNNING > /dev/null")
  if code != 0:
    print(test_num + ": TEST FAILED3")
    return False
  code = os.system("python3 db_utils.py UPDATE romimo some_log_msg " + status + " > /dev/null")
  if code != 0:
    print(test_num + ": TEST FAILED4")
    return False
  if status == "RUNNING": status = "Running"
  if status == "FAILED": status = "Failed"
  if status == "DONE": status = "Success"
  if get_status("romimo") != status:
    return False
  ans = delete_target("romimo")
  if not ans:
    print(test_num + ": TEST FAILED2")
    return False
  print(test_num + ": TEST SUCCEED")
  return True

# Sad case for updating query - adding query with the same target name  
def check_add_same_target():
  code = os.system("python3 db_utils.py ADD romimo ABCDEFG RUNNING > /dev/null")
  if code != 0:
    print("8: TEST FAILED")
    return False
  code = os.system("python3 db_utils.py ADD romimo ABCDEFG RUNNING > /dev/null")
  if code == 0:
    print("8: TEST FAILED")
    return False
  ans = delete_target("romimo")
  if not ans:
    print("8: TEST FAILED")
    return False
  print("8: TEST SUCCEED")
  return True
  
  
  
def main():
  count_T = 0
  if check_add_happy(): count_T += 1
  if check_add_bad(): count_T += 1
  if check_update_happy(): count_T += 1
  if check_update_sad(): count_T += 1
  if check_update_status("RUNNING", "5"): count_T += 1
  if check_update_status("DONE", "6"): count_T += 1
  if check_update_status("FAILED","7"): count_T += 1
  if check_add_same_target(): count_T += 1
  print("Succeed:", count_T, " ||| Failed:", 8 - count_T)

  
if __name__ == "__main__":
  main()

