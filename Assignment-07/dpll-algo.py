"""
Mahesh Bharadwaj K
185001089

Assignment 07: DPLL
"""

import copy
import random

class Symbol(object):
    __slots__ = ['name', 'value', 'sign']

    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.sign = -1 if '\'' in str(self.name) else 1

    def evaluate(self):
        if self.value is None:
            return self.value

        if self.sign == -1:
            return not self.value
        return self.value

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        tmp_1 = str(self.name).replace('\'', '') 
        tmp_2 = str(other.name).replace('\'', '')
        return tmp_1 == tmp_2

    def __hash__(self):
        return hash(str(self.name).replace('\'', ''))

class Clause(object):
    __slots__ = ['symbols']

    def __init__(self, symbols):
        self.symbols = symbols[:]

    def evaluate(self):

        # Intial case and case when clause is not strictly true or false
        # When some symbols in clause are yet to be assigned,
        # None is returned
        rVal = None
        for symbol in self.symbols:
            eval = symbol.evaluate()
            if eval is not None: 

                # If a single symbol in a clause is true, the whole clause evalutes to true
                if  eval  == True:
                 return True
                else:
                    rVal = False
        return rVal

    def __str__(self):
        s = ', '.join([str(symbol) for symbol in self.symbols])
        s = '{ ' + s + ' }'

        return s

def find_pure_symbol(clauses, symbols, model):
    # print('Inside Pure Symbol\nSymbols: %s\nModel: %s' % (str(symbols), str(model)))
    sign_symbol = {symbol: 0 for symbol in symbols}
    for symbol in model.keys():
        sign_symbol[symbol] = 0
    
    # print(sign_symbol)

    for clause in clauses:
        for symbol in clause.symbols:
            
            # Ignore assigned symbols
            if symbol in model:
                continue
            
            # First time the sign is encountered in the formula
            if sign_symbol[symbol] == 0:
                sign_symbol[symbol] = symbol.sign

            # If already encountered, but the signs are different set arbitrary value
            elif sign_symbol[symbol] != symbol.sign:
                sign_symbol[symbol] = 100

    # Finding a symbol which is always 1 or -1
    for symbol in sign_symbol.keys():
        if sign_symbol[symbol] == 1:
            return symbol, True
        elif sign_symbol[symbol] == -1:
            return symbol, False

    # No pure symbol found
    return None, None

def find_unit_symbol(clauses, symbols, model):
    
    for clause in clauses:
        num_symbols = len(clause.symbols)
        count = 0
        
        # Initialising the symbol
        symbol_temp, value_temp = None, None
        for symbol in clause.symbols:
            symbol.value = model.get(symbol)

            # Find if symbol is yet to be assigned    
            if symbol.evaluate() is None:
                symbol_temp = Symbol(symbol.name.replace('\'', ''))
                
                # Assume symbol is positive ie A
                value_temp = True

                # If negative symbol ie A'
                if symbol_temp.evaluate() == False:
                    symbol_temp.value=False
                    
            # Track number of symbols in clause which evaluate to false        
            elif symbol.evaluate() == False:
                count += 1

        # If number of false clauses is exactly one less than number of clauses,
        # Unit symbol exists
        if count == num_symbols - 1 and symbol_temp is not None:
            return symbol_temp, value_temp

    return None, None

def evaluate(clauses, model):
    for clause in clauses:
        len_symbols = len(clause.symbols)
        for i in range(len_symbols):
            value = model.get(clause.symbols[i])
            clause.symbols[i].value = value if value is not None else clause.symbols[i].value
        
        # If a single clause is false, entire formula is false
        if clause.evaluate() == False :
            return False
        
        # If a single clause is None, entire formula is undetermined
        if clause.evaluate() is None:
            return None

    # Only if all clauses were true
    return True
        

def dpll(clauses, symbols, model):

    # Base case
    rVal = evaluate(clauses, model)
    if rVal == True:
        return model, True
    if rVal == False:
        return model, False
    
    P, value = find_pure_symbol(clauses, symbols, model)
    if P is not None:
        print('Pure symbol', P, 'found')
        new_clauses = clauses[:]
        new_symbols = copy.deepcopy(symbols)
        new_symbols.remove(Symbol(P, value))
        new_model = copy.deepcopy(model)
        new_model[Symbol(P, value)] = value 
        # print('Old Model: ', model, '\nNew Model: ', new_model)

        return dpll(new_clauses, new_symbols, new_model)

    P, value = find_unit_symbol(clauses, symbols, model)
    if P is not None:
        print('Unit symbol', P, 'found')
        new_clauses = clauses[:]
        new_symbols = copy.deepcopy(symbols)
        new_symbols.remove(Symbol(P, value))
        new_model = copy.deepcopy(model)
        new_model[Symbol(P, value)] = value 


        return dpll(new_clauses, new_symbols, new_model)

    # Picking an available symbol
    P = symbols.pop()

    new_clauses = clauses[:]
    new_symbols = symbols
    new_model_t = copy.deepcopy(model)
    new_model_t[P] = True
    new_model_f = copy.deepcopy(model)
    new_model_f[P] = False

    # print('new_model_t: ', new_model_t)
    # print('new_model_f: ', new_model_f)

    # Trying out with True assigned to picked symbol
    model_t, rval_t = dpll(new_clauses, new_symbols, new_model_t)
    if rval_t:
        return model_t, True 

    # Trying out with False assigned to picked symbol
    model_f, rval_f = dpll(new_clauses, new_symbols, new_model_f) 
    if rval_f:
        return model_f, True

    # No solution exists
    return model_t, False


def generate_formula():
    epsilon = 0.50
    num_clauses = random.randint(1, 4)
    bag_symbols = set()
    list_clauses = []
    for _ in range(num_clauses):
        num_symbols = random.randint(1, 4)
        
        list_symbols = []
        
        for __ in range(num_symbols):
            name = 'A' + str(random.randint(1, 5))
            bag_symbols.add(Symbol(name))
            
            # Randomly make some symbols negative with 50% chance
            if random.random() >= epsilon:
                name += '\''
            
            list_symbols.append(Symbol(name, value=None))

        list_clauses.append(Clause(list_symbols))

    return bag_symbols, list_clauses

def main():
    symbols, clauses = generate_formula()

    s = ', '.join([str(clause) for clause in clauses])
    s = '{' + s + '}'

    print('Formula is: ', s)

    model, solution = dpll(clauses, symbols, {})

    if solution is True:
        print('Solution found!')
        s = '{'
        for symbol in model.keys():
            s += '%s: %s, ' % (str(symbol), str(model[symbol]))
        s = s[:-2] + '}'
        print(s)
    else:
        print('No solution exists!')

if __name__ == "__main__":
    main()

"""
Sample Output:
➜ python3 dpll-algo.py
Formula is:  {{ A1', A3', A5 }, { A1, A1, A3', A5 }, { A2, A4', A2' }, { A4, A5', A2', A5 }}
Pure symbol A3 found
Solution found!
{A3: False, A5: True, A4: False}
"""
