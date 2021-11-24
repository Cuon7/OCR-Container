import json, os

def json_dump (res):
  containerString = res
# For more details
  # owner_Code = containerString[0:3]

  if (containerString[3] == "U"):
    productGroup_Code = "Container chở hàng"
  if (containerString[3] == "J"):
    productGroup_Code = "Thiết bị có thể tháo rời của container chở hàng"
  if (containerString[3] == "Z"):
    productGroup_Code = "Đầu kéo hoặc mooc"

# For more details
  # serial_Number = containerString[4:10]
  # check_Digit = containerString[10]
  # size_Code = containerString[11:13]
  # type_Code = containerString[13:15]

  reg_Code = containerString[0:10]

# For more details
  # x = {
  #   "Ownder Code": owner_Code,
  #   "Product Group Code": containerString[0:3] +": "+ productGroup_Code,
  #   "Registration Number": serial_Number,
  #   "Check digit": check_Digit,
  #   "Size Code": size_Code,
  #   "Type Code": type_Code
  # }

  x = { 
      "Code": reg_Code,   
      "Loại": productGroup_Code
      }
  

  if not os.path.exists("results.json"):
      with open("results.json", "w", encoding='utf-8') as f:
          f.write("[]")

  containers = json.load(open("results.json", encoding='utf-8'))
  existed = x in containers
  print(x)
  if (existed):
    print ("Already existed")
  if not (existed):
        containers.append(x)

  with open('results.json', 'w', encoding='utf-8') as file:
      json.dump(containers, file, ensure_ascii=False, indent=4)
