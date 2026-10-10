#!/usr/bin/env python3
import socket
import time
from packet import make_packet, parse_packet, FLAG_DATA, FLAG_ACK, FLAG_FIN

RECEIVER_IP = "10.0.0.2"
RECEIVER_PORT = 12000
TIMEOUT_SECONDS = 2.0
MAX_ATTEMPTS = 8

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT_SECONDS)

# Extended message so transmission lasts long enough to test link cuts
message = "PES_University_Jackfruit_SDN_Socket_Mini_Project_Reliable_Transmission_Over_OpenFlow_Mesh!"
chunk_size = 6
chunks = [message[i:i+chunk_size].encode() for i in range(0, len(message), chunk_size)]

current_seq = 0
total_transmissions = 0
retransmissions = 0

print(f"[*] Sender running on Mininet Host h1.")
print(f"[*] Target Receiver: {RECEIVER_IP}:{RECEIVER_PORT}")
print(f"[*] Total Chunks to deliver: {len(chunks)}\n")

for idx, chunk in enumerate(chunks):
    pkt = make_packet(seq_num=current_seq, ack_num=0, flags=FLAG_DATA, payload=chunk)
    attempts = 0
    acknowledged = False
    
    while not acknowledged:
        attempts += 1
        total_transmissions += 1
        
        if attempts > 1:
            retransmissions += 1
            print(f"[RETRANSMIT] Retrying Packet {current_seq} (Chunk {idx+1}/{len(chunks)} - Attempt {attempts}/{MAX_ATTEMPTS})...")
        else:
            print(f"[SEND] Sending Packet {current_seq} (Chunk {idx+1}/{len(chunks)}: '{chunk.decode(errors='ignore')}')")
        
        sock.sendto(pkt, (RECEIVER_IP, RECEIVER_PORT))
        
        try:
            ack_data, _ = sock.recvfrom(2048)
            ack_pkt = parse_packet(ack_data)
            
            if ack_pkt and ack_pkt["flags"] == FLAG_ACK and ack_pkt["ack_num"] == current_seq:
                print(f"[ACK RECEIVED] Valid ACK {current_seq} confirmed.")
                acknowledged = True
                current_seq = 1 - current_seq
                # Pace transmissions slightly (0.4s) so link failures can be injected live
                time.sleep(0.4)
            else:
                print(f"[WARN] Stale/Invalid ACK received.")
                
        except socket.timeout:
            print(f"⏱️  [TIMEOUT] Timer expired ({TIMEOUT_SECONDS}s) for Packet {current_seq}!")
            if attempts >= MAX_ATTEMPTS:
                print("[ERROR] Max retry attempts reached. Network failure.")
                sock.close()
                exit(1)

# Graceful termination
fin_pkt = make_packet(seq_num=current_seq, ack_num=0, flags=FLAG_FIN)
sock.sendto(fin_pkt, (RECEIVER_IP, RECEIVER_PORT))

print("\n" + "="*50)
print("[+] Transmission Finished Successfully!")
print(f"[*] Total Transmissions: {total_transmissions}")
print(f"[*] Retransmissions triggered: {retransmissions}")
print("="*50)

sock.close()
