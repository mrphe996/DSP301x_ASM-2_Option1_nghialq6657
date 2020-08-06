import re
import math
import numpy as np
import pandas as pd

# filename = input("Enter a class file to grade:")
filename = input("Enter a filename (i.e. class1 for class1.txt): ")

answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
answer_key = list(answer_key.strip().split(","))

try:
    f = open("E:\assignmen2_quang_luu.zip\Data Files\class1.txt")
except:
    print("File cannot be found.")
else:   
    print("Successfully opened class1.txt")
    lines = f.readlines()
    # Close the file
    f.close()

    # After getting data from the text file, analysis begins
    valid_data = []
    invalid_line = 0
    invalid_record = []
    
    print("***** ANALYZING *****")
    for line in lines:
        line = list(line.strip().split(","))
    
        # Check whether each line is valid
        student_id = line[0]
        pattern_id = "N\d{8}"
        check_id = re.search(pattern_id,student_id)
        if len(line) != 26:
            print("Invalid line of data: does not contain exactly 26 values:")
        if not(check_id):
            print("Invalid line of data: N# is invalid")
        if len(line) != 26 or not(check_id):
            print(','.join(line))
            invalid_line += 1
            line.extend(['invalid'])
        else:
            valid_data.append([i for i in line])
        
    if invalid_line == 0:
        print("No errors found!")
    print("\n***** REPORT *****")
    print(f"Total valid lines of date:", len(valid_data))
    print(f"Total invalid lines of data: {invalid_line}")
        
    score_table = []
    score_total = 0
    student_record = []
    
    # Calculate score for each student
    for record in valid_data:
        score_personal = 0
        
        for i in range(1,len(record),1):
            if record[i] == answer_key[i-1]:
                score_personal += 4
            elif record[i] == '':
                None
            else:
                score_personal -= 1
                
        score_table.append(score_personal)
        score_total += score_personal
        student_record.append([record[0],str(score_personal)])
    
    # Calculate statistical measure
    score_max = max(score_table)
    score_min = min(score_table)
    score_mean = score_total/len(score_table)
    score_range = score_max - score_min
    score_table_sorted = sorted(score_table)
    remainder = len(score_table_sorted) % 2
    quotient = len(score_table_sorted) / 2
    if remainder == 1:
        score_median = score_table_sorted[math.floor(quotient)]
    else:
        score_median = (score_table_sorted[int(quotient)] + \
                        score_table_sorted[int(quotient-1)]) / 2
    
    # Display statistical measure
    print("\n***** Result from Manual Calculation *****")
    print(f"Mean (average) score: {score_mean}")
    print(f"Highest score: {score_max}")
    print(f"Lowest score: {score_min}")
    print(f"Range of score: {score_range}")
    print(f"Median score: {score_median}")
    
    '''
        NUMPY SECTION
        Numpy is used to calculate statistic measures
    '''
    score_table = np.array(score_table)
    print("\n***** Result from Numpy *****")
    print(f"Mean (average) score: {np.mean(score_table)}")
    print(f"Highest score: {np.max(score_table)}")
    print(f"Lowest score: {np.min(score_table)}")
    print(f"Range of score: {np.max(score_table) - np.min(score_table)}")
    print(f"Median score: {np.median(score_table)}")
    
    
    ''' 
        PANDAS SECTION
        Pandas is used to alyze the data that was previously cleaned 
    '''
    db_raw = pd.DataFrame(np.array(valid_data))
    db_score = db_raw.drop(columns = 0)
    i = 0
        
    for column in db_score.columns:
        db_score[column] = db_score[column].map(lambda x: 4 if x == answer_key[i] else x)
        db_score[column] = db_score[column].map(lambda x: 0 if x == '' else x)
        db_score[column] = db_score[column].map(lambda x: -1 if (x != 4 and x != 0) else x)
        i += 1
    
    db_sum = db_score.apply(np.sum,axis=1)
    print("\n***** Result from Pandas *****")
    print(f"Mean (average) score: {db_sum.mean()}")
    print(f"Highest score: {db_sum.max()}")
    print(f"Lowest score: {db_sum.min()}")
    print(f"Range of score: {db_sum.max() - db_sum.min()}")
    print(f"Median score: {db_sum.median()}")
    
    
    # Save result to file
    save_file = filename + "_grade.txt"
    with open(save_file, 'w') as f:
        for line in student_record:
            f.write(','.join(line)+'\n')