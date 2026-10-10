# SDN-Integrated Reliable Data Transfer (Stop-and-Wait ARQ over UDP)

## 📌 Overview
This project implements a Reliable Data Transfer (RDT) protocol at the transport layer using UDP sockets, integrated into an SDN mesh topology using Mininet and OpenFlow 1.3.

## 🏗️ Architecture
- **Topology:** Multi-path switch fabric (`s1` -> `s2` (primary) / `s3` (backup) -> `s4`).
- **Transport Layer:** Stop-and-Wait ARQ with 12-byte binary header (`struct`), CRC-32 integrity validation, and socket timeouts.
- **SDN Control Plane:** Dynamic port-status monitoring with automated OpenFlow failover rerouting.

## 🚀 How to Run
1. **Start Mininet Topology:**
   ```bash
   sudo python3 topology.py
