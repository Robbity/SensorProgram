from vicolib import scanTcpDevices
from vicolib import scanUsbDevices
from vicolib import getNumberOfDevices
from vicolib import getDeviceInfoByIndex
from vicolib import getIPAddress
from vicolib import setSlowFilterPeakingTime
from vicolib import setStopCondition
from vicolib import setMCANumberOfBins
from vicolib import setMCABytesPerBin
from vicolib import startRun
from vicolib import getRunStatus
from vicolib import getRunStatistics
from vicolib import getMCADataUInt32

from vicolibtypes import MCUStatusType
from vicolibtypes import DPPStatusType
from vicolibtypes import VICOStatusType
from vicolibtypes import InterfaceType
from vicolibtypes import StopConditionType

import time

# Simple error handling function
def CHECK_ERROR(status):
    if status != 0x00:
        print("Error encountered! Status =", status)
        TimeoutError("Error encountered! Status =", status)

def saveSpectrumToFile(intArray, numberOfBins, fileName):
    file=open(fileName,"w");
    for i in range (0, numberOfBins):
        file.write(str(intArray[i])+'\n')
    print("Spectrum successfully saved to file", fileName);
    file.close()
    

# Scan USB and Ethernet interfaces (in a range between 192.168.0.2 and 192.168.0.3) for KETEK DPP3 devices
response = scanUsbDevices()
CHECK_ERROR(response.get("vicoStatusType"))
response = scanTcpDevices('192.168.0.2', '192.168.0.3');
CHECK_ERROR(response.get("vicoStatusType"))

response = getNumberOfDevices()
CHECK_ERROR(response.get("vicoStatusType"))
numberOfDevices = response.get("numberOfDevices")
if (numberOfDevices == 0):
    print("No device found. Aborting.")
    TimeoutError("No device found. Aborting.")

# Display all found devices
print("Successfully found ", numberOfDevices, " devices.")
for i in range(numberOfDevices):
    response = getDeviceInfoByIndex(i)
    CHECK_ERROR(response.get("vicoStatusType"))
    serialNumber = response.get("serialNumber")
    deviceInterface = response.get("deviceInterface")
    print("Device #", i, " serial number:", serialNumber)
    if deviceInterface == InterfaceType.INTERFACE_ETHERNET_TCP:
        response = getIPAddress(serialNumber)
        CHECK_ERROR(response.get("dppStatusType"))
        ipAddress = response.get("ipAddress")
        print("connected over TCP interface with IP ", ipAddress)
    elif deviceInterface == InterfaceType.INTERFACE_ETHERNET_UDP:
        print("connected over UDP interface")
    elif deviceInterface == InterfaceType.INTERFACE_USB:
        print("connected over USB interface")
    elif deviceInterface == InterfaceType.INTERFACE_UNKNOWN:
        print("connected over unkown interface")

# In this example just proceed with the first found device
response = getDeviceInfoByIndex(0);
CHECK_ERROR(response.get("vicoStatusType"))
serialNumber = response.get("serialNumber")
response = getIPAddress(serialNumber)
CHECK_ERROR(response.get("dppStatusType"))
ipAddress = response.get("ipAddress")
print("Successfully initialized device with serial number ", serialNumber, " and IP address ", ipAddress)

# Set peaking time to 1 µs (1000 ns) and verify the setting. This new value will not be stored in the non-volatile memory though
peakingTime = 1000
response = setSlowFilterPeakingTime(serialNumber, peakingTime)
CHECK_ERROR(response.get("dppStatusType"))
print("Successfully set the peaking time to ", peakingTime, "ns")

# Set the measurement time to 10 s (realtime)
measurementTime = 10
response = setStopCondition(serialNumber, StopConditionType.STOP_AT_FIXED_REALTIME, measurementTime)
CHECK_ERROR(response.get("dppStatusType"))
measurementTime = response.get("stopConditionValue")
print("Successfully set the measurement time to " , measurementTime, "s")

# Set number of bins in spectrum to 4096 and bytes per bin to 3
numberOfBins = 4096
bytesPerBin = 3
response = setMCANumberOfBins(serialNumber, numberOfBins)
CHECK_ERROR(response.get("dppStatusType"))
print("Successfully set number of bins to ", numberOfBins)
response = setMCABytesPerBin(serialNumber, bytesPerBin)
CHECK_ERROR(response.get("dppStatusType"))
print("Successfully set bytes per bin to ", bytesPerBin)