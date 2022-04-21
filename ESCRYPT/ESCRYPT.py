from datetime import datetime, timedelta

#Getting the failed test cases
def get_parameters(path):
    buffer = []
    test_case = {'Passed': {}, 'Failed': {}}
    i=0
    with open('./inputFile.log') as f:
            for line in f:
                i+=1
                line_update = line.replace('\t', ' ')
                line_update = line_update.replace('\n', '')
                entries = line_update.split(' ')
                if(len(entries) == 1):
                    continue
                for entry in entries:
                    if entry=='Passed':
                        test_case['Passed'][entries[2]] = buffer
                        buffer = []
                        break
                    if entry=='Failed':
                        test_case['Failed'][entries[2]] = buffer
                        buffer = []
                        break
                    if entry=='CAN-FD':
                        buffer.append(line)
                        break
    return test_case, i
    
#Looping through the failed cases to get the first request and the response
def get_time_failed(test_case):
    log_startend = {}
    temp_log = []
    for i in test_case['Failed'].keys():
        for j in test_case['Failed'][i]:
            k = j.replace('\t', ' ')
            k = k.replace('.', ' ')
            k = k.replace('\n', '')
            entries = k.split(' ')
            for entry in entries:
                if (entry == 'after'):
                    temp_log.append(entries[1]+'.'+entries[2]) # Appending the time with ms 
                    break
                if (entry == 'Response'):
                    temp_log.append(entries[1]+'.'+entries[2]) # Appending the time with ms
                    break
        log_startend[i] = temp_log
        temp_log = []
        
    return log_startend
        
#Check if the log is DOS or Not and output the result to a file
def is_accurate_DOS(start_end):
  with open('dos_failed_cases.txt', 'w') as write_file:
    for key,val in start_end.items():
        request_time = datetime.strptime(val[0], "%H:%M:%S.%f")
        response_time = datetime.strptime(val[1], "%H:%M:%S.%f")
        # Check if the DOS time is accurate or not
        is_acc_DOS, difference = dos_time(request_time, response_time)
        write_file.write("Test Case "+ key + " - \n Request Time: " + val[0]
 + ", Response Time: "+ val[1] + ", Accurate DOS - "+ str(is_acc_DOS) + ", Difference in ms = " + str(difference) + "\n")

# Subtract request time from response time and if the result is higher than 100ms it is not accurate DOS time
def dos_time(request_time, response_time):
  diff = (response_time-request_time).microseconds
  if (diff > 100):
    return False, diff
  else:
    return True, diff

def main(path):
    logs, NOL = get_parameters(path)
    start_end = get_time_failed(logs)
    is_accurate_DOS(start_end)
    pass

if __name__ == '__main__':
    main('./inputFile.log')
    