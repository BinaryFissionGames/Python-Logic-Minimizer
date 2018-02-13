'''
#TODO implement a method to find the minimal hazard-free implementation.

This program uses the Quine-McCluskey algorithm with 
Petrick's method to find the minimum sum of products solutions.
Read more here:
https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm
https://en.wikipedia.org/wiki/Petrick%27s_method
'''
class Implicant:
    '''Represents a single Implicant'''
    ''' 
    This string tells what the binary representation is.
    It's actually more of a 'ternary' representation, since -
    may be in the string
    '''
    binrep = ""
    '''
    Tells what "size" the prime implicant is.
    The size is 2^order (order 1 is a size 1 implicant (just a simple minterm), 
    order 2 is a size 2 implicant, etc.)
    '''
    order = 0
    '''
    Minterms that said implicants are made up of.
    '''
    terms = []

    def __init__(self, binrepsize, terms, implicant1 = None, implicant2 = None):
        '''
        Pretty self explanatory, an implicant of order n is made of 2 implicants
        of order n-1, except for order 0 implicants, which are simply just a single
        term. Terms may be an empty list if 2 implicants are provided.
        '''
        self.binrep = ""
        self.order = 0
        self.terms = []

        if implicant1 == None and implicant2 == None:
            self.binrep = bin(terms[0])[2:]
            if len(self.binrep) != binrepsize:
                #Zero extend binrep
                while len(self.binrep) < binrepsize:
                    self.binrep = "0" + self.binrep
                
            self.terms = terms
        else:
            if implicant1 == None or implicant2 == None:
                print("Error: An implicant is uninitialized!")
            else:
                if implicant1.order != implicant2.order:
                    print("Error: 2 implicants of varying order were provided!")
                else:
                    distance = 0
                    self.order = implicant1.order + 1
                    self.terms = list(implicant1.terms + implicant2.terms)
                    #Mask different symbols in binrep with -. Has error checking for distance >= 2
                    for i in range(0, binrepsize):
                        if implicant1.binrep[i] != implicant2.binrep[i]:
                            self.binrep = self.binrep + "-"
                            distance += 1
                        else:
                            self.binrep = self.binrep + implicant1.binrep[i]
                    if distance > 1:
                        print("Error: Implicants had distance greater than 1!")

    def getWeight(self):
        '''
        Basically, just gets the number of 1's in the binary representation of
        said term. 
        '''
        numOnes = 0
        for c in self.binrep:
            if c == '1':
                numOnes += 1
        return numOnes
    
    def getHyphenWeight(self):
        '''
        Returns the number of non-hyphen characters in the binary representation
        '''
        weight = 0
        for c in self.binrep:
            if c != "-":
                weight += 1
        return weight

    def getDistance(self, otherTerm):
        '''
        Gets the number of different places in the 2 terms.
        '''
        difference = 0
        for i in range(0, len(self.binrep)):
            if(self.binrep[i] != otherTerm.binrep[i]):
                difference += 1
        return difference
    
    def GetAsString(self, literalStrings):
        '''
        Gets the implicant as a string, using the list
        of strings literalStrings as the literals
        '''
        implicantString = ""
        for index, c in enumerate(self.binrep):
            if c == "0":
                implicantString += literalStrings[index] + "'"
            elif c == "1":
                implicantString += literalStrings[index]
        return implicantString
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.binrep == other.binrep

    def __hash__(self):
        return self.binrep.__hash__()

class Product:
    
    def __init__(self):
        #Marks whether this is a product of sums or not.
        self.isPOS = True
        self.elements = set()
    
    def LiteralWeight(self):
        weight = 0
        for elem in self.elements:
            weight += elem.getHyphenWeight()
        return weight 

    def Distribute(self):
        if not self.isPOS:
            print("Can't distribute non product of sum term!")
            return
        if len(self.elements) <= 1:
            print("Can't distribute one term!")

        first = self.elements.pop()
        second = self.elements.pop()
        second.Multiply(first)
        self.elements.add(second)
        

    def CanDistribute(self):
        return len(self.elements) > 1 and self.isPOS

    def GetAsSum(self):
        while len(self.elements) > 1:
            self.Distribute()
        return self.elements.pop()
    
    def __hash__(self):
        hash = 0
        for elem in self.elements:
            hash ^= elem.__hash__()
        return hash
        
    def __eq__(self, other):
       return self.elements <= other.elements

class Sum:
    #marks whether this is a sum of products or not
    isSOP = True
    elements = set()

    def __init__(self):
        self.isSOP = True
        self.elements = set()

    def Multiply(self, other):
        self.TransformToSOP()
        other.TransformToSOP()
        
        newElems = set()
        while len(self.elements) > 0:
            myProd = self.elements.pop()
            for otherProduct in other.elements:
                newProd = Product()
                newProd.elements.update(myProd.elements)
                newProd.elements.update(otherProduct.elements)
                newElems.add(newProd)
        
        self.elements = newElems

    def TransformToSOP(self):
        if self.isSOP:
            return
        newElements = set()
        while len(self.elements) > 0:
            prod = Product()
            elem = self.elements.pop()
            prod.elements.add(elem)
            newElements.add(prod)
        self.elements = newElements
        self.isSOP = True

    def ApplyCovering(self):
        if self.isSOP:
            newSet = set()
            oldSet = self.elements.copy()
            '''
            Works because if there was a better (minimal) elem before it,
            It will already be removed, and therefore there is a contradiciton.
            If the better one is after it, it will be removed when we get to it.
            O(n^2)
            '''
            while len(oldSet) > 0:
                elem = oldSet.pop()
                for prod in self.elements:
                    if elem.elements <= prod.elements:
                        if prod in oldSet:
                            oldSet.remove(prod)
                        if prod in newSet:
                            newSet.remove(prod)
                newSet.add(elem)
            self.elements = newSet 


    def __hash__(self):
        hash = 0
        for elem in self.elements:
            hash ^= elem.__hash__()
        return hash

    def __eq__(self, other):
       return self.elements <= other.elements

def GetPrimeImplicants(minterms):
    '''
    Takes in the minterms, which is a list of order 0 implicants, and returns a list of
    prime implicants of varying orders.
    This basically applies step 1 of the Quine-McCluskey Algorithm
    '''
    primeImplicants = set()
    curImplicants = set()
    nextImplicants = set(minterms)
    combined = dict()

    while len(nextImplicants) > 0:
        curImplicants = nextImplicants
        nextImplicants = set()
        
        for implicant in curImplicants:
            combined[implicant] = False
        #Sort by weight, since 2 implicants can only be combined when the distance between them is 1 
        # (weight(i1) - weight(i2) <= distance(i1, i2) is the relation)
        #curImplicants.sort(key = lambda x: x.getWeight())
        while len(curImplicants) > 0:
            #TODO: Maybe use a queue instead for currentImplicants?
            currentImplicant = curImplicants.pop() 
            for implicant in curImplicants:
                '''
                if abs(currentImplicant.getWeight() - implicant.getWeight()) >= 2:
                    break
                '''
                if currentImplicant.getDistance(implicant) <= 1:
                    combined[implicant] = True
                    combined[currentImplicant] = True
                    nextImplicants.add(Implicant(len(currentImplicant.binrep), [], currentImplicant, implicant))
                    
            
            if not combined[currentImplicant]:
                #The implicant couldn't be further combined, this it is a prime implicant, though maybe not essential
                primeImplicants.add(currentImplicant)

    return list(primeImplicants)

def PetricksMethod(columnDict):
    '''
        Takes in a dictionary with keys being variables not covered by essential prime implicants, 
        and values being the list of implicants which satisfy the midterm.

        This method returns a list of lists, each list being a possible combination of terms that covers
        the remainder of the function. This is because there may be more than one minimization possible.
    '''
    # Create a sum for each column, and take the product.
    # We do this to generate a function that returns true if 
    # the implicants chosen cover the remainder of the function
    prod = Product()
    prod.isPOS = True
    
    for key, value in columnDict.items():
        sum = Sum()
        sum.isSOP = False
        sum.elements.update(set(value))
        prod.elements.add(sum)
    
    #We have a Product of sums, now we transform it into a sum of products
    sum = prod.GetAsSum()
    if not sum.isSOP:
        sum.TransformToSOP()
    #Apply the classic "Covering" theorem to the sum
    sum.ApplyCovering()

    #Now we can sort by the number of terms
    possibilities = list(sum.elements)
    possibilities.sort(key = lambda x: len(x.elements))
    lowest = len(possibilities[0].elements)
    #and filter out elements larger than the smallest value
    possibilities = list(filter(lambda x: len(x.elements) <= lowest, possibilities))
    # Now, we need the possibilites with the lowest amount of literals.
    # For right now, i'm going to assume that a'b + a'c is 4 literals, not 3, even though a' is repeated.
    possibilities.sort(key = lambda x: x.LiteralWeight())
    minWeight = possibilities[0].LiteralWeight()
    possibilities = list(filter(lambda x: x.LiteralWeight() == minWeight, possibilities))

    possibilities = list(map(lambda x: x.elements, possibilities))

    return possibilities

def menu():
    class MenuState:
        POLLSTATE, MINTERMS, MAXTERMS, EQUATION = range(4)
    '''
    Runs a menu that asks the user for input.
    returns a 3-tuple, in the following order:
    A list of strings used to represent variables
    a list of minterms
    a list of don't care terms
    '''
    state = MenuState.POLLSTATE
    #TODO More robust input
    #TODO implement entering logic expressions
    while True:
        if state == MenuState.POLLSTATE:
            print("Enter a method to input your logic function:")
            print("minterms: enter the number of each minterm (sigma shorthand notation)\nmaxterms: enter the number of each maxterm (pi shorthand notation)")
            value = input()
            if value.strip().lower() == "minterms":
                state = MenuState.MINTERMS
            elif value.strip().lower() == "maxterms":
                state = MenuState.MAXTERMS

        elif state == MenuState.MINTERMS:
            varInput = input("Enter your variables as a space seperated list:")
            variables = list(map(lambda x: x.strip(), varInput.split(" ")))
            
            mintermsInput = input("Enter the numbers corresponding to each minterm as a space seperated list:")
            minterms = list(list(map(lambda x: int(x.strip()), mintermsInput.split(" "))))

            dontcareInput = input("Enter the numbers corresponding to dontcare terms as a space seperated list:")
            if dontcareInput.strip() != "":
                dontcareterms = list(list(map(lambda x: int(x.strip()), dontcareInput.split(" "))))
            else:
                dontcareterms = []

            return (variables, minterms, dontcareterms)
            
        elif state == MenuState.MAXTERMS:
            varInput = input("Enter your variables as a space seperated list:")
            variables = list(map(lambda x: x.strip(), varInput.split(" ")))
            
            mintermsInput = input("Enter the numbers corresponding to each maxterm as a space seperated list:")
            maxterms = list(list(map(lambda x: int(x.strip()), mintermsInput.split(" "))))
            minterms = []
            for i in range(2**len(variables)):
                if i not in maxterms:
                    minterms.append(i)

            dontcareInput = input("Enter the numbers corresponding to dontcare terms as a space seperated list:")
            if dontcareInput.strip() != "":
                dontcareterms = list(list(map(lambda x: int(x.strip()), dontcareInput.split(" "))))
            else:
                dontcareterms = []

            return (variables, minterms, dontcareterms)
        else:
            print("Unkown or bad state!")
            exit()
    

def main():

    tuple = menu()
    binrepsize = len(tuple[0])
    stringrep = tuple[0]
    minterms = tuple[1]
    dontCares = tuple[2]
    implicants = []
    '''
    binrepsize = 3
    stringrep = ['X', 'Y', 'Z']
    minterms = [1, 3, 5, 6, 7]
    dontCares = []
    '''
    for term in minterms + dontCares:
        implicants.append(Implicant(binrepsize, [term]))

    primeImplicants = GetPrimeImplicants(implicants)
    #Commented code here prints out prime implicants.
    '''
    for implicant in primeImplicants:
        print("Binary rep: " + implicant.binrep)
        
        mintermstring = ""
        for term in implicant.terms:
            mintermstring += str(term) + ", "
        
        print("Minterms: " + mintermstring[0:-2])

        primeImplicantString = ""
        for index,c in enumerate(implicant.binrep):
            if c == "0":
                primeImplicantString += stringrep[index] + "'"
            elif c == "1":
                primeImplicantString += stringrep[index]
        
        print("Prime Implicant: " + primeImplicantString)
        print("")
    '''
    #Here we build the chart, in a column major sort of fashion, using a dictionary, where the keys are the minterms
    chart = dict()
    for term in minterms:
        column = []
        for implicant in primeImplicants:
            if term in implicant.terms:
                column.append(implicant)
        chart[term] = column

    #extracting essential prime implicants
    #Basically, they are the only prime implicants that satisfy a particular midterm
    essentialPrimeImplicants = set()
    chart2 = dict()
    for term, column in chart.items():
        if len(column) == 1:
            essentialPrimeImplicants.add(column[0])
        else:
            chart2[term] = column
    chart = chart2

    #remove all terms covered by prime implicants
    for implicant in essentialPrimeImplicants:
        for term in implicant.terms:
            if term in chart:
                del chart[term]
    '''
    Now, we have our essential prime implicants.
    In some cases, this may cover the original function, which we will check for (by seeing if chart has any columns left).
    However, in many cases, these essential prime implicants cannot cover the function, so some non-essential prime implicants
    must be chosen. Which ones should be chosen? This question is answered using Petrick's method, which is a mechanical
    method for deciding which terms to choose.
    '''
    def MapImplicationsToString(x):
            total=''
            for implicant in x: 
                total += implicant.GetAsString(stringrep) + " + "
            return total[0:-3]

    possibleAdditionStrings = [""]
    if len(chart) != 0:
        #essential implicants don't cover, Petrick's method must be used.
        possibleAdditions = PetricksMethod(chart)
        #Convert to strings
        possibleAdditionStrings = list(map(MapImplicationsToString, possibleAdditions))
    
    essentialPrimeImplicantsString = MapImplicationsToString(essentialPrimeImplicants)
    print("Possible Minimizations:")
    for string in possibleAdditionStrings:
        if string != "":
            if essentialPrimeImplicantsString != "":
                print(essentialPrimeImplicantsString + " + " + string)
            else:
                print(string)
        else:
            print(essentialPrimeImplicantsString)
if __name__ == '__main__':
    main()
