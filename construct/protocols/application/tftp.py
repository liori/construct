'''
TFTP: Trivial File Transfer Protocol

See RFC 1350 for details.
'''
from construct import Struct, ByteRange, Select, Terminator, OneOf, UBInt16, CString, Const 


class PacketTypes:
    RRQ=1
    WRQ=2
    DATA=3
    ACK=4
    ERROR=5


class Modes:
    ''' Note: the TFTP protocol accepts all possible capitalizations of these
    strings. Do not compare these strings without .lower()! '''
    NetASCII='netascii'
    Octet='octet'
    Mail='mail'


class Errors:
    Undefined=0
    FileNotFound=1
    AccessViolation=2
    DiskFull=3
    IllegalOperation=4
    UnknownTransferID=5
    FileAlreadyExists=6
    NoSuchUser=7


request = Struct("TFTPRequest",
    OneOf(UBInt16("type"), [PacketTypes.RRQ, PacketTypes.WRQ]),
    CString("filename"),
    CString("mode"),
    Terminator)


data = Struct("TFTPData",
    Const(UBInt16("type"), PacketTypes.DATA),
    UBInt16("index"),
    ByteRange("data", 0, 512),
    Terminator)


ack = Struct("TFTPACK",
    Const(UBInt16("type"), PacketTypes.ACK),
    UBInt16("index"),
    Terminator)


error = Struct("TFTPError",
    Const(UBInt16("type"), PacketTypes.ERROR),
    UBInt16("code"),
    CString("message"),
    Terminator)


tftp = Select("TFTP", request, data, ack, error)
