# Main Executable File to create NA Gamma Readiness Test Data
# Packages and modules import
import os
import string
import random
import smtplib
import pyautogui
import pywinauto
import pyperclip
import subprocess
from time import sleep
from datetime import date
import importlib
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import  Service
from webdriver_manager.firefox import GeckoDriverManager
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import EU_UtrGrJSONS
import UtrGrLocators
import EU_UtrGrUserInput

user = os.getlogin()
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
Exwait = WebDriverWait(driver,50)

DynamicPackagesList = []
StubbedPackages = []
TrIDs = []
ReceivePackages = []
DepartPackages = []

class DataCreation():

    # Function to perform MidWay Authentication
    def Auth():

        driver.get(UtrGrLocators.EUFlexTool)
        AuthUser = Exwait.until(EC.presence_of_element_located((By.XPATH, UtrGrLocators.AuthLoginIDField)))
        AuthUser.send_keys(user)
        AuthUserB = Exwait.until(EC.presence_of_element_located((By.XPATH, UtrGrLocators.AuthIDButton)))
        AuthUserB.click()
        AuthPass = Exwait.until(EC.visibility_of_element_located((By.XPATH, UtrGrLocators.AuthPassField)))
        AuthPass.send_keys(EU_UtrGrUserInput.KeyPassword)
        sleep(20)

    # Function to create Dynamic Packages
    def FlexCreatePackages(MP, PackageType, ShipmentMethod, Station, PackageCount):

        #driver.get(UtrGrLocators.EUFlexTool)
        Country = Exwait.until(EC.element_to_be_clickable((By.XPATH, UtrGrLocators.FlexCountryCodeField)))
        CDD = Select(Country)
        CDD.select_by_visible_text(MP)
        
        sleep(3)
        PackType = Exwait.until(EC.element_to_be_clickable((By.XPATH, UtrGrLocators.FlexPackageTypeField)))
        PTDD = Select(PackType)
        PTDD.select_by_visible_text(PackageType)

        sleep(3)
        ShipMethod = Exwait.until(EC.element_to_be_clickable((By.XPATH, UtrGrLocators.FlexShipmentField)))
        SMDD = Select(ShipMethod)
        SMDD.select_by_visible_text(ShipmentMethod)

        flexStt = Exwait.until(EC.element_to_be_clickable((By.XPATH, UtrGrLocators.FlexStationField)))
        DSDD = Select(flexStt)
        DSDD.select_by_visible_text(Station)
        sleep(2)
        
        i = 1
        while (i <= PackageCount):
            CreateShipment = Exwait.until(EC.element_to_be_clickable((By.XPATH, UtrGrLocators.FlexCreateShipmentButton)))
            CreateShipment.click()
            sleep(3)

            try: 
                Package_IDField = Exwait.until(EC.visibility_of_element_located((By.XPATH, UtrGrLocators.PackageIDField)))
                Package_ID = Package_IDField.text
            except:
                Package_ID = "PC Failed"
                
            DynamicPackagesList.append(Package_ID)
            i += 1

        print(DynamicPackagesList)

    # Function to create Stubbed Packages
    def MCO_Package():
        for MCO_toStub_PID in DynamicPackagesList[2:]:
            if MCO_toStub_PID == "PC Failed":
                continue
            else:
                EU_UtrGrUserInput.ToStubList.append(MCO_toStub_PID)
                StubbedPackages.append(MCO_toStub_PID)
        print(EU_UtrGrUserInput.ToStubList)
        print(StubbedPackages)

        try:
            driver.get(UtrGrLocators.STTS_EU)
            sleep(10)
            driver.refresh()
            sleep(30)

            importlib.reload(EU_UtrGrJSONS)
            print(EU_UtrGrJSONS.UpdateSortZoneEU)
            DataCreation.RTM_APIRequest(UtrGrLocators.STTS_Route_API, EU_UtrGrJSONS.UpdateSortZoneEU)
            sleep(15)

        except:
            print ("Stubbing Failed in STTS")

    # Function to perform API Request in RTM
    def RTM_APIRequest(APIRequest, APIRJson):
        pyautogui.press('up')
        pyautogui.press('up')
        sleep(15)
        driver.implicitly_wait(15)
        ApiSearch = Exwait.until(EC.element_to_be_clickable((By.XPATH, UtrGrLocators.RTMSearchField)))
        ApiSearch.click()
        Search = Exwait.until(EC.visibility_of_element_located((By.XPATH, UtrGrLocators.RTMSearchInputField)))
        Search.send_keys(APIRequest)
        driver.find_element(By.XPATH, value=UtrGrLocators.RTM_APILocator).click()
        Request = Exwait.until(EC.presence_of_element_located((By.XPATH, UtrGrLocators.RTMRequest_JSONField)))
        Request.send_keys(Keys.CONTROL+"A")
        Request.send_keys(Keys.DELETE)
        Request.send_keys(APIRJson)
        pyautogui.press('down')
        pyautogui.press('down')
        PostReq = Exwait.until(EC.presence_of_element_located((By.XPATH, UtrGrLocators.RTM_PostRequestButton)))
        PostReq.click()

    # Function to perform package status update for RTS in RTM
    def RTS_RTM_StatusUpdate():
        try:
            driver.get(UtrGrLocators.EU_RTM)
            sleep(10)
            driver.refresh()
            sleep(30)

            importlib.reload(EU_UtrGrUserInput)
            EU_UtrGrUserInput.j = StubbedPackages[-1]
            
            importlib.reload(EU_UtrGrJSONS)
            from EU_UtrGrJSONS import GetTRJson
            DataCreation.RTM_APIRequest(UtrGrLocators.RTM_APIGetTr, GetTRJson)

            importlib.reload(EU_UtrGrUserInput)
            Exwait.until(EC.visibility_of_element_located((By.XPATH, UtrGrLocators.RTM_Response_Locator)))
            RequestResp = str(driver.find_element(By.XPATH, value=UtrGrLocators.RTM_TrResponseLocator).text)
            trdir = (((RequestResp.split('"id"'))[1]).split('"')[1]).split('"')[0]
            EU_UtrGrUserInput.Ctr = trdir
            print(EU_UtrGrUserInput.Ctr)
            
            importlib.reload(EU_UtrGrJSONS)
            from EU_UtrGrJSONS import EU_RTS_BeginTRJson, TRPickUp_JSON, FakeTRJson_DeliveryA_BusinessC

            DataCreation.RTM_APIRequest(UtrGrLocators.RTM_APIBeginTr, EU_RTS_BeginTRJson)
            DataCreation.RTM_APIRequest(UtrGrLocators.RTM_APIUpdateFakeTr, TRPickUp_JSON)
            DataCreation.RTM_APIRequest(UtrGrLocators.RTM_APIUpdateFakeTr, FakeTRJson_DeliveryA_BusinessC)
            ReceivePackages.append(StubbedPackages[-1])
        except:
            ReceivePackages.append("Receive Status Update failed in RTM")
            print('Receive Status Update failed in RTM')
        sleep(3)
        print(ReceivePackages)

    # Function to perform package status update for Depart in RTM
    def Depart_RTM_StatusUpdate():
        
        driver.get(UtrGrLocators.EUFlexTool)
        DataCreation.FlexCreatePackages(EU_UtrGrUserInput.MP, EU_UtrGrUserInput.PackageType, EU_UtrGrUserInput.ShipmentMethod, EU_UtrGrUserInput.DepartStation, EU_UtrGrUserInput.DepartPackageCount)

        try: 
            DPackage_ID = driver.find_element(By.XPATH, value='//*[@id = "shipmentTrackingId"]').text
        except:
            DPackage_ID = "PC Failed"

        try:
            driver.get(UtrGrLocators.EU_RTM)
            sleep(10)
            driver.refresh()
            sleep(30)

            importlib.reload(EU_UtrGrUserInput)
            EU_UtrGrUserInput.j = DPackage_ID

            importlib.reload(EU_UtrGrJSONS)
            from EU_UtrGrJSONS import GetTRJson
            DataCreation.RTM_APIRequest(UtrGrLocators.RTM_APIGetTr, GetTRJson)

            importlib.reload(EU_UtrGrUserInput)
            Exwait.until(EC.visibility_of_element_located((By.XPATH, UtrGrLocators.RTM_Response_Locator)))
            RequestResp = str(driver.find_element(By.XPATH, value=UtrGrLocators.RTM_TrResponseLocator).text)
            trdir = (((RequestResp.split('"id"'))[1]).split('"')[1]).split('"')[0]
            EU_UtrGrUserInput.Ctr = trdir
            print(EU_UtrGrUserInput.Ctr)

            importlib.reload(EU_UtrGrJSONS)
            from EU_UtrGrJSONS import EU_Depart_BeginTRJson, TRPickUp_JSON, FakeTRJson_Rejected

            DataCreation.RTM_APIRequest(UtrGrLocators.RTM_APIBeginTr, EU_Depart_BeginTRJson)
            DataCreation.RTM_APIRequest(UtrGrLocators.RTM_APIUpdateFakeTr, TRPickUp_JSON)
            DataCreation.RTM_APIRequest(UtrGrLocators.RTM_APIUpdateFakeTr, FakeTRJson_Rejected)

            DepartPackages.append(DPackage_ID)
        except:
            DepartPackages.append("Depart Status Update failed in RTM")
            print('Depart Status Update failed in RTM')
        sleep(3)
        print(DepartPackages)

    # Function to start ACP Tool
    def OpenACP():

        cmd = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE)
        cmd.stdin.write(b'cd\ \n')
        ccdir1 = (b'cd Users\\')
        ccdir2 = user.encode("utf-8")
        ccdir3 = (b'\Desktop\EU_Pick\n')
        ccdir = ccdir1 + ccdir2 + ccdir3
        cmd.stdin.write(ccdir)
        cmd.stdin.write(b'start create_picklist\n')
        sleep(5)

    # Function to create Test Data for Pick and Stage using ACP Tool
    def Pick():
        try:
            DataCreation.OpenACP()

            SL = 4
            global RouteName
            RouteName = ''.join(random.choices(string.ascii_uppercase, k=SL))
            print(RouteName)
            
            App = Application(backend= "uia").connect(title="Auto Create Picklist", timeout=50)
            #App.AutoCreatePicklist.print_control_identifiers()
            pywinauto.keyboard.send_keys('^{TAB}')
            pywinauto.keyboard.send_keys(RouteName)
            sleep(2)
            pywinauto.keyboard.send_keys('^{TAB}')
            pywinauto.keyboard.send_keys(EU_UtrGrUserInput.PickBagCount)
            sleep(2)
            pywinauto.keyboard.send_keys('^{TAB}')
            pywinauto.keyboard.send_keys(''+StubbedPackages[-2]+','+StubbedPackages[-3]+','+StubbedPackages[-4]+'')
            sleep(2)
            pywinauto.keyboard.send_keys('^{TAB}')
            pywinauto.keyboard.send_keys(''+StubbedPackages[-5]+','+StubbedPackages[-6]+'')
            sleep(2)
            pywinauto.keyboard.send_keys('^{TAB}')
            pywinauto.keyboard.send_keys(EU_UtrGrUserInput.PickColorCodes)
            sleep(2)
            pywinauto.keyboard.send_keys('^{TAB}')
            pywinauto.keyboard.send_keys(EU_UtrGrUserInput.PickLabels)
            sleep(2)
            pywinauto.keyboard.send_keys('^{TAB}')
            pywinauto.keyboard.send_keys(EU_UtrGrUserInput.PickSortLabels)
            sleep(2)
            pywinauto.keyboard.send_keys('^{TAB}')
            sleep(2)
            pywinauto.keyboard.send_keys('{VK_SPACE}')
            sleep(40)
            Result = Application(backend= "uia").connect(title="Result", timeout=50)
            #Result.Result.print_control_identifiers()
            RMenu = Result.Result.child_window(title="System", control_type="MenuItem")
            RMenu.click_input()
            sleep(2)
            RMenu.click_input()
            pywinauto.keyboard.send_keys('^{TAB}')
            pywinauto.keyboard.send_keys('^a')
            pywinauto.keyboard.send_keys('^c')
            sleep(3)
            global ACPResponse
            ACPResponse = pyperclip.paste()
            print(ACPResponse)
            Result.Result.child_window(title="Close", control_type="Button").click_input()
            App.AutoCreatePicklist.child_window(title="Close", control_type="Button").click_input()
        except:
            ACPResponse = 'ACP \n Failed'

    # Funtion to construct mail content
    def MailContent():

        DynamicPackages = DynamicPackagesList[:2]
        Mail_Header = '<font face="calibri"><strong> Hi All, </strong><br> Kindly use the below packages for EU Gamma Readiness Testing<br><br>'
        Mail_Header = Mail_Header + '<font face="calibri"><strong>MP: </strong>EU<br><strong>Station: </strong>TST3<br><strong>Depart Station: </strong>XYZ1<br><strong>Sort Zone: </strong>C1-1D<br><strong>Sort Zone Location: </strong>feb6307f-fd02-982b-26dc-ac8bf66edcd8 <br><strong>Pallet Location :</strong>74b981f6-4351-45b7-732e-078d9644ec34 (XYZ1)<br>'
        Mail_Header = Mail_Header + '<font face="calibri"><strong>Overflow Location :</strong>6eb9f14c-ffe6-6e81-026b-3fad4b506fe5 (XYZ1) <br><strong>Transporter :</strong>A1YMQBJ93G3WTE (TST3) / AK5H86HSFDJW6 (XYZ1)<br><br>'

        Mail_Body = '''
        <meta charset="utf-8"/>
        <style type = "text/css">
        table, th, td {border: 2px solid black; border-collapse: collapse; padding: 5px; text-align: center} 
        </style>
        <table>
        <tr>
            <th colspan="4" bgcolor="#90B8E0" style="text-align:center"><B><font face="Calibri">TEST DATA</th>
        </tr>
        <tr>
            <th bgcolor="#90B8E0" style="text-align:center"><B><font face="Calibri">Dynamic Packages</th>
            <th bgcolor="#90B8E0" style="text-align:center"><B><font face="Calibri">Induct / Stow / PS</th>
            <th bgcolor="#90B8E0" style="text-align:center"><B><font face="Calibri">RTS</th>
            <th bgcolor="#90B8E0" style="text-align:center"><B><font face="Calibri">Depart</th>
        </tr>'''
        Mail_Body = Mail_Body + '\n' + '<tr>'

        Mail_Body = Mail_Body + '\n' +'<td style="text-align:center">'
        for s in (DynamicPackages):
            Mail_Body = Mail_Body + '\n'+ s + ','
        Mail_Body = Mail_Body + '\n' + '</td>'

        Mail_Body = Mail_Body + '\n' +'<td style="text-align:center">'
        for l in (StubbedPackages[:-6]):
            Mail_Body = Mail_Body + '\n'+ l + ','
        Mail_Body = Mail_Body + '\n' + '</td>'
        Mail_Body = Mail_Body + '\n' +'<td style="text-align:center">'
        for m in (ReceivePackages):
            Mail_Body = Mail_Body + '\n'+ m + ','
        Mail_Body = Mail_Body + '\n' + '</td>'
        Mail_Body = Mail_Body + '\n' +'<td style="text-align:center">'   
        for n in (DepartPackages):
            Mail_Body = Mail_Body + '\n'+ n + ','
        Mail_Body = Mail_Body + '\n' + '</td>'
        
        Mail_Body = Mail_Body + '\n' + '</tr>'
        Mail_Body = Mail_Body + '\n' + '</table>' + '<br>'

        Mail_Body = Mail_Body + '''
        <meta charset="utf-8"/>
        <style type = "text/css">
        table, th, td {border:2px solid black; border-collapse:collapse; padding:5px} 
        </style>
        <table>
        <tr>
            <th colspan="4" bgcolor="#90B8E0" style="text-align:center"><B><font face="Calibri">ACP Response / Packages</th>
        </tr>'''

        PickOUTP = ACPResponse.split('\n')
        Mail_Body = Mail_Body + '\n' + '<tr>'
        Mail_Body = Mail_Body + '\n' +'<td style="text-align:left">'
        for p in PickOUTP:
            Mail_Body = Mail_Body + '\n'+ p + '<br>' 
        Mail_Body = Mail_Body + '\n' + '</td>'
        Mail_Body = Mail_Body + '\n' +'<td style="text-align:left"><strong>Bag Packages: </strong>'+StubbedPackages[-2]+','+StubbedPackages[-3]+','+StubbedPackages[-4]+'<br><strong>OV Packages: </strong>'+StubbedPackages[-5]+','+StubbedPackages[-6]+''
        Mail_Body = Mail_Body + '\n' + '</td>'
        Mail_Body = Mail_Body + '\n' + '</tr>'
        Mail_Body = Mail_Body + '\n' + '</table>'

        Mail_Footer = '<br><font face="calibri">This is an automated email. Do not reply.<br><br>Thanks,<br><strong>UTR-Tech QS BOT</strong>'
        EODReport = Mail_Header + Mail_Body + Mail_Footer

        return EODReport

    # Function to send mail
    def SendEmail():
        DataCreation.MailContent()

        To = "dolphin-qs@amazon.com"
        CC = "karjayap@amazon.com"
        Date = str(date.today())

        MailC = DataCreation.MailContent()
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = 'Gamma Readiness EU Test Data : '+Date+''
        MESSAGE['From'] = "Gamma-Readiness-TestData@amazon.com"
        MESSAGE['To'] = To
        MESSAGE['CC'] = CC

        HTML_BODY = MIMEText(MailC, 'html')
        MESSAGE.attach(HTML_BODY)

        smtpobj = smtplib.SMTP('smtp.amazon.com')
        smtpobj.sendmail("Gamma-Readiness-TestData@amazon.com", ["hdavisvi@amazon.com"], MESSAGE.as_string())
        #smtpobj.sendmail("Gamma-Readiness-TestData@amazon.com", ["hdavisvi@amazon.com", "karjayap@amazon.com", "thiyaaga@amazon.com", "dineannk@amazon.com", "gajayasa@amazon.com", "sivaperg@amazon.com", "hhemansk@amazon.com", "mjypr@amazon.com", "shrejaya@amazon.com", "bkarthii@amazon.com", "mtniranj@amazon.com", "pdmavak@amazon.com", "gpriyd@amazon.com", "raghnit@amazon.com", "srvpn@amazon.com", "tshali@amazon.com", "tpshashi@amazon.com", "sddhanra@amazon.com", "sosurenh@amazon.com", "soundrk@amazon.com", "anaaka@amazon.com", "skarunac@amazon.com", "bavath@amazon.com", "kdhashnh@amazon.com", "adhivaka@amazon.com", "vijaramy@amazon.com"], MESSAGE.as_string())
        smtpobj.quit()

    # Function to call the other funtions
    def GRTDC_Start():
        DataCreation.Auth()
        DataCreation.FlexCreatePackages(EU_UtrGrUserInput.MP, EU_UtrGrUserInput.PackageType, EU_UtrGrUserInput.ShipmentMethod, EU_UtrGrUserInput.Station, EU_UtrGrUserInput.DynamicPackage_Count)
        DataCreation.MCO_Package()
        DataCreation.RTS_RTM_StatusUpdate()
        DataCreation.Depart_RTM_StatusUpdate()
        driver.quit()
        DataCreation.Pick()
        DataCreation.SendEmail()
        
    
DataCreation.GRTDC_Start()