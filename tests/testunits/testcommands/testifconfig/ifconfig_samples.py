NEWLINE = "\n"

ifconfig_android = """
wlan0: ip 192.168.20.153 mask 255.255.255.0 flags [up broadcast running multicast]
""".split(NEWLINE)

ifconfig_linux = '''
eth0      Link encap:Ethernet  HWaddr d0:67:e5:0b:bf:04  
          inet addr:192.168.20.51  Bcast:192.168.20.255  Mask:255.255.255.0
          inet6 addr: fe80::d267:e5ff:fe0b:bf04/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:5995546 errors:0 dropped:0 overruns:0 frame:0
          TX packets:2629592 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:8622791848 (8.6 GB)  TX bytes:219865580 (219.8 MB)
          Interrupt:46 Base address:0xc000 

'''.split(NEWLINE)

