from typing import List
from loguru import logger

def bin_search(input_data: int):
    logger.add("file1.log", rotation = "1 MB")
    input_list1 = [90, 7, 1, 5, 30, 10, 2, 4, 6, 8, 50]

    def sorting(l1: List) -> List:
        l1.sort()
        return l1

    #input_data = int(input("Enter the input number to search from the list: "))

    #input_data = 90

    #beginging of the binary search

    sorted_list = sorting (input_list1)

    middle_element = int(len(sorted_list) / 2) 
    start_pos = 0
    ending_pos = len(sorted_list) -1 
    position_found  = False

    try:
        while start_pos <= ending_pos:
            if (input_data == sorted_list[middle_element]):
                position_found = True
                break
            if (input_data > sorted_list[middle_element]):
                start_pos = middle_element + 1
                middle_element = start_pos + int((ending_pos - start_pos )/2)
                logger.info ("inside the second half: ", start_pos, ending_pos)
            else:
                ending_pos = middle_element -1
                middle_element = start_pos + int((ending_pos - start_pos )/2)
                logger.info ("inside the first half: ", start_pos, ending_pos)
    except Exception as e:
        logger.exception ("Error Occurred: ", e)
    
    if (position_found == False):
        middle_element = -1

    return (middle_element)




