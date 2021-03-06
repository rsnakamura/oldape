
# python standard library
import string


NAMED = r"(?P<{name}>{pattern})"
GROUP = r"({group})"
CLASS = "[{0}]"
OR = "|"
NOT = "^"


SPACE = r'\s'
NOT_SPACE = r'\S'
DIGIT = r"\d"
ANYTHING = '.'
WORD_ENDING = r'\b'
LINE_ENDING = r"$"
LINE_START = "^"


M_TO_N_TIMES = "{{{m},{n}}}"
ONE_TO_3 = M_TO_N_TIMES.format(m=1, n=3)
EXACTLY = "{{{0}}}"
ONE_OR_MORE = "+"
ZERO_OR_MORE = '*'
ZERO_OR_ONE = '?'

EVERYTHING = ANYTHING + ZERO_OR_MORE


LETTER = CLASS.format(string.ascii_letters)
LETTERS = LETTER + ONE_OR_MORE
ALPHA_NUM = string.ascii_letters + string.digits
ALPHA_NUMS = CLASS.format(ALPHA_NUM) + ONE_OR_MORE
ALPHA_NUM_UNDERSCORE = r'\w'
ALPHA_NUM_UNDERSCORES = ALPHA_NUM_UNDERSCORE + ONE_OR_MORE
SPACE_OPTIONAL = SPACE + ZERO_OR_ONE
SPACES_OPTIONAL = SPACE + ZERO_OR_MORE
SPACES = SPACE + ONE_OR_MORE
DOT = r"\."


HEX = CLASS.format(string.hexdigits)
HEXADECIMALS = HEX + ONE_OR_MORE
INTEGER = DIGIT + ONE_OR_MORE
FLOAT = INTEGER + DOT + INTEGER
REAL = INTEGER + GROUP.format(group=DOT + INTEGER) + ZERO_OR_ONE


OCTET = DIGIT + ONE_TO_3
OCTET_DOT = OCTET + DOT

IP_ADDRESS_NAME = "ip_address"
IP_ADDRESS = NAMED.format(name=IP_ADDRESS_NAME,
                       pattern=DOT.join([OCTET] * 4))

MAC_ADDRESS_NAME = "mac_address"
HEX_PAIR = HEX + EXACTLY.format(2)
MAC_ADDRESS = NAMED.format(name=MAC_ADDRESS_NAME,
                           pattern=":".join([HEX_PAIR] * 6))

LINUX_IP = SPACES.join('inet addr:'.split()) + IP_ADDRESS
LINUX_MAC = "HWaddr" + SPACES + MAC_ADDRESS
ANDROID_IP = 'ip' + SPACES + IP_ADDRESS


INTERFACE_STATE_NAME = "state"
INTERFACE_STATE =  NAMED.format(name=INTERFACE_STATE_NAME,
                                pattern="UP" + OR + "DOWN")

NETCFG_IP = SPACES + INTERFACE_STATE + SPACES + IP_ADDRESS + EVERYTHING + MAC_ADDRESS
INTERFACE_NAME = "interface"
INTERFACE = NAMED.format(name=INTERFACE_NAME,
                                pattern=LETTERS + INTEGER) 
NETCFG_INTERFACE = INTERFACE + NETCFG_IP


RTT = NAMED.format(name="rtt", pattern=REAL)

PING = SPACES.join([EVERYTHING + IP_ADDRESS + ":"
                    + EVERYTHING + 
                    "time" + SPACES_OPTIONAL + "(=|<)" + SPACES_OPTIONAL + RTT])


PSE_NAME = "pse"
PID_NAME = 'pid'
PID = NAMED.format(name=PID_NAME,  pattern=INTEGER)
TTY = GROUP.format(group="\?" + OR + "pts/" + INTEGER)
TIME = ":".join([DIGIT + EXACTLY.format(2)] * 3)
PROCESS_NAME = "process"
PROCESS = NAMED.format(name=PROCESS_NAME,pattern=CLASS.format(NOT + SPACE) + ONE_OR_MORE)
PSE_LINUX = SPACES.join([PID, TTY, TIME, PROCESS])


USER = ALPHA_NUM_UNDERSCORES
PPID = INTEGER
VSIZE = INTEGER
RSS = INTEGER
WCHAN = ALPHA_NUMS
PC = HEXADECIMALS
S_OR_R = "(S" + OR + "R)"
PS_ANDROID = SPACES.join((USER, PID, PPID, VSIZE, RSS, WCHAN, PC, S_OR_R, PROCESS))


IW_INTERFACE = "Interface" + SPACES + INTERFACE

RSSI_NAME = 'rssi'
IW_RSSI = "signal:" + SPACES + NAMED.format(name=RSSI_NAME,
                                            pattern="-" + INTEGER + SPACES + "dBm")


WPA_MAC = "address=" + MAC_ADDRESS
WPA_IP = "ip_address=" + IP_ADDRESS
WPA_INTERFACE = "Using" + SPACES + "interface" + SPACES + "'" + INTERFACE + "'"
SSID_NAME = "ssid"
SSID = NAMED.format(name=SSID_NAME,
                    pattern=EVERYTHING + WORD_ENDING)
WPA_SSID = LINE_START + "ssid=" + SSID
SUPPLICANT_STATE_NAME = "supplicant_state"
SUPPLICANT_STATE = NAMED.format(name=SUPPLICANT_STATE_NAME,
                                pattern=LETTERS)
WPA_SUPPLICANT_STATE = "wpa_state=" + SUPPLICANT_STATE
