import OCR_Data_Analysis

def main():
    # get input string from the command line
    input_str = input("Enter search query: ")

    # call search function with input string
    OCR_Data_Analysis.search(input_str)

if __name__ == '__main__':
    main()