#!/usr/bin/env python3
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()

# ----------------- PAGE MARGINS -----------------
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# ----------------- COLOR PALETTE -----------------
COLOR_NAVY = RGBColor(16, 44, 87)       # #102C57
COLOR_TEXT = RGBColor(33, 37, 41)       # #212529
COLOR_GRAY = RGBColor(108, 117, 125)    # #6C757D

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = parse_xml(f'<w:{m} {nsdecls("w")} w:w="{val}" w:type="dxa"/>')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_body_p(text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.name = 'Calibri'
        r_b.font.size = Pt(10.5)
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_TEXT
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(10.5)
    r.font.color.rgb = COLOR_TEXT
    return p

def add_image_smart(pattern_or_name, width_in_inches, caption_text=""):
    """Robust image locator searching current and parent directories."""
    found = None
    search_dirs = [".", "/home/arvind/sdn-socket-project"]
    for d in search_dirs:
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            if pattern_or_name.lower() in f.lower() and f.lower().endswith(('.png', '.jpg', '.jpeg')):
                found = os.path.join(d, f)
                break
        if found:
            break

    if found and os.path.exists(found):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        run = p_img.add_run()
        run.add_picture(found, width=Inches(width_in_inches))
        if caption_text:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Calibri'
            r_cap.font.size = Pt(9.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = COLOR_GRAY
    else:
        if caption_text:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run(f"[{caption_text}]")
            r_cap.font.name = 'Calibri'
            r_cap.font.size = Pt(9.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = COLOR_GRAY

# ==================== PAGE 1: TITLE & TEAM METADATA ====================
p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_inst.paragraph_format.space_after = Pt(2)
r = p_inst.add_run("PES UNIVERSITY")
r.font.name = 'Calibri'
r.font.size = Pt(17)
r.font.bold = True
r.font.color.rgb = COLOR_NAVY

p_dept = doc.add_paragraph()
p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dept.paragraph_format.space_after = Pt(2)
r = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
r.font.name = 'Calibri'
r.font.size = Pt(11)
r.font.bold = True
r.font.color.rgb = COLOR_GRAY

p_course = doc.add_paragraph()
p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_course.paragraph_format.space_after = Pt(8)
r = p_course.add_run("Computer Networks Laboratory (UE23CS252) • Mini-Project Report")
r.font.name = 'Calibri'
r.font.size = Pt(10)
r.font.italic = True
r.font.color.rgb = COLOR_GRAY

# Title Box
title_table = doc.add_table(rows=1, cols=1)
title_table.alignment = WD_TABLE_ALIGNMENT.CENTER
title_table.autofit = False
title_table.columns[0].width = Inches(6.8)
cell_t = title_table.cell(0, 0)
set_cell_background(cell_t, "EBF3FA")
set_cell_margins(cell_t, top=100, bottom=100, left=150, right=150)

p_t1 = cell_t.paragraphs[0]
p_t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_t1.paragraph_format.space_after = Pt(3)
r_proj = p_t1.add_run("PROJECT #7 • TEAM 5")
r_proj.font.name = 'Calibri'
r_proj.font.size = Pt(9.5)
r_proj.font.bold = True
r_proj.font.color.rgb = COLOR_NAVY

p_t2 = cell_t.add_paragraph()
p_t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_t2.paragraph_format.space_after = Pt(0)
r_title = p_t2.add_run("Packet Loss Detection and Recovery over Software-Defined Networks\n(Stop-and-Wait ARQ & Dynamic OpenFlow Path Failover)")
r_title.font.name = 'Calibri'
r_title.font.size = Pt(12.5)
r_title.font.bold = True
r_title.font.color.rgb = COLOR_NAVY

p_sp = doc.add_paragraph()
p_sp.paragraph_format.space_before = Pt(4)
p_sp.paragraph_format.space_after = Pt(4)

# 2-Column Student Name & SRN Table
meta_table = doc.add_table(rows=4, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_table.autofit = False
widths = [Inches(3.8), Inches(3.0)]
for row in meta_table.rows:
    for idx, width in enumerate(widths):
        row.cells[idx].width = width

meta_headers = ["Student Name", "SRN"]
for i, h in enumerate(meta_headers):
    c = meta_table.cell(0, i)
    set_cell_background(c, "102C57")
    set_cell_margins(c, top=70, bottom=70, left=120, right=120)
    p = c.paragraphs[0]
    r = p.add_run(h)
    r.font.name = 'Calibri'
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

team_data = [
    ("Arvind Namaji", "PES1UG25CS102"),
    ("Anirudh S", "PES1UG25CS069"),
    ("Bapathi Venkata Sri Abhivaran Reddy", "PES1UG25CS122")
]

for row_idx, data in enumerate(team_data, start=1):
    bg_color = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(data):
        c = meta_table.cell(row_idx, col_idx)
        set_cell_background(c, bg_color)
        set_cell_margins(c, top=60, bottom=60, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(9.5)
        if col_idx == 0:
            r.font.bold = True
        r.font.color.rgb = COLOR_TEXT

# Section 1: Abstract (Directly on Page 1)
add_heading_1("1. ABSTRACT")
add_body_p(
    "In traditional computer networks, the User Datagram Protocol (UDP) offers lightweight, connectionless datagram transport without delivery, ordering, or data integrity assurances. In contrast, standard Transmission Control Protocol (TCP) hides internal error detection and flow recovery within the operating system kernel. This project designs, implements, and benchmarks a two-tier reliable networked application that integrates custom transport-layer protocol engineering with Software-Defined Networking (SDN) in a virtualized Mininet environment."
)
add_body_p(
    "At the transport layer, we engineered an alternating-bit Stop-and-Wait Automatic Repeat reQuest (ARQ) protocol over raw UDP sockets featuring a strict 12-byte binary header, CRC-32 integrity validation, and non-blocking timeout retransmissions. At the network layer, we configured a redundant multi-path mesh topology across four Open vSwitch (OVS) nodes operated under OpenFlow 1.3 rules. A custom SDN controller dynamically tracks physical port statuses, automatically rerouting traffic from a broken primary link (s1 <-> s2) to an alternate backup link (s1 <-> s3 <-> s4) in under 0.5 seconds, ensuring uninterrupted transport delivery without session termination."
)

doc.add_page_break()

# ==================== PAGE 2: ARCHITECTURE & PACKET SPECS ====================
add_heading_1("2. SYSTEM ARCHITECTURE & PACKET SPECIFICATION")
add_heading_2("2.1 Multi-Path Mesh Topology in Mininet")
add_body_p(
    "The physical-layer emulation is implemented inside Mininet using Open vSwitch bridges configured in secure fail mode (failMode='secure'). Traffic flows between host h1 (Sender) and host h2 (Receiver) across two disjoint paths:"
)

# Textual Topology Diagram in Preserved Monospace Block
arch_table = doc.add_table(rows=1, cols=1)
arch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
arch_table.columns[0].width = Inches(6.8)
cell_a = arch_table.cell(0, 0)
set_cell_background(cell_a, "F8F9FA")
set_cell_margins(cell_a, top=80, bottom=80, left=120, right=120)
p_a = cell_a.paragraphs[0]
p_a.paragraph_format.line_spacing = 1.05
r_a = p_a.add_run(
    "                      [ Switch s1 ]\n"
    "                     /             \\\n"
    "       Primary Path /               \\  Backup Path\n"
    "      (5ms latency)/                 \\ (20ms latency)\n"
    "             [ Switch s2 ]      [ Switch s3 ]\n"
    "                   \\                 /\n"
    "                    \\               /\n"
    "                     \\             /\n"
    "                      [ Switch s4 ]\n"
    "                            |\n"
    "                  [ Host h2 (10.0.0.2) ]\n"
    "                  (Socket Receiver / ACK)"
)
r_a.font.name = 'Consolas'
r_a.font.size = Pt(8.5)
r_a.font.color.rgb = COLOR_TEXT

add_body_p(
    "• Host h1 (10.0.0.1, Port 1 on s1): Transmits UDP packets as the Stop-and-Wait sender.\n"
    "• Primary Path (s1 <-> s2 <-> s4): 10 Mbps bandwidth, 5 ms propagation delay (Mininet TCLink).\n"
    "• Backup Path (s1 <-> s3 <-> s4): 10 Mbps bandwidth, 20 ms propagation delay for failover redundancy.\n"
    "• Host h2 (10.0.0.2, Port 1 on s4): Listens on UDP port 12000, validates checksums, and sends ACKs."
)

add_heading_2("2.2 Custom Binary Header Framing Specification")
add_body_p(
    "To avoid text parsing overhead, all datagrams are framed into binary format using Python's struct module adhering to Big-Endian Network Byte Order ('!IIHH'):"
)

# Binary Framing Table
header_table = doc.add_table(rows=6, cols=5)
header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
header_table.autofit = False
h_widths = [Inches(1.2), Inches(0.8), Inches(1.0), Inches(0.8), Inches(3.0)]
for row in header_table.rows:
    for idx, width in enumerate(h_widths):
        row.cells[idx].width = width

h_titles = ["Field Name", "Size", "Data Type", "Offset", "Protocol Function"]
for i, h in enumerate(h_titles):
    c = header_table.cell(0, i)
    set_cell_background(c, "102C57")
    set_cell_margins(c, top=60, bottom=60, left=70, right=70)
    p = c.paragraphs[0]
    r = p.add_run(h)
    r.font.name = 'Calibri'
    r.font.size = Pt(9)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

h_data = [
    ("seq_num", "4 Bytes", "uint32", "0 – 3", "1-Bit alternating sequence flag (0 or 1)"),
    ("ack_num", "4 Bytes", "uint32", "4 – 7", "Sequence number acknowledged by the receiver"),
    ("flags", "2 Bytes", "uint16", "8 – 9", "Bitmask: 0x01 (DATA), 0x02 (ACK), 0x04 (FIN)"),
    ("checksum", "2 Bytes", "uint16", "10 – 11", "Lower 16 bits of CRC-32 computed on payload"),
    ("payload", "Variable", "Raw Bytes", "12 – N", "Application data chunk (e.g., 6 bytes/packet)")
]

for row_idx, data in enumerate(h_data, start=1):
    bg_color = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(data):
        c = header_table.cell(row_idx, col_idx)
        set_cell_background(c, bg_color)
        set_cell_margins(c, top=50, bottom=50, left=70, right=70)
        p = c.paragraphs[0]
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        if col_idx == 0:
            r.font.name = 'Consolas'
            r.font.bold = True
        r.font.color.rgb = COLOR_TEXT

# ==================== PAGE 3: PROTOCOL LOGIC & CONTROLLER ====================
add_heading_1("3. PROTOCOL LOGIC & DYNAMIC CONTROLLER DESIGN")
add_heading_2("3.1 Alternating-Bit Stop-and-Wait ARQ State Machine")
add_body_p(
    "Because Stop-and-Wait ARQ operates with a sliding window size W = 1, exactly one unacknowledged datagram exists in transit. This allows a 1-bit sequence number (0 <-> 1) to distinguish new packets from duplicate retransmissions with zero ambiguity:"
)
add_body_p(
    "• Sender Logic: Transmits chunk with active sequence bit (Seq 0). Starts a socket timeout timer (2.0s). Upon receiving ACK 0, it clears the timer, flips to Seq 1, and transmits the next chunk. If a timeout occurs, it triggers retransmission up to an 8-attempt ceiling.\n"
    "• Receiver Logic: Computes CRC-32 on payload. If checksum is valid and seq_num matches expected_seq, it writes to the buffer, returns ACK, and toggles expected_seq. If seq_num is duplicate, it discards data to prevent buffer corruption and re-sends the previous ACK."
)

add_heading_2("3.2 SDN OpenFlow Controller & Link Monitoring")
add_body_p(
    "The SDN controller (sdn_controller.py) communicates with Open vSwitch via OpenFlow 1.3. It inspects switch ports every 500 ms. When an administrator triggers a link drop, the controller detects PORT_DOWN on s1-eth2, purges old flow entries, and installs high-priority alternate routes through switch s3."
)

add_image_smart("mininet", 4.8, "Figure 1: Mininet Topology Setup and Runtime Failure Injection ('link s1 s2 down')")

# ==================== PAGE 4: VERIFICATION & SCREENSHOT EVIDENCE ====================
add_heading_1("4. EXPERIMENTAL VERIFICATION & ROBUSTNESS TESTING")
add_body_p(
    "During active socket streaming of a 15-chunk string from host h1 to h2, a physical link disruption was injected by bringing s1-eth2 down. The system successfully executed end-to-end failover recovery without application failure."
)

add_image_smart("controller", 4.8, "Figure 2: SDN Controller Real-Time Link Drop Detection and Dynamic Flow Rerouting to Backup Path (s3)")
add_image_smart("node h1", 4.5, "Figure 3: Node h1 (Sender) Event Trace Showing Timeout and Successful Retransmission")
add_image_smart("node h2", 4.5, "Figure 4: Node h2 (Receiver) Event Trace Showing Zero-Loss In-Order Message Reassembly")
add_image_smart("221517", 5.2, "Figure 5: Integrated Multi-Window Execution Trace (Mininet CLI, SDN Controller, h1 Sender, h2 Receiver)")

# ==================== PAGE 5: PERFORMANCE EVALUATION ====================
add_heading_1("5. PERFORMANCE EVALUATION & COMPARISON")
add_body_p(
    "To evaluate performance against conventional setups, we benchmarked our dynamic SDN framework against a static baseline network (without SDN dynamic rerouting capabilities):"
)

add_image_smart("220759", 4.8, "Figure 6: Execution Benchmark Comparing Static Baseline Routing vs. Proposed Dynamic SDN + ARQ")

# Quantitative Benchmark Table
perf_table = doc.add_table(rows=8, cols=3)
perf_table.alignment = WD_TABLE_ALIGNMENT.CENTER
perf_table.autofit = False
p_widths = [Inches(2.6), Inches(2.1), Inches(2.1)]
for row in perf_table.rows:
    for idx, width in enumerate(p_widths):
        row.cells[idx].width = width

p_headers = ["Evaluation Metric", "Static Baseline (No SDN)", "Proposed (Dynamic SDN + ARQ)"]
for i, h in enumerate(p_headers):
    c = perf_table.cell(0, i)
    set_cell_background(c, "102C57")
    set_cell_margins(c, top=60, bottom=60, left=80, right=80)
    p = c.paragraphs[0]
    r = p.add_run(h)
    r.font.name = 'Calibri'
    r.font.size = Pt(9)
    r.font.bold = True
    r.font.color.rgb = RGBColor(255, 255, 255)

perf_data = [
    ("Total Message Chunks", "15 Chunks", "15 Chunks"),
    ("Primary Link Cut Injected", "Yes (at Chunk 5)", "Yes (at Chunk 5)"),
    ("Network Failover Latency", "Infinite (No alternate path)", "< 0.5 seconds"),
    ("Retransmissions Incurred", "8 Retries (Exhausted)", "1 Retransmission"),
    ("Transmission Status", "Failed / Session Broken", "100% Complete & Delivered"),
    ("Total Completion Time", "Timed Out (> 16.0s)", "8.4 seconds"),
    ("Integrity Check (CRC-32)", "Truncated / Corrupted", "100% In-Order Match")
]

for row_idx, data in enumerate(perf_data, start=1):
    bg_color = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(data):
        c = perf_table.cell(row_idx, col_idx)
        set_cell_background(c, bg_color)
        set_cell_margins(c, top=50, bottom=50, left=80, right=80)
        p = c.paragraphs[0]
        r = p.add_run(text)
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        if col_idx == 0:
            r.font.bold = True
        r.font.color.rgb = COLOR_TEXT

# ==================== CONCLUSION & REPRODUCTION ====================
add_heading_1("6. REPRODUCTION INSTRUCTIONS")
add_body_p(
    "1. Clone the project repository and enter the directory:\n"
    "    git clone https://github.com/<your-username>/<your-repo-name>.git && cd sdn-socket-project\n"
    "2. Start Mininet with the multi-path topology:\n"
    "    sudo mn -c && sudo python3 topology.py\n"
    "3. Start the SDN controller in a second terminal:\n"
    "    sudo python3 sdn_controller.py\n"
    "4. Spawn host shells in Mininet ('xterm h1 h2') and launch:\n"
    "    h2 terminal: python3 receiver.py\n"
    "    h1 terminal: python3 sender.py\n"
    "5. Inject link failure during active streaming: mininet> link s1 s2 down"
)

add_heading_1("7. CONCLUSION")
add_body_p(
    "This project successfully integrated low-level UDP socket programming with Software-Defined Networking. The application-level Stop-and-Wait protocol ensures zero data loss, CRC-32 integrity validation, and duplicate rejection. Simultaneously, the SDN control plane provides sub-second network self-healing by detecting interface state transitions and rewriting OpenFlow 1.3 flow tables. Together, they demonstrate robust, fault-tolerant communication over an unreliable network fabric."
)

output_filename = "Project_Report.docx"
doc.save(output_filename)
print(f"Successfully generated: {output_filename}")
