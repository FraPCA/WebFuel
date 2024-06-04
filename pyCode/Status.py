from pyCode.setupConnection import conn
from datetime import datetime

db = conn['admin']

def update():
    #while True:
    #    rs_status = db.command({'replSetGetStatus': 1})
    #    print(rs_status)
    rs_status = db.command({'replSetGetStatus': 1})
    clean(rs_status)
    return rs_status

def clean(status):
    status["date"] = status.get("date").strftime("%d/%m/%Y, %H:%M:%S.%f")[:-3]
    del status['myState']
    del status['syncSourceHost']
    del status['syncSourceId']
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
    








    
    