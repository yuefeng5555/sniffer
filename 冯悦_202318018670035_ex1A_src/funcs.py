import psutil
import netifaces as nif


def get_all_interfaces():
    d = psutil.net_if_stats()
    d2 = psutil.net_if_addrs()
    r = []
    m = []
    for i in d2.keys():
        # select NIFs whose "isup" attribute equals TRUE and save as list of tuples [(name,macaddress),...]
        print(i)
        print(d2[i][0].address.lower().replace("-", ":"))

        if "Loopback" not in i and d[i][0]:
            print(i, d2[i][0].address)
            r.append(i)
            m.append(d2[i][0].address.lower().replace("-", ":"))

    return r,m


def mac_for_ip(ip):
    'Returns a list of MACs for interfaces that have given IP, returns None if not found'
    for i in nif.interfaces():
        addrs = nif.ifaddresses(i)
        try:
            if_mac = addrs[nif.AF_LINK][0]['addr']
            if_ip = addrs[nif.AF_INET][0]['addr']
        except : #ignore ifaces that dont have MAC or IP
            if_mac = if_ip = None
        if if_ip == ip:
            return if_mac
    return "mafeeeeesh"


