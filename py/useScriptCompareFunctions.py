from classes.itemEntry import itemEntry

def compareDicts(json_1, json_2):
    # Takes 2 Dictionaries
    # Returns success code and reformed array
    # specified to values where key of identifier is strName
    
    # 0 - No clash
    # 1 - String clash but duplicate entry
    # 2 - String clash with non-duplicate entry
    # 3 - Failed to resolve clash 
    clashLevel = 0
    clashArr = []

    for item_1 in json_1:
        for item_2 in json_2:
            if item_1['strName'] == item_2['strName']:
                print('Entry duplicate ' + item_1['strName'])
                if clashLevel < 1: clashLevel = 1
                if item_1['aCOs'] != item_2['aCOs']:
                    if clashLevel < 2: clashLevel = 2
                    clashArr.append(item_1['strName'])
                    resolvedClash = resolveStringClash(item_1['aCOs'], item_2['aCOs'])
                    if resolvedClash is False:
                        return[3, [item_1['strName']]]
                    item_1['aCOs'] = resolvedClash
                    print('Resolved ' + item_1['strName'] + ' clash')
                    
    return {'level': clashLevel, 'json': json_1, 'clashArray': clashArr}

def resolveStringClash(arr_1, arr_2):
    # Three different possible situations here:
    ## EITHER we have an existing array of values where we need to 
    ## check if there are duplicates.

    ## OR we have a single | delimited string where we need to split 
    ## out and calcualte the weights.

    ## OR we have an array of values where an arbitrary number could
    ## be pipe delimited strings. This will be very fragile.

    ### This next check is a little fragile as if a name contains a pipe (|) the check
    ### will return true where it should be false

    # Edge case: If either arr has no length, return the other arr  
    if len(arr_1) < 1: return arr_2
    if len(arr_2) < 1: return arr_1

    a1_clashType = checkClashType(arr_1)
    a2_clashType = checkClashType(arr_2)

    if a1_clashType != a2_clashType: return False

    if a1_clashType == 'mixed':
        # Mixed array, start crying now
        return False
    elif a1_clashType:
        # Multiple entry array of single values
        completeArr = []
        for value in arr_1:
            completeArr.append(value)
            splitVal = value.split('=')[0]
            for compareValue in arr_2:
                if splitVal == compareValue.split('=')[0]:
                    pass
                elif completeArr.__contains__(compareValue):
                    pass
                else:
                    completeArr.append(compareValue)
        return completeArr        
    else:
        # Single entry pipe delimited arrays
        completeArr = []

        arr_1 = arr_1[0].split('|')
        arr_2 = arr_2[0].split('|')

        for value in arr_1:
            completeArr.append(value)
            splitVal = value.split('=')[0]
            for compareValue in arr_2:
                if splitVal == compareValue.split('=')[0]:
                    pass
                elif completeArr.__contains__(compareValue):
                    pass
                else:
                    completeArr.append(compareValue)
        return resolveValueWeights(completeArr)
    return False


def checkClashType(arr):
    # True - Multiple entry array
    # False - Single string Pipe delimited array
    # Mixed - Multiple entry array with some pipe delimited strings
    if len(arr) > 1:
        for value in arr:
            if len(value.split('|')) > 1: return 'mixed'
        return True
    return len(arr[0].split('|')) == 1

def resolveValueWeights(arr):
    modifiedList = []
    for value in arr:
        tmp = value.split('=')
        tmp2 = tmp[1].split('x')
        modifiedList.append(
            itemEntry(tmp[0], tmp2[0], tmp2[1])
        )
    # convert values to percentages of 1.0
    total = 0
    for value in modifiedList:
        total += float(value.weight)

    for value in modifiedList:
        value.weight = round(float(value.weight) / total, 5)

    # make last value large to avoid floating point error
    modifiedList[-1].weight = 0.5

    # Combine modified values back into a Pipe delimited string
    reformattedString = ''
    for value in modifiedList:
        valueString = (
            value.name + '=' +
            str(value.weight) + 'x' +
            value.quantity + '|'
        )
        reformattedString += valueString
    # Remove trailing Pipe
    reformattedString = reformattedString[0:-1]

    # Remember to return as an array
    return [reformattedString]