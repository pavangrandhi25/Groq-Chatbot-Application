from scapy.all import rdpcap
import os

class Sniff_packet():

    def __init__(self):
        pass
    
    def extract(self,file_path): 
        if file_path.exists():
            packets = rdpcap(file_path)
            print('packets : ',packets)
    
    def transform(self):
        pass

    def load(self):
        pass


if __name__ == '__main__':
    file_path = 'C:\Users\ggrkp\LocalDrive\Python\AI\git_projects\\network_protocol_analysis\pcap\dhcp_handshake.pcap'
    sniff = Sniff_packet()
    sniff.extract(file_path)
        