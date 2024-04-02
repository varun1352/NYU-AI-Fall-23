import sys
import argparse
import copy
from collections import OrderedDict

def Assigner(Assignments):
    if None in Assignments.values():
        for key in Assignments.keys():
            if Assignments[key] == None:
                Assignments[key] = False
    return Assignments

def parseInput(board_values):
    board = [[0 for _ in range(9)] for _ in range(9)]
    
    for i in range(len(board_values)):
        row_number_value = int(board_values[i][0])
        coloumn_numberoumn_value = int(board_values[i][1])
        board[row_number_value - 1][coloumn_numberoumn_value - 1] = int(board_values[i][3])
    # error case to be added for out of bounds row_number and coloumn_numberumn indices and values 
    
    return board

def easySIngletonLiteral(Clauses):
    for Clause in Clauses:
        if len(Clause) == 1:
            return Clause[0]
    return []

def propagate(Literal, Clauses, Assignments):
    if Literal[0] == '!':
        Literal = Literal[1:]
        
    for i in range(len(Clauses)):
        #if the literal is true and the negation of that literal is present in a Clause
        if '!'+Literal in Clauses[i] and Assignments[Literal] == True:
            Clauses[i].remove('!'+Literal)
        # if the literal is true and is present in a Clause or it is false and its negation is present in a Clause
        elif (Literal in Clauses[i] and Assignments[Literal] == True) or ('!'+Literal in Clauses[i] and Assignments[Literal] == False):
            Clauses[i] = None
        # if the literal is False and is present in a clause, it is removed from the clause 
        elif Literal in Clauses[i] and Assignments[Literal] == False:
            Clauses[i].remove(Literal)
        
    TrueClauses = [Clause for Clause in Clauses if Clause != None]
    return TrueClauses

def sudokuConstraints(board):
    Clauses = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                Clause = 'n'+ str(board[i][j]) + '_r' + str(i+1) + '_c' + str(j+1)
                Clauses.append(Clause)
    # Clauses for not same value in the same place
    # for (1,1)
    for i in range(1,10): # row_number
        for j in range(1,10): # coloumn_numberoumn 
            for k in range(1, 10): # value 
                for l in range(k+1, 10): # new value 
                    Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(l) + '_r' + str(i) + '_c' + str(j)
                    Clauses.append(Clause)
                for m in range(j+1,10):
                    
                    Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i) + '_c' + str(m)
                    Clauses.append(Clause)
                for n in range(i+1, 10):
                    Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(n) + '_c' + str(j)
                    Clauses.append(Clause)
                
                if i % 3 == 1: # Clauses for the remaining squares in the same 3*3 box 
                    if j % 3 == 1:
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j+1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j+2)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+2) + '_c' + str(j+1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+2) + '_c' + str(j+2)
                        Clauses.append(Clause)
                    if j % 3 == 2:
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j-1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j+1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+2) + '_c' + str(j-1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+2) + '_c' + str(j+1)
                        Clauses.append(Clause)
                    if j % 3 == 0:
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j-2)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j-1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+2) + '_c' + str(j-2)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+2) + '_c' + str(j-1)
                        Clauses.append(Clause)
                
                if i % 3 == 2:
                    if j % 3 == 1:
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j+1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j+2)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j+1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j+2)
                        Clauses.append(Clause)
                    if j % 3 == 2:
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j-1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j+1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j-1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j+1)
                        Clauses.append(Clause)
                    if j % 3 == 0:
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j-2)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j-1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j-2)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i+1) + '_c' + str(j-1)
                        Clauses.append(Clause)
                
                if i % 3 == 0:
                    if j % 3 == 1:
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-2) + '_c' + str(j+1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-2) + '_c' + str(j+2)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j+1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j+2)
                        Clauses.append(Clause)
                    if j % 3 == 2:
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-2) + '_c' + str(j-1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-2) + '_c' + str(j+1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j-1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j+1)
                        Clauses.append(Clause)
                    if j % 3 == 0:
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-2) + '_c' + str(j-2)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-2) + '_c' + str(j-1)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j-2)
                        Clauses.append(Clause)
                        Clause = '!n' + str(k) + '_r' + str(i) + '_c' + str(j) + ' !n' + str(k) + '_r' + str(i-1) + '_c' + str(j-1)
                        Clauses.append(Clause)

            Clause = 'n1_r'+ str(i) +'_c' + str(j) + ' n2_r'+ str(i) +'_c' + str(j) + ' n3_r'+ str(i) +'_c' + str(j) + ' n4_r'+ str(i) +'_c' + str(j) + ' n5_r'+ str(i) +'_c' + str(j) + ' n6_r'+ str(i) +'_c' + str(j) + ' n7_r'+ str(i) +'_c' + str(j) + ' n8_r'+ str(i) +'_c' + str(j) + ' n9_r'+ str(i) +'_c' + str(j)   
            Clauses.append(Clause)
    Clauses_cnf_2d = []
    for i in Clauses:
        x = i.split(' ')
        Clauses_cnf_2d.append(x)
    
    return Clauses_cnf_2d
    
def easyPureLiteral(Clauses):
    dict = OrderedDict()
    for ClauseList in Clauses:
        for Clause in ClauseList:
            if Clause not in dict:
                dict[Clause] = 1
    PureLiteralList = list(dict.keys())
    for Clause in PureLiteralList:
        if Clause == 0:
            continue
        elif Clause[0] != '!':
            ClauseIndicator = PureLiteralList.index('!'+Clause)
            if ClauseIndicator != None:
                PureLiteralList[ClauseIndicator] = 0
            else:
                return Clause
        else:
            ClauseIndicator = PureLiteralList.index(Clause[1:])
            if ClauseIndicator != None:
                PureLiteralList[ClauseIndicator] = 0
            else:
                return Clause
            
def dpll(Clauses, Verbose = False):
    Values = OrderedDict()
    for row_number in range(1, 10):
        for coloumn_number in range(1, 10):
            for box_value in range(1, 10):
                Clause = f'n{box_value}_r{row_number}_c{coloumn_number}'
                Values[Clause] = None
    Answer = solver(Clauses, Values, Verbose)
    if Answer == None:
        print('Error: No assignment possible for the given question')
        sys.exit()
    else:
        if Verbose == True:
            print()
            print('-----Answer-----')
            for key in Answer.keys():
                print(key, Answer[key])
        return Answer

def solver(Clauses, Assignments, Verbose = False):
    while True:
        if [] in Clauses:
            return None    
            
        elif not Clauses:
            Assignments = Assigner(copy.deepcopy(Assignments))
            return Assignments
        
        elif easySIngletonLiteral(Clauses) != []:
            singleton = easySIngletonLiteral(Clauses)
            if singleton[0] == '!':
                Assignments[singleton[1:]] = False
            else:
                Assignments[singleton] = True
            Clauses = propagate(singleton, Clauses, Assignments)
            if Verbose == True:
                print('Easy Case found for a singleton literal:', singleton)
        
        elif easyPureLiteral(Clauses) != None:
            literal = easyPureLiteral(Clauses)
            if literal[0] == '!':
                Assignments[literal[1:]] = False
            else:
                Assignments[literal] = True
            for i in range(len(Clauses)):
                if literal in Clauses[i]:
                    Clauses[i] = None
            Clauses = [Clause for Clause in Clauses if Clause != None]
    
            if Verbose == True:
                print('Easy Case found for a pure Literal:', literal)
        else:
            break

    for key in Assignments.keys():
        if Assignments[key] == None:
            HardCaseLiteral = key
            break

    Assignments[HardCaseLiteral] = True
    if Verbose == True:
        print('Hard Case considered where', HardCaseLiteral,'is assigned True')
    TrueClauses = propagate(HardCaseLiteral, copy.deepcopy(Clauses), copy.deepcopy(Assignments))
    True_assn = solver(copy.deepcopy(TrueClauses), copy.deepcopy(Assignments), Verbose == True)
    if True_assn != None:
        return True_assn

    
    Assignments[HardCaseLiteral] = False
    if Verbose == True:
        print('Hard Case considered where', HardCaseLiteral,'is assigned False')
    forFalseClauses = propagate(HardCaseLiteral, copy.deepcopy(Clauses), copy.deepcopy(Assignments))
    return solver(copy.deepcopy(forFalseClauses), copy.deepcopy(Assignments), Verbose == True)

if __name__ =="__main__":
    Verbose = False
    parser = argparse.ArgumentParser(description='Sudoke solver using cnf and DPLL')
    parser.add_argument('values', nargs='+', help="Sudoku Assignments in the format 'rc=v'")
    parser.add_argument('-v', action='store_true', required=False, help='Optional flag for Verbose == True mode')
    args = parser.parse_args()
    Verbose = args.v    
    values = args.values
    board  = parseInput(values)
    Clauses = sudokuConstraints(board)
    Answer = dpll(Clauses, Verbose)
    board = [[0 for _ in range(9)] for _ in range(9)]

    for key in Answer.keys():
        if Answer[key] == True:
            box_value, row_number, coloumn_number = int(key[1]), int(key[4]), int(key[7]) 
            board[row_number-1][coloumn_number-1] = box_value
    print('-----The Solved Sudoku board should look like this -----')
    for i in board:
        print('  '.join(map(str, i)))
