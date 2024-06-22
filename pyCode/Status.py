from pymongo import errors
from pyCode.setupConnection import conn
from datetime import datetime

db = conn['admin']


def cleanFail(error):
    errorList = error.args[0].split(',')
    print(errorList)
    if('"Primary()"' in errorList[0]):    #Almeno un nodo attivo, cambia il messaggio di errore.
        pos1 = 5
        pos2 = 10
        pos3 = 15
        if("RSSecondary" not in errorList[pos1]):
            nodeA = "offline"
        else:
            nodeA = "online"

        if("RSSecondary" not in errorList[pos2]):
            nodeB = "offline"
        else:
            nodeB = "online"
        if("RSSecondary" not in errorList[pos3]):
            nodeC = "offline"
        else:
            nodeC = "online"    
        
    else:
        if (len(errorList) > 40): #Modo migliore per capire che uno è entrato in quiescenza
            pos1 = 9
            pos2 = 8
            pos3 = 7
            if("'ShutdownInProgress'" in errorList[pos1]):
                nodeA = "offline"
                nodeB = "offline"
                nodeC = "offline"
            if("'ShutdownInProgress'" in errorList[pos2]):
                nodeB = "offline"
                nodeA = "offline"
                nodeC = "offline"
            if("'ShutdownInProgress'" in errorList[pos3]):
                nodeC = "offline"
                nodeA = "offline"
                nodeB = "offline"  
        else:
                
            pos1 = 0
            pos2 = 2
            pos3 = 4
            if("WinError 10061" or "WinError 10054" in errorList[pos1]): #Primo per spento, secondo per chiusura.
                nodeA = "offline"
            else:
                nodeA = "online"

            if("WinError 10061" or "WinError 10054" in errorList[pos2]):
                nodeB = "offline"
            else:
                nodeB = "online"
            if("WinError 10061" or "WinError 10054" in errorList[pos3]):
                nodeC = "offline"
            else:
                nodeC = "online"    
        
    status = {"nodeA": nodeA, "nodeB": nodeB, "nodeC": nodeC}
    return status
    

def update():
    #while True:
    #    rs_status = db.command({'replSetGetStatus': 1})
    #    print(rs_status)
    try:
        rs_status = db.command({'replSetGetStatus': 1})
        clean(rs_status)
        return rs_status
    except errors.ServerSelectionTimeoutError as error:
        return cleanFail(error)
        
def clean(status):
    status["date"] = status.get("date").strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
    del status['myState']
    del status.get('optimes').get('lastCommittedOpTime')["t"]
    status.get("optimes")["lastCommittedOpTime"] = status.get("optimes").get("lastCommittedOpTime")["ts"].as_datetime().strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]

    
    if "readConcernMajorityOpTime" in status.get("optimes"):
        del status.get("optimes").get("readConcernMajorityOpTime")["t"]
        status.get("optimes")["readConcernMajorityOpTime"] = status.get("optimes").get("readConcernMajorityOpTime")["ts"].as_datetime().strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]

    
    if "readConcernMajorityWallTime" in status.get("optimes"):
        status.get("optimes")["readConcernMajorityWallTime"] = status.get("optimes")["readConcernMajorityWallTime"].strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]    
    
    del status.get('optimes').get('appliedOpTime')["t"]
    status.get("optimes")["appliedOpTime"] = status.get("optimes").get("appliedOpTime")["ts"].as_datetime().strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
    del status.get('optimes').get('durableOpTime')["t"]
    status.get("optimes")["durableOpTime"] = status.get("optimes").get("durableOpTime")["ts"].as_datetime().strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
    status.get('optimes')['lastAppliedWallTime'] = status.get("optimes")['lastAppliedWallTime'].strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
    status.get('optimes')['lastDurableWallTime'] = status.get("optimes")['lastDurableWallTime'].strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
    status.get('optimes')['lastCommittedWallTime'] = status.get("optimes")['lastCommittedWallTime'].strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]

    del status['lastStableRecoveryTimestamp']
        
    del status.get('electionCandidateMetrics')['lastCommittedOpTimeAtElection']
    status.get('electionCandidateMetrics')['lastElectionDate'] = status.get('electionCandidateMetrics')['lastElectionDate'].strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
    del status.get('electionCandidateMetrics')['lastSeenOpTimeAtElection']
    del status.get('electionCandidateMetrics')['numVotesNeeded']
    status.get('electionCandidateMetrics')['newTermStartDate'] = status.get('electionCandidateMetrics')['newTermStartDate'].strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
    status.get('electionCandidateMetrics')['wMajorityWriteAvailabilityDate'] = status.get('electionCandidateMetrics')['wMajorityWriteAvailabilityDate'].strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
    
    if "electionParticipantMetrics" in status:
        del status.get('electionParticipantMetrics')['lastAppliedOpTimeAtElection']
        del status.get('electionParticipantMetrics')['maxAppliedOpTimeInSet']
        del status.get('electionParticipantMetrics')['newTermStartDate']
        status.get('electionParticipantMetrics')['lastVoteDate'] = status.get('electionParticipantMetrics')['lastVoteDate'].strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
    
    for member in status['members']:
       del member.get("optime")["t"]
       member["optime"] = member.get("optime")["ts"].as_datetime().strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
       member[("optimeDate")] = member.get("optimeDate").strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
       del member["lastAppliedWallTime"]
       del member["lastDurableWallTime"]
       
       if "lastHeartbeat" in member:
           member["lastHeartbeat"] = member.get("lastHeartbeat").strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
           member["lastHeartbeatRecv"] = member.get("lastHeartbeatRecv").strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]

       
       if "electionTime" in member:
           member["electionTime"] = member.get("electionTime").as_datetime().strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
           member["electionDate"] = member.get("electionDate").strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
       
       if "optimeDurable" in member:
           del member.get("optimeDurable")["t"]
           member["optimeDurable"] = member.get("optimeDurable")["ts"].as_datetime().strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
           member["optimeDurableDate"] = member.get("optimeDurableDate").strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
           
    
    del status["$clusterTime"]
    del status["operationTime"]
    
    return status
    








    
    