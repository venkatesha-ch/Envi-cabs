import datetime
import time
import pandas as pd

#Retriving data from excel
read_file = pd.read_excel('InterviewPuzzle.xlsx')
read_file.to_csv('datafile.csv')
data = pd.DataFrame(pd.read_csv('datafile.csv'))
data = data.iloc[0:62]

read_file = pd.read_excel('InterviewPuzzle.xlsx', sheet_name='travelTime')
read_file.to_csv('data_timefile.csv')
timedata = pd.DataFrame(pd.read_csv('data_timefile.csv'))

Source = timedata['Source']
Destination = timedata['Destination']
TravelTimeInMin = timedata['TravelTimeInMin']
Traveltimelist = {}

#Storing Travel time 
for i in range(len(Source)):
    val = ''
    val+=Source[i]+'_'+Destination[i]
    #rounding time to 30 min
    Traveltimelist.update({val : ((TravelTimeInMin[i]//30)+1)*30})


Date = data['Date']
Time = data['Time']
Source = data['sourceRegion']
Destination = data['destRegion']
Booked = data['booked']
tripDetails = []


#Storing trip details

for i in range(len(Date)):
    for j in range(0, int(Booked[i])):
        datetimeval = datetime.datetime.strptime(Date[i]+ " " + Time[i], f'%d-%m-%Y %H:%M')
        tripDetails.append([datetimeval, Source[i], Destination[i]])

driversCount = 30
assignmentTable = [0] * len(tripDetails)
# DriverTrips = [0] * driversCount
tempassignment = set()
allpossibletrips = []
TotalIdleTime = 0

# def idleTimeCalc(j, endPosition):
#     idleTime = 0
#     if(endPosition != '' and endPosition != tripDetails[j][1]):
#         sourceDest = ''
#         sourceDest += endPosition + '_' + tripDetails[j][1]
#         idleTime = Traveltimelist[sourceDest]
#     return idleTime

def calculateTotalIdle(tempassignment):
    idleTime = 0
    for item in tempassignment:
        endPosition = tripDetails[item][1]
        break
    for i in range(len(tempassignment)):
        if(endPosition == tripDetails[i+1][1]):
            continue
        sourceDest = ''
        sourceDest += endPosition + '_' + tripDetails[i+1][1]
        idleTime += Traveltimelist[sourceDest]
    return idleTime

def assignBestTrip(i,endPosition,start,endtimeTracker = 0, idleTime = 0, TotalIdleTime = 0):
    for j in range(start, len(tripDetails)):
        # print(tempassignment)
        if j == len(tripDetails)-1 or len(tempassignment) == 5:
            allpossibletrips.append([tempassignment, calculateTotalIdle(tempassignment)])
            return
        stime = tripDetails[j][0]
        startTime = stime.hour*60 + stime.minute
        # if(startTime > 1230):
        #     return
        string_val = ''
        string_val += tripDetails[j][1]+'_'+tripDetails[j][2]
        endTime = startTime + Traveltimelist[string_val]
        if(endPosition != '' and endPosition != tripDetails[j][1]):
            sourceDest = ''
            sourceDest += endPosition + '_' + tripDetails[j][1]
            idleTime = Traveltimelist[sourceDest]
        else:
            idleTime = 0
        if(assignmentTable[j] == 0 and endtimeTracker + idleTime <= startTime):
            tempassignment.add(j)
            endPosition = tripDetails[j][2]
            endtimeTracker = endTime
            TotalIdleTime += idleTime
            assignBestTrip(i,endPosition,j, endtimeTracker, idleTime, TotalIdleTime)
            return


for i in range(driversCount):
    for j in range(len(tripDetails)):
        tempassignment = set()
        assignBestTrip(i, '', j)
        print(i, j)
    test = allpossibletrips
    allpossibletrips = sorted(test, key= lambda x:x[1])
    print(allpossibletrips)
     
    time.sleep(10)
    print(allpossibletrips[0][0])
    for pos in allpossibletrips[0][0]:
        assignmentTable[pos] = i+1
    allpossibletrips = []

# print(assignmentTable.count(0), len(assignmentTable))

# for i in range(len(tripDetails)):
#     print("Driver -", assignmentTable[i], tripDetails[i][1], tripDetails[i][2], tripDetails[i][0])

print(assignmentTable)
print(assignmentTable.count(0))

