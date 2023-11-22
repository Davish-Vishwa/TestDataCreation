import json
from EU_UtrGrUserInput import j , Ctr , ToStubList

UpdateSortZoneEU = '''{
"Operation": "com.amazon.stationtesttoolsservice#UpdateRouteAndSortZones",
"Service": "com.amazon.stationtesttoolsservice#StationTestToolsService",
"Input": {
"trackingIds": '''+json.dumps(ToStubList)+''',
"routeZone": "CYCLE_1",
"sortZone": "C1-1D",
"sequenceIdentifier": {
"expectedExecutionOrder": 1994
}
}
}'''

GetTRJson = '''{
"Operation": "com.amazon.rabbittestmanager#GetTRsByScannableId",
"Service": "com.amazon.rabbittestmanager#RabbitTestManager",
"Input": {
"scannableId": "'''+j+'''"
}
}'''

TRPickUp_JSON = '''{
"Operation": "com.amazon.rabbittestmanager#UpdateFakeTRs",
"Service": "com.amazon.rabbittestmanager#RabbitTestManager",
"Input": {
"updateFakeTRsList":
[{"trId": "'''+Ctr+'''",
"trState": "OPEN",
"trObjectState": "PICKED_UP",
"trObjectReason": "NONE",
"signatureID": "foo",
"failureExpected": true,
"validatecall": true}]
}
}'''

FakeTRJson_DeliveryA_BusinessC = '''{
"Operation": "com.amazon.rabbittestmanager#UpdateFakeTRs",
"Service": "com.amazon.rabbittestmanager#RabbitTestManager",
"Input": {
"updateFakeTRsList":
[{"trId": "'''+Ctr+'''",
"trState": "OPEN",
"trObjectState": "DELIVERY_ATTEMPTED",
"trObjectReason": "BUSINESS_CLOSED",
"signatureID": "foo",
"failureExpected": true,
"validatecall": true}]
}
}'''

FakeTRJson_Rejected = '''{
"Operation": "com.amazon.rabbittestmanager#UpdateFakeTRs",
"Service": "com.amazon.rabbittestmanager#RabbitTestManager",
"Input": {
"updateFakeTRsList":
[{"trId": "'''+Ctr+'''",
"trState": "OPEN",
"trObjectState": "REJECTED",
"trObjectReason": "NONE",
"signatureID": "foo",
"failureExpected": true,
"validatecall": true}]
}
}'''

EU_RTS_BeginTRJson = '''{
"Operation": "com.amazon.rabbittestmanager#BeginTRsExecution",
"Service": "com.amazon.rabbittestmanager#RabbitTestManager",
"Input": {
"trIds": [ "'''+Ctr+'''"],
"transporterId": "A1YMQBJ93G3WTE",
"operator": "Rufus",
"allowOnRoadTransfer": true
}
}'''

EU_Depart_BeginTRJson = '''{
"Operation": "com.amazon.rabbittestmanager#BeginTRsExecution",
"Service": "com.amazon.rabbittestmanager#RabbitTestManager",
"Input": {
"trIds": [ "'''+Ctr+'''"],
"transporterId": "AK5H86HSFDJW6",
"operator": "Rufus",
"allowOnRoadTransfer": true
}
}'''