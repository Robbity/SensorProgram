import os
from ctypes import cdll
from ctypes import create_string_buffer
from ctypes import pointer
from ctypes import c_bool
from ctypes import c_uint8
from ctypes import c_uint16
from ctypes import c_uint32
from ctypes import c_float
from ctypes import c_double
from ctypes import c_char_p
from vicolibtypes import VersionType
from vicolibtypes import InterfaceType
from vicolibtypes import RunStatisticsType
from vicolibtypes import BaselineTrimType
from vicolibtypes import FirmwareVersionType
from vicolibtypes import MCUStatusInfoType
from vicolibtypes import ResetDetectionType
from vicolibtypes import TriggerSourceType
from vicolibtypes import TriggerTimeoutType
from vicolibtypes import EthernetProtocolType
from vicolibtypes import EthernetSpeedType
from vicolibtypes import SoftwarePackage
from vicolibtypes import BootloaderSessionType
from vicolibtypes import BootloaderReasonType
from vicolibtypes import LiveInfo1VICOType
from vicolibtypes import LiveInfo2VICOType
from vicolibtypes import LiveInfoBoundariesVICOType
from vicolibtypes import LiveInfo1VIAMPType
from vicolibtypes import LiveInfo2VIAMPType
from vicolibtypes import LiveInfoBoundariesVIAMPType
from vicolibtypes import DevInfo1BootloaderType
from vicolibtypes import DevInfo1VICOType
from vicolibtypes import TempType
from vicolibtypes import DbgClpType
from vicolibtypes import DbgClpExtType
from vicolibtypes import DPPStatusType
from vicolibtypes import VICOStatusType
from vicolibtypes import MCUStatusType

abspath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
cdll.LoadLibrary(f"{abspath}/Qt5Core.dll")
cdll.LoadLibrary(f"{abspath}/Qt5Network.dll")
_vicolib = cdll.LoadLibrary(f"{abspath}/VICOLib1.dll")

UINT_MIN = 0
UINT_8_MAX = 255
UINT_16_MAX = 65535
UINT_32_MAX = 4294967295

def getLibraryVersion():
    versionType = VersionType()
    statusType = _vicolib.getLibraryVersion(pointer(versionType))
    return {"vicoStatusType" : statusType, "major" : versionType.major, "minor" : versionType.minor, "patch" : versionType.patch, "build" : versionType.build}

def getDaemonVersion():
    versionType = VersionType()
    statusType = _vicolib.getDaemonVersion(pointer(versionType))
    return {"vicoStatusType" : statusType, "major" : versionType.major, "minor" : versionType.minor, "patch" : versionType.patch, "build" : versionType.build}

def scanTcpDevices(fromIpAddress, toIpAddress):
    fromIp = create_string_buffer(fromIpAddress.encode('UTF-8'), 15)
    toIp = create_string_buffer(toIpAddress.encode('UTF-8'), 15)
    statusType = _vicolib.scanTcpDevices(fromIp.value, toIp.value)
    return {"vicoStatusType" : statusType}

def cancelTcpScan():
    statusType = _vicolib.cancelTcpScan()
    return {"vicoStatusType" : statusType}

def scanUdpDevices(netaddress, netmask):
    if netmask < UINT_MIN or netmask > UINT_8_MAX:
        return {"vicoStatusType" : VICOStatusType.VICO_INVALID_ARGUMENT_ERROR}
    fromIp = create_string_buffer(netaddress.encode('UTF-8'), 15)
    nmask = c_uint8(netmask)
    statusType = _vicolib.scanUdpDevices(fromIp.value, pointer(nmask))
    return {"vicoStatusType" : statusType}

def cancelUdpScan():
    statusType = _vicolib.cancelUdpScan()
    return {"vicoStatusType" : statusType}

def scanUsbDevices():
    statusType = _vicolib.scanUsbDevices()
    return {"vicoStatusType" : statusType}

def getNumberOfDevices():
    numOfDev = c_uint8(0)
    statusType = _vicolib.getNumberOfDevices(pointer(numOfDev))
    return {"vicoStatusType" : statusType, "numberOfDevices" : numOfDev.value}

def getPreferredInterface(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    interfaceType = c_uint8(InterfaceType.INTERFACE_UNKNOWN)
    statusType = _vicolib.getPreferredInterface(serNum.value, pointer(interfaceType))
    return {"vicoStatusType" : statusType, "deviceInterface" : interfaceType.value}

def setPreferredInterface(serialNumber, deviceInterface):
    if deviceInterface < UINT_MIN or deviceInterface > UINT_8_MAX:
        return {"vicoStatusType" : VICOStatusType.VICO_INVALID_ARGUMENT_ERROR}
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setPreferredInterface(serNum.value, deviceInterface)
    return {"vicoStatusType" : statusType}

def getDeviceInfoByIndex(index):
    if index < UINT_MIN or index > UINT_8_MAX:
        return {"vicoStatusType" : VICOStatusType.VICO_INVALID_ARGUMENT_ERROR}
    size = 12
    serNumSize = c_uint8(size)
    serNum = create_string_buffer(size)
    interfaceType = c_uint32(InterfaceType.INTERFACE_UNKNOWN)
    statusType = _vicolib.getDeviceInfoByIndex(index, serNumSize.value, pointer(serNum), pointer(interfaceType))
    return {"vicoStatusType" : statusType, "serialNumber" : serNum.value.decode('UTF-8', "replace"), "deviceInterface" : interfaceType.value}

def refreshDeviceConnections():
    statusType = _vicolib.refreshDeviceConnections()
    return {"vicoStatusType" : statusType}

def startRun(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.startRun(serNum.value)
    return {"dppStatusType" : statusType}

def resumeRun(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.resumeRun(serNum.value)
    return {"dppStatusType" : statusType}

def stopRun(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.stopRun(serNum.value)
    return {"dppStatusType" : statusType}

def getStopCondition(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    stopCondType = c_uint32(0)
    stopCondVal = c_double(0)
    statusType = _vicolib.getStopCondition(serNum.value, pointer(stopCondType), pointer(stopCondVal))
    return {"dppStatusType" : statusType, "stopConditionType" : stopCondType.value, "stopConditionValue" : stopCondVal.value}

def setStopCondition(serialNumber, stopConditionType, stopConditionValue):
    if stopConditionType < UINT_MIN or stopConditionType > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    stopCondType = c_uint8(stopConditionType)
    stopCondVal = c_double(stopConditionValue)
    statusType = _vicolib.setStopCondition(serNum.value, stopCondType.value, pointer(stopCondVal))
    return {"dppStatusType" : statusType, "stopConditionValue" : stopCondVal.value}

def getRunStatus(serialNumber):
    isRunAct = c_bool(False)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getRunStatus(serNum.value, pointer(isRunAct))
    return {"dppStatusType" : statusType, "isRunActive" : isRunAct.value}

def getRunRealtime(serialNumber):
    rtime = c_double(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getRunRealtime(serNum.value, pointer(rtime))
    return {"dppStatusType" : statusType, "realtime" : rtime.value}

def getRunLivetime(serialNumber):
    ltime = c_double(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getRunLivetime(serNum.value, pointer(ltime))
    return {"dppStatusType" : statusType, "livetime" : ltime.value}

def getRunOutputCounts(serialNumber):
    ocounts = c_uint32(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getRunOutputCounts(serNum.value, pointer(ocounts))
    return {"dppStatusType" : statusType, "outputCounts" : ocounts.value}

def getRunInputCounts(serialNumber):
    icounts = c_uint32(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getRunInputCounts(serNum.value, pointer(icounts))
    return {"dppStatusType" : statusType, "inputCounts" : icounts.value}

def getRunOutputCountRate(serialNumber):
    ocr = c_uint32(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getRunOutputCountRate(serNum.value, pointer(ocr))
    return {"dppStatusType" : statusType, "outputCountRate" : ocr.value}

def getRunInputCountRate(serialNumber):
    icr = c_uint32(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getRunInputCountRate(serNum.value, pointer(icr))
    return {"dppStatusType" : statusType, "inputCountRate" : icr.value}

def getRunStatistics(serialNumber):
    rsType = RunStatisticsType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getRunStatistics(serNum.value, pointer(rsType))
    return {"dppStatusType" : statusType, "isRunActive" : rsType.isRunActive, "realtime" : rsType.realtime, "livetime" : rsType.livetime, "outputCounts" : rsType.outputCounts, "inputCounts" : rsType.inputCounts, "outputCountRate" : rsType.outputCountRate, "inputCountRate" : rsType.inputCountRate}

def getMCADataRaw(serialNumber, mcaDataSize):
    if mcaDataSize < UINT_MIN or mcaDataSize > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    size = c_uint16(mcaDataSize)
    mcaData = (c_uint8*mcaDataSize)()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMCADataRaw(serNum.value, size.value, pointer(mcaData))
    return {"dppStatusType" : statusType, "mcaData" : mcaData}

def getMCADataUInt32(serialNumber, bytesPerBin, numberOfBins):
    if bytesPerBin < UINT_MIN or bytesPerBin > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    if numberOfBins < UINT_MIN or numberOfBins > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    bpb = c_uint8(bytesPerBin)
    nob = c_uint16(numberOfBins)
    mcaData = (c_uint32*numberOfBins)()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMCADataUInt32(serNum.value, bpb.value, nob.value, pointer(mcaData))
    return {"dppStatusType" : statusType, "mcaData" : mcaData}

def getMCAData1BytePerBin(serialNumber, numberOfBins):
    if numberOfBins < UINT_MIN or numberOfBins > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    nob = c_uint16(numberOfBins)
    mcaData = (c_uint8*numberOfBins)()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMCAData1BytePerBin(serNum.value, nob.value, pointer(mcaData))
    return {"dppStatusType" : statusType, "mcaData" : mcaData}

def getMCAData2BytesPerBin(serialNumber, numberOfBins):
    if numberOfBins < UINT_MIN or numberOfBins > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    nob = c_uint16(numberOfBins)
    mcaData = (c_uint16*numberOfBins)()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMCAData2BytesPerBin(serNum.value, nob.value, pointer(mcaData))
    return {"dppStatusType" : statusType, "mcaData" : mcaData}

def getMCAData3BytesPerBin(serialNumber, numberOfBins):
    if numberOfBins < UINT_MIN or numberOfBins > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    nob = c_uint16(numberOfBins)
    mcaData = (c_uint32*numberOfBins)()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMCAData3BytesPerBin(serNum.value, nob.value, pointer(mcaData))
    return {"dppStatusType" : statusType, "mcaData" : mcaData}

def setMCANumberOfBins(serialNumber, numberOfBins):
    if numberOfBins < UINT_MIN or numberOfBins > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    nob = c_uint16(numberOfBins)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setMCANumberOfBins(serNum.value, pointer(nob))
    return {"dppStatusType" : statusType, "numberOfBins" : nob.value}

def getMCANumberOfBins(serialNumber):
    nob = c_uint16(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMCANumberOfBins(serNum.value, pointer(nob))
    return {"dppStatusType" : statusType, "numberOfBins" : nob.value}

def setMCABytesPerBin(serialNumber, bytesPerBin):
    if bytesPerBin < UINT_MIN or bytesPerBin > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    bpb = c_uint8(bytesPerBin)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setMCABytesPerBin(serNum.value, pointer(bpb))
    return {"dppStatusType" : statusType, "bytesPerBin" : bpb.value}

def getMCABytesPerBin(serialNumber):
    bpb = c_uint8(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMCABytesPerBin(serNum.value, pointer(bpb))
    return {"dppStatusType" : statusType, "bytesPerBin" : bpb.value}

def setFastFilterPeakingTime(serialNumber, peakingTime):
    pt = c_float(peakingTime)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setFastFilterPeakingTime(serNum.value, pointer(pt))
    return {"dppStatusType" : statusType, "peakingTime" : pt.value}

def getFastFilterPeakingTime(serialNumber):
    pt = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getFastFilterPeakingTime(serNum.value, pointer(pt))
    return {"dppStatusType" : statusType, "peakingTime" : pt.value}

def getFastFilterGapTime(serialNumber):
    gt = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getFastFilterGapTime(serNum.value, pointer(gt))
    return {"dppStatusType" : statusType, "gapTime" : gt.value}

def getMediumFilterPeakingTime(serialNumber):
    pt = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMediumFilterPeakingTime(serNum.value, pointer(pt))
    return {"dppStatusType" : statusType, "peakingTime" : pt.value}

def getMediumFilterGapTime(serialNumber):
    gt = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMediumFilterGapTime(serNum.value, pointer(gt))
    return {"dppStatusType" : statusType, "gapTime" : gt.value}

def setSlowFilterPeakingTime(serialNumber, peakingTime):
    pt = c_float(peakingTime)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setSlowFilterPeakingTime(serNum.value, pointer(pt))
    return {"dppStatusType" : statusType, "peakingTime" : pt.value}

def getSlowFilterPeakingTime(serialNumber):
    pt = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getSlowFilterPeakingTime(serNum.value, pointer(pt))
    return {"dppStatusType" : statusType, "peakingTime" : pt.value}

def setSlowFilterGapTime(serialNumber, peakingTime):
    gt = c_float(peakingTime)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setSlowFilterGapTime(serNum.value, pointer(gt))
    return {"dppStatusType" : statusType, "gapTime" : gt.value}

def getSlowFilterGapTime(serialNumber):
    gt = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getSlowFilterGapTime(serNum.value, pointer(gt))
    return {"dppStatusType" : statusType, "gapTime" : gt.value}

def setFastFilterTriggerThreshold(serialNumber, triggerThreshold):
    if triggerThreshold < UINT_MIN or triggerThreshold > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    tt = c_uint16(triggerThreshold)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setFastFilterTriggerThreshold(serNum.value, pointer(tt))
    return {"dppStatusType" : statusType, "triggerThreshold" : tt.value}

def getFastFilterTriggerThreshold(serialNumber):
    tt = c_uint16(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getFastFilterTriggerThreshold(serNum.value, pointer(tt))
    return {"dppStatusType" : statusType, "triggerThreshold" : tt.value}

def setMediumFilterTriggerThreshold(serialNumber, triggerThreshold):
    if triggerThreshold < UINT_MIN or triggerThreshold > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    tt = c_uint16(triggerThreshold)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setMediumFilterTriggerThreshold(serNum.value, pointer(tt))
    return {"dppStatusType" : statusType, "triggerThreshold" : tt.value}

def getMediumFilterTriggerThreshold(serialNumber):
    tt = c_uint16(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMediumFilterTriggerThreshold(serNum.value, pointer(tt))
    return {"dppStatusType" : statusType, "triggerThreshold" : tt.value}

def enableMediumFilterPulseDetection(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.enableMediumFilterPulseDetection(serNum.value)
    return {"dppStatusType" : statusType}

def disableMediumFilterPulseDetection(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.disableMediumFilterPulseDetection(serNum.value)
    return {"dppStatusType" : statusType}

def isMediumFilterPulseDetectionEnabled(serialNumber):
    pd = c_bool(False)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.isMediumFilterPulseDetectionEnabled(serNum.value, pointer(pd))
    return {"dppStatusType" : statusType, "enabled" : pd.value}

def setFastFilterMaxWidth(serialNumber, maxWidth):
    mw = c_float(maxWidth)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setFastFilterMaxWidth(serNum.value, pointer(mw))
    return {"dppStatusType" : statusType, "maxWidth" : mw.value}

def getFastFilterMaxWidth(serialNumber):
    tt = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getFastFilterMaxWidth(serNum.value, pointer(tt))
    return {"dppStatusType" : statusType, "maxWidth" : tt.value}

def setMediumFilterMaxWidth(serialNumber, maxWidth):
    mw = c_float(maxWidth)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setMediumFilterMaxWidth(serNum.value, pointer(mw))
    return {"dppStatusType" : statusType, "maxWidth" : mw.value}

def getMediumFilterMaxWidth(serialNumber):
    tt = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMediumFilterMaxWidth(serNum.value, pointer(tt))
    return {"dppStatusType" : statusType, "maxWidth" : tt.value}

def setResetInhibitTime(serialNumber, resetInhibitTime):
    rit = c_float(resetInhibitTime)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setResetInhibitTime(serNum.value, pointer(rit))
    return {"dppStatusType" : statusType, "resetInhibitTime" : rit.value}

def getResetInhibitTime(serialNumber):
    rit = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getResetInhibitTime(serNum.value, pointer(rit))
    return {"dppStatusType" : statusType, "resetInhibitTime" : rit.value}

def setBaselineAverageLength(serialNumber, averageLength):
    if averageLength < UINT_MIN or averageLength > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    bal = c_uint8(averageLength)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setBaselineAverageLength(serNum.value, pointer(bal))
    return {"dppStatusType" : statusType, "averageLength" : bal.value}

def getBaselineAverageLength(serialNumber):
    bal = c_uint8(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getBaselineAverageLength(serNum.value, pointer(bal))
    return {"dppStatusType" : statusType, "averageLength" : bal.value}

def setBaselineTrim(serialNumber, baselineTrim):
    if baselineTrim < UINT_MIN or baselineTrim > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setBaselineTrim(serNum.value, baselineTrim)
    return {"dppStatusType" : statusType}

def getBaselineTrim(serialNumber):
    bt = c_uint32(BaselineTrimType.LONGEST_POSSIBLE_MEDIUM_FILTER)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getBaselineTrim(serNum.value, pointer(bt))
    return {"dppStatusType" : statusType, "baselineTrim" : bt.value}

def enableBaselineCorrection(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.enableBaselineCorrection(serNum.value)
    return {"dppStatusType" : statusType}

def disableBaselineCorrection(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.disableBaselineCorrection(serNum.value)
    return {"dppStatusType" : statusType}

def isBaselineCorrectionEnabled(serialNumber):
    bc = c_bool(False)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.isBaselineCorrectionEnabled(serNum.value, pointer(bc))
    return {"dppStatusType" : statusType, "enabled" : bc.value}

def setDigitalEnergyGain(serialNumber, gain):
    if gain < UINT_MIN or gain > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    deg = c_uint16(gain)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setDigitalEnergyGain(serNum.value, pointer(deg))
    return {"dppStatusType" : statusType, "gain" : deg.value}

def getDigitalEnergyGain(serialNumber):
    deg = c_uint16(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getDigitalEnergyGain(serNum.value, pointer(deg))
    return {"dppStatusType" : statusType, "gain" : deg.value}

def setDigitalEnergyOffset(serialNumber, offset):
    if offset < UINT_MIN or offset > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    deg = c_uint16(offset)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setDigitalEnergyOffset(serNum.value, deg.value)
    return {"dppStatusType" : statusType, "offset" : deg.value}

def getDigitalEnergyOffset(serialNumber):
    deg = c_uint16(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getDigitalEnergyOffset(serNum.value, pointer(deg))
    return {"dppStatusType" : statusType, "offset" : deg.value}

def enableDynamicReset(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.enableDynamicReset(serNum.value)
    return {"dppStatusType" : statusType}

def disableDynamicReset(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.disableDynamicReset(serNum.value)
    return {"dppStatusType" : statusType}

def isDynamicResetEnabled(serialNumber):
    dr = c_bool(False)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.isDynamicResetEnabled(serNum.value, pointer(dr))
    return {"dppStatusType" : statusType, "enabled" : dr.value}

def setDynamicResetThreshold(serialNumber, threshold):
    if threshold < UINT_MIN or threshold > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    drt = c_uint16(threshold)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setDynamicResetThreshold(serNum.value, pointer(drt))
    return {"dppStatusType" : statusType, "threshold" : drt.value}

def getDynamicResetThreshold(serialNumber):
    drt = c_uint16(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getDynamicResetThreshold(serNum.value, pointer(drt))
    return {"dppStatusType" : statusType, "threshold" : drt.value}

def setDynamicResetDuration(serialNumber, duration):
    drd = c_float(duration)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setDynamicResetDuration(serNum.value, pointer(drd))
    return {"dppStatusType" : statusType, "duration" : drd.value}

def getDynamicResetDuration(serialNumber):
    drd = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getDynamicResetDuration(serNum.value, pointer(drd))
    return {"dppStatusType" : statusType, "duration" : drd.value}

def setResetDetection(serialNumber, resetDetection):
    if resetDetection < UINT_MIN or resetDetection > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    drd = c_uint8(resetDetection)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setResetDetection(serNum.value, drd.value)
    return {"dppStatusType" : statusType}

def getResetDetection(serialNumber):
    drd = c_uint8(ResetDetectionType.PIN)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getResetDetection(serNum.value, pointer(drd))
    return {"dppStatusType" : statusType, "resetDetection" : drd.value}

def loadDefaultParameterSet(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.loadDefaultParameterSet(serNum.value)
    return {"dppStatusType" : statusType}

def loadParameterSet(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.loadParameterSet(serNum.value)
    return {"dppStatusType" : statusType}

def saveDefaultParameterSet(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.saveDefaultParameterSet(serNum.value)
    return {"dppStatusType" : statusType}

def saveParameterSet(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.saveParameterSet(serNum.value)
    return {"dppStatusType" : statusType}

def getFirmwareVersion(serialNumber):
    vt = FirmwareVersionType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getFirmwareVersion(serNum.value, pointer(vt))
    return {"dppStatusType" : statusType, "major" : vt.major, "minor" : vt.minor, "patch" : vt.patch, "build" : vt.build, "variant" : vt.variant}

def getMCUStatusInfo(serialNumber):
    st = MCUStatusInfoType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getMCUStatusInfo(serNum.value, pointer(st))
    return {"dppStatusType" : statusType, "hasPower" : st.hasPower, "isReady" : st.isReady, "isAlmostReady" : st.isAlmostReady}

def getBoardTemperature(serialNumber):
    tmp = c_uint16(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getBoardTemperature(serNum.value, pointer(tmp))
    return {"dppStatusType" : statusType, "temperature" : tmp.value}

def enableAnalogHardwarePowerdown(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.enableAnalogHardwarePowerdown(serNum.value)
    return {"dppStatusType" : statusType}

def disableAnalogHardwarePowerdown(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.disableAnalogHardwarePowerdown(serNum.value)
    return {"dppStatusType" : statusType}

def isAnalogHardwarePowerdownEnabled(serialNumber):
    hp = c_bool(False)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.isAnalogHardwarePowerdownEnabled(serNum.value, pointer(hp))
    return {"dppStatusType" : statusType, "enabled" : hp.value}

def setClockingSpeed(serialNumber, clockingSpeed):
    if clockingSpeed < UINT_MIN or clockingSpeed > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setClockingSpeed(serNum.value, clockingSpeed)
    return {"dppStatusType" : statusType}

def getClockingSpeed(serialNumber):
    cs = c_uint8(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getClockingSpeed(serNum.value, pointer(cs))
    return {"dppStatusType" : statusType, "clockingSpeed" : cs.value}

def getAllParameters(serialNumber, allParametersSize):
    allParametersSizeVar = c_uint16(allParametersSize)
    allParameters = (c_uint8*allParametersSize)()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getAllParameters(serNum.value, allParametersSizeVar.value, allParameters)
    return {"dppStatusType" : statusType, "allParameters" : allParameters}

def setEventTriggerSource(serialNumber, triggerSource):
    if triggerSource < UINT_MIN or triggerSource > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    cs = c_uint8(triggerSource)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setEventTriggerSource(serNum.value, cs.value)
    return {"dppStatusType" : statusType}

def getEventTriggerSource(serialNumber):
    cs = c_uint8(TriggerSourceType.INSTANT_TRIGGER)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getEventTriggerSource(serNum.value, pointer(cs))
    return {"dppStatusType" : statusType, "triggerSource" : cs.value}

def setEventTriggerValue(serialNumber, triggerValue):
    if triggerValue < UINT_MIN or triggerValue > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    tv = c_uint16(triggerValue)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setEventTriggerValue(serNum.value, tv.value)
    return {"dppStatusType" : statusType}

def getEventTriggerValue(serialNumber):
    tv = c_uint16(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getEventTriggerValue(serNum.value, pointer(tv))
    return {"dppStatusType" : statusType, "triggerValue" : tv.value}

def setEventScopeSamplingInterval(serialNumber, samplingInterval):
    if samplingInterval < UINT_MIN or samplingInterval > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    samplingIntervalVar = c_uint16(samplingInterval)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setEventScopeSamplingInterval(serNum.value, pointer(samplingIntervalVar))
    return {"dppStatusType" : statusType, "samplingInterval" : samplingIntervalVar.value}

def getEventScopeSamplingInterval(serialNumber):
    si = c_uint16(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getEventScopeSamplingInterval(serNum.value, pointer(si))
    return {"dppStatusType" : statusType, "samplingInterval" : si.value}

def setEventScopeTriggerTimeout(serialNumber, triggerTimeout):
    if triggerTimeout < UINT_MIN or triggerTimeout > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setEventScopeTriggerTimeout(serNum.value, triggerTimeout)
    return {"dppStatusType" : statusType}

def getEventScopeTriggerTimeout(serialNumber):
    tt = c_uint8(TriggerTimeoutType.TIMEOUT_1_SECOND)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getEventScopeTriggerTimeout(serNum.value, pointer(tt))
    return {"dppStatusType" : statusType, "triggerTimeout" : tt.value}

def getEventScope(serialNumber, eventScopeType):
    if eventScopeType < UINT_MIN or eventScopeType > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    est = c_uint8(eventScopeType)
    eventScopeSize = 8192
    ess = c_uint16(eventScopeSize)
    eventScope = (c_uint32*eventScopeSize)()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getEventScope(serNum.value, est.value, ess.value, pointer(eventScope))
    return {"dppStatusType" : statusType, "eventScope" : eventScope}

def calculateEventRate(serialNumber, triggerDuration):
    if triggerDuration < UINT_MIN or triggerDuration > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    triggerTimeVal = c_uint32(triggerDuration)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.calculateEventRate(serNum.value, triggerTimeVal.value)
    return {"dppStatusType" : statusType}

def deleteFirmware(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.deleteFirmware(serNum.value)
    return {"dppStatusType" : statusType}

def writeFirmwareSection(serialNumber, segmentNumber, firmwareSection):
    if segmentNumber < UINT_MIN or segmentNumber > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    segNo = c_uint16(segmentNumber)
    firmwareSectionSize = 1024
    fss = c_uint16(firmwareSectionSize)
    firmware = (c_uint8*firmwareSectionSize)(*firmwareSection)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.writeFirmwareSection(serNum.value, pointer(segNo), fss.value, firmware)
    return {"dppStatusType" : statusType, "segmentNumber" : segNo.value}

def readFirmwareSection(serialNumber, segmentNumber):
    if segmentNumber < UINT_MIN or segmentNumber > UINT_16_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    segNo = c_uint16(segmentNumber)
    firmwareSectionSize = 1024
    fss = c_uint16(firmwareSectionSize)
    fs = (c_uint8*firmwareSectionSize)()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.readFirmwareSection(serNum.value, pointer(segNo), fss.value, pointer(fs))
    return {"dppStatusType" : statusType, "segmentNumber" : segNo.value, "firmwareSection" : fs}

def getEventRate(serialNumber):
    si = c_uint32(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getEventRate(serNum.value, pointer(si))
    return {"dppStatusType" : statusType, "eventRate" : si.value}

def setServiceCode(serialNumber, serviceCode):
    if serviceCode < UINT_MIN or serviceCode > UINT_32_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setServiceCode(serNum.value, serviceCode)
    return {"dppStatusType" : statusType}

def getServiceCode(serialNumber):
    sc = c_uint32(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getServiceCode(serNum.value, pointer(sc))
    return {"dppStatusType" : statusType, "serviceCode" : sc.value}

def enableEthernetPowerdown(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.enableEthernetPowerdown(serNum.value)
    return {"dppStatusType" : statusType}

def disableEthernetPowerdown(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.disableEthernetPowerdown(serNum.value)
    return {"dppStatusType" : statusType}

def isEthernetPowerdownEnabled(serialNumber):
    ep = c_bool(False)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.isEthernetPowerdownEnabled(serNum.value, pointer(ep))
    return {"dppStatusType" : statusType, "enabled" : ep.value}

def setEthernetProtocol(serialNumber, ethernetProtocol):
    if ethernetProtocol < UINT_MIN or ethernetProtocol > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    ep = c_uint8(ethernetProtocol)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setEthernetProtocol(serNum.value, ep.value)
    return {"dppStatusType" : statusType}

def getEthernetProtocol(serialNumber):
    ep = c_uint8(EthernetProtocolType.TCP)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getEthernetProtocol(serNum.value, pointer(ep))
    return {"dppStatusType" : statusType, "ethernetProtocol" : ep.value}

def setEthernetSpeed(serialNumber, ethernetSpeed):
    if ethernetSpeed < UINT_MIN or ethernetSpeed > UINT_8_MAX:
        return {"dppStatusType" : DPPStatusType.DPP_INVALID_ARGUMENT_ERROR}
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setEthernetSpeed(serNum.value, ethernetSpeed)
    return {"dppStatusType" : statusType}

def getEthernetSpeed(serialNumber):
    ep = c_uint32(EthernetSpeedType.AUTO_NEGOTIATION)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getEthernetSpeed(serNum.value, pointer(ep))
    return {"dppStatusType" : statusType, "ethernetSpeed" : ep.value}

def setIPAddress(serialNumber, ipAddress):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    ipAddr = create_string_buffer(ipAddress.encode('UTF-8'), 15)
    statusType = _vicolib.setIPAddress(serNum.value, ipAddr.value)
    return {"dppStatusType" : statusType}

def getIPAddress(serialNumber):
    size = 15
    ipAddressSizeVar = c_uint8(size)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    ipAddr = create_string_buffer(size)
    statusType = _vicolib.getIPAddress(serNum.value, ipAddressSizeVar.value, pointer(ipAddr))
    return {"dppStatusType" : statusType, "ipAddress" : ipAddr.value.decode('UTF-8', "replace")}

def setSubnetMask(serialNumber, subnetMask):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    ipAddr = create_string_buffer(subnetMask.encode('UTF-8'), 15)
    statusType = _vicolib.setSubnetMask(serNum.value, ipAddr.value)
    return {"dppStatusType" : statusType}

def getSubnetMask(serialNumber):
    size = 15
    subnetMaskSizeVar = c_uint8(size)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    ipAddr = create_string_buffer(size)
    statusType = _vicolib.getSubnetMask(serNum.value, subnetMaskSizeVar.value, pointer(ipAddr))
    return {"dppStatusType" : statusType, "subnetMask" : ipAddr.value.decode('UTF-8', "replace")}

def setGatewayIPAddress(serialNumber, gatewayIpAddress):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    ipAddr = create_string_buffer(gatewayIpAddress.encode('UTF-8'), 15)
    statusType = _vicolib.setGatewayIPAddress(serNum.value, ipAddr.value)
    return {"dppStatusType" : statusType}

def getGatewayIPAddress(serialNumber):
    size = 15
    gatewayIpAddressSizeVar = c_uint8(size)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    ipAddr = create_string_buffer(size)
    statusType = _vicolib.getGatewayIPAddress(serNum.value, gatewayIpAddressSizeVar.value, pointer(ipAddr))
    return {"dppStatusType" : statusType, "gatewayIpAddress" : ipAddr.value.decode('UTF-8', "replace")}

def getEthernetPort(serialNumber):
    ep = c_uint16(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getEthernetPort(serNum.value, pointer(ep))
    return {"dppStatusType" : statusType, "ethernetPort" : ep.value}

def setMACAddress(serialNumber, macAddress):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    mac = create_string_buffer(macAddress.encode('UTF-8'), 17)
    statusType = _vicolib.setMACAddress(serNum.value, mac.value)
    return {"dppStatusType" : statusType}

def getMACAddress(serialNumber):
    size = 17
    macAddrSize = c_uint8(size)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    mac = create_string_buffer(size)
    statusType = _vicolib.getMACAddress(serNum.value, macAddrSize, pointer(mac))
    return {"dppStatusType" : statusType, "macAddress" : mac.value.decode('UTF-8', "replace")}

def applyEthernetConfiguration(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.applyEthernetConfiguration(serNum.value)
    return {"dppStatusType" : statusType}

def enableUSBPowerdown(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.enableUSBPowerdown(serNum.value)
    return {"dppStatusType" : statusType}

def disableUSBPowerdown(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.disableUSBPowerdown(serNum.value)
    return {"dppStatusType" : statusType}

def isUSBPowerdownEnabled(serialNumber):
    up = c_bool(False)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.isUSBPowerdownEnabled(serNum.value, pointer(up))
    return {"dppStatusType" : statusType, "enabled" : up.value}

def enableSPIPowerdown(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.enableSPIPowerdown(serNum.value)
    return {"dppStatusType" : statusType}

def disableSPIPowerdown(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.disableSPIPowerdown(serNum.value)
    return {"dppStatusType" : statusType}

def isSPIPowerdownEnabled(serialNumber):
    up = c_bool(False)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.isSPIPowerdownEnabled(serNum.value, pointer(up))
    return {"dppStatusType" : statusType, "enabled" : up.value}
    
def swPkgGetActive(serialNumber):
    pkg = c_uint8(SoftwarePackage.Bootloader)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.swPkgGetActive(serNum.value, pointer(pkg))
    return {"mcuStatusType" : statusType, "swPkg" : pkg.value}

def flashRead(serialNumber, addStart, length):
    if addStart < UINT_MIN or addStart > UINT_32_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    if length < UINT_MIN or length > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    addStartVar = c_uint32(addStart)
    lengthVar = c_uint8(length)
    data = (c_uint8*length)()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.flashRead(serNum.value, addStartVar.value, lengthVar.value, pointer(data))
    return {"mcuStatusType" : statusType, "data" : data}

def flashWriteSessionStart(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.flashWriteSessionStart(serNum.value)
    return {"mcuStatusType" : statusType}

def flashWriteSessionExit(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.flashWriteSessionExit(serNum.value)
    return {"mcuStatusType" : statusType}

def flashWriteSessionReset(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.flashWriteSessionReset(serNum.value)
    return {"mcuStatusType" : statusType}

def flashWriteSessionData(serialNumber, addStart, data):
    if addStart < UINT_MIN or addStart > UINT_32_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    addStartVar = c_uint32(addStart)
    dataSize = 128
    firmware = (c_uint8*dataSize)(*data)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.flashWriteSessionData(serNum.value, addStartVar.value, firmware)
    return {"mcuStatusType" : statusType}

def blGetSession(serialNumber):
    blSession = c_uint8(BootloaderSessionType.Default)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.blGetSession(serNum.value, pointer(blSession))
    return {"mcuStatusType" : statusType, "blSession" : blSession.value}

def blGetReason(serialNumber):
    blReason = c_uint8(BootloaderReasonType.RescuePinActive)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.blGetReason(serNum.value, pointer(blReason))
    return {"mcuStatusType" : statusType, "blReason" : blReason.value}

def swPkgStartApplication(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.swPkgStartApplication(serNum.value)
    return {"mcuStatusType" : statusType}

def swPkgStartBootloader(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.swPkgStartBootloader(serNum.value)
    return {"mcuStatusType" : statusType}

def liveInfo1VICO(serialNumber):
    liveInfo = LiveInfo1VICOType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.liveInfo1VICO(serNum.value, pointer(liveInfo))
    return {"mcuStatusType" : statusType, "st" : liveInfo.st, "er" : liveInfo.er, "vIn" : liveInfo.vIn, "pwr" : liveInfo.pwr, "therm1" : liveInfo.therm1, "therm2" : liveInfo.therm2}

def liveInfo2VICO(serialNumber):
    liveInfo = LiveInfo2VICOType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.liveInfo2VICO(serNum.value, pointer(liveInfo))
    return {"mcuStatusType" : statusType, "st" : liveInfo.st, "er" : liveInfo.er, "vIn" : liveInfo.vIn, "p5v" : liveInfo.p5v, "n5vActive" : liveInfo.n5vActive, "mcu3v3" : liveInfo.mcu3v3, "ref2v5" : liveInfo.ref2v5, "hvActive" : liveInfo.hvActive, "hvDac" : liveInfo.hvDac, "hv" : liveInfo.hv, "pwr" : liveInfo.pwr, "usb" : liveInfo.usb, "gpio" : liveInfo.gpio, "reqfbl" : liveInfo.reqfbl, "fpga3v3" : liveInfo.fpga3v3, "therm1" : liveInfo.therm1, "therm2" : liveInfo.therm2}

def liveInfoBoundariesVICO(serialNumber):
    liveInfo = LiveInfoBoundariesVICOType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.liveInfoBoundariesVICO(serNum.value, pointer(liveInfo))
    return {"mcuStatusType" : statusType, "vInMin" : liveInfo.vInMin, "vInMax" : liveInfo.vInMax, "p5vMin" : liveInfo.p5vMin, "p5vMax" : liveInfo.p5vMax, "mcu3v3Min" : liveInfo.mcu3v3Min, "mcu3v3Max" : liveInfo.mcu3v3Max, "ref2v5Min" : liveInfo.ref2v5Min, "ref2v5Max" : liveInfo.ref2v5Max, "hvMin" : liveInfo.hvMin, "hvMax" : liveInfo.hvMax, "therm1Max" : liveInfo.therm1Max, "therm2Max" : liveInfo.therm2Max}

def liveInfo1VIAMP(serialNumber):
    liveInfo = LiveInfo1VIAMPType(0,0,0,0,0,0,0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.liveInfo1VIAMP(serNum.value, pointer(liveInfo))
    return {"mcuStatusType" : statusType, "st" : liveInfo.st, "er" : liveInfo.er, "itec" : liveInfo.itec, "utec" : liveInfo.utec, "sddTmp" : liveInfo.sddTmp, "rdy" : liveInfo.rdy, "hotSide" : liveInfo.hotSide}

def liveInfo2VIAMP(serialNumber):
    liveInfo = LiveInfo2VIAMPType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.liveInfo2VIAMP(serNum.value, pointer(liveInfo))
    return {"mcuStatusType" : statusType, "st" : liveInfo.st, "er" : liveInfo.er, "viampAdc" : liveInfo.viampAdc, "r1" : liveInfo.r1, "bk" : liveInfo.bk, "rx" : liveInfo.rx, "itec" : liveInfo.itec, "utec" : liveInfo.utec, "sddTmp" : liveInfo.sddTmp, "targetTmp" : liveInfo.targetTmp, "rdy" : liveInfo.rdy, "ardy" : liveInfo.ardy, "hotSide" : liveInfo.hotSide, "monSigFinal" : liveInfo.monSigFinal, "ctrlSigFinal" : liveInfo.ctrlSigFinal, "iPartLimit" : liveInfo.iPartLimit, "tecActive" : liveInfo.tecActive, "tecDac" : liveInfo.tecDac, "pPart" : liveInfo.pPart, "iPart" : liveInfo.iPart, "dPart" : liveInfo.dPart}

def liveInfoBoundariesVIAMP(serialNumber):
    liveInfo = LiveInfoBoundariesVIAMPType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.liveInfoBoundariesVIAMP(serNum.value, pointer(liveInfo))
    return {"mcuStatusType" : statusType, "viampAdcMin" : liveInfo.viampAdcMin, "viampAdcMax" : liveInfo.viampAdcMax, "r1Min" : liveInfo.r1Min, "r1Max" : liveInfo.r1Max, "bkMin" : liveInfo.bkMin, "bkMax" : liveInfo.bkMax, "rxMin" : liveInfo.rxMin, "rxMax" : liveInfo.rxMax, "itecMax" : liveInfo.itecMax, "utecMax" : liveInfo.utecMax, "kp" : liveInfo.kp, "ki" : liveInfo.ki, "kd" : liveInfo.kd}

def devInfo1Bootloader(serialNumber):
    devInfo = DevInfo1BootloaderType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.devInfo1Bootloader(serNum.value, pointer(devInfo))
    return {"mcuStatusType" : statusType, "smj" : devInfo.smj, "smi" : devInfo.smi, "sms" : devInfo.sms, "smb" : devInfo.smb}

def devInfo1VICO(serialNumber):
    devInfo = DevInfo1VICOType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.devInfo1VICO(serNum.value, pointer(devInfo))
    return {"mcuStatusType" : statusType, "smj" : devInfo.smj, "smi" : devInfo.smi, "sms" : devInfo.sms, "smb" : devInfo.smb}

def devInfo2VICO(serialNumber):
    size = 21
    infoSizeVar = c_uint8(size)
    voPcbArtNo = create_string_buffer(size)
    voPcbSerNo = create_string_buffer(size)
    voProdArtNo = create_string_buffer(size)
    voProdSerNo = create_string_buffer(size)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.devInfo2VICO(serNum.value, infoSizeVar.value, pointer(voPcbArtNo), pointer(voPcbSerNo), pointer(voProdArtNo), pointer(voProdSerNo))
    return {"mcuStatusType" : statusType, "voPcbArtNo" : voPcbArtNo.value.decode('UTF-8', "replace"), "voPcbSerNo" : voPcbSerNo.value.decode('UTF-8', "replace"), "voProdArtNo" : voProdArtNo.value.decode('UTF-8', "replace"), "voProdSerNo" : voProdSerNo.value.decode('UTF-8', "replace")}

def devInfo1VIAMP(serialNumber):
    size = 21
    infoSizeVar = c_uint8(size)
    vpPcbArtNo = create_string_buffer(size)
    vpPcbSerNo = create_string_buffer(size)
    vpProdArtNo = create_string_buffer(size)
    vpProdSerNo = create_string_buffer(size)
    targetTmpEep = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.devInfo1VIAMP(serNum.value, infoSizeVar.value, pointer(vpPcbArtNo), pointer(vpPcbSerNo), pointer(vpProdArtNo), pointer(vpProdSerNo), pointer(targetTmpEep))
    return {"mcuStatusType" : statusType, "vpPcbArtNo" : vpPcbArtNo.value.decode('UTF-8', "replace"), "vpPcbSerNo" : vpPcbSerNo.value.decode('UTF-8', "replace"), "vpProdArtNo" : vpProdArtNo.value.decode('UTF-8', "replace"), "vpProdSerNo" : vpProdSerNo.value.decode('UTF-8', "replace"), "targetTmpEep" : targetTmpEep.value}

def setMode(serialNumber, md):
    if md < UINT_MIN or md > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    mdVar = c_uint8(md)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setMode(serNum.value, mdVar.value)
    return {"mcuStatusType" : statusType}

def resetMCU(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.resetMCU(serNum.value)
    return {"mcuStatusType" : statusType}

def resetFPGA(serialNumber):
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.resetFPGA(serNum.value)
    return {"mcuStatusType" : statusType}

def getTemp(serialNumber):
    temp = TempType(0,0,False, False)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getTemp(serNum.value, pointer(temp))
    return {"mcuStatusType" : statusType, "sddTmp" : temp.sddTmp, "targetTmp" : temp.targetTmp, "rdy" : temp.rdy, "ardy" : temp.ardy}

def setTemp(serialNumber, targetTmp):
    targetTmpVar = c_float(targetTmp)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    _vicolib.setTemp.argtypes = [c_char_p, c_float]
    statusType = _vicolib.setTemp(serNum.value, targetTmpVar)
    return {"mcuStatusType" : statusType}

def setRdy(serialNumber, dvtn, prd):
    dvtnVar = c_float(dvtn)
    prdVar = c_float(prd)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setRdy(serNum.value, dvtnVar.value, prdVar.value)
    return {"mcuStatusType" : statusType}

def setARdy(serialNumber, dvtn, prd):
    dvtnVar = c_float(dvtn)
    prdVar = c_float(prd)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setARdy(serNum.value, dvtnVar.value, prdVar.value)
    return {"mcuStatusType" : statusType}

def getRdy(serialNumber):
    dvtnVar = c_float(0)
    prdVar = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getRdy(serNum.value, pointer(dvtnVar), pointer(prdVar))
    return {"mcuStatusType" : statusType, "dvtn" : dvtnVar.value, "prd" : prdVar.value}

def getARdy(serialNumber):
    dvtnVar = c_float(0)
    prdVar = c_float(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getARdy(serNum.value, pointer(dvtnVar), pointer(prdVar))
    return {"mcuStatusType" : statusType, "dvtn" : dvtnVar.value, "prd" : prdVar.value}

def getEEP(serialNumber, addStart, length):
    if addStart < UINT_MIN or addStart > UINT_16_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    if length < UINT_MIN or length > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    addStartVar = c_uint16(addStart)
    lengthVar = c_uint8(length)
    data = (c_uint8*length)()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getEEP(serNum.value, addStartVar.value, lengthVar.value, pointer(data))
    return {"mcuStatusType" : statusType, "data" : data}

def setEEP(serialNumber, addStart, length, data):
    if addStart < UINT_MIN or addStart > UINT_16_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    if length < UINT_MIN or length > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    addStartVar = c_uint16(addStart)
    lengthVar = c_uint8(length)
    dataVar = (c_uint8*length)(*data)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setEEP(serNum.value, addStartVar.value, lengthVar.value, dataVar)
    return {"mcuStatusType" : statusType}

def twi(serialNumber, ad, md, ses, res, sendData):
    if ad < UINT_MIN or ad > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    if md < UINT_MIN or md > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    if ses < UINT_MIN or ses > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    if res < UINT_MIN or res > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    adVar = c_uint8(ad)
    mdVar = c_uint8(md)
    sesVar = c_uint8(ses)
    resVar = c_uint8(res)
    sendDataVar = (c_uint8*len(sendData))(*sendData)
    
    recData = (c_uint8*res)()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.twi(serNum.value, adVar.value, mdVar.value, sesVar.value, resVar.value, sendDataVar, pointer(recData))
    return {"mcuStatusType" : statusType, "recData" : recData}

def getIO(serialNumber, por, pin):
    if por < UINT_MIN or por > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    if pin < UINT_MIN or pin > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    porVar = c_uint8(por)
    pinVar = c_uint8(pin)
    valVar = c_bool(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getIO(serNum.value, porVar.value, pinVar.value, pointer(valVar))
    return {"mcuStatusType" : statusType, "val" : valVar.value}

def setIO(serialNumber, por, pin, val):
    if por < UINT_MIN or por > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    if pin < UINT_MIN or pin > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    porVar = c_uint8(por)
    pinVar = c_uint8(pin)
    valVar = c_bool(val)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setIO(serNum.value, porVar.value, pinVar.value, valVar.value)
    return {"mcuStatusType" : statusType}

def getADC(serialNumber, por, pin):
    if por < UINT_MIN or por > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    if pin < UINT_MIN or pin > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    porVar = c_uint8(por)
    pinVar = c_uint8(pin)
    adcVar = c_uint16(0)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.getADC(serNum.value, porVar.value, pinVar.value, pointer(adcVar))
    return {"mcuStatusType" : statusType, "adcVal" : adcVar.value}

def setDAC(serialNumber, por, pin, dacVal):
    if por < UINT_MIN or por > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    if pin < UINT_MIN or pin > UINT_8_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    if dacVal < UINT_MIN or dacVal > UINT_16_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    porVar = c_uint8(por)
    pinVar = c_uint8(pin)
    valVar = c_uint16(dacVal)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setDAC(serNum.value, porVar.value, pinVar.value, valVar.value)
    return {"mcuStatusType" : statusType}

def setIMax(serialNumber, itecMax):
    if itecMax < UINT_MIN or itecMax > UINT_16_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    itecMaxVar = c_uint16(itecMax)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setIMax(serNum.value, itecMaxVar.value)
    return {"mcuStatusType" : statusType}

def setUMax(serialNumber, utecMax):
    if utecMax < UINT_MIN or utecMax > UINT_16_MAX:
        return {"mcuStatusType" : MCUStatusType.MCU_INVALID_ARGUMENT_ERROR}
    utecMaxVar = c_uint16(utecMax)
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.setUMax(serNum.value, utecMaxVar.value)
    return {"mcuStatusType" : statusType}

def dbgClp(serialNumber):
    dbgClpVar = DbgClpType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.dbgClp(serNum.value, pointer(dbgClpVar))
    return {"mcuStatusType" : statusType, "stepCounter" : dbgClpVar.stepCounter, "sddTmp" : dbgClpVar.sddTmp, "itec" : dbgClpVar.itec, "utec" : dbgClpVar.utec, "monSigFinal" : dbgClpVar.monSigFinal, "pPart" : dbgClpVar.pPart, "iPart" : dbgClpVar.iPart, "rdy" : dbgClpVar.rdy}

def dbgClpExt(serialNumber):
    dbgClpExtVar = DbgClpExtType()
    serNum = create_string_buffer(serialNumber.encode('UTF-8'), 12)
    statusType = _vicolib.dbgClpExt(serNum.value, pointer(dbgClpExtVar))
    return {"mcuStatusType" : statusType, "stepCounter" : dbgClpExtVar.stepCounter, "targetTmp" : dbgClpExtVar.targetTmp, "sddTmp" : dbgClpExtVar.sddTmp, "itec" : dbgClpExtVar.itec, "utec" : dbgClpExtVar.utec, "monStepSize" : dbgClpExtVar.monStepSize, "monSigFinal" : dbgClpExtVar.monSigFinal, "ctrlSigFinal" : dbgClpExtVar.ctrlSigFinal, "pPart" : dbgClpExtVar.pPart, "iPart" : dbgClpExtVar.iPart, "iPartLimit" : dbgClpExtVar.iPartLimit, "dPart" : dbgClpExtVar.dPart, "rdy" : dbgClpExtVar.rdy, "aRdy" : dbgClpExtVar.aRdy, "grnLed" : dbgClpExtVar.grnLed, "hotSide" : dbgClpExtVar.hotSide}
