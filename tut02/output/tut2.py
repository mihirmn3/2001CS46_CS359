from scapy.all import *

# TCP 3-way handshake starting packets
def tcp_start_packets():
    sport = 5000
    dport = 443

    SYN = IP(dst="www.medlineplus.gov") / TCP(sport=sport, dport=dport, seq=1000)
    SYNACK = sr1(SYN)
    ACK = IP(dst="www.medlineplus.gov") / TCP(sport=sport,
                                            dport=dport, flags='A', seq=SYN.seq + 1, ack=SYNACK.seq + 1)

    wrpcap("TCP_3_way_handshake_start_2001CS46.pcap", SYN)
    wrpcap("TCP_3_way_handshake_start_2001CS46.pcap", SYNACK, append=True)
    wrpcap("TCP_3_way_handshake_start_2001CS46.pcap", ACK, append=True)

# TCP closing packets
def tcp_close_packets():
    sport = 5000
    dport = 443

    SYN = IP(dst="www.medlineplus.gov") / TCP(sport=sport, dport=dport, seq=1000)
    SYNACK = sr1(SYN)
    ACK = IP(dst="www.medlineplus.gov") / TCP(sport=sport,
                                            dport=dport, flags='A', seq=SYN.seq + 1, ack=SYNACK.seq + 1)
    send(ACK)

    FIN = IP(dst="www.medlineplus.gov") / TCP(sport=sport, dport=dport, flags="FA", seq=SYNACK.ack, ack=SYNACK.seq + 1)
    FINACK = sr1(FIN)
    LASTACK = IP(dst="www.medlineplus.gov") / TCP(sport=sport, dport=dport, flags="A", seq=FINACK.ack, ack=FINACK.seq + 1)
    send(LASTACK)

    wrpcap("TCP_handshake_close_2001CS46.pcap", FIN)
    wrpcap("TCP_handshake_close_2001CS46.pcap", FINACK, append=True)
    wrpcap("TCP_handshake_close_2001CS46.pcap", LASTACK, append=True)

# DNS packets
def dns_packets():
    dnsreq = IP(dst="8.8.8.8") / UDP(dport=53) /  DNS(rd=1, qd=DNSQR(qname="www.medlineplus.gov"))
    dnsans = sr1(dnsreq, verbose=0)

    wrpcap("DNS_request_response_2001CS46.pcap", dnsreq)
    wrpcap("DNS_request_response_2001CS46.pcap", dnsans, append=True)

# PING packets
def ping_packets():
    ping = IP(dst="www.medlineplus.gov") / ICMP()
    pingres = sr1(ping, timeout=10)

    if pingres:
        print("Host is up.")
    else:
        print("Host is down.")

    wrpcap("PING_request_response_2001CS46.pcap", ping)
    wrpcap("PING_request_response_2001CS46.pcap", pingres, append =True)

# ARP packets
def arp_basic_packets():
    arp_packet =  Ether(dst="ff:ff:ff:ff:ff:ff") / ARP()

    wrpcap("ARP_2001CS46.pcap", arp_packet, append=False)

# ARP request response packets
def arp_req_res_packets():
    # Requesting from mobile phone
    ip = "172.16.173.101"

    arp_packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    arp_response = srp1(arp_packet)

    wrpcap("ARP_request_response_2001CS46.pcap", arp_packet)
    wrpcap("ARP_request_response_2001CS46.pcap", arp_response, append=True)

# FTP starting closing packets
def ftp_packets():
    ftp = sniff(filter="tcp port 21", count=14)
    wrpcap("FTP_connection_start_2001CS46_temp.pcap", ftp)

    ftp2= sniff(filter="tcp port 21", count=6)
    wrpcap("FTP_connection_end_2001CS46_temp.pcap", ftp2)

if __name__ == "__main__":
    print()
#call the required function here
