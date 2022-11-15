import enum
import ctypes

class VICOStatusType(enum.IntEnum):
    VICO_SUCCESS =                              0x00
    VICO_NO_DEVICE_WITH_ID_CONNECTED_ERROR =    0x50
    VICO_VICODAEMON_IS_STOPPED =                0x51
    VICO_VICOLIB_TIMEOUT_ERROR =                0x52
    VICO_RESPONSE_OUT_OF_BOUNDS_ERROR =         0x53
    VICO_INVALID_ARGUMENT_ERROR =               0x54
    VICO_INVALID_RESPONSE_DATA_ERROR =          0x55
    VICO_UNDEFINED_ERROR =                      0xFF

class InterfaceType(enum.IntEnum):
    INTERFACE_UNKNOWN =                         0x00
    INTERFACE_ETHERNET_TCP =                    0x01
    INTERFACE_ETHERNET_UDP =                    0x02
    INTERFACE_USB =                             0x03
    INTERFACE_USB_HID =                         0x04
    
class DPPStatusType(enum.IntEnum):
    DPP_SUCCESS =                               0x00
    DPP_OUT_OF_RANGE_ERROR =                    0x01
    DPP_PARAMETER_READ_ONLY_ERROR =             0x02
    DPP_PARAMETER_NOT_EXISTING_ERROR =          0x03
    DPP_INVALID_COMMAND_ERROR =                 0x04
    DPP_REQUEST_CURRENTLY_NOT_POSSIBLE_ERROR =  0x05
    DPP_TIMEOUT_ERROR =                         0x06
    DPP_SYNTAX_ERROR_INVALID_REQUEST_ERROR =    0x07
    
    DPP_NO_DEVICE_WITH_ID_CONNECTED_ERROR =     0x50
    DPP_VICODAEMON_IS_STOPPED =                 0x51
    DPP_VICOLIB_TIMEOUT_ERROR =                 0x52
    DPP_RESPONSE_OUT_OF_BOUNDS_ERROR =          0x53
    DPP_INVALID_ARGUMENT_ERROR =                0x54
    DPP_INVALID_RESPONSE_DATA_ERROR =           0x55
    
    DPP_VICOLIB_OUT_OF_RANGE_ERROR =            0x56
    DPP_COMMAND_NOT_SUPPORTED_ERROR =           0x57
    DPP_UNDEFINED_ERROR =                       0xFF

class VersionType(ctypes.Structure):
    _fields_ = [
        ("major", ctypes.c_uint16),
        ("minor", ctypes.c_uint16),
        ("patch", ctypes.c_uint16),
        ("build", ctypes.c_uint16)
    ]

class CommandType(enum.IntEnum):
    READ =                                      0x00
    WRITE =                                     0x01

class StopConditionType(enum.IntEnum):
    NONE =                                      0x00
    STOP_AT_FIXED_LIVETIME =                    0x01
    STOP_AT_FIXED_REALTIME =                    0x02
    STOP_AT_FIXED_INPUT_COUNTS =                0x03
    STOP_AT_FIXED_OUTPUT_COUNTS =               0x04

class RunStatisticsType(ctypes.Structure):
    _fields_ = [
        ("isRunActive", ctypes.c_bool),
        ("realtime", ctypes.c_double),
        ("livetime", ctypes.c_double),
        ("outputCounts", ctypes.c_uint32),
        ("inputCounts", ctypes.c_uint32),
        ("outputCountRate", ctypes.c_uint32),
        ("inputCountRate", ctypes.c_uint32)
    ]

class BaselineTrimType(enum.IntEnum):
    LONGEST_POSSIBLE_MEDIUM_FILTER =            0x00
    LONG_MEDIUM_FILTER =                        0x01
    INTERMEDIATE_MEDIUM_FILTER =                0x02
    SHORT_MEDIUM_FILTER =                       0x03
    SHORTEST_POSSIBLE_MEDIUM_FILTER =           0x04

class ResetDetectionType(enum.IntEnum):
    SDD =                                       0x00
    PIN =                                       0x01

class ClockingSpeedType(enum.IntEnum):
    MHZ_80 =                                    0x00

class TriggerSourceType(enum.IntEnum):
    INSTANT_TRIGGER =                           0x00
    SPECIFIC_ADC_VALUE =                        0x01
    ADC_OUT_OF_RANGE =                          0x02
    FASTFILTER_TRIGGER =                        0x03
    FASTFILTER_RESET_DETECTED =                 0x04
    FASTFILTER_PILEUP =                         0x05
    MEDIUMFILTER_TRIGGER =                      0x06
    MEDIUMFILTER_RESET_DETECTED =               0x07
    MEDIUMFILTER_PILEUP =                       0x08
    NEW_OUTPUT_COUNT_ANY_ENERGY =               0x09
    NEW_OUTPUT_COUNT_SPECIFIC_ENERGY =          0x0A
    NEW_BASELINE_SAMPLE =                       0x0B
    ACTIVE_RESET_INITIATE =                     0x0C

class TriggerTimeoutType(enum.IntEnum):
    TIMEOUT_1_SECOND =                          0x00
    TIMEOUT_2_SECOND =                          0x01
    TIMEOUT_4_SECOND =                          0x02
    TIMEOUT_8_SECOND =                          0x03
    TIMEOUT_16_SECOND =                         0x04

class EventScopeType(enum.IntEnum):
    ADC_DATA =                                  0x00
    FASTFILTER =                                0x01
    MEDIUMFILTER =                              0x02
    SLOWFILTER =                                0x03
    BASELINE_AVERAGE =                          0x04
    BASELINE_SAMPLE =                           0x05
    
class EthernetProtocolType(enum.IntEnum):
    TCP =                                       0x01
    UDP =                                       0x02

class EthernetSpeedType(enum.IntEnum):
    AUTO_NEGOTIATION =                          0x00
    HALF_DUPLEX_10_MBITS =                      0x01
    FULL_DUPLEX_10_MBITS =                      0x02
    HALF_DUPLEX_100_MBITS =                     0x03
    FULL_DUPLEX_100_MBITS =                     0x04

class TriggerDurationType(enum.IntEnum):
    TRIGGER_DURATION_1_SECOND =                 0x00
    TRIGGER_DURATION_2_SECONDS =                0x01
    TRIGGER_DURATION_4_SECONDS =                0x02
    TRIGGER_DURATION_8_SECONDS =                0x03
    TRIGGER_DURATION_16_SECONDS =               0x04

class FirmwareVersionType(ctypes.Structure):
    _fields_ = [
        ("major", ctypes.c_uint16),
        ("minor", ctypes.c_uint16),
        ("patch", ctypes.c_uint16),
        ("build", ctypes.c_uint16),
        ("variant", ctypes.c_uint16)
    ]

class MCUStatusInfoType(ctypes.Structure):
    _fields_ = [
        ("hasPower", ctypes.c_bool),
        ("isReady", ctypes.c_bool),
        ("isAlmostReady", ctypes.c_bool)
    ]

class MCUStatusType(enum.IntEnum):
    MCU_SUCCESS =                               0x00
    MCU_COMMAND_NOT_SUPPORTED =                 0x01
    MCU_WRONG_CRC_CHECKSUM =                    0x02
    MCU_COMMAND_LENGTH_MISMATCH =               0x03
    MCU_VERSION_NOT_SUPPORTED =                 0x04
	
    MCU_ERROR =                                 0x10
	
    MCU_LEN_OUT_OF_VALID_RANGE =                0x20
    MCU_ADDRESS_OUT_OF_VALID_RANGE =            0x21
    MCU_SYSTEM_IS_NOT_IN_EEA_MODE =             0x22
	
    MCU_BL_FLASH_SESSION_ACTIVE =               0x30
    MCU_BL_NO_FLASH_SESSION_ACTIVE =            0x31
    MCU_BL_ADDRESS_OUT_OF_VALID_RANGE =         0x32
    MCU_BL_LEN_OUT_OF_VALID_RANGE =             0x33
    MCU_BL_DATA_NOT_IN_SEQUENCE_WITHIN_SESSION =0x34
    MCU_BL_APPLICATION_CHECKSUM_INVALID =       0x35
    MCU_BL_ALREADY_IN_APPLICATION =             0x36
    
    MCU_NO_DEVICE_WITH_ID_CONNECTED_ERROR =     0x50
    MCU_VICODAEMON_IS_STOPPED =                 0x51
    MCU_VICOLIB_TIMEOUT_ERROR =                 0x52
    MCU_RESPONSE_OUT_OF_BOUNDS_ERROR =          0x53
    MCU_INVALID_ARGUMENT_ERROR =                0x54
    MCU_INVALID_RESPONSE_DATA_ERROR =           0x55
    
    MCU_UART_TIMEOUT_ERROR =                    0xED
    MCU_NO_ACCESS_TO_INTERNAL_MEMORY_ERROR =    0xEE
    MCU_INCOMPLETE_UART_COMMAND_ERROR =         0xEF

MCUStatusType;

class SoftwarePackage(enum.IntEnum):
    Bootloader =                                0x10
    Application =                               0x20
    
class BootloaderSessionType(enum.IntEnum):
    Default =                                   0x01
    Flash =                                     0x02
    
class BootloaderReasonType(enum.IntEnum):
    RescuePinActive =                           0x10
    FlashRequest =                              0x20
    AppCrcInvalid =                             0x30
    
class LiveInfoVICOStateType(enum.IntEnum):
    INIT =                                      0x00
    OPERATION =                                 0x01
    VICO_ERROR =                                0x02
    ECO3 =                                      0x03
    EEA =                                       0x04
    
class LiveInfoVICOErrorType(enum.IntEnum):
    NO_VICO_ERROR =                             0x00
    VOERR_01 =                                  0x01
    VOERR_02 =                                  0x02
    VOERR_03 =                                  0x03
    VOERR_11 =                                  0x04
    VOERR_12 =                                  0x05
    VOERR_13 =                                  0x06
    VOERR_14 =                                  0x07
    UNKNOWN_VICO_ERROR =                        0xFF

class LiveInfo1VICOType(ctypes.Structure):
    _fields_ = [
        ("st", ctypes.c_uint32),
        ("er", ctypes.c_uint32),
        ("vIn", ctypes.c_float),
        ("pwr", ctypes.c_bool),
        ("therm1", ctypes.c_float),
        ("therm2", ctypes.c_float)
    ]

class LiveInfo2VICOType(ctypes.Structure):
    _fields_ = [
        ("st", ctypes.c_uint32),
        ("er", ctypes.c_uint32),
        ("vIn", ctypes.c_float),
        ("p5v", ctypes.c_float),
        ("n5vActive", ctypes.c_bool),
        ("mcu3v3", ctypes.c_float),
        ("ref2v5", ctypes.c_float),
        ("hvActive", ctypes.c_bool),
        ("hvDac", ctypes.c_uint16),
        ("hv", ctypes.c_float),
        ("pwr", ctypes.c_bool),
        ("usb", ctypes.c_bool),
        ("gpio", ctypes.c_bool),
        ("reqfbl", ctypes.c_bool),
        ("fpga3v3", ctypes.c_float),
        ("therm1", ctypes.c_float),
        ("therm2", ctypes.c_float)
    ]

class LiveInfoBoundariesVICOType(ctypes.Structure):
    _fields_ = [
        ("vInMin", ctypes.c_float),
        ("vInMax", ctypes.c_float),
        ("p5vMin", ctypes.c_float),
        ("p5vMax", ctypes.c_float),
        ("mcu3v3Min", ctypes.c_float),
        ("mcu3v3Max", ctypes.c_float),
        ("ref2v5Min", ctypes.c_float),
        ("ref2v5Max", ctypes.c_float),
        ("hvMin", ctypes.c_float),
        ("hvMax", ctypes.c_float),
        ("therm1Max", ctypes.c_float),
        ("therm2Max", ctypes.c_float)
    ]

class LiveInfoVIAMPStateType(enum.IntEnum):
    INACTIVE =                                  0x00
    EN_VOLTAGE =                                0x01
    CHECK_CONN_TEMP =                           0x02
    CHECK_CONN_I2C =                            0x03
    DISCONNECTED =                              0x04
    VALIDATE_EEPCONTENT =                       0x05
    NO_OPERATION =                              0x06
    ENABLE_HV =                                 0x07
    VIAMP_ERROR =                               0x08
    PREPARE_OPERATION =                         0x09
    OP_READY =                                  0x0A
    OP_ECO1 =                                   0x0B
    OP_FULL =                                   0x0C
    DISABLE_HV =                                0x0D
    OP_ECO2 =                                   0x0E

class LiveInfoVIAMPErrorType(enum.IntEnum):
    NO_VIAMP_ERROR =                            0x00
    VPERR_01 =                                  0x01
    VPERR_02 =                                  0x02
    VPERR_03 =                                  0x03
    VPERR_04 =                                  0x04
    VPERR_05 =                                  0x05
    VPERR_06 =                                  0x06
    UNKNOWN_VIAMP_ERROR =                       0xFF

class LiveInfo1VIAMPType(ctypes.Structure):
    _fields_ = [
        ("st", ctypes.c_uint32),
        ("er", ctypes.c_uint32),
        ("itec", ctypes.c_float),
        ("utec", ctypes.c_float),
        ("sddTmp", ctypes.c_float),
        ("rdy", ctypes.c_bool),
        ("hotSide", ctypes.c_float),
    ]

class LiveInfo2VIAMPType(ctypes.Structure):
    _fields_ = [
        ("st", ctypes.c_uint32),
        ("er", ctypes.c_uint32),
        ("viampAdc", ctypes.c_float),
        ("r1", ctypes.c_float),
        ("bk", ctypes.c_float),
        ("rx", ctypes.c_float),
        ("itec", ctypes.c_float),
        ("utec", ctypes.c_float),
        ("sddTmp", ctypes.c_float),
        ("targetTmp", ctypes.c_float),
        ("rdy", ctypes.c_bool),
        ("ardy", ctypes.c_bool),
        ("hotSide", ctypes.c_float),
        ("monSigFinal", ctypes.c_float),
        ("ctrlSigFinal", ctypes.c_float),
        ("iPartLimit", ctypes.c_bool),
        ("tecActive", ctypes.c_bool),
        ("tecDac", ctypes.c_uint16),
        ("pPart", ctypes.c_float),
        ("iPart", ctypes.c_float),
        ("dPart", ctypes.c_float)
    ]

class LiveInfoBoundariesVIAMPType(ctypes.Structure):
    _fields_ = [
        ("viampAdcMin", ctypes.c_float),
        ("viampAdcMax", ctypes.c_float),
        ("r1Min", ctypes.c_float),
        ("r1Max", ctypes.c_float),
        ("bkMin", ctypes.c_float),
        ("bkMax", ctypes.c_float),
        ("rxMin", ctypes.c_float),
        ("rxMax", ctypes.c_float),
        ("itecMax", ctypes.c_float),
        ("utecMax", ctypes.c_float),
        ("kp", ctypes.c_float),
        ("ki", ctypes.c_float),
        ("kd", ctypes.c_float)
    ]

class DevInfo1VICOType(ctypes.Structure):
    _fields_ = [
        ("smj", ctypes.c_uint8),
        ("smi", ctypes.c_uint8),
        ("sms", ctypes.c_uint8),
        ("smb", ctypes.c_uint16)
    ]

class DevInfo1BootloaderType(ctypes.Structure):
    _fields_ = [
        ("smj", ctypes.c_uint8),
        ("smi", ctypes.c_uint8),
        ("sms", ctypes.c_uint8),
        ("smb", ctypes.c_uint16)
    ]

class ModeType(enum.IntEnum):
    NO_REQUEST =                                0x00
    FULL_MODE =                                 0x01
    ECO1_MODE =                                 0x02
    ECO2_MODE =                                 0x03
    ECO3_MODE =                                 0x04
    EEA_MODE =                                  0x05

class TWIModeType(enum.IntEnum):
    TWI_WRITE =                                 0x00
    TWI_READ =                                  0x01
    TWI_WRITE_READ =                            0x02

class TempType(ctypes.Structure):
    _fields_ = [
        ("sddTmp", ctypes.c_float),
        ("targetTmp", ctypes.c_float),
        ("rdy", ctypes.c_bool),
        ("ardy", ctypes.c_bool)
    ]

class PortType(enum.IntEnum):
    PORT_A =                                    0x00
    PORT_B =                                    0x01
    PORT_C =                                    0x02
    PORT_D =                                    0x03
    PORT_E =                                    0x04
    PORT_F =                                    0x05
    PORT_G =                                    0x06
    PORT_H =                                    0x07
    PORT_J =                                    0x08
    PORT_K =                                    0x09
    PORT_L =                                    0x0A
    PORT_M =                                    0x0B
    PORT_N =                                    0x0C
    PORT_P =                                    0x0D
    PORT_Q =                                    0x0E
    PORT_R =                                    0x0F

class DbgClpType(ctypes.Structure):
    _fields_ = [
        ("stepCounter", ctypes.c_uint32),
        ("sddTmp", ctypes.c_float),
        ("itec", ctypes.c_float),
        ("utec", ctypes.c_float),
        ("monSigFinal", ctypes.c_float),
        ("pPart", ctypes.c_float),
        ("iPart", ctypes.c_float),
        ("rdy", ctypes.c_bool)
    ]

class DbgClpExtType(ctypes.Structure):
    _fields_ = [
        ("stepCounter", ctypes.c_uint32),
        ("targetTmp", ctypes.c_float),
        ("sddTmp", ctypes.c_float),
        ("itec", ctypes.c_float),
        ("utec", ctypes.c_float),
        ("monStepSize", ctypes.c_float),
        ("monSigFinal", ctypes.c_float),
        ("ctrlSigFinal", ctypes.c_float),
        ("pPart", ctypes.c_float),
        ("iPart", ctypes.c_float),
        ("iPartLimit", ctypes.c_bool),
        ("dPart", ctypes.c_float),
        ("rdy", ctypes.c_bool),
        ("aRdy", ctypes.c_bool),
        ("grnLed", ctypes.c_bool),
        ("hotSide", ctypes.c_float)
    ]
