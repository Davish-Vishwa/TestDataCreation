NAFlexTool = "https://flextools-na-gamma-iad-jlb-iad.iad.proxy.amazon.com/generateShipment.do"
EUFlexTool = "https://flextools-eu-gamma-dub-jlb-dub.dub.proxy.amazon.com/generateShipment.do"

AuthLoginIDField = '//*[@id="user_name_field"]'
AuthIDButton = '//*[@id="user_name_btn"]'
AuthPassField = '//*[@id="password_field"]'

FlexCountryCodeField = '//*[@id="country_code"]'
FlexPackageTypeField = '//*[@id="afn_packageType"]'
FlexShipmentField = '//*[@id="ship_method"]'
FlexStationField = '//*[@id="delivery_stationcode"]'
FlexCreateShipmentButton = '//*[@id="createAfnShipment"]'
PackageIDField = '//*[@id = "shipmentTrackingId"]'

STTS_NA = 'https://coral.amazon.com/StationTestToolsService/NA/Gamma/explorer'
STTS_EU = 'https://coral.amazon.com/StationTestToolsService/EU/Gamma/explorer'

STTS_Route_API = 'UpdateRouteAndSortZones'

NAnis = 'https://conduit.security.a2z.com/accounts/aws/525817805522/attributes'
EUnis = 'https://conduit.security.a2z.com/accounts/aws/503358037459/attributes'

AdministratorField = '/html/body/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[2]/div/div/div[2]/div/div[1]/div/awsui-select/div/div/awsui-select-trigger/div/div/span'
AdminstratorLocator = '/html/body/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[2]/div/div/div[2]/div/div[1]/div/awsui-select/div/div/awsui-select-dropdown/div/div[2]/ul/li[1]/ul/li[1]'
ConsoleAccessBotton = '/html/body/div/div/awsui-app-layout/div/main/div/div[2]/div/span/div/div[2]/div/div/div[2]/div/div[3]/div/awsui-button/a'
S3Bucket = '/html/body/div[2]/div[2]/div/div/div/div/div/main/div/div[2]/div/div[1]/div/div/div[4]/div[2]/div/div[65]/div/div/div[1]/div/div[2]/div/div/div[2]/div/div/div/div/div/a'
S3FolderInputField = '//*[@id = "polaris-table-formfield-filter"]'
EUS3FolderSelect = "//*[text()='induct-qa-mock-dcas-master-eu']"
NAS3FolderSelect = "//*[text()='induct-qa-mock-dcas-master-na']"
AMZLLocator = "//*[text()='AMZL/']"
AMZLUploadButton = "//*[text()='Upload']"
NisAddFilesLocator = '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/main/div/div[2]/div/div/div[2]/awsui-form/div/div[2]/span/div/div[2]/input[1]'
S3Upload = '/html/body/div[2]/div[2]/div/div/div/div/div/div/div/main/div/div[2]/div/div/div[2]/awsui-form/div/div[4]/span/div/div[2]/button'
S3UploadSuccess = "//*[text()='Upload succeeded']"

NA_RTM = 'https://coral.amazon.com/RabbitTestManager/Gamma/explorer'
EU_RTM = 'https://coral.amazon.com/RabbitTestManager/EU/Gamma/explorer'

RTM_APIGetTr = 'GetTRsByScannableId'
RTM_APIBeginTr = 'BeginTRsExecution'
RTM_APIUpdateFakeTr = 'UpdateFakeTRs'

RTMSearchField = '/html/body/div[2]/div[1]/table/tbody/tr/td[2]/div[2]/div[1]/div/div/div/div[2]'
RTMSearchInputField = '/html/body/div[2]/div[1]/table/tbody/tr/td[2]/div[2]/div[1]/div/div/div/div[2]/div/div/input'
RTM_APILocator = '/html/body/div[2]/div[1]/table/tbody/tr/td[2]/div[2]/div[1]/div/div/div/div[2]/div/ul/li[2]'
RTMRequest_JSONField = '/html/body/div[2]/div[1]/table/tbody/tr/td[2]/div[2]/div[1]/div/div/div/div[3]/textarea'
RTM_PostRequestButton = '/html/body/div[2]/div[1]/table/tbody/tr/td[1]/form[1]/div[3]/button[1]'
RTM_TrResponseLocator = '/html/body/div[2]/div[1]/table/tbody/tr/td[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[3]'
RTM_Response_Locator = "/html/body/div[2]/div[1]/table/tbody/tr/td[2]/div[2]/div[2]/div[1]/div[2]/div/div[1]/pre[2]/span[1]"
