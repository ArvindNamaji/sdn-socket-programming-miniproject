#!/usr/bin/env python3
import socket
from packet import parse_packet, make_packet, FLAG_DATA, FLAG_ACK, FLAG_FIN

RECEIVER_IP = "10.0.0.2"
RECEIVER_PORT = 12000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((RECEIVER_IP, RECEIVER_PORT))

print(f"[*] Receiver listening on Mininet Host h2 ({RECEIVER_IP}:{RECEIVER_PORT})\n")

expected_seq = 0
received_data = []

while True:
    data, sender_addr = sock.recvfrom(2048)
    pkt = parse_packet(data)
    
    if pkt is None or not pkt["is_valid"]:
        print("[!] Corrupted packet received. Dropping silently.")
        continue

    if pkt["flags"] == FLAG_FIN:
        print("[*] FIN received. Sending FIN-ACK and closing.")
        fin_ack = make_packet(seq_num=0, ack_num=pkt["seq_num"], flags=FLAG_ACK)
        sock.sendto(fin_ack, sender_addr)
        break

    print(f"[RECV] Packet {pkt['seq_num']} received ({len(pkt['payload'])} bytes).")

    if pkt["seq_num"] == expected_seq:
        received_data.append(pkt["payload"].decode(errors="ignore"))
        ack_pkt = make_packet(seq_num=0, ack_num=expected_seq, flags=FLAG_ACK)
        sock.sendto(ack_pkt, sender_addr)
        print(f"[ACK] Sent ACK {expected_seq} to sender.")
        expected_seq = 1 - expected_seq
    else:
        last_ack = 1 - expected_seq
        print(f"[DUPLICATE] Got Seq {pkt['seq_num']}, expected {expected_seq}. Resending ACK {last_ack}.")
        ack_pkt = make_packet(seq_num=0, ack_num=last_ack, flags=FLAG_ACK)
        sock.sendto(ack_pkt, sender_addr)

sock.close()
print("\n[+] Full message reassembled at Receiver (h2):")
print("".join(received_data))
