import easyocr

def main():
    reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
    result = reader.readtext('test.png')
    print(result)

if __name__ == '__main__':
    main()
