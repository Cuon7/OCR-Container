import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract'

def error_check(formatted_code):
    fixed_code = list(formatted_code)
    for i in range(4):
        if fixed_code[i] == '1':
            fixed_code[i] = 'I'
        if fixed_code[i] == '4':
            fixed_code[i] = 'A'
        if fixed_code[i] == '6':
            fixed_code[i] = 'G'
        if fixed_code[i] == '8':
            fixed_code[i] = 'B'
    for i in range(4, 9):
        if fixed_code[i] == 'I':
            fixed_code[i] = '1'
        if fixed_code[i] == 'A':
            fixed_code[i] = '4'
        if fixed_code[i] == 'G':
            fixed_code[i] = '6'
        if fixed_code[i] == 'B':
            fixed_code[i] = '8'
    if fixed_code[13] == '6':
        fixed_code[13] = 'G'
    if fixed_code[14] == 'I' or fixed_code[14] == '1':
        fixed_code[14] = '1'
    else:
        fixed_code[14] = '1'
    fixed_code = "".join(fixed_code)
    return fixed_code

def reformat_code(original_code):
    formatted_code = None
    n = len(original_code)
    formatted_code = original_code[0:n - 1] 
    formatted_code = formatted_code.replace(" ", "") 
    formatted_code = formatted_code.replace("\n", "")  
    return formatted_code

def build_tesseract_options(is_sidecode=False):
    alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    options = "--psm 3" 
    options += " --oem 3"
    options += " -c tessedit_char_whitelist={}".format(alphanumeric)
    options += " load_freq_dawg=false load_system_dawg=false"
    return options

def find_code(img):
    options = build_tesseract_options(False)
    result = pytesseract.image_to_string(img, config=options)
    result = reformat_code(result)
    result = error_check(result)
    return result
