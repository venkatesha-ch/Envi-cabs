import datetime
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


driversCount = 60
assignmentTable = [0] * len(tripDetails)
DriverTrips = [0] * driversCount

def dayShiftAssignment(driversCount, assignmentTable, DriverTrips):
    for i in range(driversCount//2):
        endtimeTracker = 0
        idleTime = 0
        endPosition = ''
        for j in range(len(tripDetails)):
            stime = tripDetails[j][0]
            startTime = stime.hour*60 + stime.minute
            '''
            if the start time is in next shift just ignore this trip,
            it will be handled in other function
            '''
            if(startTime > 1230):
                continue
            string_val = ''
            string_val += tripDetails[j][1]+'_'+tripDetails[j][2]
            endTime = startTime + Traveltimelist[string_val]
            '''
            Checking whether its driver's first trip or not.
            if first trip assign the trip to driver i
            else check whether the idle time + endtime of last trip is less than starttime of this trip
            if this check pass, assign this trip to driver i
            else start checking with next trip
            '''
            if(endPosition != '' and endPosition != tripDetails[j][1]):
                sourceDest = ''
                sourceDest += endPosition + '_' + tripDetails[j][1]
                idleTime = Traveltimelist[sourceDest]
            else:
                idleTime = 0
            if(assignmentTable[j] == 0 and endtimeTracker + idleTime <= startTime):
                assignmentTable[j] = i+1
                DriverTrips[i]+=1
                endPosition = tripDetails[j][2]
                endtimeTracker = endTime


def nightShiftAssignment(startDriverId, driversCount, assignmentTable, DriverTrips):
    for i in range(startDriverId, driversCount):
        endtimeTracker = 0
        idleTime = 0
        endPosition = ''
        for j in range(len(tripDetails)):
            stime = tripDetails[j][0]
            startTime = stime.hour*60 + stime.minute
            '''
            if the start time is in next shift just ignore this trip,
            it will be handled in other function
            '''
            if(1230 > startTime > 510):
                continue
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
                assignmentTable[j] = i+1
                DriverTrips[i]+=1
                endPosition = tripDetails[j][2]
                endtimeTracker = endTime




#Differnt function for day/night shifts

dayShiftAssignment(driversCount, assignmentTable, DriverTrips)
nightShiftAssignment(driversCount//2, driversCount, assignmentTable, DriverTrips)
# dayShiftAssignment(driversCount, assignmentTable, DriverTrips)
# nightShiftAssignment(driversCount//2, driversCount, assignmentTable, DriverTrips)

# for i in range(len(tripDetails)):
#     print("Driver -", assignmentTable[i], tripDetails[i][1], tripDetails[i][2], tripDetails[i][0])

# print(assignmentTable.count(0), len(assignmentTable), DriverTrips)
print(assignmentTable)