# -*- coding: utf-8 -*-
"""
Created on Tue Oct 28 22:46:57 2014

@author: thtran89
"""
import sys
try:
    import numpy as np
except ImportError as errorMessage:
    sys.exit("%s\nThis program requires Numpy." % errorMessage)

"""This functions takes an input file as a command argument, validate it and exports a 9x9 matrix that represent a sudoku.
If any of the file and sudoku validations are not passed, the program would exit automatically."""
def ImportSudoku():
    try: 
        inputFileLocation=sys.argv[1]
        try:
            inputFile=open(inputFileLocation)
            try:
                sudoku=np.loadtxt(inputFile,dtype=int, delimiter=",")
                ValidateSudoku(sudoku)                
            except ValueError as errorMessage:
                sys.exit("The input file contains invalid characters. Valid characters are integers from 0-9.\n Details: %s" % errorMessage)
        except IOError:
            print "The input file is not found. Please check the file location." 
    except IndexError:
        print "No input file. Please enter the file location as an argument."

    return sudoku #When all of the validations pass, return sudoku


"""This function validates 2 criteria: 
- sudoku has 9 rows and 9 columns
- all numbers in the sudoku range from 0 to 9
"""
def ValidateSudoku(sudoku):
    if sudoku.shape!=(9,9):
        sys.exit("Sudoku dimensions are not valid. Valid dimesions are 9x9.")
    if not((sudoku<=9).all() and (sudoku>=0).all()):
        sys.exit("Sudoku contains invalid characters. Valid characters are integers from 0-9.")
  
"""This function takes a sudoku and export it to a csv file"""
def ExportSudoku(sudoku):
    np.savetxt("output.csv",sudoku,delimiter=",", fmt="%d")


"""This function takes an initial unsolved sudoku and try to solve it by recursive backtracking.
Look for an unassigned positions (value of 0) and get the coordinate of it
Loop through all digits from 1 to 9. 
If a digit is found wit no conflict, temporarily assign it to the position and recursively apply the function to fill it the rest of the unassigned ones.
If all digits have been tried and not worked out, return false and backtrack to previous point.
If the end result is true, the sudoku is solved"""
def SolveSudoku(sudoku,row=0,col=0):
    isUnassigned,row,col = FindUnassignedLocation(sudoku,row,col) #Find an unassigned location
    if not(isUnassigned):                                       #If there's no unassigned location, sudoku is solved
        return True      
    for num in range(1,10):                      #loop through all number from 1 to 9
        if (NoConflicts(sudoku,row,col,num)):    #If there's no conflict, temporarily asssign the number to the given coordinate
            sudoku[row][col]=num 
            if (SolveSudoku(sudoku,row,col)):   #recur
                return True                     #if success, sudoku is solved
            sudoku[row][col]= 0                 #if fail, undo it and try again
    return False #trigger backtracking 

"""This function looks for an unassigned coordinate in a 9x9 matrix
If found,stop looking, return the coordinate and a True value to isUnassigned flag
If not found, return the False value to isUassgined flag."""
def FindUnassignedLocation(sudoku, row, col):
    for row in range(9):
        for col in range(9):
            if sudoku[row][col]==0:
                return (True, row, col)
                break
    return (False,row,col)

"""This function checks to see the given number has any conflict in row, column, or box.
If the number is already assigned in the row, column, or box, return False.
Else return True"""
def NoConflicts(sudoku, row, col, num):
    return (not(UsedInRow(sudoku,row,num))) and (not(UsedInCol(sudoku,col,num)) and (not(UsedInBox(sudoku,row,col,num))))
  
"""This function checks to see the number has assigned in the given row of the sudoku. 
If it's already been used, return True. Otherwise, return False"""  
def UsedInRow(sudoku, row, num):
    for col in range(9):
        if sudoku[row][col]==num:
            return True
    return False

"""This function checks to see the number has assigned in the given column of the sudoku. 
If it's already been used, return True. Otherwise, return False"""      
def UsedInCol(sudoku, col, num):
    for row in range(9):
        if sudoku[row][col]==num:
            return True
    return False
 

"""This function checks to see the number has assigned in the given box of the sudoku. 
If it's already been used, return True. Otherwise, return False"""    
def UsedInBox(sudoku,row,col,num):
    BoxStartRow = 3*(row/3)     #Get the Coordinate of the Box's start row
    BoxEndRow   = BoxStartRow+3 #Get the Coordinate of the Box's end row
    BoxStartCol = 3*(col/3)     #Get the Coordinate of the Box's start column
    BoxEndCol   = BoxStartCol+3 #Get the Coordinate of the Box's end column
    for BoxRow in range(BoxStartRow,BoxEndRow):
        for BoxCol in range(BoxStartCol,BoxEndCol):
            if sudoku[BoxRow][BoxCol]==num:
                return True
    return False
  
def main():
    sudoku=ImportSudoku()   #Get the sudoku from file
    SolveSudoku(sudoku)     #solve it
    ExportSudoku(sudoku)   #export the solved sudoku to the output file
    
     
if __name__ == '__main__':
    main()

