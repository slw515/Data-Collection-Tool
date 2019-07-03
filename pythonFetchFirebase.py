from firebase import firebase
from password import *
import datetime
import csv
import json

today = datetime.datetime.now()
today.strftime('%Y-%m-%d')
firebase = firebase.FirebaseApplication('', None)
## insert Firebase link in above quotation marks
firstDate = input("What starting date do you wish to retrieve the data from (input as: ex. MM/DD/YYYY)")
endDate = input("What starting date do you wish to retrieve the data from (input as: ex. MM/DD/YYYY)")
firstDayLength = len(firstDate)
endDayLength = len(endDate)
stateLowered = "y"

while firstDayLength != 10 or endDayLength != 10:
     firstDate = input("Please give a valid start date!")
     endDate = input("Please give a valid end date!")
     firstDayLength = len(firstDate)
     endDayLength = len(endDate)
while firstDayLength == 10 or endDayLength == 10 and stateLowered == "y":
     
     start = datetime.datetime.strptime(firstDate, "%m/%d/%Y")
     end = datetime.datetime.strptime(endDate, "%m/%d/%Y")
     date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
     
     firstDateValues = (firstDate.split('/'))
     firstDateResult = firebase.get(firstDateValues[2] +'/' + firstDateValues[0] + '/' + firstDateValues[1], None)
     firstDateFinal = str(firstDateValues[2] +'.' + firstDateValues[0] + '.' + firstDateValues[1])

     csvName = str(firstDateFinal + ".csv")

     with open("test1.csv", "a", newline='') as csvfile:
          fieldnames = ['apartment number', 'area name', 'building number', 'email', 'emirate', 'entry date', 'key', 'name', 'nearest landmark', 'number', 'street name']
          writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
          writer.writeheader()
          
     arr = []    
     for date in date_generated:
          arr.append(date.strftime("%m/%d/%Y"))
     splitPeriodDates = str(arr[0].replace('/','.') + ' - ' + arr[-1].replace('/','.') + '.csv')
     with open("newData2.csv",'r') as test:
          dataRead = test.read()
     stripped = [s.strip() for s in dataRead.splitlines()]
     lists = []
     for s in stripped:
          try: 
               splitted = s.split(",")
               value = splitted[6]
               lists.append(value)
          except:
               continue
     testValue = 0     
     for userBig in arr:
          endDateValues = (userBig.split('/'))
          endDateResult = firebase.get(endDateValues[2] +'/' + endDateValues[0] + '/' + endDateValues[1], None)
          try:
               for user in endDateResult:
                    testValue += 1

                    if user not in lists:
                         with open("newData2.csv", "a", newline='') as infile:
                            writer = csv.DictWriter(infile, fieldnames=endDateResult[user].keys())
                            writer.writerow(endDateResult[user])
                         with open(splitPeriodDates, "a", newline='') as infile:
                            writer = csv.DictWriter(infile, fieldnames=endDateResult[user].keys())
                            writer.writerow(endDateResult[user])

                    else:
                         continue

          except:
               continue
          
     print("data stored in " + splitPeriodDates + ".csv")
     print("data appended into allData.csv")
     state = input("Would you like to keep adding data? Y/N")
     stateLowered = state.lower()

     if stateLowered == "n":
          break 

     firstDate = input("Add another starting date? MM/DD/YYYY")
     endDate = input("Add another end date? MM/DD/YYYY")
     firstDayLength = len(firstDate)
     endDayLength = len(endDate)



