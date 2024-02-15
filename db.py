import gspread

ga = gspread.service_account(filename='key.json')
gh = ga.open('Uni_Alarm')

def readAlarm():
    wks = gh.worksheet('AlarmSt')
    event = []
    res = wks.get_all_values()
    for row in res[1:]:
        event.append(row)    
    return event

def readData():
    wks = gh.worksheet('ComSt')
    data = []
    res = wks.get_all_values()
    for row in res[1:]:
        data.append(row)    
    return data

def setDb():
    wks = gh.worksheet('ListSt')
    req = wks.get_all_values()
    for s_row in req[1:]:
        if s_row[3] == '_On':
            wks.update_acell('F'+ str(s_row[2]), 'Off')

def esetDb(pos):
    print(pos)
    wks = gh.worksheet('ListSt')
    wks.update_acell('F'+ pos, 'Set')
  
       


