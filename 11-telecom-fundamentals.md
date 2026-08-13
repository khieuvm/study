# 11 - Telecom Fundamentals for C/C++ Engineers — Bilingual VI/EN

Kiến thức telecom cơ bản dành cho C/C++ engineer chuyển sang làm việc trong môi trường viễn thông (Ericsson, Nokia, Tieto...).
Bao gồm: 3GPP, LTE/4G, 5G NR, protocol stack, DSP/multi-core, RTOS, và telecom software engineering practices.

---

## BẢNG GIẢI THÍCH VIẾT TẮT (Abbreviation Glossary)

Các viết tắt telecom thường gặp, giải thích cho người mới bắt đầu:

### Mạng và Kiến trúc (Network & Architecture)

| Viết tắt | Đầy đủ | Giải thích |
|---|---|---|
| **UE** | User Equipment | Thiết bị của nguoi dùng (điện thoại, modem, IoT device) |
| **RAN** | Radio Access Network | Phần mạng vô tuyến, báo gồm các trạm gốc (eNodeB/gNodeB) |
| **CN** | Core Network | Phần mạng lỗi, xử lý đang ky, xác thực, kết nối Internet |
| **eNodeB** | evolved NodeB | Trạm gốc (base station) trong 4G LTE. "NodeB" là ten từ 3G, "e" = evolved |
| **gNodeB** | next-generation NodeB | Trạm gốc trong 5G NR. "g" = next generation |
| **EPC** | Evolved Packet Core | Core network của 4G LTE |
| **5GC** | 5G Core | Core network của 5G |
| **MME** | Mobility Management Entity | Node signaling chính trong EPC — xử lý attach, handover, paging |
| **S-GW** | Serving Gateway | Node chuyển tiếp user data trong EPC, anchor khi handover |
| **P-GW** | PDN Gateway | Gateway kết nối ra Internet, cấp phát địa chỉ IP |
| **HSS** | Home Subscriber Server | Cơ sở dữ liệu subscriber (thông tin thuê báo, khóa xác thực) |
| **AMF** | Access and Mobility Management Function | Tương đương MME trong 5G Core |
| **UPF** | User Plane Function | Tương đương S-GW + P-GW (user plane) trong 5G Core |
| **UDM** | Unified Data Management | Tương đương HSS trong 5G Core |
| **Cũ** | Central Unit | Phần trung tạm của gNodeB (xử lý RRC, PDCP) |
| **Đủ** | Distributed Unit | Phần phần tan của gNodeB (xử lý RLC, MAC, High-PHY) |
| **RU** | Radio Unit | Phần radio của gNodeB (xử lý Low-PHY, RF) |
| **O-RAN** | Open RAN | Kiến trúc RAN mo, cho phép thiết bị từ nhiều vendor làm viec cũng nhau |

### Protocol Stack

| Viết tắt | Đầy đủ | Giải thích |
|---|---|---|
| **PHY** | Physical Layer | Lop vật lý — xử lý tín hiệu radio: điều chế, mã hóa, OFDM |
| **MAC** | Medium Access Control | Lop điều khiển truy nhập — scheduling, HARQ, multiplexing |
| **RLC** | Radio Link Control | Lop điều khiển liên kết radio — phân đoạn (segmentation), lặp lai (ARQ) |
| **PDCP** | Packet Data Convergence Protocol | Nên header, mã hóa (ciphering), báo ve toan ven (integrity) |
| **SDAP** | Service Data Adaptation Protocol | (Chi 5G) Anh xa QoS flow sáng radio bearer |
| **RRC** | Radio Resource Control | Quản lý kết nối radio, mobility, cấu hình do luồng |
| **NAS** | Non-Access Stratum | Signaling end-to-end giữa UE và core (Attach, Authentication) |
| **L1/L2/L3** | Layer 1/2/3 | PHY = L1, MAC+RLC+PDCP = L2, RRC = L3 |

### Giao thức và Kỹ thuật (Protocols & Techniques)

| Viết tắt | Đầy đủ | Giải thích |
|---|---|---|
| **3GPP** | 3rd Generation Partnership Project | To chuc tiêu chuẩn hóa mạng di động quốc tế |
| **TS** | Technical Specification | Van ban tiêu chuẩn kỹ thuật của 3GPP |
| **LTE** | Long Term Evolution | Ten gọi thế hệ mạng 4G |
| **NR** | New Radio | Ten gọi giao diện vô tuyến 5G |
| **OFDM** | Orthogonal Frequency Division Multiplexing | Kỹ thuật chia bawng tan thành nhiều sóng mạng còn vuông góc — chong nhiều tốt |
| **MIMO** | Multiple Input Multiple Output | Dùng nhiều anten phát/thu đồng thời để tăng throughput |
| **QoS** | Quality of Service | Đảm bảo chat luồng dịch vụ (do tre, throughput, mat gọi) |
| **HARQ** | Hybrid Automatic Repeat reQuest | Kết hợp FEC + retransmission, tăng do tin cậy truyền dẫn |
| **ARQ** | Automatic Repeat reQuest | Cơ chế yêu cầu gửi lại gọi bị lỗi |
| **FEC** | Forward Error Correction | Mã hóa sua lỗi: thêm redundancy để receiver từ sua lỗi |
| **RACH** | Random Access Channel | Kênh để UE truy nhập mạng lan đầu (gửi preamble) |
| **DRX** | Discontinuous Reception | UE tắt radio định ky để tiet kiểm pin |
| **RNTI** | Radio Network Temporary Identifier | Định danh tạm thoi của UE trong cell (dùng cho scheduling) |
| **SRB** | Signaling Radio Bearer | Kênh mạng tín hiệu điều khiển giữa UE và eNodeB |
| **DRB** | Data Radio Bearer | Kênh mạng dữ liệu nguoi dùng giữa UE và eNodeB |
| **TTI** | Transmission Time Interval | Khoang thời gian truyen 1 subframe (1ms trong LTE) |
| **SCS** | Subcarrier Spacing | Khoang cách giữa các sóng mạng còn trong OFDM |
| **BWP** | Bandwidth Part | (5G) Phần bảng thong mà UE được cấu hình để monitor |

### Giao thức mạng (Network Protocols)

| Viết tắt | Đầy đủ | Giải thích |
|---|---|---|
| **S1AP** | S1 Application Protocol | Giao thức signaling giữa eNodeB và MME |
| **X2AP** | X2 Application Protocol | Giao thức signaling giữa các eNodeB (dùng cho handover) |
| **GTP** | GPRS Tunneling Protocol | Giao thức đóng gói (tunnel) dữ liệu qua core network |
| **GTP-U** | GTP User plane | Tunnel dữ liệu nguoi dùng (UDP port 2152) |
| **GTP-C** | GTP Control plane | Tunnel signaling quản lý session (UDP port 2123) |
| **TEID** | Tunnel Endpoint Identifier | ID 32-bit định danh đầu cũối tunnel, định tuyến dữ liệu |
| **SCTP** | Stream Control Transmission Protocol | Transport protocol cho signaling telecom (thay TCP) |
| **ASN.1** | Abstract Syntax Notation One | Ngon ngu mô tả cấu trúc message, dùng trong telecom từ 1984 |
| **PER** | Packed Encoding Rules | Cách encode ASN.1 compact nhất (dùng cho RRC, S1AP) |
| **UPER** | Unaligned PER | PER không cần byte-align (dùng cho RRC messages) |

### Phần mềm và Hệ thống (Software & Systems)

| Viết tắt | Đầy đủ | Giải thích |
|---|---|---|
| **DSP** | Digital Signal Processor | Vi xử lý chuyên xử lý tín hiệu số — dùng cho PHY layer |
| **GPP** | General Purpose Processor | Vi xử lý đa năng (ARM, x86) — dùng cho L3, OAM |
| **RTOS** | Real-Time Operating System | OS đảm bảo thời gian đáp ứng cố định (VxWorks, OSE) |
| **OSE** | Operating System Embedded | RTOS của Enea, dùng nhiều trong Ericsson — IPC bằng signals |
| **FPGA** | Field-Programmable Gate Array | Chip lập trình được, xử lý song song — dùng cho L1 |
| **IPC** | Inter-Process Communication | Giao tiếp giữa các process (message, shared memory) |
| **DMA** | Direct Memory Access | Chuyển data giữa memory regions không cần CPU |
| **ISSU** | In-Service Software Upgrade | Nâng cấp phần mềm không cần tắt hệ thống |
| **MTBF** | Mean Time Between Failures | Thời gian trung bình giữa các lần lỗi |
| **OAM** | Operation, Administration, Maintenance | Hệ thống quản lý và cấu hình |
| **NFV** | Network Function Virtualization | Ảo hóa các chức năng mạng trên phần mềm |
| **NSA** | Non-Standalone | 5G dùng 4G core (giai đoạn chuyển tiếp) |
| **SA** | Standalone | 5G dùng 5G core đầy đủ |

---

## Phần 1: TONG QUAN Mạng Vìễn thông (Cellular Network Overview)

---

### Q1. Mô tả kiến trúc tong quan của một mạng cellular (từ 2G đến 5G). Các thành phần chính là gì?

**A:**
- EN: A cellular network has three main components: UE (User Equipment), RAN (Radio Access Network — eNodeB/gNodeB), and CN (Core Network — EPC/5GC). Architecture evolved from hierarchical (2G/3G) to flat (4G/5G) with control/user plane separation.
- VI: Mạng cellular gồm 3 thành phần chính: UE (thiết bị đầu cũối), RAN (mạng truy nhập vô tuyến — eNodeB/gNodeB), và CN (core network — EPC/5GC). Kiến trúc tiến hóa từ phân cấp (2G/3G) sáng phang (4G/5G) với tách riêng control/user plane.

Mạng cellular gồm 3 thành phần chính:

| Thành phần | Vai tro | Ví dụ |
|---|---|---|
| **UE (User Equipment)** | Thiết bị đầu cũối (điện thoại, IoT device) | Smartphone, modem |
| **RAN (Radio Access Network)** | Mạng truy nhập vô tuyến, kết nối UE với core | eNodeB (4G), gNodeB (5G) |
| **CN (Core Network)** | Xử lý đang ky, xác thực, định tuyến, tinh cuộc | EPC (4G), 5GC (5G) |

**Tiến hóa qua các thế hệ:**

```
2G (GSM):     MS  --> BTS --> BSC --> MSC/VLR --> HLR
3G (UMTS):    UE  --> NodeB --> RNC --> SGSN/GGSN --> HSS
4G (LTE):     UE  --> eNodeB ------------> MME/S-GW/P-GW --> HSS
5G (NR):      UE  --> gNodeB (CU/DU/RU) -> AMF/SMF/UPF --> UDM
```

**Xu hướng tiến hóa:**
- **Flat architecture**: giảm số node trung gian (3G có RNC, 4G bỏ RNC, eNodeB kết nối thang core)
- **Control/User plane separation (CUPS)**: tách riêng signaling và data (5G làm triet để)
- **Virtualization**: từ hardware chuyên dụng sáng NFV/cloud-native (5G)

**Lien he C/C++:** Phần lớn software trên eNodeB/gNodeB (RAN side) được viết bằng C/C++ chạy trên DSP/multi-core platforms. Đầy là nơi C/C++ engineer làm viec nhiều nhất.

---

### Q2. 3GPP là gì? Release là gì? Tại sao developer cần biết ve 3GPP?

**A:**
- EN: 3GPP is the international standards body that defines mobile network protocols and architecture through numbered Releases. Developers must know 3GPP because every code feature traces back to a specific TS (Technical Specification) section. 36.xxx = LTE, 38.xxx = 5G NR.
- VI: 3GPP là tổ chức tiêu chuẩn quốc tế định nghĩa giao thức và kiến trúc mạng di động qua các Release. Developer cần biết 3GPP vì mọi feature trong code trace nguoc ve 1 section TS cụ thể. 36.xxx = LTE, 38.xxx = 5G NR.

**3GPP (3rd Generation Partnership Project)** là tổ chức tiêu chuẩn hóa quốc tế, định nghĩa các giao thức và kiến trúc cho mạng di động.

- Gom 7 tổ chức thành vien: ETSI (Chau Au), ARIB/TTC (Nhất), CCSA (Trung Quoc), ATIS/TIA (My), TTA (Han Quoc)
- Không sản xuất phần mềm/phần cứng — chi tạo **specifications (specs)**

**Release system:**

| Release | Năm | Công nghệ chính |
|---|---|---|
| R8/R9 | 2008-2010 | LTE (4G) cơ bản |
| R10/R11 | 2011-2013 | LTE-Advanced (CA, eICIC) |
| R12/R13 | 2014-2016 | LTE-A Pro, NB-IoT, eMTC |
| R15 | 2018 | **5G NR Phase 1** (NSA + SA) |
| R16 | 2020 | 5G NR Phase 2 (URLLC, V2X) |
| R17 | 2022 | NTN, RedCap, XR |
| R18+ | 2024+ | 5G-Advanced |

**Tại sao developer cần biết:**
- Mọi tính năng trong code đều trace nguoc ve một spec 3GPP cụ thể (VD: TS 36.321 cho MAC layer LTE)
- Khi implement một feature, ban đọc spec để hiểu chính xác behavior cần làm
- Code review thường reference 3GPP section number

**Cách đọc 3GPP spec:**
- **TS = Technical Specification** (spec chính thực)
- **36.xxx** = LTE series, **38.xxx** = 5G NR series
- VD: **TS 38.331** = 5G NR RRC specification

```
Vi du doc spec:
TS 36.321 Section 5.4.3.1 — Random Access procedure
  -> Day la noi mo ta chinh xac cac buoc RACH trong LTE
  -> Developer doc section nay de implement RACH module
```

---

### Q3. Phân biệt Non-Standalone (NSA) và Standalone (SA) trong 5G. Tại sao dieu này quan trọng với developer?

**A:**
- EN: NSA (Non-Standalone) uses 4G core with 5G radio (transition phase); SA (Standalone) uses full 5G core + radio (full features including network slicing). Developer impact: gNodeB code must handle both modes, and the X2/Xn interface between eNodeB and gNodeB must be implemented.
- VI: NSA dùng 4G core với 5G radio (giai đoạn chuyển tiếp); SA dùng đầy đủ 5G core + radio (full features gồm cả network slicing). Ảnh hưởng developer: code gNodeB phải handle cả 2 mode, và interface X2/Xn giữa eNodeB và gNodeB phải được implement.

| | NSA (Non-Standalone) | SA (Standalone) |
|---|---|---|
| Core Network | Dùng EPC (4G core) | Dùng 5GC (5G core) |
| Control Plane | Qua LTE eNodeB | Qua 5G gNodeB |
| User Plane | 5G NR + LTE (Dual Connectivity) | Chi 5G NR |
| Deployment | Giai đoạn đầu (tiet kiểm chi phí) | Giai đoạn sau (full 5G features) |
| Network Slicing | Không ho tro | Ho tro đầy đủ |

```
NSA (Option 3x):
  UE ---> eNodeB (control) + gNodeB (data) ---> EPC

SA (Option 2):
  UE ---> gNodeB (control + data) ---> 5GC
```

**Tại sao developer cần biết:**
- Code trên gNodeB phải handle cả 2 mode: khi làm NSA, gNodeB chi xử lý user plane, control plane do eNodeB dam nhận
- Interface giữa eNodeB và gNodeB (X2/Xn) cần được implement
- Testing matrix phức tạp hơn: phải test ca NSA và SA scenarios
- Nhiều operator đang transition từ NSA sáng SA, nên code phải support cả hai

---

## Phần 2: LTE (4G) ARCHITECTURE Chi tiết

---

### Q4. Mô tả chi tiết kiến trúc EPC (Evolved Packet Core) trong LTE. Vai tro của tung node?

**A:**
- EN: LTE EPC consists of: MME (signaling — attach, handover, paging), S-GW (user plane anchor during handover), P-GW (gateway to Internet, IP assignment, QoS), HSS (subscriber database). Key interfaces: S1-MME (S1AP/SCTP), S1-U (GTP-U/UDP), X2 (X2AP/SCTP). Message encoding uses ASN.1.
- VI: EPC của LTE gom: MME (signaling — attach, handover, paging), S-GW (anchor user plane khi handover), P-GW (gateway ra Internet, cấp IP, QoS), HSS (database subscriber). Interface chính: S1-MME (S1AP/SCTP), S1-U (GTP-U/UDP), X2 (X2AP/SCTP). Message encoding dùng ASN.1.

EPC là core network của LTE, gồm các node chính:

```
                    +-------+
                    |  HSS  |  (Home Subscriber Server)
                    +---+---+
                        |
+----+    +--------+  +-+--+   +------+   +------+
| UE +--->| eNodeB +->| MME|   | S-GW +-->| P-GW +---> Internet/IMS
+----+    +--------+  +----+   +------+   +------+
             E-UTRAN     |                    |
                         +--- Control Plane --+
                              User Plane -----+
```

| Node | Chuc nang chính |
|---|---|
| **MME (Mobility Management Entity)** | Signaling: attach, detach, handover, paging, authentication. không xử lý user data |
| **S-GW (Serving Gateway)** | Anchor point cho user plane khi handover giữa eNodeBs. Forward data packets |
| **P-GW (PDN Gateway)** | Kết nối ra mạng ngoài (Internet). Cấp IP, QoS enforcement, charging |
| **HSS (Home Subscriber Server)** | Database lưu thông tin subscriber: profile, authentication keys, location |
| **PCRF (Policy & Charging Rules Function)** | QoS policy, charging rules |

**Interfaces quan trọng:**

| Interface | Giữa | Giao thức |
|---|---|---|
| S1-MME | eNodeB <-> MME | S1AP (SCTP) |
| S1-U | eNodeB <-> S-GW | GTP-U (UDP) |
| X2 | eNodeB <-> eNodeB | X2AP (SCTP) |
| S6a | MME <-> HSS | Diameter |
| S5/S8 | S-GW <-> P-GW | GTP |
| SGi | P-GW <-> Internet | IP |

**Điểm quan trọng cho developer:**
- **S1AP, X2AP** là các protocol stack mà C/C++ engineer thường implement/maintain
- Message encoding dùng **ASN.1** (Abstract Syntax Notation One) — cần hiểu ASN.1 PER/BER encoding
- Transport layer dùng **SCTP** (không phải TCP) — multi-homing, multi-streaming

---

### Q5. eNodeB là gì? Cấu trúc phần mềm bên trong eNodeB như thế nào?

**A:**
- EN: eNodeB is the LTE base station handling all radio functions. Software layers: PHY (DSP, C/Assembly, hard real-time 1ms), MAC (C, scheduling every TTI), RLC/PDCP (C/C++, near real-time), RRC/S1AP/X2AP (C/C++, protocol state machines), OAM (management). L1/L2 require fixed-point math, zero-copy buffers, and lock-free queues.
- VI: eNodeB là trạm gốc LTE xử lý tất cả chức năng radio. Các lop phần mềm: PHY (DSP, C/Assembly, hard real-time 1ms), MAC (C, scheduling mỗi TTI), RLC/PDCP (C/C++, near real-time), RRC/S1AP/X2AP (C/C++, protocol state machines), OAM (management). L1/L2 cần fixed-point math, zero-copy buffer, lock-free queue.

**eNodeB (evolved NodeB)** là trạm gốc trong LTE, xử lý tất cả các chức năng radio và giao tiếp trực tiếp với core network (không có RNC như 3G).

**Chuc nang chính của eNodeB:**
1. **Radio Resource Management (RRM)**: scheduling, power control, interference management
2. **IP header compression & encryption**: PDCP layer
3. **Mobility management**: handover decisions
4. **Scheduling**: phân bổ tài nguyên radio cho tung UE mỗi ms (subframe)

**Kiến trúc phần mềm eNodeB (giai don):**

```
+--------------------------------------------------+
|                  OAM (Operation & Maintenance)     |
+--------------------------------------------------+
|  RRC  |  S1AP  |  X2AP  |  (Control Plane)       |
+-------+--------+--------+------------------------+
|  PDCP  |  RLC   |  MAC   |  (User + Control)     |
+---------+--------+--------+-----------------------+
|          PHY Layer (L1)                           |
|    (DSP firmware / FPGA - real-time processing)   |
+--------------------------------------------------+
|          RF / Antenna                             |
+--------------------------------------------------+
```

**Mapping vào phần mềm thực tế:**

| Layer | Chạy trên | Ngon ngu | Đặc điểm |
|---|---|---|---|
| PHY (L1) | DSP / FPGA | C / Assembly | Hard real-time, ~1ms deadline |
| MAC (L2) | DSP hoặc ARM | C | Soft real-time, scheduling mỗi TTI (1ms) |
| RLC, PDCP (L2) | ARM / GPP | C/C++ | Near real-time |
| RRC, S1AP, X2AP (L3) | GPP (Linux/RTOS) | C/C++ | Non real-time, complex state machines |
| OAM | GPP | C++/Java/Python | Management, configuration |

**Điểm quan trọng cho C/C++ engineer:**
- **L1/L2** rat performance-critical: fixed-point math, zero-copy buffer, lock-free queue
- **L3** là protocol state machines: ASN.1 encode/decode, timer management, complex logic
- Code thường chia thành nhiều process/thread với IPC (message passing)
- **Memory management** cực kỳ quan trọng: memory pool, pre-allocated buffers, nó malloc at runtime

---

## Phần 3: PROTOCOL STACK Chi tiết

---

### Q6. Giải thích chi tiết LTE/5G protocol stack (L1-L3). Mọi layer làm gì?

**A:**
- EN: LTE/5G protocol stack layers (bottom to top): PHY (modulation, OFDM, channel coding), MAC (scheduling, HARQ, RACH), RLC (segmentation, ARQ in AM mode), PDCP (header compression, ciphering, integrity), RRC (connection management, mobility, bearer setup), NAS (end-to-end UE-to-core signaling, transparent through eNodeB).
- VI: Protocol stack LTE/5G (dưới lên trên): PHY (điều chế, OFDM, mã kênh), MAC (scheduling, HARQ, RACH), RLC (phân đoạn, ARQ trong Âm mode), PDCP (nên header, mã hóa, integrity), RRC (quản lý kết nối, mobility, bearer setup), NAS (signaling end-to-end UE-core, transparent qua eNodeB).

Protocol stack chia thành 3 layer chính, mỗi layer có nhiều sub-layer:

```
+-------------------------------------------+
|  NAS (Non-Access Stratum)                 |  <-- UE <-> Core Network (end-to-end)
+-------------------------------------------+
|  RRC (Radio Resource Control)             |  <-- L3: Connection/mobility mgmt
+-------------------------------------------+
|  PDCP (Packet Data Convergence Protocol)  |  <-- Header compression, ciphering
+-------------------------------------------+
|  RLC (Radio Link Control)                 |  <-- Segmentation, ARQ
+-------------------------------------------+
|  MAC (Medium Access Control)              |  <-- Scheduling, HARQ, multiplexing
+-------------------------------------------+
|  PHY (Physical Layer)                     |  <-- Modulation, coding, OFDM
+-------------------------------------------+
```

**Chi tiết tung layer:**

**1. PHY (Physical Layer) — L1**
- Modulation: QPSK, 16QAM, 64QAM, 256QAM
- OFDMA (downlink) / SC-FDMA (uplink) trong LTE; OFDMA cả hai hướng trong 5G NR
- Channel coding: Turbo code (LTE) / LDPC + Polar code (5G NR)
- MIMO: spatial multiplexing, beamforming
- **Developer task**: implement signal processing algorithms trên DSP, optimize FFT/IFFT

**2. MAC (Medium Access Control) — L2**
- **Scheduling**: quyết định UE nào được truyền data, trên Resource Block nào, mỗi 1ms (LTE) hoặc configurable (5G NR)
- **HARQ (Hybrid ARQ)**: error correction với retransmission. Combine failed + retransmitted data
- **Multiplexing**: gom data từ nhiều logical channel vào 1 transport block
- **Random Access (RACH)**: UE truy nhập mạng lan đầu
- **BSR (Buffer Status Report)**: UE báo cao luồng data cần gửi
- **Developer task**: implement scheduler (rat phức tạp, là "brain" của eNodeB), HARQ manager

**3. RLC (Radio Link Control) — L2**
- 3 modes:
  - **TM (Transparent Mode)**: không xử lý gì, pass-through (dùng cho broadcast)
  - **UM (Unacknowledged Mode)**: segmentation + reassembly, không retransmit (dùng cho VoLTE)
  - **Âm (Acknowledged Mode)**: ARQ (retransmission), reordering, duplicate detection (dùng cho data)
- **Segmentation/Reassembly**: cat RLC SDU thành các RLC PDU vừa với MAC grant
- **Developer task**: implement ARQ state machine, SDU/PDU buffer management

**4. PDCP (Packet Data Convergence Protocol) — L2**
- **Header compression**: ROHC (Robust Header Compression) — nên IP/UDP/RTP header từ ~40 bytes xuống ~1-4 bytes
- **Ciphering (encryption)**: mã hóa data và signaling
- **Integrity protection**: báo ve signaling messages
- **Reordering**: đảm bảo thứ tự packet dùng khi handover
- **Duplicate detection**: loại bỏ packet trung lặp
- **Developer task**: integrate crypto libraries, implement reordering window

**5. RRC (Radio Resource Control) — L3**
- **Connection management**: RRC_IDLE <-> RRC_CONNECTED (+ RRC_INACTIVE trong 5G)
- **Mobility**: measurement configuration, handover command
- **System Information**: broadcast thông tin cell (SIB1, SIB2...)
- **Security**: activate ciphering/integrity
- **Bearer management**: thiết lập/modify/release radio bearers
- **Developer task**: implement complex state machines, ASN.1 encode/decode cho RRC messages

**6. NAS (Non-Access Stratum)**
- Chạy end-to-end giữa UE và MME/AMF (transparent qua eNodeB)
- Attach/Detach, Authentication, PDN connectivity
- eNodeB chi forward NAS messages, không xử lý nội dung

---

### Q7. HARQ (Hybrid ARQ) hoạt động như thế nào? Tại sao no quan trọng trong telecom?

**A:**
- EN: HARQ combines Forward Error Correction with retransmission. Receiver stores failed data, combines with retransmission (Chase Combining or Incremental Redundancy). LTE: 8 parallel HARQ processes, 8ms round-trip. 5G NR: 16 processes, flexible timing. Critical for performance — runs every 1ms TTI.
- VI: HARQ kết hợp FEC với retransmission. Receiver lưu data lỗi, kết hợp với retransmission (Chase Combining hoặc Incremental Redundancy). LTE: 8 HARQ process song song, 8ms round-trip. 5G NR: 16 process, timing linh hoạt. Cực kỳ quan trọng cho performance — chạy mỗi 1ms TTI.

HARQ kết hợp Forward Error Correction (FEC) với Automatic Repeat reQuest (ARQ) để tăng do tin cậy truyền dẫn.

**Nguyen ly:**

```
Sender (eNodeB)                    Receiver (UE)
    |                                   |
    |--- Data (1st transmission) ------>|
    |                                   | Decode? FAIL
    |<-------- NACK -------------------|  (luu data vao buffer)
    |                                   |
    |--- Data (retransmission) -------->|
    |                                   | Combine 1st + 2nd -> Decode? OK
    |<-------- ACK --------------------|
    |                                   |
```

**Chase Combining vs Incremental Redundancy:**

| Kiểu | Mô tả | Hiệu quả |
|---|---|---|
| **Chase Combining (CC)** | Retransmit cũng 1 data, combine bằng cách cổng tín hiệu (soft combining) | Đơn gìản, SNR gain ~3dB |
| **Incremental Redundancy (IR)** | Retransmit các redundancy bits khác nhau, giảm code rate | Hiệu quả hon CC, dùng nhiều trong thực tế |

**Trong LTE:**
- **8 HARQ processes** chạy song song (pipeline) để không phải đổi ACK/NACK trước khi gửi data mọi
- Round-trip time: 8ms (4ms processing + 4ms transmission)
- Synchronous HARQ (uplink), Asynchronous HARQ (downlink)

**Trong 5G NR:**
- So HARQ process tăng lên **16** (linh hoạt hon)
- Timing linh hoạt hon (không cố định 8ms như LTE)

```c
// Simplified HARQ process state machine
typedef enum {
    HARQ_IDLE,
    HARQ_WAITING_ACK,
    HARQ_NACK_RECEIVED,
    HARQ_MAX_RETX_REACHED
} harq_state_t;

typedef struct {
    harq_state_t state;
    uint8_t process_id;
    uint8_t retx_count;
    uint8_t max_retx;        // typically 4
    uint8_t* soft_buffer;    // store for combining
    uint32_t soft_buffer_size;
    uint8_t redundancy_version; // 0,1,2,3
} harq_process_t;

void harq_handle_feedback(harq_process_t* proc, bool ack) {
    if (ack) {
        proc->state = HARQ_IDLE;
        proc->retx_count = 0;
        free_soft_buffer(proc);
    } else {
        proc->retx_count++;
        if (proc->retx_count >= proc->max_retx) {
            proc->state = HARQ_MAX_RETX_REACHED;
            // notify RLC for ARQ retransmission
        } else {
            proc->state = HARQ_NACK_RECEIVED;
            proc->redundancy_version = (proc->redundancy_version + 1) % 4;
        }
    }
}
```

**Tại sao quan trọng:**
- HARQ là một trong nhưng module performance-critical nhất — chạy mỗi 1ms TTI
- Buffer management của soft combining cần tối ưu memory
- Sai logic HARQ -> mat data hoặc giảm throughput nghiêm trọng

---

### Q8. ASN.1 là gì? Tại sao no được dùng trong telecom? Làm sao C/C++ engineer làm viec với ASN.1?

**A:**
- EN: ASN.1 (Abstract Syntax Notation One) is a data structure description language used in telecom to define messages. Encoding rules: PER/UPER for RRC messages (most compact), APER for S1AP/X2AP. Workflow: ASN.1 spec → ASN.1 compiler → generated C/C++ encode/decode code. Developer integrates generated code into protocol stack.
- VI: ASN.1 là ngon ngu mô tả cấu trúc dữ liệu dùng trong telecom để định nghĩa message. Encoding rules: PER/UPER cho RRC messages (compact nhất), APER cho S1AP/X2AP. Workflow: ASN.1 spec → ASN.1 compiler → code C/C++ encode/decode. Developer integrate code generated vào protocol stack.

**ASN.1 (Abstract Syntax Notation One)** là ngon ngu mô tả cấu trúc dữ liệu, được dùng rong rai trong telecom để định nghĩa các messages giữa các node mạng.

**Tại sao dùng ASN.1 (không dùng JSON/Protobuf)?**
- Được chuan hoa boi ITU-T từ 1984, trước khi có JSON/Protobuf
- **Compact encoding**: tiet kiểm bandwidth trên radio interface
- **Formal specification**: 3GPP specs định nghĩa messages bằng ASN.1
- **Cross-platform**: bất kỳ implementation nào cũng decode được

**Encoding rules:**

| Encoding | Đặc điểm | Dùng trong |
|---|---|---|
| **BER (Basic)** | Tag-Length-Value, variable length | General purpose |
| **DER (Distinguished)** | Canonical form của BER | Certificates, security |
| **PER (Packed)** | Compact nhất, bit-aligned | **RRC, S1AP** (telecom) |
| **UPER (Unaligned PER)** | Không align theo byte | **RRC messages** |
| **APER (Aligned PER)** | Align theo byte | **S1AP, X2AP messages** |

**Ví dụ ASN.1 definition từ 3GPP TS 36.331 (RRC):**

```asn1
-- RRC Connection Request message
RRCConnectionRequest ::= SEQUENCE {
    criticalExtensions CHOICE {
        rrcConnectionRequest-r8 RRCConnectionRequest-r8-IEs,
        ...
    }
}

RRCConnectionRequest-r8-IEs ::= SEQUENCE {
    ue-Identity     InitialUE-Identity,
    establishmentCause  EstablishmentCause,
    spare           BIT STRING (SIZE (1))
}

EstablishmentCause ::= ENUMERATED {
    emergency, highPriorityAccess, mt-Access,
    mo-Signalling, mo-Data, delayTolerantAccess-v1020,
    mo-VoiceCall-v1280, spare1
}
```

**Workflow cho developer:**

```
3GPP ASN.1 spec (.asn file)
        |
        v
   ASN.1 Compiler (asn1c, ffasn1c, commercial tools)
        |
        v
   Generated C/C++ code (encode/decode functions)
        |
        v
   Developer integrate vao protocol stack
```

**Ví dụ code C sau khi generate:**

```c
// Encoding RRC Connection Request
RRCConnectionRequest_t *msg = calloc(1, sizeof(*msg));
msg->criticalExtensions.present = 
    RRCConnectionRequest__criticalExtensions_PR_rrcConnectionRequest_r8;

RRCConnectionRequest_r8_IEs_t *r8 = 
    &msg->criticalExtensions.choice.rrcConnectionRequest_r8;
r8->establishmentCause = EstablishmentCause_mo_Data;

// Encode to UPER
asn_enc_rval_t enc_ret;
uint8_t buffer[128];
enc_ret = uper_encode_to_buffer(
    &asn_DEF_RRCConnectionRequest, NULL, msg, buffer, sizeof(buffer));

if (enc_ret.encoded > 0) {
    int bytes = (enc_ret.encoded + 7) / 8;
    send_to_lower_layer(buffer, bytes);
}
ASN_STRUCT_FREE(asn_DEF_RRCConnectionRequest, msg);
```

**Developer cần biết:**
- Không phải tự viết encoder/decoder — dùng ASN.1 compiler
- Cần hiểu ASN.1 syntax để đọc spec và debug
- Memory management của generated code (calloc/free patterns)
- UPER encoding là bit-level, debug kho hon byte-level protocols

---

### Q9. Giải thích qua trình RRC Connection Setup trong LTE. Các bước và message nào trao đổi?

**A:**
- EN: RRC Connection Setup: (1) UE sends RRCConnectionRequest via RACH, (2) eNodeB responds with RRCConnectionSetup (SRB1 config), (3) UE sends RRCConnectionSetupComplete (with NAS Attach Request), (4) eNodeB forwards to MME via S1AP. Total: ~10-15ms. Implementation involves RRC state machine, ASN.1 UPER encoding, and timer management.
- VI: RRC Connection Setup: (1) UE gửi RRCConnectionRequest qua RACH, (2) eNodeB trả lỗi RRCConnectionSetup (cấu hình SRB1), (3) UE gửi RRCConnectionSetupComplete (kem NAS Attach Request), (4) eNodeB forward lên MME qua S1AP. Tong: ~10-15ms. Implementation gom RRC state machine, ASN.1 UPER encoding, và timer management.

RRC Connection Setup là qua trình UE thiết lập kết nối signaling với eNodeB.

```
     UE                          eNodeB                         MME
      |                              |                            |
      |-- (1) RRCConnectionRequest ->|                            |
      |      (via RACH: preamble +   |                            |
      |       Msg3 on UL-SCH)        |                            |
      |                              |                            |
      |<- (2) RRCConnectionSetup ----|                            |
      |      (SRB1 config, MAC       |                            |
      |       config, PHY config)    |                            |
      |                              |                            |
      |-- (3) RRCConnectionSetup --->|                            |
      |       Complete               |                            |
      |      (+ NAS: Attach Request) |                            |
      |                              |-- (4) S1AP: Initial UE --->|
      |                              |       Message              |
      |                              |       (NAS forwarded)      |
      |                              |                            |
```

**Chi tiết từng bước:**

**Bước 1: RRCConnectionRequest (UE -> eNodeB)**
- UE gửi qua RACH (Random Access Channel): preamble -> RAR -> Msg3
- Nội dùng: UE identity (S-TMSI hoặc random), establishment cause (mo-Data, emergency, ...)
- Encoded: UPER, rat ngan (~6 bytes)

**Bước 2: RRCConnectionSetup (eNodeB -> UE)**
- eNodeB cấu hình SRB1 (Signaling Radio Bearer 1)
- Chưa cấu hình: RLC config, MAC config (BSR, PHR, DRX), PHY config (CQI reporting, SRS)
- UE ap dùng các config này và chuyển sáng RRC_CONNECTED

**Bước 3: RRCConnectionSetupComplete (UE -> eNodeB)**
- UE xác nhận đã cấu hình xong
- Định kem NAS message (VD: Attach Request) để eNodeB forward lên MME
- Từ đầy SRB1 được thiết lập, UE có thể gửi/nhận signaling

**Implementation perspective (C/C++):**

```c
// RRC state machine trong eNodeB
typedef enum {
    RRC_IDLE,
    RRC_CONNECTION_SETUP_PENDING,
    RRC_CONNECTED,
    RRC_CONNECTION_RELEASE_PENDING
} rrc_state_t;

typedef struct {
    rrc_state_t state;
    uint16_t ue_id;
    uint16_t rnti;         // Radio Network Temporary Identifier
    timer_t setup_timer;   // T300-like timer
    // ... bearer configs
} rrc_ue_context_t;

void handle_rrc_connection_request(
    rrc_ue_context_t* ctx,
    RRCConnectionRequest_t* msg)
{
    // 1. Allocate RNTI for UE
    ctx->rnti = allocate_rnti();
    
    // 2. Build RRCConnectionSetup message
    RRCConnectionSetup_t* setup = build_rrc_conn_setup(ctx);
    
    // 3. Encode (UPER) and send via MAC
    uint8_t buf[256];
    int len = encode_uper_rrc_conn_setup(setup, buf, sizeof(buf));
    mac_send_dl(ctx->rnti, LCID_SRB0, buf, len);
    
    // 4. Start timer, wait for Complete
    ctx->state = RRC_CONNECTION_SETUP_PENDING;
    start_timer(&ctx->setup_timer, T300_MS);
}
```

**Điểm thường hỏi trong phỏng vấn:**
- Toan bỏ qua trình mat báo lau? (~10-15ms)
- Khi nào cần RRC Connection Rẻ-establishment? (radio link failure, handover failure)
- Tại sao dùng UPER encoding cho RRC messages? (tiet kiểm bandwidth trên air interface)

---

## Phần 4: 5G NR — Điểm Khác Biết

---

### Q10. 5G NR khác gì số với LTE ve mat protocol stack và kiến trúc? Nhưng điểm nào ảnh hưởng đến software implementation?

**A:**
- EN: 5G NR key differences from LTE: CU/DU/RU disaggregation, flexible numerology (15/30/60/120/240 kHz subcarrier spacing), mini-slots for URLLC, new SDAP layer for QoS flow mapping, RRC_INACTIVE state, dynamic TDD, beam management. Numerology impacts all timing — slot duration = 1ms / 2^mu.
- VI: 5G NR khác LTE chính: Cũ/Đủ/RU tách rời, numerology linh hoạt (15/30/60/120/240 kHz subcarrier spacing), mini-slot cho URLLC, layer SDAP mọi cho QoS flow mapping, trang thai RRC_INACTIVE, dynamic TDD, beam management. Numerology ảnh hưởng tất cả timing — slot duration = 1ms / 2^mu.

**Kiến trúc gNodeB: Cũ/Đủ/RU split**

5G NR tách gNodeB thành 3 phần (O-RAN architecture):

```
LTE eNodeB (monolithic):          5G gNodeB (disaggregated):
+------------------+              +-------+
|  RRC, PDCP       |              |  CU   | (Central Unit)
|  RLC, MAC        |              |  RRC, PDCP, SDAP
|  PHY             |              +---+---+
+------------------+                  | F1 interface
                                  +---+---+
                                  |  DU   | (Distributed Unit)
                                  |  RLC, MAC, High-PHY
                                  +---+---+
                                      | Fronthaul (eCPRI)
                                  +---+---+
                                  |  RU   | (Radio Unit)
                                  |  Low-PHY, RF
                                  +-------+
```

**Điểm khác biết chính ảnh hưởng đến implementation:**

| Feature | LTE | 5G NR | Impact lên code |
|---|---|---|---|
| Subcarrier spacing | 15 kHz cố định | 15/30/60/120/240 kHz (numerology) | Flexible timing, scheduling phức tạp hon |
| Slot duration | 1ms cố định | 0.0625ms - 1ms (tuy numerology) | Timer resolution cao hơn |
| Bandwidth Part (BWP) | Không có | Có | UE chi monitor 1 phần của carrier bandwidth |
| Mini-slot | Không có | 2/4/7 symbols | Low-latency scheduling, URLLC |
| SDAP layer | Không có | Có (mọi) | QoS flow mapping, thêm 1 layer xử lý |
| Beam management | Đơn gìản | Beam sweeping, beam tracking | Phức tạp hon nhiều, mỗi cell nhiều beam |
| RRC state | IDLE / CONNECTED | IDLE / **INACTIVE** / CONNECTED | Thêm 1 state, tiet kiểm pin và signaling |
| Duplex | FDD / TDD | FDD / TDD / **Dynamic TDD** | Scheduler phải handle linh hoạt DL/UL |
| DRX | Đơn gìản | Multi-level DRX | Power saving phức tạp hon |

**SDAP (Service Data Adaptation Protocol) — layer mọi trong 5G:**

```
IP packet voi QoS Flow ID (QFI)
        |
   +----v----+
   |  SDAP   |  Map QFI -> DRB (Data Radio Bearer)
   +---------+
        |
   +----v----+
   |  PDCP   |
   +---------+
```

**Numerology — concept mọi quan trọng nhất:**

```
Numerology (mu) | SCS    | Slot duration | Symbols/slot | Use case
0               | 15 kHz | 1 ms          | 14           | LTE-like, sub-6 GHz
1               | 30 kHz | 0.5 ms        | 14           | Sub-6 GHz 5G (pho bien)
2               | 60 kHz | 0.25 ms       | 14           | Sub-6 & mmWave
3               | 120 kHz| 0.125 ms      | 14           | mmWave (FR2)
4               | 240 kHz| 0.0625 ms     | 14           | mmWave (sync only)
```

**Code impact:**
```c
// LTE: thoi gian co dinh
#define TTI_MS  1  // luon la 1ms

// 5G NR: thoi gian phu thuoc numerology
static inline double slot_duration_ms(uint8_t numerology) {
    return 1.0 / (1 << numerology);  // 1ms, 0.5ms, 0.25ms, ...
}

// Scheduler phai aware numerology
void nr_schedule_slot(uint8_t mu, uint16_t slot_idx) {
    double slot_dur = slot_duration_ms(mu);
    // Mini-slot scheduling for URLLC
    if (has_urllc_traffic()) {
        schedule_mini_slot(2);  // 2-symbol mini-slot
    }
    // eMBB scheduling
    schedule_full_slot(slot_idx);
}
```

---

## Phần 5: DSP Và MULTI-CORE PLATFORMS

---

### Q11. DSP (Digital Signal Processor) là gì? Tại sao telecom dùng DSP? So sánh DSP vs GPP (General Purpose Processor)?

**A:**
- EN: DSP (Digital Signal Processor) is optimized for repetitive signal processing with deterministic timing. Telecom uses DSP for PHY/MAC layers requiring hard real-time (~1ms deadline). Key differences from GPP: fixed-point hardware, tightly-coupled memory, DMA, software pipelining, cycle-accurate profiling instead of wall-clock time.
- VI: DSP được tối ưu cho xử lý tín hiệu lặp lai với timing cố định. Telecom dùng DSP cho PHY/MAC layer yêu cầu hard real-time (~1ms deadline). Khác GPP: fixed-point hardware, tightly-coupled memory, DMA, software pipelining, profiling theo cycle thay vì wall-clock time.

**DSP** là vi xử lý chuyên dụng cho xử lý tín hiệu số (digital signal processing), được tối ưu cho các phep tinh toan lặp di lặp lai trên luồng dữ liệu liên tục.

**Tại sao telecom dùng DSP:**
- Xử lý PHY layer cần tinh toan **FFT, filtering, modulation** rat nhanh và cố định (deterministic)
- Cần **hard real-time**: xử lý 1 subframe trong dùng 1ms, không được tre
- Power efficiency cao hơn GPU/CPU cho signal processing workloads

**So sánh:**

| Đặc điểm | DSP | GPP (ARM/x86) | GPU |
|---|---|---|---|
| Tối ưu cho | Signal processing, MAC (multiply-accumulate) | General computing | Parallel computing |
| Pipeline | Deep, specialized | Deep, general | Massively parallel |
| Memory | Tightly coupled (TCM), DMA | Cache hierarchy | Global/shared memory |
| Fixed-point | Hardware support | Software emulation | Limited |
| Real-time | Deterministic | Non-deterministic | Non-deterministic |
| Power | Thấp | Trung binh | Cao |
| Ví dụ | TI C6000, Qualcomm Hexagon | ARM Cortex-A, Intel Xeon | NVIDIA GPU |
| Dùng trong telecom | PHY (L1), MAC (L2) | L2 upper, L3, OAM | 5G massive MIMO (emerging) |

**Kiến trúc DSP điển hình (TI C66x):**

```
+------------------------------------------------------+
|  Core 0  |  Core 1  |  Core 2  |  ...  |  Core 7    |
|  +----+  |  +----+  |  +----+  |       |  +----+    |
|  | L1D|  |  | L1D|  |  | L1D|  |       |  | L1D|    |
|  | L1P|  |  | L1P|  |  | L1P|  |       |  | L1P|    |
|  +----+  |  +----+  |  +----+  |       |  +----+    |
+----------+----------+----------+-------+-------------+
|                   L2 Cache (Shared)                   |
+------------------------------------------------------+
|                   MSMC (Shared RAM)                   |
+------------------------------------------------------+
|          DDR3 Controller -> External RAM              |
+------------------------------------------------------+
|  DMA (EDMA)  |  Ethernet  |  SRIO  |  PCIe  |  ...  |
+------------------------------------------------------+
```

**Lập trình DSP khác GPP:**

```c
// GPP: dung float, compiler toi uu
float result = a * b + c;

// DSP: dung fixed-point de tan dung hardware MAC
// Q15 format: 16-bit integer đại diện số thuc [-1, 1)
int16_t a_q15 = 16384;   // 0.5 in Q15
int16_t b_q15 = 8192;    // 0.25 in Q15
int32_t temp = (int32_t)a_q15 * b_q15;  // MAC instruction
int16_t result_q15 = (int16_t)(temp >> 15);  // 0.125 in Q15

// DSP intrinsics (TI C6000)
#include <c6x.h>
int32_t dot = _dotp2(a_packed, b_packed);  // 2 multiplies in 1 cycle
```

**Nhưng thu developer cần làm khi code DSP:**
- Quản lý memory manually (không có malloc thông thường)
- Dùng DMA để move data giữa memory levels
- Pipeline software manually (software pipelining)
- Align data cho SIMD operations
- Profile cycles, không phải wall-clock time

---

### Q12. Multi-core programming trong telecom khác gì với multi-threading thông thường? Các pattern phổ biến?

**A:**
- EN: Multi-core telecom programming differs from general multi-threading: developer assigns tasks to specific cores (no OS scheduler), uses physical shared memory (possibly non-coherent), message passing or lock-free queues for IPC, DMA for data transfer, and must meet deterministic deadlines. Key patterns: pipeline processing, core affinity + message passing, DMA transfer, manual cache management.
- VI: Multi-core trong telecom khác multi-threading thông thường: developer từ gần task vào core cụ thể (không có OS scheduler), dùng physical shared memory (có thể non-coherent), message passing hoặc lock-free queue cho IPC, DMA để transfer data, và phải đặt deterministic deadline. Pattern chính: pipeline processing, core affinity + message passing, DMA transfer, manual cache management.

Trong telecom embedded, multi-core programming có nhưng đặc thù riêng:

**Khác biết chính:**

| Aspect | Multi-threading (GPP) | Multi-core telecom |
|---|---|---|
| OS | Linux, full OS | RTOS hoặc bare-metal |
| Scheduling | OS scheduler | Developer từ assign task vào core |
| Shared memory | Virtual memory, cache coherent | Physical memory, có thể non-coherent |
| Sync | mutex, condition_variable | Spinlock, HW semaphore, message passing |
| Memory alloc | malloc/free | Memory pools, static allocation |
| Latency | Best-effort | Deterministic, deadline-driven |
| Debug | gdb, valgrind | JTAG, trace buffer, logic analyzer |

**Pattern 1: Pipeline Processing**

```
Core 0 (L1 RX)     Core 1 (MAC)       Core 2 (RLC/PDCP)    Core 3 (L1 TX)
    |                    |                    |                    |
    | subframe data      |                    |                    |
    +----- DMA --------->|                    |                    |
    |                    | decoded TBs         |                    |
    |                    +----- msg queue ---->|                    |
    |                    |                    | IP packets          |
    |                    |                    |                    |
    |                    | scheduling grant    |                    |
    |                    +----- DMA -------------------------------->|
    |                    |                    |                    |
    v                    v                    v                    v
  1ms deadline        1ms deadline         soft RT              1ms deadline
```

**Pattern 2: Core Affinity + Message Passing**

```c
// Moi core chay 1 "task" co dinh, giao tiếp qua message queue
typedef struct {
    uint32_t msg_id;
    uint32_t src_core;
    uint32_t length;
    uint8_t  payload[MAX_MSG_SIZE];
} ipc_msg_t;

// Lock-free SPSC (Single Producer Single Consumer) queue
typedef struct {
    volatile uint32_t head;
    volatile uint32_t tail;
    ipc_msg_t buffer[QUEUE_SIZE];  // power of 2
} spsc_queue_t;

bool spsc_push(spsc_queue_t* q, const ipc_msg_t* msg) {
    uint32_t next = (q->head + 1) & (QUEUE_SIZE - 1);
    if (next == q->tail) return false;  // full
    q->buffer[q->head] = *msg;
    __sync_synchronize();  // memory barrier
    q->head = next;
    return true;
}

bool spsc_pop(spsc_queue_t* q, ipc_msg_t* msg) {
    if (q->head == q->tail) return false;  // empty
    *msg = q->buffer[q->tail];
    __sync_synchronize();
    q->tail = (q->tail + 1) & (QUEUE_SIZE - 1);
    return true;
}
```

**Pattern 3: DMA Transfer (Zero-copy khi có thể)**

```c
// Thay vi memcpy, dung DMA engine de move data giua cores
void transfer_subframe_data(uint8_t src_core, uint8_t dst_core,
                            void* src_addr, void* dst_addr, 
                            uint32_t size) {
    dma_descriptor_t desc = {
        .src = (uint32_t)src_addr,
        .dst = (uint32_t)dst_addr,
        .count = size,
        .mode = DMA_MODE_BLOCK,
        .callback = on_transfer_complete
    };
    dma_submit(&desc);
    // CPU free to do other work while DMA transfers
}
```

**Pattern 4: Shared Memory với Cache Coherence**

```c
// Tren non-coherent multi-core, phai manual cache management
void send_data_to_other_core(void* data, uint32_t size) {
    // 1. Write data
    memcpy(shared_mem_region, data, size);
    
    // 2. Writeback cache (dam bao data ra toi shared memory)
    cache_writeback(shared_mem_region, size);
    
    // 3. Signal other core (qua HW semaphore hoac interrupt)
    hw_semaphore_post(SEM_DATA_READY);
}

void receive_data_from_other_core(void* buf, uint32_t size) {
    // 1. Wait for signal
    hw_semaphore_wait(SEM_DATA_READY);
    
    // 2. Invalidate cache (force re-read tu shared memory)
    cache_invalidate(shared_mem_region, size);
    
    // 3. Read data
    memcpy(buf, shared_mem_region, size);
}
```

---

## Phần 6: RTOS (Real-Time Operating System)

---

### Q13. RTOS là gì? So sánh RTOS với Linux. Khi nào dùng RTOS trong telecom?

**A:**
- EN: RTOS provides deterministic, bounded latency (microseconds) unlike Linux (milliseconds, variable). Used for L1/L2 in telecom. Enea OSE (common in Ericsson): signal-based IPC model (no shared-memory mutexes). VxWorks: task-based, POSIX-like. Choice: bare-metal/RTOS for L1-L2, Linux for L3/OAM.
- VI: RTOS cũng cấp latency cố định, có giới hạn (microsecond) khác Linux (millisecond, biến động). Dùng cho L1/L2 trong telecom. Enea OSE (phổ biến o Ericsson): IPC model dua trên signal (không dùng shared-memory mutex). VxWorks: task-based, giống POSIX. Lua chon: bare-metal/RTOS cho L1-L2, Linux cho L3/OAM.

**RTOS** là hệ điều hành đảm bảo đáp ứng yêu cầu ve thời gian (deadline) một cách **deterministic** (có thể dự đoán được).

**So sánh:**

| Đặc điểm | RTOS (VxWorks, OSE, FreeRTOS) | Linux (General Purpose) |
|---|---|---|
| Scheduling | Priority-based preemptive, deterministic | CFS (Completely Fair Scheduler), best-effort |
| Latency | Microseconds (cố định) | Milliseconds (biến động) |
| Context switch | ~1-5 us | ~5-50 us |
| Interrupt latency | ~1 us, bounded | Variable, có thể bị delay |
| Memory protection | Tuy cấu hình (có thể không có) | Đầy đủ (virtual memory, MMU) |
| Footprint | ~10KB - ~1MB | ~10MB+ |
| File system | Tùy chọn (có thể không có) | Đầy đủ (ext4, btrfs...) |
| Boot time | Milliseconds | Seconds |
| Dùng cho | L1 PHY, L2 MAC (hard real-time) | L3, OAM, management (soft real-time) |

**Phần loại real-time:**

| Loại | Yếu câu | Ví dụ |
|---|---|---|
| **Hard real-time** | Miss deadline = system failure | DSP processing L1 (1ms), HARQ timing |
| **Firm real-time** | Miss deadline = result vo giá trị nhưng không crash | Video frame rendering |
| **Soft real-time** | Miss deadline = giảm chat luồng | RRC signaling, OAM |

**RTOS trong telecom — Enea OSE:**

OSE là RTOS rat phổ biến trong Ericsson products:

```c
// OSE: Signal-based IPC (khong dung mutex/semaphore nhu POSIX)
// Moi process co mailbox, giao tiếp bang signals

// Dinh nghia signal
#define TIMER_EXPIRED_SIG  0x1001
#define DATA_IND_SIG       0x1002

union SIGNAL {
    SIGSELECT sig_no;
    struct timer_expired {
        SIGSELECT sig_no;
        uint32_t timer_id;
    } timer_expired;
    struct data_ind {
        SIGSELECT sig_no;
        uint16_t ue_id;
        uint8_t  data[MAX_DATA_SIZE];
        uint32_t length;
    } data_ind;
};

// Process (co dinh, khong phai thread)
OS_PROCESS(mac_scheduler_proc) {
    static const SIGSELECT sel[] = {2, TIMER_EXPIRED_SIG, DATA_IND_SIG};
    union SIGNAL *sig;
    
    while (1) {
        sig = receive(sel);  // block cho den khi co signal
        
        switch (sig->sig_no) {
            case TIMER_EXPIRED_SIG:
                handle_tti_tick(sig->timer_expired.timer_id);
                break;
            case DATA_IND_SIG:
                handle_data_indication(sig->data_ind.ue_id,
                                       sig->data_ind.data,
                                       sig->data_ind.length);
                break;
        }
        free_buf(&sig);  // tra signal buffer ve pool
    }
}

// Gui signal tu process khac
void send_data_to_mac(uint16_t ue_id, uint8_t* data, uint32_t len) {
    union SIGNAL *sig = alloc(sizeof(struct data_ind), DATA_IND_SIG);
    sig->data_ind.ue_id = ue_id;
    memcpy(sig->data_ind.data, data, len);
    sig->data_ind.length = len;
    send(&sig, mac_scheduler_pid);  // gui toi process MAC scheduler
}
```

**VxWorks basics:**

```c
// VxWorks: task-based, giong POSIX hon
#include <taskLib.h>
#include <semLib.h>
#include <msgQLib.h>

SEM_ID data_sem;
MSG_Q_ID msg_queue;

void mac_task(void) {
    char msg_buf[MAX_MSG_SIZE];
    
    while (1) {
        // Block wait for message
        int len = msgQReceive(msg_queue, msg_buf, MAX_MSG_SIZE, WAIT_FOREVER);
        if (len > 0) {
            process_mac_data(msg_buf, len);
        }
    }
}

void init_mac(void) {
    // Create message queue
    msg_queue = msgQCreate(64, MAX_MSG_SIZE, MSG_Q_FIFO);
    
    // Create task voi priority
    taskSpawn("tMacTask", 
              100,           // priority (0 = highest)
              0,             // options
              8192,          // stack size
              (FUNCPTR)mac_task,
              0,0,0,0,0,0,0,0,0,0);
}
```

**Khi nào dùng gì trong telecom:**

```
+-------------------+---------------------------+
|  L1 PHY (DSP)     |  Bare-metal hoac RTOS     |
|  L2 MAC           |  RTOS (OSE, VxWorks)      |
|  L2 upper (RLC)   |  RTOS hoac RT Linux       |
|  L3 (RRC, S1AP)   |  Linux (hoac RTOS)        |
|  OAM              |  Linux                    |
+-------------------+---------------------------+
```

---

### Q14. Giải thích Priority Inversion trong RTOS. Tại sao no nguy hiểm và cách phong tránh?

**A:**
- EN: Priority Inversion: a high-priority task is blocked because a low-priority task holds a needed lock, and medium-priority tasks preempt the low-priority task — causing unbounded blocking. Solutions: Priority Inheritance Protocol (temporarily boost low task to high's priority), Priority Ceiling Protocol, or message passing instead of shared locks (OSE style). Famous case: Mars Pathfinder 1997.
- VI: Priority Inversion: task priority cao bị block vì task priority thấp giữ lock, và task priority trung bình preempt task thấp — gây blocking vo han. Giai phap: Priority Inheritance Protocol (tạm nang priority task thấp lên bảng task cao), Priority Ceiling Protocol, hoặc message passing thay vì shared lock (kiểu OSE). Case nổi tiếng: Mars Pathfinder 1997.

**Priority Inversion** xảy ra khi task có priority cao bị block boi task có priority thấp — vì task priority thấp giữ lock mà task priority cao cần.

**Kích ban:**

```
Priority:  High(H)  Medium(M)  Low(L)

Time  H                M              L
  |                               [Lock mutex]
  |                               [doing work...]
  |   [Wake up!]                  [still holds mutex]
  |   [Try lock -> BLOCKED]       [still holds mutex]
  |                  [Wake up!]   [preempted by M!]
  |   [STILL blocked]  [running]  [can't run, lower prio than M]
  |   [STILL blocked]  [running]  [STILL holds mutex]
  |   ...              [done]     [resumes, releases mutex]
  |   [Got mutex!]                
```

**Van để**: Task H bị block boi task M (không liên quan) vì task L giữ mutex nhưng bi M preempt. H bị block **vo han định** nếu có nhiều task M.

**Cách phong tránh:**

**1. Priority Inheritance Protocol (PIP):**

```c
// Khi H block tren mutex do L giu:
// -> Tam thoi nang priority cua L len bang H
// -> L chay nhanh, release mutex, H duoc unblock
// -> L tro ve priority cu

// VxWorks: tu dong ho tro
SEM_ID mutex = semMCreate(SEM_Q_PRIORITY | SEM_INVERSION_SAFE);

// POSIX:
pthread_mutexattr_t attr;
pthread_mutexattr_init(&attr);
pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_INHERIT);
pthread_mutex_init(&mutex, &attr);
```

**2. Priority Ceiling Protocol (PCP):**

```c
// Moi mutex co 1 "ceiling priority" = max priority cua tat ca tasks co the lock no
// Khi task lock mutex, priority tam tang len ceiling
// Tranh deadlock va priority inversion hoan toan

// VxWorks:
SEM_ID mutex = semMCreate(SEM_Q_PRIORITY | SEM_INVERSION_SAFE);
// (VxWorks tu implement ceiling internally)

// POSIX:
pthread_mutexattr_setprotocol(&attr, PTHREAD_PRIO_PROTECT);
pthread_mutexattr_setprioceiling(&attr, HIGH_PRIORITY);
```

**3. Dùng message passing thay vì shared mutex (OSE style):**

```c
// Thay vi:
//   Task L: lock(mutex); shared_data = x; unlock(mutex);
//   Task H: lock(mutex); read(shared_data); unlock(mutex);
//
// Dung signal/message:
//   Task L: send(data_signal, task_H_pid);
//   Task H: sig = receive(sel); process(sig->data);
//
// -> Khong co shared lock -> khong co priority inversion
```

**Case study thực tế: Mars Pathfinder (1997)**
- VxWorks RTOS trên Mars rover
- Priority inversion giữa bus management task (low) và data collection task (high)
- System bị reset liên tục do watchdog timer
- Fix: bắt Priority Inheritance cho mutex
- Bài hoc: priority inversion có thể xảy ra trong bất kỳ RTOS system nào

---

## Phần 7: TELECOM SOFTWARE ENGINEERING

---

### Q15. Carrier-grade software có nhưng yêu cầu gì? Tại sao telecom software khác với web/mobile software?

**A:**
- EN: Carrier-grade software requires 99.999% availability (~5min downtime/year), <50ms failover, in-service software upgrade (no downtime), defensive programming (validate all inputs, handle all errors), and watchdog/self-healing. Techniques: active/standby redundancy with state sync, backward-compatible message formats, escalating restart policies.
- VI: Phần mềm carrier-grade yêu cầu 99.999% availability (~5 phut downtime/năm), failover <50ms, nâng cấp phần mềm không downtime (ISSU), defensive programming (validate tất cả input, xử lý mọi lỗi), và watchdog/self-healing. Kỹ thuật: active/standby redundancy với state sync, message format backward-compatible, chính sach restart leo thang.

**Carrier-grade** là tiêu chuẩn chất lượng cho phần mềm viễn thông, đòi hỏi **độ tin cậy cuc cao**.

**Yếu câu carrier-grade:**

| Yếu câu | Mục tiêu | So sánh với web |
|---|---|---|
| **Availability** | 99.999% ("five nines") = ~5 phut downtime/năm | Web: 99.9% = ~8.7 gio/năm |
| **Reliability** | MTBF > 20 năm | Web: MTBF vai thang |
| **Recovery** | Failover < 50ms | Web: failover vai giay |
| **Upgrade** | In-service upgrade (không downtime) | Web: maintenance window OK |
| **Scalability** | Handle hang trieu UE | Web: auto-scale |
| **Performance** | Deterministic latency | Web: best-effort |

**Các kỹ thuật đảm bảo carrier-grade:**

**1. Redundancy & Failover:**

```
+----------+    Heartbeat    +----------+
| Active   |<--------------->| Standby  |
| Node     |    State sync   | Node     |
+----------+                 +----------+
     |                            |
     | Failure detected           |
     | (<50ms)                    |
     +---------> Standby becomes Active
                 (state already synced)
```

```c
// Heartbeat mechanism
typedef struct {
    uint32_t sequence;
    uint64_t timestamp;
    uint32_t state_checksum;
} heartbeat_msg_t;

void heartbeat_monitor(void) {
    while (1) {
        send_heartbeat(peer_node);
        if (!receive_heartbeat_within(HEARTBEAT_TIMEOUT_MS)) {
            consecutive_misses++;
            if (consecutive_misses >= MAX_MISSES) {
                trigger_failover();
            }
        } else {
            consecutive_misses = 0;
        }
        sleep_ms(HEARTBEAT_INTERVAL_MS);
    }
}
```

**2. In-Service Software Upgrade (ISSU):**

```
Buoc 1: Load new software vao standby node
Buoc 2: Upgrade standby, verify
Buoc 3: Switchover: standby thanh active (< 50ms)
Buoc 4: Upgrade old active (now standby)
Buoc 5: (Optional) switchback

Yeu cau:
- Backward compatible message format (them field moi, khong xoa field cu)
- State migration giua versions
- Rollback mechanism neu upgrade fail
```

**3. Defensive Programming:**

```c
// Moi function phai handle moi truong hop loi
int process_rrc_message(uint8_t* buf, uint32_t len) {
    // Input validation
    if (!buf || len == 0 || len > MAX_RRC_MSG_SIZE) {
        LOG_ERROR("Invalid input: buf=%p len=%u", buf, len);
        increment_counter(CNT_INVALID_INPUT);
        return ERR_INVALID_PARAM;
    }
    
    // Decode with error handling
    RRCMessage_t* msg = NULL;
    asn_dec_rval_t ret = uper_decode(NULL, &asn_DEF_RRCMessage, 
                                      (void**)&msg, buf, len, 0, 0);
    if (ret.code != RC_OK) {
        LOG_WARN("Decode failed: code=%d consumed=%zu", ret.code, ret.consumed);
        increment_counter(CNT_DECODE_FAIL);
        return ERR_DECODE;
    }
    
    // Process with resource cleanup guarantee
    int result = handle_decoded_message(msg);
    ASN_STRUCT_FREE(asn_DEF_RRCMessage, msg);
    
    return result;
}
```

**4. Watchdog & Self-healing:**

```c
// Software watchdog: moi task phai "kick" watchdog định kỳ
// Neu khong kick -> task bi coi la hang -> restart

void task_main_loop(void) {
    while (1) {
        watchdog_kick(my_task_id);
        
        process_incoming_messages();
        run_periodic_tasks();
        
        // Neu task mat qua lau o day -> watchdog timeout -> restart
    }
}

// Supervisor restart policy
// - Restart chi task loi (khong restart ca system)
// - Escalation: restart group -> restart subsystem -> restart node
```

---

### Q16. Debug và profiling trong môi trường telecom embedded như thế nào? Những tool và kỹ thuật nào thường dùng?

**A:**
- EN: Telecom embedded debugging uses: ring-buffer logging (zero-copy, non-blocking, filterable by module), protocol traces (message sequence charts for call flows), crash info snapshots (registers, stack dump saved to non-volatile memory), cycle-accurate profiling (hardware cycle counters), and memory pool integrity checks (guard patterns at head/tail of each block).
- VI: Debug embedded telecom dùng: logging ring-buffer (zero-copy, non-blocking, filter theo module), protocol trace (message sequence chart cho call flow), crash info snapshot (register, stack dump lưu vào non-volatile memory), profiling chính xác theo cycle (hardware cycle counter), và kiểm tra toan ven memory pool (guard pattern ở đầu/cũối mỗi block).

Debug telecom embedded khác debug application thường vì: không có gdb thông thường, code chạy trên DSP/RTOS, và lỗi thường liên quan timing.

**1. Logging & Tracing (phổ biến nhất):**

```c
// Telecom logging system: phai fast, non-blocking, filterable
// Khong dung printf (qua cham, block, khong thread-safe)

typedef enum {
    LOG_ERROR,   // Loi nghiem trong
    LOG_WARNING, // Bat thuong nhung khong crash
    LOG_INFO,    // Thong tin hoat dong binh thuong
    LOG_DEBUG,   // Chi bat khi debug
    LOG_TRACE    // Chi tiet tung message/event
} log_level_t;

// Zero-copy logging: ghi vao ring buffer, separate thread flush
typedef struct {
    uint64_t timestamp;   // high-resolution timer
    uint16_t module_id;   // MAC, RLC, RRC, ...
    uint16_t log_level;
    uint32_t log_id;      // pre-defined log ID (khong dung string)
    uint32_t params[4];   // parameters (khong format string at runtime)
} log_entry_t;

// Fast log macro
#define LOG_FAST(module, level, id, p1, p2, p3, p4) do { \
    if (g_log_mask[module] & (1 << level)) { \
        log_entry_t* e = log_ring_alloc(); \
        if (e) { \
            e->timestamp = read_hw_timer(); \
            e->module_id = module; \
            e->log_level = level; \
            e->log_id = id; \
            e->params[0] = (uint32_t)(p1); \
            e->params[1] = (uint32_t)(p2); \
            e->params[2] = (uint32_t)(p3); \
            e->params[3] = (uint32_t)(p4); \
            log_ring_commit(e); \
        } \
    } \
} while(0)

// Trace: ghi lai toàn bộ message flow
// UE attach: RRCConnectionRequest -> RRCConnectionSetup -> ...
// Xem trace de debug tai sao UE khong attach duoc
```

**2. Protocol Trace (Message Sequence Chart):**

```
Khi debug loi protocol, dung tool de capture va hien thi message flow:

  UE              eNodeB           MME
   |                |                |
   |--RRCConnReq--->|                |    t=0.000
   |                |                |
   |<-RRCConnSetup--|                |    t=0.005
   |                |                |
   |--RRCConnSetup->|                |    t=0.010
   |   Complete     |                |
   |                |--InitialUE---->|    t=0.011
   |                |   Message      |
   |                |                |
   |                |<-InitialCtx----|    t=0.050
   |                |   SetupReq     |
   X  TIMEOUT!      |                |    t=0.350
   |  (T300 expired)|                |
   
Debug: Tai sao UE timeout? -> Check eNodeB log -> InitialContextSetupReq
       decode fail -> ASN.1 encoding bug trong MME
```

**3. Core Dump Analysis (khi crash trên embedded):**

```c
// RTOS thuong khong co full core dump nhu Linux
// Thay vao do: luu register snapshot + stack trace + memory region

typedef struct {
    uint32_t registers[32];    // CPU registers tai thoi diem crash
    uint32_t pc;               // Program Counter
    uint32_t lr;               // Link Register (return address)
    uint32_t sp;               // Stack Pointer
    uint32_t stack_dump[256];  // Stack content
    uint32_t exception_type;   // Data abort, prefetch abort, ...
    uint64_t timestamp;
} crash_info_t;

// Exception handler
void data_abort_handler(void) {
    crash_info_t info;
    save_registers(&info);
    info.exception_type = DATA_ABORT;
    info.timestamp = read_hw_timer();
    
    // Luu vao non-volatile memory (survive reboot)
    nvm_write(CRASH_LOG_ADDR, &info, sizeof(info));
    
    // Trigger controlled restart
    system_restart(RESTART_REASON_CRASH);
}
```

**4. Performance Profiling:**

```c
// Cycle-accurate profiling tren DSP
// Dung hardware cycle counter

static inline uint64_t read_cycles(void) {
    uint32_t low, high;
    // ARM: PMCCNTR
    asm volatile("mrc p15, 0, %0, c9, c13, 0" : "=r" (low));
    return (uint64_t)low;
}

#define PROFILE_START(name) uint64_t _prof_##name = read_cycles()
#define PROFILE_END(name) do { \
    uint64_t elapsed = read_cycles() - _prof_##name; \
    update_stats(#name, elapsed); \
} while(0)

void process_subframe(void) {
    PROFILE_START(fft);
    run_fft(data, N);
    PROFILE_END(fft);          // VD: 15000 cycles
    
    PROFILE_START(channel_est);
    channel_estimation(pilots);
    PROFILE_END(channel_est);  // VD: 8000 cycles
    
    PROFILE_START(decode);
    turbo_decode(soft_bits);
    PROFILE_END(decode);       // VD: 45000 cycles
    
    // Total budget: 1ms * CPU_freq cycles
    // VD: 1GHz CPU -> 1,000,000 cycles/subframe
}
```

**5. Memory Debugging:**

```c
// Trong embedded, valgrind khong chay duoc
// Dung memory pool voi guard patterns

#define GUARD_PATTERN 0xDEADBEEF

typedef struct mem_block {
    uint32_t guard_head;
    uint32_t size;
    uint32_t alloc_id;       // track ai alloc
    uint8_t  data[];         // flexible array member
    // guard_tail at data[size]
} mem_block_t;

void* pool_alloc(mem_pool_t* pool, uint32_t size, uint32_t alloc_id) {
    mem_block_t* block = get_free_block(pool, size);
    if (!block) return NULL;
    
    block->guard_head = GUARD_PATTERN;
    block->size = size;
    block->alloc_id = alloc_id;
    // Set tail guard
    *(uint32_t*)(block->data + size) = GUARD_PATTERN;
    
    return block->data;
}

// Periodic check: scan all allocated blocks for corruption
void pool_check_integrity(mem_pool_t* pool) {
    for (int i = 0; i < pool->num_blocks; i++) {
        mem_block_t* b = &pool->blocks[i];
        if (b->guard_head != GUARD_PATTERN) {
            LOG_ERROR("HEAD corruption block %d (alloc_id=%u)", 
                      i, b->alloc_id);
        }
        uint32_t tail = *(uint32_t*)(b->data + b->size);
        if (tail != GUARD_PATTERN) {
            LOG_ERROR("TAIL corruption block %d (alloc_id=%u)", 
                      i, b->alloc_id);
        }
    }
}
```

---

## Phần 8: SCTP Và TRANSPORT PROTOCOLS

---

### Q17. Tại sao telecom dùng SCTP thay vì TCP? Các đặc điểm chính của SCTP?

**A:**
- EN: SCTP (Stream Control Transmission Protocol) is used for telecom signaling (S1AP, X2AP) instead of TCP because it provides: multi-homing (automatic failover between IPs), multi-streaming (no head-of-line blocking — one stream's loss doesn't block others), and message boundaries (unlike TCP's byte stream). Port 36412 for S1AP.
- VI: SCTP được dùng cho signaling telecom (S1AP, X2AP) thay vì TCP vì no cũng cấp: multi-homing (tự động failover giữa các IP), multi-streaming (không head-of-line blocking — mat 1 stream không block stream khác), và message boundary (khác TCP là byte stream). Port 36412 cho S1AP.

**SCTP (Stream Control Transmission Protocol)** được thiết kế cho signaling telecom, khác phuc các han che của TCP.

**So sánh:**

| Đặc điểm | TCP | SCTP | UDP |
|---|---|---|---|
| Connection | 1-to-1 | 1-to-1 (nhưng multi-homed) | Connectionless |
| Reliability | Có | Có | Không |
| Ordered delivery | Có (strict) | Có (per-stream) | Không |
| Multi-streaming | Không | **Có** | Không |
| Multi-homing | Không | **Có** | Không |
| Message boundary | Không (byte stream) | **Có** (message-based) |  Có |
| Head-of-line blocking | **Có** | **Không** (per-stream) | Không |
| Dùng trong telecom | Không (cho signaling) | **S1AP, X2AP, M3AP** | GTP-U (user plane) |

**Multi-homing:**

```
eNodeB                               MME
  IP1: 10.0.1.1  ----path 1----  IP1: 10.0.2.1
  IP2: 10.0.1.2  ----path 2----  IP2: 10.0.2.2

SCTP association dung cả 2 path:
- Primary path: IP1 <-> IP1
- Backup path: IP2 <-> IP2
- Khi primary fail -> tu dong chuyen sang backup (< 1 second)
- Khong can application xu ly failover
```

**Multi-streaming:**

```
Trong 1 SCTP association, co nhieu streams doc lap:

Stream 0: UE-1 signaling  [msg1] [msg2] [msg3] ...
Stream 1: UE-2 signaling  [msg1] [msg2] ...
Stream 2: UE-3 signaling  [msg1] [msg2] [msg3] [msg4] ...

- Neu msg2 cua Stream 0 bị mất -> chi Stream 0 bị delay (retransmit)
- Stream 1, 2 van tiep tuc binh thuong
- TCP: 1 packet mat -> TAT CA data bị block (head-of-line blocking)
```

**Code example (Linux SCTP socket):**

```c
#include <sys/socket.h>
#include <netinet/sctp.h>

// Server: S1AP endpoint tren MME
int setup_sctp_server(void) {
    int fd = socket(AF_INET, SOCK_STREAM, IPPROTO_SCTP);
    
    // Bind nhieu IP (multi-homing)
    struct sockaddr_in addrs[2];
    addrs[0].sin_family = AF_INET;
    addrs[0].sin_port = htons(36412);  // S1AP port
    addrs[0].sin_addr.s_addr = inet_addr("10.0.2.1");
    addrs[1].sin_family = AF_INET;
    addrs[1].sin_port = htons(36412);
    addrs[1].sin_addr.s_addr = inet_addr("10.0.2.2");
    
    sctp_bindx(fd, (struct sockaddr*)addrs, 2, SCTP_BINDX_ADD_ADDR);
    
    // Configure streams
    struct sctp_initmsg initmsg;
    initmsg.sinit_num_ostreams = 16;    // outgoing streams
    initmsg.sinit_max_instreams = 16;   // incoming streams
    initmsg.sinit_max_attempts = 4;
    initmsg.sinit_max_init_timeo = 30000;
    setsockopt(fd, IPPROTO_SCTP, SCTP_INITMSG, &initmsg, sizeof(initmsg));
    
    listen(fd, 10);
    return fd;
}

// Send S1AP message tren specific stream
int send_s1ap_msg(int fd, uint16_t stream_id, uint8_t* msg, uint32_t len) {
    struct sctp_sndrcvinfo sinfo = {0};
    sinfo.sinfo_stream = stream_id;
    sinfo.sinfo_ppid = htonl(18);  // S1AP PPID = 18
    
    return sctp_send(fd, msg, len, &sinfo, 0);
}
```

---

## Phần 9: MEMORY MANAGEMENT Trong TELECOM

---

### Q18. Memory management trong telecom embedded khác gì với application thông thường? Các kỹ thuật quan trọng?

**A:**
- EN: Telecom embedded never uses malloc/free at runtime due to non-deterministic latency and fragmentation. Instead: memory pools (pre-allocated fixed-size blocks, O(1) alloc/free), ring buffers (for streaming data, producer-consumer), buffer descriptors (zero-copy forwarding between protocol layers by passing pointers with offset manipulation).
- VI: Embedded telecom không báo gio dùng malloc/free lúc runtime vì latency không cố định và fragmentation. Thay vào do: memory pool (block cố định cấp phát sẵn, O(1) alloc/free), ring buffer (cho streaming data, producer-consumer), buffer descriptor (zero-copy forwarding giữa các layer bằng cách truyen pointer với offset manipulation).

Trong telecom embedded, **không được dùng malloc/free trong runtime** vì:
- malloc có thể fail (hết memory)
- malloc có latency không dự đoán được (fragmentation -> search free list)
- free có thể không trả memory thực sự (fragmentation)

**Kỹ thuật 1: Memory Pool (phổ biến nhất)**

```c
// Pre-allocate blocks co kich thuoc co dinh
// Alloc/free la O(1), khong fragmentation

typedef struct {
    uint8_t* base;          // pointer to pre-allocated memory
    uint32_t block_size;    // kich thuoc moi block
    uint32_t num_blocks;    // tong số blocks
    uint32_t free_count;    // số block con trong
    uint32_t* free_list;    // stack cua free block indices
    uint32_t free_top;      // top of free stack
} mem_pool_t;

int mem_pool_init(mem_pool_t* pool, uint32_t block_size, uint32_t num_blocks) {
    pool->block_size = block_size;
    pool->num_blocks = num_blocks;
    pool->free_count = num_blocks;
    
    pool->base = (uint8_t*)malloc(block_size * num_blocks);  // chi malloc 1 lần lúc init
    pool->free_list = (uint32_t*)malloc(sizeof(uint32_t) * num_blocks);
    
    if (!pool->base || !pool->free_list) return -1;
    
    // Init free list (stack)
    for (uint32_t i = 0; i < num_blocks; i++) {
        pool->free_list[i] = i;
    }
    pool->free_top = num_blocks;
    
    return 0;
}

void* mem_pool_alloc(mem_pool_t* pool) {
    if (pool->free_top == 0) return NULL;  // het block
    uint32_t idx = pool->free_list[--pool->free_top];
    pool->free_count--;
    return pool->base + (idx * pool->block_size);
}

void mem_pool_free(mem_pool_t* pool, void* ptr) {
    uint32_t idx = ((uint8_t*)ptr - pool->base) / pool->block_size;
    pool->free_list[pool->free_top++] = idx;
    pool->free_count++;
}
```

**Kỹ thuật 2: Ring Buffer (cho streaming data)**

```c
// Producer-consumer pattern, zero-copy khi co the
typedef struct {
    uint8_t* buffer;
    uint32_t size;      // phai la power of 2
    volatile uint32_t read_pos;
    volatile uint32_t write_pos;
} ring_buffer_t;

uint32_t ring_write(ring_buffer_t* rb, const uint8_t* data, uint32_t len) {
    uint32_t available = rb->size - (rb->write_pos - rb->read_pos);
    if (len > available) len = available;
    
    uint32_t write_idx = rb->write_pos & (rb->size - 1);
    uint32_t to_end = rb->size - write_idx;
    
    if (len <= to_end) {
        memcpy(rb->buffer + write_idx, data, len);
    } else {
        memcpy(rb->buffer + write_idx, data, to_end);
        memcpy(rb->buffer, data + to_end, len - to_end);
    }
    
    __sync_synchronize();
    rb->write_pos += len;
    return len;
}
```

**Kỹ thuật 3: Buffer Descriptor (zero-copy forwarding)**

```c
// Thay vi copy data giua layers, chi forward pointer (descriptor)
typedef struct buf_desc {
    uint8_t* data;          // pointer to actual data
    uint32_t length;        // data length
    uint32_t offset;        // current read offset (moi layer tang offset)
    uint32_t pool_id;       // pool de tra ve
    uint16_t ref_count;     // nhieu noi reference -> chi free khi ref_count = 0
    struct buf_desc* next;  // linked list cho scatter-gather
} buf_desc_t;

// PHY -> MAC: chi tang offset (bo PHY header), khong copy
void mac_receive(buf_desc_t* bd) {
    bd->offset += PHY_HEADER_SIZE;
    bd->length -= PHY_HEADER_SIZE;
    // Parse MAC header tai bd->data + bd->offset
    mac_header_t* hdr = (mac_header_t*)(bd->data + bd->offset);
    // Forward to RLC
    bd->offset += MAC_HEADER_SIZE;
    bd->length -= MAC_HEADER_SIZE;
    rlc_receive(hdr->lcid, bd);
}
```

---

## Phần 10: Câu Hỏi Phỏng vấn Thường GAP

---

### Q19. Nếu ban được hỏi "Ban biết gì ve LTE/5G?", trả lỗi như thế nào nếu chưa có kinh nghiệm telecom?

**A:**
- EN: When asked 'What do you know about LTE/5G?' without telecom experience: mention basic architecture (UE → eNodeB → EPC), protocol stack layers, key concepts (DSP, real-time processing, multi-core). Connect to your existing experience (embedded, optimization). Show genuine interest and honesty about your knowledge level.
- VI: Khi được hỏi 'Ban biết gì ve LTE/5G?' mà chưa có kinh nghiệm telecom: nếu kiến trúc cơ bản (UE → eNodeB → EPC), các layer protocol stack, khái niệm chính (DSP, real-time processing, multi-core). Lien he với kinh nghiệm hiện có (embedded, optimization). Thể hiện su quan tạm thực sự và trung thực ve muc do hiểu biết.

**Cách trả lỗi tốt (thể hiện hiểu biết cơ bản + lien he kinh nghiệm):**

> "Tối đa tìm hiểu cơ bản ve kiến trúc mạng LTE và 5G. Tới hiểu rang LTE dùng kiến trúc EPC với các thành phần như eNodeB, MME, S-GW, P-GW. Protocol stack gồm các layer PHY, MAC, RLC, PDCP, RRC — mỗi layer có chức năng riêng, từ xử lý tín hiệu vật lý đến quản lý kết nối.
>
> 5G NR có nhưng thay đổi quan trọng như Cũ/Đủ/RU split, flexible numerology, và network slicing. Tới thay các khái niệm như DSP programming, real-time processing, và multi-core architecture kha gần với kinh nghiệm embedded của tới trên Toradex iMX — nơi tối đa làm viec với GStreamer pipelines và tối ưu từ 30fps lên 60fps.
>
> Tới cũng hiểu rang code trong telecom phải đặt carrier-grade với yêu cầu 99.999% availability, và phần lớn L1/L2 code chạy trên DSP với hard real-time constraints. Đầy là linh vuc tới muốn hoc thêm và tới tin kinh nghiệm C/C++ system programming sẽ giúp tới nhanh chóng bắt kip."

**Nhưng điểm interviewer danh gia cao:**
1. Biết ten các thành phần cơ bản (không nhất thìết hiểu sau)
2. Lien he được với kinh nghiệm hiện tại
3. Thể hiện su chu đóng tìm hiểu
4. Trung thực ve muc do hiểu biết

---

### Q20. Các câu hỏi C/C++ thường gap khi phỏng vấn vào vì tri telecom. Chung khác gì với phỏng vấn C/C++ thông thường?

**A:**
- EN: Telecom C/C++ interviews focus more on: embedded memory management (memory pools, why no malloc at runtime), real-time concurrency (spinlock vs mutex on multi-core, priority inversion), bit manipulation (extract/set fields in protocol headers), endianness (network byte order conversion), and state machines (table-driven design for protocol handling).
- VI: Phỏng vấn C/C++ telecom tap trung hon vào: quản lý memory embedded (memory pool, tại sao không malloc lúc runtime), concurrency real-time (spinlock vs mutex trên multi-core, priority inversion), bit manipulation (extract/set field trong protocol header), endianness (chuyển đổi network byte order), và state machine (thiết kế table-driven cho protocol handling).

Phỏng vấn telecom C/C++ tap trung hon vào **embedded, performance, và reliability**:

**1. Memory — hướng embedded:**
- "Tại sao không dùng `new`/`malloc` trong real-time code?"
  -> Latency không deterministic, fragmentation, có thể fail
- "Implement memory pool với O(1) alloc/free"
  -> Dùng free-list stack (như Q18)
- "Buffer overflow xảy ra thì sao? Làm sao phong tránh trên embedded?"
  -> Guard patterns, bounds checking, static analysis

**2. Concurrency — hướng real-time:**
- "Mutex vs Spinlock — khi nào dùng cai nào trên multi-core embedded?"
  -> Spinlock: critical section ngan, không được sleep, interrupt context
  -> Mutex: critical section dai, có thể sleep, có priority inheritance
- "Lock-free queue dùng trong trường hợp nào?"
  -> IPC giữa cores, producer-consumer với 1 writer + 1 reader
- "Priority Inversion là gì? Cách xử lý?"
  -> (Như Q14)

**3. Bit manipulation — rat thường gap trong telecom:**
```c
// "Extract field tu mot protocol header"
// VD: MAC header co cac field packed trong vài bytes

// Extract bits [high:low] tu gia tri 32-bit
static inline uint32_t extract_bits(uint32_t val, int high, int low) {
    uint32_t mask = ((1u << (high - low + 1)) - 1) << low;
    return (val & mask) >> low;
}

// Set bits [high:low]
static inline uint32_t set_bits(uint32_t val, int high, int low, uint32_t field) {
    uint32_t mask = ((1u << (high - low + 1)) - 1) << low;
    return (val & ~mask) | ((field << low) & mask);
}

// Vi du: MAC subheader
// | R | R | E | LCID (5 bits) | => 1 byte
uint8_t lcid = extract_bits(header_byte, 4, 0);   // bits [4:0]
uint8_t e_bit = extract_bits(header_byte, 5, 5);   // bit 5
```

**4. Endianness — quan trọng trong networking:**
```c
// "Convert host byte order sang network byte order cho protocol message"
// Telecom protocols thuong dung network byte order (big-endian)

uint32_t teid = htonl(local_teid);  // GTP TEID
uint16_t port = htons(36412);       // S1AP port

// Tren DSP (co the la little-endian hoac big-endian)
// Can biet target platform endianness
#if __BYTE_ORDER__ == __ORDER_LITTLE_ENDIAN__
    #define SWAP16(x) __builtin_bswap16(x)
    #define SWAP32(x) __builtin_bswap32(x)
#else
    #define SWAP16(x) (x)
    #define SWAP32(x) (x)
#endif
```

**5. State machine — core skill trong telecom:**
```c
// "Implement 1 state machine don gian"
// Telecom code day state machines: RRC, HARQ, RACH, ...

typedef enum { S_IDLE, S_CONNECTING, S_CONNECTED, S_RELEASING } state_t;
typedef enum { E_CONNECT_REQ, E_CONNECT_DONE, E_RELEASE, E_TIMEOUT } event_t;

typedef state_t (*handler_fn)(void* ctx, void* event_data);

// Table-driven state machine
static const handler_fn state_table[4][4] = {
//              CONNECT_REQ       CONNECT_DONE      RELEASE           TIMEOUT
/* IDLE */    { handle_conn_req,  NULL,              NULL,             NULL },
/* CONNECTING */{ NULL,           handle_conn_done,  handle_release,   handle_timeout },
/* CONNECTED */ { NULL,           NULL,              handle_release,   NULL },
/* RELEASING */ { NULL,           NULL,              NULL,             handle_rel_timeout }
};

state_t process_event(state_t current, event_t event, void* ctx, void* data) {
    handler_fn fn = state_table[current][event];
    if (fn) {
        return fn(ctx, data);
    }
    LOG_WARN("Unexpected event %d in state %d", event, current);
    return current;  // stay in current state
}
```

---

### Q21. GTP (GPRS Tunneling Protocol) là gì? Tại sao cần tunneling trong mạng cellular?

**A:**
- EN: GTP (GPRS Tunneling Protocol) tunnels user data and signaling between core network nodes. GTP-C (control, UDP:2123) manages sessions/bearers. GTP-U (user data, UDP:2152) carries encapsulated IP packets using a 32-bit TEID (Tunnel Endpoint Identifier) for routing. Tunneling enables IP address preservation during handover.
- VI: GTP tunnel dữ liệu và signaling giữa các node core network. GTP-C (control, UDP:2123) quản lý session/bearer. GTP-U (user data, UDP:2152) mạng IP packet đóng gói dùng TEID 32-bit (Tunnel Endpoint Identifier) để định tuyến. Tunneling cho phép giữ IP address khi handover.

**GTP** là protocol dùng để truyen dữ liệu và signaling giữa các node trong mạng cellular (core network).

**Tại sao cần tunneling:**
- UE di chuyển giữa các cell -> IP address không đổi
- Data phải được "tunnel" (đóng gói) để chuyển từ S-GW này sáng S-GW khác khi handover
- Tách biết user data khác nhau trên cũng 1 physical link

**2 loại GTP:**

| | GTP-C (Control) | GTP-U (User) |
|---|---|---|
| Chuc nang | Session management, bearer setup | Chuyển user data packets |
| Transport | UDP port 2123 | UDP port 2152 |
| Dùng giữa | MME <-> S-GW, S-GW <-> P-GW | eNodeB <-> S-GW, S-GW <-> P-GW |
| Throughput | Thấp (signaling) | Cao (user data) |

**GTP-U header format:**

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Ver|P|T|  Res  |  Message Type |         Length                |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    TEID (Tunnel Endpoint ID)                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|    Sequence Number (optional) |  N-PDU Number | Next Ext Hdr  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**TEID (Tunnel Endpoint Identifier):**
- 32-bit identifier duy nhất cho mỗi tunnel
- Mọi UE có ít nhất 1 TEID cho uplink và 1 cho downlink
- Khi handover: S-GW thay đổi TEID mapping để chuyển data sáng eNodeB mọi

```c
// GTP-U encapsulation
typedef struct __attribute__((packed)) {
    uint8_t  flags;      // version, PT, E, S, PN
    uint8_t  msg_type;   // 0xFF = G-PDU (user data)
    uint16_t length;     // payload length
    uint32_t teid;       // Tunnel Endpoint ID
} gtpu_header_t;

int gtpu_encapsulate(uint8_t* ip_packet, uint32_t ip_len,
                     uint32_t teid, uint8_t* output) {
    gtpu_header_t* hdr = (gtpu_header_t*)output;
    hdr->flags = 0x30;           // version=1, PT=1
    hdr->msg_type = 0xFF;        // G-PDU
    hdr->length = htons(ip_len);
    hdr->teid = htonl(teid);
    
    memcpy(output + sizeof(gtpu_header_t), ip_packet, ip_len);
    return sizeof(gtpu_header_t) + ip_len;
}

int gtpu_decapsulate(uint8_t* gtp_packet, uint32_t gtp_len,
                     uint32_t* teid, uint8_t** payload) {
    gtpu_header_t* hdr = (gtpu_header_t*)gtp_packet;
    *teid = ntohl(hdr->teid);
    *payload = gtp_packet + sizeof(gtpu_header_t);
    return ntohs(hdr->length);
}
```

---

### Q22. Handover trong LTE hoạt động như thế nào? Qua trình này ảnh hưởng gì đến software implementation?

**A:**
- EN: LTE X2 Handover: UE sends measurement report → source eNodeB sends HO Request to target → target responds with HO Request Ack (containing RRC config) → source sends RRC Reconfiguration to UE → UE performs RACH on target → path switch through MME/S-GW. Critical: data forwarding (source → target), PDCP SN preservation, timer management (T304, T_RELOC).
- VI: LTE X2 Handover: UE gửi measurement report → source eNodeB gửi HO Request tới target → target trả lỗi HO Request Ack (chưa RRC config) → source gửi RRC Reconfiguration cho UE → UE thực hiện RACH trên target → path switch qua MME/S-GW. Quan trọng: data forwarding (source → target), báo toan PDCP SN, quản lý timer (T304, T_RELOC).

**Handover** là qua trình chuyển UE từ cell này sáng cell khác mà không gian doan dịch vụ.

**Intra-LTE X2 Handover (phổ biến nhất):**

```
    UE              Source eNB         Target eNB          MME        S-GW
     |                  |                  |                 |          |
     |--Meas Report---->|                  |                 |          |
     |  (neighbor cell  |                  |                 |          |
     |   stronger)      |                  |                 |          |
     |                  |--X2: HO Request->|                 |          |
     |                  |  (UE context,    |                 |          |
     |                  |   target cell    |                 |          |
     |                  |   config)        |                 |          |
     |                  |<-X2: HO Req Ack--|                 |          |
     |                  |  (RRC reconfig   |                 |          |
     |                  |   for target)    |                 |          |
     |<-RRC Reconfig----|                  |                 |          |
     |  (HO Command)    |                  |                 |          |
     |                  |                  |                 |          |
     |  [Detach from    |                  |                 |          |
     |   source cell]   |                  |                 |          |
     |                  |===Data Forward==>|                 |          |
     |                  |  (buffered data) |                 |          |
     |                  |                  |                 |          |
     |--RACH------------|----------------->|                 |          |
     |  (access target) |                  |                 |          |
     |<-RRC Reconfig----|------------------|                 |          |
     |  Complete        |                  |                 |          |
     |                  |                  |--Path Switch--->|          |
     |                  |                  |   Request       |--------->|
     |                  |                  |                 | Modify   |
     |                  |                  |                 | Bearer   |
     |                  |                  |<-Path Switch----|<---------|
     |                  |                  |   Req Ack       |          |
     |                  |<-X2: UE Context--|                 |          |
     |                  |   Release        |                 |          |
```

**Điểm quan trọng cho implementation:**

**1. Measurement & Decision:**
```c
// eNodeB cau hinh UE do luong cac cell lan can
typedef struct {
    uint16_t pci;          // Physical Cell ID
    int16_t  rsrp;         // Reference Signal Received Power (dBm)
    int16_t  rsrq;         // Reference Signal Received Quality (dB)
} meas_result_t;

// A3 event: neighbor cell tot hon serving cell + offset
bool check_a3_event(int16_t serving_rsrp, int16_t neighbor_rsrp,
                    int16_t offset, int16_t hysteresis) {
    // Neighbor > Serving + Offset - Hysteresis
    return (neighbor_rsrp > serving_rsrp + offset - hysteresis);
}

// Time-to-trigger: A3 phai dung lien tuc trong khoang thoi gian nay
// -> Tranh handover "ping-pong" (chuyen di chuyen lai)
```

**2. Data Forwarding (critical path):**
```c
// Source eNB forward data chua gui cho UE sang target eNB
// -> Dam bao khong mat data trong qua trinh handover

// PDCP cua source eNB:
// - Cac PDCP SDU chua gui -> forward sang target
// - PDCP SN (Sequence Number) phai duoc bao toan
// -> Target eNB tiep tuc tu PDCP SN do

// Implementation challenge:
// - Forward nhanh (< vài ms)
// - Xu ly duplicate (UE co the nhan tu ca source va target)
// - Memory: buffer data trong luc forward
```

**3. Timer management:**
```c
// Handover co nhieu timers, miss timer = handover fail
typedef enum {
    T_RELOC_PREP,      // Source: cho HO Request Ack (< 1s)
    T_RELOC_OVERALL,   // Source: toàn bộ qua trinh (< 2s)
    T304,              // UE: cho RACH thanh cong o target (< 2s)
    T_RELOC_COMPLETE   // Target: cho HO Complete (< 1s)
} ho_timer_t;

// Neu T304 expire o UE -> RRC Connection Re-establishment
// Neu T_RELOC expire o source -> cancel handover, keep UE
```

---

## FLASH CARDS

---

### Q23. Flash cards — On nhanh các khái niệm telecom cơ bản

**A:**
- EN: Flash cards for quick review of 24 key telecom concepts covering 3GPP, protocol stack layers, HARQ, ASN.1, SCTP, GTP, 5G architecture, RTOS, priority inversion, carrier-grade requirements, memory management, and DSP concepts.
- VI: Flash card để ôn nhanh 24 khái niệm telecom chính báo gồm 3GPP, protocol stack layers, HARQ, ASN.1, SCTP, GTP, kiến trúc 5G, RTOS, priority inversion, yêu cầu carrier-grade, memory management, và khái niệm DSP.

| # | Câu hỏi | Trả lỗi ngan |
|---|---|---|
| 1 | 3GPP là gì? | To chuc tiêu chuẩn hóa mạng di động, ra các specs (TS) theo Release |
| 2 | eNodeB/gNodeB là gì? | Trạm gốc (base station) trong LTE/5G, xử lý radio và kết nối core |
| 3 | EPC gom nhưng gì? | MME (signaling), S-GW (data anchor), P-GW (Internet gateway), HSS (subscriber DB) |
| 4 | Protocol stack layers? | PHY -> MAC -> RLC -> PDCP -> RRC -> NAS |
| 5 | MAC làm gì? | Scheduling, HARQ, multiplexing, RACH |
| 6 | RLC làm gì? | Segmentation, reassembly, ARQ (Âm mode) |
| 7 | PDCP làm gì? | Header compression (ROHC), ciphering, integrity, reordering |
| 8 | RRC làm gì? | Connection management, mobility (handover), bearer setup |
| 9 | ASN.1 là gì? | Ngon ngu mô tả cấu trúc message, dùng PER/UPER encoding trong telecom |
| 10 | HARQ là gì? | Hybrid ARQ: kết hợp FEC + retransmission, 8 processes song song (LTE) |
| 11 | SCTP vs TCP? | SCTP: multi-homing + multi-streaming, dùng cho signaling (S1AP, X2AP) |
| 12 | GTP là gì? | Tunneling protocol: GTP-C (signaling), GTP-U (user data), dùng TEID |
| 13 | 5G Cũ/Đủ/RU? | gNodeB tách thành Central Unit, Distributed Unit, Radio Unit |
| 14 | Numerology là gì? | 5G NR: subcarrier spacing linh hoạt (15/30/60/120/240 kHz) |
| 15 | NSA vs SA? | NSA: dùng 4G core + 5G radio. SA: dùng 5G core + 5G radio (full features) |
| 16 | RTOS vs Linux? | RTOS: deterministic latency, dùng cho L1/L2. Linux: dùng cho L3/OAM |
| 17 | OSE IPC model? | Signal-based message passing (không dùng shared memory + mutex) |
| 18 | Priority Inversion? | Task cao bị block vì task thấp giữ lock. Fix: Priority Inheritance |
| 19 | Five nines? | 99.999% uptime = ~5 phut downtime/năm |
| 20 | Memory pool? | Pre-allocated fixed-size blocks, O(1) alloc/free, không fragmentation |
| 21 | Tại sao không malloc? | Non-deterministic latency, fragmentation, có thể fail |
| 22 | DSP vs GPP? | DSP: tối ưu signal processing, fixed-point, deterministic. GPP: general purpose |
| 23 | Handover? | Chuyển UE giữa cells mà không gian doan. X2 handover phổ biến nhất |
| 24 | ISSU? | In-Service Software Upgrade: nâng cấp không downtime, dùng active/standby |

