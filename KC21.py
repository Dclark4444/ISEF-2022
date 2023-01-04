import random

#Creats evenly distributed random list of decoys and real transmissions
#0 = decoy and 1 = real
def createRealAndDecoy(keySize):
    typeList = []
    
    for x in range(keySize):
        typeList.append("1")
        typeList.append("0")

    random.shuffle(typeList)

    return typeList

#Creats random list of measurement
def createMeasurement(qubits):
    measureList = []

    for x in range(qubits):
        temp = random.randrange(2)

        if temp == 0:
            measureList.append("0")
        else:
            measureList.append("1")

    return measureList

#Compares the input transmission's decoys
def compareDecoys(typeList, inputList1, inputList2):
    changeState = 0
    for x in range(len(typeList)):
        if typeList[x] == "0" and inputList1[x] != inputList2[x]:
            if random.randrange(2) == 1:
                inputList1[x] = inputList2[x]
                changeState = 1
    return inputList1, changeState
            
#Testing to see if Eve was caught evesdropping
def checkEves(typeList, begining, ending):
    return compareDecoys(typeList, begining, ending)[1]

#Save the collected data into a CSV
def saveData(start, end, data):
    splitData = data.split(",")
    dataRange = []
    writableData = ""
    for x in range(start, end):
        dataRange.append(x)
    for x in range(len(splitData)):
        writableData += str(dataRange[x]) + "," + splitData[x] + "\n"      
    with open("output.csv", "w") as FILE:
        FILE.write(writableData)

#Run multiple tests of the transmission from Alice to Eve to Bob
def simulate(startKeySize=5, totalKeySize=10, runsPerData=5, requestToSave=False):
    totalKeySize += 1
    runsPerData += 1
    output = []
    keySize = startKeySize
    for x in range(startKeySize, totalKeySize):
        tempOutput = []
        for y in range(runsPerData):
            qubits = keySize*2

            typeList = createRealAndDecoy(keySize)

            alice = createMeasurement(qubits)
            eve = createMeasurement(qubits)
            bob = createMeasurement(qubits)

            transmission = compareDecoys(typeList, alice, eve)[0]
            transmission = compareDecoys(typeList, eve, bob)[0]

            eveState = checkEves(typeList, alice, transmission)
            tempOutput.append(eveState)
        output.append((sum(tempOutput)/runsPerData)*100)
        keySize += 1
    displayableOutput = ""
    for x in output:
        displayableOutput += str(x) + ","
    displayableOutput = str(displayableOutput)[:-1]
    if requestToSave:
        try:
            saveData(startKeySize, totalKeySize, displayableOutput)
            print("The collected data was saved successfully")
        except:
            print("The collected data was unable to be saved. Make sure 'output.csv' is not open when running simulations.")
    print(displayableOutput)

print("To simulate the KC21 protocal type the following command and insert your specific values in place of asterisks: simulate(*where you want the key size to start*, *Where you want the key size to end*, *How many simulations per key size do you want to be ran and then averaged*, *Do you want the collected data to be saved? (True or False)*)")






