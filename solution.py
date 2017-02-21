assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
row_units = []
column_units = []
square_units = []
units = {}
unitlist = []
peers = {}
boxes = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        print(box,value)
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for u in unitlist:
        # Find all instances of naked twins
        possible_twins_b = [ box for box in u if len(values[box]) == 2]
        possible_twins_v = [ values[box] for box in u if len(values[box]) == 2]
        
        twins = {}

        for t in zip(possible_twins_b,possible_twins_v):
            if(possible_twins_v.count(t[1]) == 2): 
                if t[1] in twins: twins[t[1]].append(t[0])
                else: twins[t[1]] = [t[0]]
        print(twins)
        
        # Eliminate the naked twins as possibilities for their peers    
        print(u)
        print("=============================")
        for t in twins.keys():
            print(twins[t])
            print("------------------")
            for b in u: 
                if(b not in t[1]):
                    print(b)
        print("+++++++++++++++++++++++++++++++")
    
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    global boxes
    boxes = cross(rows, cols)
    grid = dict(zip(boxes, grid))
    for key,values in zip(grid.keys(), grid.values()):
        if values == '.':
           grid[key] = '123456789'
    return grid

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for key in values.keys():
        if len(values[key]) == 1:
            for key2 in peers[key]:
                values[key2] = values[key2].replace(values[key],'')
    return values

def only_choice(values):
    for unit in unitlist:
        for c in ["1","2","3","4","5","6","7","8","9"]:
            pos = [box for box in unit if c in values[box]]
            if(len(pos) == 1):
                values[pos[0]] = c
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if(values == False):
        return False
    poss = [ box for box in values.keys() if len(values[box]) == 1]
    if(len(poss) == 81):
        return values
    
    # Choose one of the unfilled squares with the fewest possibilities
    poss = [ [box,len(values[box])] for box in values.keys() if len(values[box]) > 1]
    poss_s = sorted(poss, key=lambda poss: poss[1])
    root_index = poss_s[0]
    root = values[root_index[0]]
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for c in root:
        new_values = dict(values)
        new_values[root_index[0]] = c
        res = search(new_values)
        if (res):
            return res

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    global row_units, column_units, square_units, unitlist, units, peers
    
    values = grid_values(grid)
    
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    unitlist = row_units + column_units + square_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    values = search(values)
    
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
