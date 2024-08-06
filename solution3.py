import datetime
import time
import pandas as pd
from templates import Booking, Driver, TimeEstimate

read_file = pd.read_excel('InterviewPuzzle.xlsx')
read_file.to_csv('datafile.csv')
data = pd.DataFrame(pd.read_csv('datafile.csv'))
data = data.head(62)

read_file = pd.read_excel('InterviewPuzzle.xlsx', sheet_name='travelTime')
read_file.to_csv('data_timefile.csv')
timedata = pd.DataFrame(pd.read_csv('data_timefile.csv'))


Source = timedata['Source']
Destination = timedata['Destination']
TravelTimeInMin = timedata['TravelTimeInMin']
Traveltimelist = {}
for i in range(len(Source)):
    val = ''
    val+=Source[i]+'_'+Destination[i]
    Traveltimelist.update({val : ((TravelTimeInMin[i]//30)+1)*30})

# print(Traveltimelist)
# print(Traveltimelist['ADUGODI_INDIRANAGAR'])

Date = data['Date']
Time = data['Time']
Source = data['sourceRegion']
Destination = data['destRegion']
Booked = data['booked']
tripDetails = []

for i in range(len(Date)):
    for j in range(int(Booked[i])):
        datetimeval = datetime.datetime.strptime(Date[i]+ " " + Time[i], f'%d-%m-%Y %H:%M')
        tripDetails.append([datetimeval, Source[i], Destination[i]])

# print(len(tripDetails))
# print(tripDetails[0])
driversCount = 30
assignmentTable = [0] * len(tripDetails)
idleTime = [99999] * len(tripDetails)
DriverTrips = [0] * driversCount

for i in range(driversCount):
    timetracker = [[0] * len(tripDetails)]
    endtimeTracker = 0
    driverPosition = ''
    for j in range(len(tripDetails)):
        stime = tripDetails[j][0]
        startTime = stime.hour*60+ stime.minute
        string_val = ''
        string_val += tripDetails[j][1]+'_'+tripDetails[j][2]
        endTime = startTime + Traveltimelist[string_val]
        if(DriverTrips[i] != 0):
            sourceDest = ''
            if(driverPosition != tripDetails[j][2]):
                sourceDest += driverPosition + '_' + tripDetails[j][2]
                currIdleTime = Traveltimelist[sourceDest]
            else:
                currIdleTime = 0
            if(idleTime[j] > currIdleTime and (endtimeTracker + currIdleTime)< startTime):
                if(DriverTrips[assignmentTable[j]-1] > 1):
                    DriverTrips[assignmentTable[j]-1] -= 1
                else:
                    DriverTrips[assignmentTable[j]-1] = 0
                assignmentTable[j] = i+1
                driverPosition = tripDetails[j][2]
                idleTime[j] = currIdleTime
                endtimeTracker = endTime
                DriverTrips[i] += 1
        elif(assignmentTable[j] == 0 and endtimeTracker < startTime):
            assignmentTable[j] = i+1
            driverPosition = tripDetails[j][2]
            endtimeTracker = endTime
            #idleTime[j] = 0
            DriverTrips[i] += 1



# for i in range(len(tripDetails)):
#     print(assignmentTable[i], tripDetails[i][1], tripDetails[i][2], tripDetails[i][0])
print(assignmentTable)
# print(DriverTrips)
# print(idleTime)







