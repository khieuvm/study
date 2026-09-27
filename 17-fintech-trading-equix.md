# 17 - Fintech & Trading Systems — Equix Technologies (Bilingual VI/EN)

Kiến thức phỏng vấn liên quan đến fintech, trading platform, OMS, market data, FIX protocol — sát với domain của Equix Technologies (white-label trading, FX, derivatives, portfolio management, market data microservices).

---

## 1) Trading Platform Architecture

### Q1. Kiến trúc tổng quan của một trading platform gồm những thành phần nào?

**A:**
- EN: A trading platform typically consists of: **Market Data** (real-time price feeds), **Order Management System** (OMS — lifecycle of orders), **Execution Management** (routing to exchanges/venues), **Risk Engine** (pre-trade/post-trade checks), **Position & P&L** (real-time portfolio valuation), **Client Gateway** (API/UI for end users), and **Back Office** (settlement, reconciliation, reporting).
- VI: Trading platform gồm: Market Data, OMS, Execution, Risk Engine, Position/P&L, Client Gateway, và Back Office.

```
┌──────────────────────────────────────────────────────┐
│                   Client Layer                        │
│  Web App / Mobile App / Desktop / API (REST/WS)      │
├──────────────────────────────────────────────────────┤
│                  API Gateway                          │
│  Authentication, Rate Limiting, Load Balancing        │
├─────────┬──────────┬───────────┬─────────────────────┤
│ Market  │  Order   │  Risk     │  Portfolio           │
│ Data    │ Mgmt     │  Engine   │  & P&L               │
│ Service │ (OMS)    │           │                      │
├─────────┼──────────┼───────────┼─────────────────────┤
│         │ Execution│           │  Back Office          │
│         │ Engine   │           │  (Settlement,         │
│         │ (FIX)    │           │   Reconciliation)     │
├─────────┴──────────┴───────────┴─────────────────────┤
│    Message Bus (Kafka / RabbitMQ / Redis Streams)     │
├──────────────────────────────────────────────────────┤
│  Database Layer (PostgreSQL, TimescaleDB, Redis)      │
└──────────────────────────────────────────────────────┘
```

Equix context: Equix cung cấp white-label trading platform (5000+ TPS, 100K concurrent users) kết nối 10+ markets, tích hợp TradingView charting.

---

### Q2. White-label trading platform là gì? Thách thức kỹ thuật khi xây dựng?

**A:**
- EN: A white-label platform is a fully built product that clients rebrand as their own. Technical challenges: multi-tenancy (data isolation per broker), customizable UI/theming, configurable business rules per tenant, separate market connectivity per client, scalable infrastructure, and maintaining a single codebase serving multiple brands.
- VI: White-label là platform xây sẵn, client rebrand thành sản phẩm riêng. Thách thức: multi-tenancy, custom UI, business rules per tenant, kết nối market riêng, scale từ 1 codebase.

Multi-tenancy patterns:
```
1. Shared DB, tenant column    — đơn giản, risk data leak
2. Schema-per-tenant           — isolation tốt hơn, migration phức tạp
3. DB-per-tenant               — isolation cao nhất, ops overhead lớn

Equix approach (likely): Schema-per-tenant hoặc hybrid
- Shared infrastructure (API gateway, auth)
- Isolated data (orders, positions, user data)
- Configurable: themes, fees, market access, risk rules
```

Key features cần support:
- Branded UI (logo, colors, fonts) — deploy nhanh trong 2 tuần
- Per-tenant fee schedules & commission rules
- Market access control (tenant A chỉ ASX, tenant B thêm NYSE)
- Regulatory reporting per jurisdiction

---

### Q3. Làm sao đạt throughput 5000+ TPS cho order processing?

**A:**
- EN: Key techniques: event-driven architecture (async order processing via message queue), in-memory order book, lock-free data structures for matching, connection pooling for DB, write-ahead logging, batch commits, horizontal scaling of stateless services, and LMAX Disruptor pattern for single-thread high-throughput.
- VI: Đạt 5000+ TPS bằng: event-driven async, in-memory order book, lock-free structures, connection pooling, batch commits, horizontal scaling, LMAX Disruptor pattern.

```
                    ┌───────────────┐
  Order Request ──→ │  API Gateway  │
                    └──────┬────────┘
                           │ (async)
                    ┌──────▼────────┐
                    │ Message Queue │  ← Kafka partition per symbol
                    └──────┬────────┘
                           │
                    ┌──────▼────────┐
                    │ Order Service │  ← Stateless, horizontally scaled
                    │ (validate,    │
                    │  risk check)  │
                    └──────┬────────┘
                           │
                    ┌──────▼────────┐
                    │ Matching /    │  ← In-memory, single-threaded per symbol
                    │ Routing (FIX) │
                    └───────────────┘
```

C++ specific optimizations:
- Ring buffer (lock-free SPSC queue) cho inter-thread communication
- Memory-mapped files cho persistent order log
- `std::pmr::monotonic_buffer_resource` cho allocation-free hot path
- Kernel bypass (DPDK/RDMA) cho ultra-low-latency networking

---

## 2) FIX Protocol

### Q4. FIX protocol là gì và tại sao quan trọng trong trading?

**A:**
- EN: FIX (Financial Information eXchange) is the industry-standard messaging protocol for electronic trading. It defines message formats for orders (New/Cancel/Replace), execution reports, market data, and administrative functions. Most exchanges, brokers, and ECNs communicate via FIX. Current version: FIX 4.4 / 5.0 SP2.
- VI: FIX là protocol chuẩn ngành cho giao dịch điện tử. Định nghĩa format message cho orders, executions, market data. Hầu hết sàn/broker dùng FIX.

FIX message structure:
```
8=FIX.4.4|9=176|35=D|49=SENDER|56=TARGET|34=2|52=20240101-12:00:00|
11=ORDER123|21=1|55=BHP.AX|54=1|60=20240101-12:00:00|38=1000|
40=2|44=45.50|10=123|

Key tags:
  8  = BeginString (protocol version)
  35 = MsgType (D=NewOrderSingle, 8=ExecutionReport, F=CancelRequest)
  49 = SenderCompID
  56 = TargetCompID
  11 = ClOrdID (client order ID)
  55 = Symbol
  54 = Side (1=Buy, 2=Sell)
  38 = OrderQty
  40 = OrdType (1=Market, 2=Limit)
  44 = Price
```

Common FIX message types:
| MsgType | Name | Direction |
|---------|------|-----------|
| D | NewOrderSingle | Client → Exchange |
| F | OrderCancelRequest | Client → Exchange |
| G | OrderCancelReplaceRequest | Client → Exchange |
| 8 | ExecutionReport | Exchange → Client |
| 9 | OrderCancelReject | Exchange → Client |
| W | MarketDataSnapshotFullRefresh | Exchange → Client |
| X | MarketDataIncrementalRefresh | Exchange → Client |

---

### Q5. FIX session management gồm những bước nào?

**A:**
- EN: A FIX session lifecycle: **Logon** (35=A, exchange credentials + heartbeat interval), **Heartbeat** (35=0, keep-alive), **Message Exchange** (orders/executions), **Sequence Number Management** (gap detection + resend), **Logout** (35=5). Sessions persist sequence numbers across TCP reconnects for guaranteed delivery.
- VI: FIX session: Logon → Heartbeat → Message Exchange → Sequence Management → Logout. Sequence number persist qua reconnect để đảm bảo không mất message.

```
Client                           Exchange
  │                                 │
  │──── Logon (35=A) ────────────→ │
  │←─── Logon (35=A) ────────────  │
  │                                 │
  │←─── Heartbeat (35=0) ────────  │  (every N seconds)
  │──── Heartbeat (35=0) ────────→ │
  │                                 │
  │──── NewOrder (35=D) ─────────→ │  seq=2
  │←─── ExecReport (35=8) ───────  │  seq=2
  │                                 │
  │  [network blip — reconnect]     │
  │                                 │
  │──── Logon (35=A) ────────────→ │  seq=3
  │←─── ResendRequest (35=2) ────  │  gap detected!
  │──── SequenceReset (35=4) ────→ │
  │                                 │
  │──── Logout (35=5) ───────────→ │
  │←─── Logout (35=5) ───────────  │
```

Libraries phổ biến:
- **QuickFIX/C++**: Open-source, widely used
- **QuickFIX/J**: Java version
- **Fix8**: Modern C++ FIX engine, higher performance
- **OnixS**: Commercial, ultra-low-latency

---

### Q6. Sequence number trong FIX hoạt động thế nào? Xử lý gap ra sao?

**A:**
- EN: Each FIX session maintains two independent sequence counters: outgoing (MsgSeqNum sent) and incoming (expected from counterparty). If a received message has a higher sequence than expected → gap detected → send ResendRequest for the missing range. If lower → possible duplicate → PossDupFlag check. Sequences persist to file/DB and survive restarts.
- VI: Mỗi session có 2 counter: outgoing và incoming. Gap → ResendRequest. Sequence lưu persistent qua restart.

Gap handling:
```cpp
// Pseudo-code for sequence gap handling
void onMessage(const FIX::Message& msg) {
    int received_seq = msg.getField(FIX::FIELD::MsgSeqNum);
    if (received_seq == expected_seq) {
        process(msg);
        expected_seq++;
    } else if (received_seq > expected_seq) {
        // Gap detected — request resend
        sendResendRequest(expected_seq, received_seq - 1);
        queue(msg);  // process after gap filled
    } else {
        // received_seq < expected_seq
        if (msg.getField(FIX::FIELD::PossDupFlag) == "Y")
            ignoreDuplicate(msg);
        else
            handleError("Sequence too low without PossDup");
    }
}
```

Production considerations:
- Persist sequences to file (QuickFIX: `FileStoreFactory`)
- Daily sequence reset (common practice, coordinated at market close)
- Graceful vs hard disconnect handling

---

## 3) Order Management System (OMS)

### Q7. Vòng đời (lifecycle) của một order trong OMS?

**A:**
- EN: Order lifecycle: **New** (client submits) → **Pending** (pre-trade risk check) → **Open/Working** (sent to exchange/venue) → **Partially Filled** (some quantity executed) → **Filled** (fully executed) / **Cancelled** / **Rejected**. Each state transition generates an event/audit trail. An order can also be **Amended** (price/qty change) at any open state.
- VI: Vòng đời order: New → Pending (risk check) → Open → Partially Filled → Filled / Cancelled / Rejected. Mỗi transition tạo event/audit log.

```
                    ┌──────────┐
        ┌──────────→│ Rejected │
        │           └──────────┘
  ┌─────┴────┐    ┌───────────┐    ┌─────────────────┐    ┌────────┐
  │   New    │───→│  Pending  │───→│  Open / Working │───→│ Filled │
  └──────────┘    │(risk chk) │    └────────┬────────┘    └────────┘
                  └───────────┘             │
                                   ┌────────▼────────┐
                                   │Partially Filled │───→ Filled
                                   └────────┬────────┘
                                            │
                                   ┌────────▼────────┐
                                   │   Cancelled     │
                                   └─────────────────┘
```

Key OMS responsibilities:
- Order validation (symbol, qty, price, account)
- Pre-trade risk checks (buying power, position limits)
- Smart Order Routing (SOR) — chọn venue tốt nhất
- Execution management (partial fills aggregation)
- Post-trade: allocation, settlement instructions
- Full audit trail (regulatory requirement)

---

### Q8. Pre-trade risk check bao gồm những gì?

**A:**
- EN: Pre-trade risk checks run before order reaches the market: **Buying Power** (sufficient funds/margin), **Position Limits** (max exposure per symbol/sector), **Order Size Limits** (max qty/notional), **Price Reasonability** (reject orders far from market price), **Fat Finger Check** (qty/price sanity), **Restricted List** (blocked securities), **Regulatory** (short-sell restrictions, circuit breaker status).
- VI: Pre-trade risk: Buying Power, Position Limits, Order Size, Price Reasonability, Fat Finger, Restricted List, Regulatory checks.

```cpp
struct RiskCheckResult {
    bool passed;
    std::string reject_reason;
};

RiskCheckResult preTradeRiskCheck(const Order& order, const Account& acct) {
    // 1. Buying power
    double notional = order.qty * order.price;
    if (notional > acct.available_funds)
        return {false, "Insufficient buying power"};

    // 2. Position limit
    double new_exposure = acct.getExposure(order.symbol) + notional;
    if (new_exposure > acct.max_exposure_per_symbol)
        return {false, "Position limit exceeded"};

    // 3. Fat finger — order size vs ADV
    double adv = marketData.getADV(order.symbol);  // Average Daily Volume
    if (order.qty > adv * 0.1)  // > 10% of ADV
        return {false, "Order size exceeds 10% ADV"};

    // 4. Price reasonability
    double last_price = marketData.getLastPrice(order.symbol);
    double deviation = std::abs(order.price - last_price) / last_price;
    if (deviation > 0.05)  // > 5% from last price
        return {false, "Price deviation too large"};

    return {true, ""};
}
```

Performance requirement: Risk checks phải < 1ms vì nằm trên critical path.

---

### Q9. Smart Order Routing (SOR) là gì?

**A:**
- EN: SOR automatically routes orders to the best execution venue based on: price (best bid/offer across venues), liquidity (order book depth), fees (exchange/ECN fees), latency, and fill probability. Regulatory requirement (e.g., MiFID II Best Execution, ASIC Best Execution). SOR must consider dark pools, lit markets, and crossing networks.
- VI: SOR tự động route order tới venue tốt nhất dựa trên price, liquidity, fees, latency. Là yêu cầu regulatory (Best Execution).

```
                   Order
                     │
              ┌──────▼──────┐
              │     SOR      │
              │  (evaluate   │
              │   venues)    │
              └──┬───┬───┬───┘
                 │   │   │
         ┌───────┘   │   └────────┐
         ▼           ▼            ▼
    ┌─────────┐ ┌─────────┐ ┌──────────┐
    │  ASX    │ │ Chi-X   │ │ Dark     │
    │ (lit)   │ │ (lit)   │ │ Pool     │
    └─────────┘ └─────────┘ └──────────┘
```

Equix context: Kết nối 10+ markets/platforms. SOR cần consider:
- Australian markets: ASX, Chi-X, NSX
- International connectivity
- FIX routing to multiple venues simultaneously
- Partial fills across venues → aggregate execution report

---

## 4) Market Data

### Q10. Real-time market data pipeline xử lý thế nào?

**A:**
- EN: Market data flows: **Feed Handler** (connects to exchange, normalizes raw data) → **Ticker Plant** (consolidates, conflates, distributes) → **Distribution Layer** (pub/sub to consumers: OMS, risk, UI). Key challenges: handling burst rates (millions of updates/sec), conflation (drop stale updates), maintaining order book integrity, and multicast vs TCP delivery.
- VI: Market data: Feed Handler → Ticker Plant → Distribution. Thách thức: burst rate triệu msg/s, conflation, order book integrity.

```
Exchange A ─── [Feed Handler A] ──┐
                                   ├─→ [Ticker Plant] ─→ [Pub/Sub Bus]
Exchange B ─── [Feed Handler B] ──┘         │                   │
                                   conflation &          ┌──────┴──────┐
                                   normalization         │  Consumers  │
                                                    ┌────┴───┐  ┌─────┴────┐
                                                    │ OMS/   │  │ Web UI   │
                                                    │ Risk   │  │ (WebSocket│
                                                    └────────┘  │  push)   │
                                                                └──────────┘
```

Data types:
| Type | Description | Update Rate |
|------|-------------|-------------|
| Quote (BBO) | Best bid/offer price & size | High (100K+/sec) |
| Trade | Last trade price & volume | Medium |
| Depth (L2) | Full order book (multiple levels) | Very high |
| OHLCV | Candle/bar data | Low (per interval) |
| Reference | Symbol info, corporate actions | Daily |

Conflation strategy cho UI:
```python
# Chỉ giữ latest quote, drop stale updates
# Throttle push to client: max 4-10 updates/sec per symbol
class ConflatingPublisher:
    def __init__(self, max_rate_hz=10):
        self.latest = {}
        self.interval = 1.0 / max_rate_hz

    def on_quote(self, symbol, quote):
        self.latest[symbol] = quote  # overwrite stale

    def publish_tick(self):
        for symbol, quote in self.latest.items():
            self.push_to_clients(symbol, quote)
        self.latest.clear()
```

Equix context: Finsight — Market Data as a Service, cloud-native microservices, elastic scalability.

---

### Q11. Order book (sổ lệnh) hoạt động thế nào?

**A:**
- EN: An order book maintains all outstanding buy (bid) and sell (ask) orders for a symbol, sorted by price-time priority. Bids sorted descending (highest first), asks sorted ascending (lowest first). The spread is the gap between best bid and best ask. When a new order crosses the spread, a trade occurs (matching).
- VI: Order book chứa tất cả lệnh buy/sell, sắp xếp theo price-time priority. Bid giảm dần, ask tăng dần. Spread = gap giữa best bid và best ask.

```
         BID (Buy)                    ASK (Sell)
  Price    Qty    Orders       Price    Qty    Orders
  45.50    2000   [A,B]        45.52    500    [E]
  45.48    1500   [C]          45.55    3000   [F,G]
  45.45    5000   [D]          45.60    1000   [H]
         ◄─── spread ───►
         45.50    45.52

New Market Buy order qty=600:
  → Match 500 @ 45.52 (fills order E completely)
  → Match 100 @ 45.55 (partially fills order F)
  → Execution report: avg price = (500*45.52 + 100*45.55) / 600 = 45.525
```

C++ implementation considerations:
```cpp
// Price-time priority order book
struct PriceLevel {
    double price;
    std::deque<Order> orders;  // time-ordered FIFO
    int64_t total_qty;
};

// Bid side: max-heap (highest price first)
// Ask side: min-heap (lowest price first)
// Or use std::map with custom comparator for O(log N) insert/find
std::map<double, PriceLevel, std::greater<>> bids;  // descending
std::map<double, PriceLevel, std::less<>> asks;      // ascending
```

---

## 5) FX Trading

### Q12. FX trading có gì đặc biệt so với equity trading?

**A:**
- EN: FX is decentralized (OTC, no single exchange), trades 24/5, uses currency pairs (EUR/USD), quotes with bid/ask spread, settles T+2 (spot) or T+0 (same-day), uses leverage/margin, liquidity from multiple providers (banks, ECNs). Pricing uses pips (0.0001 for most pairs). Key: managing multiple liquidity providers and aggregating best prices.
- VI: FX là OTC (không có sàn tập trung), giao dịch 24/5, dùng currency pairs, settle T+2, leverage/margin, liquidity từ nhiều provider. Cần aggregate price từ nhiều nguồn.

```
                    ┌─────────────────────┐
                    │  FX Aggregator      │
                    │  (Best Bid/Offer    │
                    │   from all LPs)     │
                    └───┬─────┬─────┬─────┘
                        │     │     │
                  ┌─────┘     │     └──────┐
                  ▼           ▼            ▼
           ┌──────────┐ ┌──────────┐ ┌──────────┐
           │ Bank LP1 │ │ Bank LP2 │ │  ECN     │
           │(Deutsche)│ │(Citi)    │ │(EBS/     │
           │          │ │          │ │ Reuters) │
           └──────────┘ └──────────┘ └──────────┘

LP = Liquidity Provider
```

Equix context: Night Vision FX — real-time FX trading cho banks (Techcombank, VietinBank). Cần hiểu:
- Spot, Forward, Swap, NDF (Non-Deliverable Forward)
- Markup/spread management per client
- RFQ (Request For Quote) vs streaming price
- Settlement workflow (T+2, Netting)

Key FX concepts:
| Term | Meaning |
|------|---------|
| Pip | Smallest price move (0.0001 for EUR/USD) |
| Lot | Standard unit (100,000 of base currency) |
| Spread | Bid-Ask difference (revenue source) |
| Swap points | Interest rate differential for forward |
| Margin | Collateral required for leveraged position |
| Rollover | Extending settlement date |

---

### Q13. Derivatives (Options, Futures, Swaps) — kiến thức cơ bản cần biết?

**A:**
- EN: Derivatives derive value from an underlying asset. **Futures**: obligation to buy/sell at fixed price on future date. **Options**: right (not obligation) to buy (call) or sell (put). **Swaps**: exchange of cash flows (interest rate swap, FX swap). Trading systems must handle: complex pricing models, margin calculations, expiry management, and exercise/assignment workflows.
- VI: Derivatives: Futures (nghĩa vụ mua/bán), Options (quyền mua call/bán put), Swaps (trao đổi cash flow). System cần: pricing models, margin, expiry, exercise.

```
Futures P&L:
  Long 1 contract @ 100
  Current price = 105
  P&L = (105 - 100) × contract_size = +5 × multiplier

Options pricing (Black-Scholes simplified):
  C = S·N(d1) - K·e^(-rT)·N(d2)
  where:
    S = spot price
    K = strike price
    r = risk-free rate
    T = time to expiry
    N() = cumulative normal distribution
    d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)
    d2 = d1 - σ√T
```

Equix context: Vision Swap — automates lifecycle of derivatives (options, futures, swaps). System cần handle:
- Trade capture & booking
- Real-time mark-to-market
- Margin calculation (initial + variation)
- Expiry calendar management
- Exercise/assignment processing
- Regulatory reporting (EMIR, ASIC)

---

## 6) WebSocket & Real-time Communication

### Q14. Tại sao dùng WebSocket cho trading UI thay vì REST polling?

**A:**
- EN: REST polling wastes bandwidth (constant requests with mostly empty responses), adds latency (poll interval delay), and doesn't scale for real-time price updates. WebSocket provides full-duplex persistent connection: server pushes updates instantly, low overhead (2-byte frame header vs HTTP headers), and supports high-frequency data like market quotes.
- VI: REST polling lãng phí bandwidth, thêm latency. WebSocket là full-duplex, server push tức thì, overhead thấp, phù hợp real-time market data.

```
REST Polling (bad for real-time):
  Client ─── GET /price/BHP ──→ Server   (every 1s)
  Client ←── {price: 45.50} ──  Server
  Client ─── GET /price/BHP ──→ Server   (1s later, maybe no change)
  Client ←── {price: 45.50} ──  Server   (wasted request)

WebSocket (good):
  Client ←──→ Server  (persistent connection)
  Client ←── {BHP: 45.52} ── Server  (push only when changed)
  Client ←── {BHP: 45.55} ── Server  (instant, 100μs latency)
```

Architecture for 100K concurrent users:
```
┌──────────┐     ┌──────────────────────────┐
│ Clients  │────→│  Load Balancer (sticky)  │
│ (100K)   │     └──────────┬───────────────┘
└──────────┘                │
              ┌─────────────┼──────────────┐
              ▼             ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ WS Node 1│  │ WS Node 2│  │ WS Node N│
        │ (10K     │  │ (10K     │  │ (10K     │
        │  conns)  │  │  conns)  │  │  conns)  │
        └────┬─────┘  └────┬─────┘  └────┬─────┘
             └──────────────┼──────────────┘
                     ┌──────▼──────┐
                     │ Redis Pub/  │  ← fan-out across nodes
                     │ Sub Cluster │
                     └─────────────┘
```

Considerations:
- Connection draining during deployment (graceful shutdown)
- Heartbeat/ping-pong for dead connection detection
- Subscription management (client subscribes to specific symbols)
- Binary protocol (MessagePack/Protobuf) vs JSON for bandwidth

---

### Q15. Scaling WebSocket connections tới 100K+ concurrent users?

**A:**
- EN: Techniques: use epoll/kqueue for async I/O (single thread handles 10K+ connections), horizontal scaling with sticky sessions (L4 load balancer), fan-out via Redis Pub/Sub or Kafka across WS nodes, connection-level subscription filtering (only push data client cares about), conflation to reduce message rate.
- VI: Scale WS: epoll/kqueue async I/O, horizontal scaling + sticky session, Redis Pub/Sub fan-out, subscription filtering, conflation.

Per-node capacity planning:
```
1 WS node (4 cores, 8GB RAM):
  - ~10,000-50,000 concurrent connections (depending on message rate)
  - Each connection ~10KB memory overhead
  - 50K × 10KB = 500MB base memory
  - Message throughput: 100K+ msgs/sec outbound

For 100K users:
  - ~3-10 WS nodes behind L4 LB
  - Redis Pub/Sub cluster for cross-node fan-out
  - Subscription-based filtering: each user watches ~10-20 symbols
```

Node.js example (common in Equix-style platforms):
```javascript
const WebSocket = require('ws');
const Redis = require('ioredis');

const wss = new WebSocket.Server({ port: 8080, perMessageDeflate: false });
const subscriber = new Redis();

// Per-client subscription tracking
const subscriptions = new Map(); // ws → Set<symbol>

wss.on('connection', (ws) => {
    ws.on('message', (msg) => {
        const { action, symbols } = JSON.parse(msg);
        if (action === 'subscribe') {
            subscriptions.set(ws, new Set(symbols));
        }
    });
});

// Fan-out from Redis
subscriber.subscribe('market-data');
subscriber.on('message', (channel, data) => {
    const update = JSON.parse(data);
    for (const [ws, syms] of subscriptions) {
        if (syms.has(update.symbol) && ws.readyState === WebSocket.OPEN) {
            ws.send(data);
        }
    }
});
```

---

## 7) Security & Compliance

### Q16. Bảo mật trading platform cần chú ý gì?

**A:**
- EN: Financial platform security: **Authentication** (MFA, OAuth 2.0 / OpenID Connect, session management), **Authorization** (RBAC — role-based access per account/feature), **Data encryption** (TLS 1.3 in transit, AES-256 at rest), **API security** (rate limiting, input validation, CSRF/XSS protection), **Audit logging** (every action logged, immutable), **Network** (WAF, DDoS protection, VPN for internal services).
- VI: Bảo mật finance: MFA + OAuth/OIDC, RBAC, TLS 1.3 + AES-256, rate limiting, audit logging bất biến, WAF + DDoS protection.

Equix context: SSO, OAuth integration cho Finsight Market Data service.

Regulatory requirements:
```
- Data residency: Dữ liệu client phải lưu trong jurisdiction phù hợp
- PCI DSS: Nếu xử lý payment
- SOC 2 Type II: Security controls audit
- ASIC regulatory reporting: Trade reporting obligations
- GDPR / Privacy Act: User data protection
- Encryption at rest: Database, backups, logs
```

Common attack vectors cho trading platform:
| Attack | Mitigation |
|--------|-----------|
| Account takeover | MFA, device fingerprinting, anomaly detection |
| Order manipulation | Server-side validation, idempotency keys |
| Market data spoofing | Signed data feeds, source verification |
| DDoS on trading hours | WAF, rate limiting, CDN for static |
| Insider threat | RBAC, audit logs, 4-eyes principle |

---

### Q17. Regulatory compliance trong fintech Australia cần biết gì?

**A:**
- EN: Australian financial regulations: **ASIC** (Australian Securities & Investments Commission) — regulates markets & financial services. **AFSL** (Australian Financial Services License) — required to provide financial services. **Best Execution** — obligation to get best outcome for clients. **Trade Reporting** — report OTC derivatives to trade repository. **Anti-Money Laundering (AML/CTF)** — KYC, transaction monitoring, suspicious activity reporting.
- VI: Australia: ASIC quản lý thị trường, AFSL license bắt buộc, Best Execution obligation, Trade Reporting cho OTC, AML/KYC.

System requirements cho compliance:
```
1. Audit Trail
   - Mọi order action phải logged (timestamp, user, IP, action, params)
   - Immutable logs (append-only, tamper-evident)
   - Retention: 7+ years

2. Best Execution
   - Record venue selection rationale
   - Prove best price was obtained across available venues

3. KYC/AML
   - Identity verification workflow
   - Transaction monitoring (unusual patterns)
   - PEP (Politically Exposed Person) screening
   - Sanctions list checking

4. Reporting
   - ASIC Market Integrity Rules compliance
   - T+1 trade reporting for OTC derivatives
```

---

## 8) Microservices & Cloud Architecture

### Q18. Microservices architecture cho trading platform thiết kế thế nào?

**A:**
- EN: Key services: API Gateway, Auth Service, Market Data Service, Order Service, Risk Service, Position Service, Settlement Service, Notification Service. Communication: synchronous (gRPC/REST) for request-response, asynchronous (Kafka/RabbitMQ) for events. Each service owns its data (database-per-service pattern). Use event sourcing for order/trade audit trail.
- VI: Microservices: API Gateway, Auth, Market Data, Order, Risk, Position, Settlement, Notification. Sync (gRPC) + Async (Kafka). Database-per-service. Event sourcing cho audit.

```
┌──────────────────────────────────────────────────┐
│              API Gateway (Kong/Envoy)             │
│        Auth, Rate Limit, Routing, SSL            │
└──────────┬───────────┬──────────┬────────────────┘
           │           │          │
    ┌──────▼───┐ ┌─────▼────┐ ┌──▼──────────┐
    │Auth Svc  │ │Market    │ │Order Svc    │
    │(OAuth/   │ │Data Svc  │ │(OMS logic)  │
    │ JWT)     │ │(feeds,   │ │             │
    └──────────┘ │ cache)   │ └──────┬──────┘
                 └──────────┘        │ (async event)
                              ┌──────▼──────┐
                              │Risk Svc     │
                              │(pre-trade)  │
                              └──────┬──────┘
                                     │
                    ┌────────────────┬┴──────────────┐
                    ▼                ▼                ▼
             ┌───────────┐  ┌────────────┐  ┌────────────┐
             │Position   │  │Settlement  │  │Notification│
             │Svc        │  │Svc         │  │Svc (email, │
             └───────────┘  └────────────┘  │ push, SMS) │
                                            └────────────┘
```

Equix tech stack (inferred):
- Cloud-native microservices (Finsight = Market Data as a Service)
- Elastic scalability
- API-first design (REST + WebSocket)
- OAuth/SSO integration

Event sourcing for orders:
```json
// Order event stream
{"type": "OrderCreated", "orderId": "123", "symbol": "BHP", "qty": 1000, "price": 45.50, "ts": "..."}
{"type": "OrderAccepted", "orderId": "123", "exchangeId": "EX456", "ts": "..."}
{"type": "OrderPartiallyFilled", "orderId": "123", "fillQty": 500, "fillPrice": 45.50, "ts": "..."}
{"type": "OrderFilled", "orderId": "123", "fillQty": 500, "fillPrice": 45.52, "ts": "..."}
// Current state = replay all events
```

---

### Q19. Message queue nào phù hợp cho trading system?

**A:**
- EN: **Kafka**: high-throughput, durable, ordered per partition — ideal for market data distribution, order event streaming, audit logs. **RabbitMQ**: flexible routing, lower latency for RPC patterns — good for order routing, notifications. **Redis Streams**: ultra-low-latency, in-memory — good for real-time price fan-out. **ZeroMQ**: broker-less, minimal latency — used in HFT internal communication.
- VI: Kafka (throughput cao, bền, ordered) cho market data/events. RabbitMQ (routing linh hoạt) cho order routing. Redis Streams (low-latency) cho price fan-out. ZeroMQ cho HFT.

| Feature | Kafka | RabbitMQ | Redis Streams |
|---------|-------|----------|--------------|
| Throughput | 1M+ msg/s | 50K msg/s | 500K+ msg/s |
| Latency | ~5ms | ~1ms | <1ms |
| Durability | Yes (disk) | Yes (optional) | Optional (AOF) |
| Ordering | Per partition | Per queue | Per stream |
| Replay | Yes (offset) | No (consumed = gone) | Yes (ID-based) |
| Use in trading | Event store, audit | Order routing, RPC | Price distribution |

Kafka partition strategy cho market data:
```
Topic: market-data
  Partition 0: symbols A-F    ← guaranteed order per symbol
  Partition 1: symbols G-M
  Partition 2: symbols N-S
  Partition 3: symbols T-Z

Key = symbol → same symbol always goes to same partition
Consumer group: each OMS instance reads all partitions
```

---

## 9) Database & Data Architecture

### Q20. Database choices cho trading system?

**A:**
- EN: Multiple databases for different needs: **PostgreSQL** (orders, accounts, reference data — ACID transactions), **TimescaleDB/InfluxDB** (time-series: price history, OHLCV candles), **Redis** (caching: real-time prices, session data, rate limiting), **MongoDB** (flexible schema: user preferences, configurations), **Event Store** (order event log for audit/replay).
- VI: PostgreSQL cho orders/accounts (ACID), TimescaleDB cho time-series prices, Redis cho cache real-time, MongoDB cho config, Event Store cho audit.

```
┌────────────────┐
│  Order Service │
│                │──→ PostgreSQL (orders, trades, accounts)
│                │──→ Kafka (order events → audit trail)
└────────────────┘

┌────────────────┐
│ Market Data Svc│
│                │──→ Redis (latest quotes cache)
│                │──→ TimescaleDB (historical OHLCV)
└────────────────┘

┌────────────────┐
│ Config Service │
│                │──→ MongoDB/PostgreSQL (tenant config, themes)
└────────────────┘
```

TimescaleDB for OHLCV:
```sql
-- Hypertable for price data
CREATE TABLE quotes (
    time        TIMESTAMPTZ NOT NULL,
    symbol      TEXT NOT NULL,
    bid         DECIMAL(18,8),
    ask         DECIMAL(18,8),
    bid_size    BIGINT,
    ask_size    BIGINT
);
SELECT create_hypertable('quotes', 'time');

-- Continuous aggregate for 1-minute candles
CREATE MATERIALIZED VIEW ohlcv_1m
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 minute', time) AS bucket,
    symbol,
    first(bid, time) AS open,
    max(bid) AS high,
    min(bid) AS low,
    last(bid, time) AS close,
    sum(bid_size) AS volume
FROM quotes
GROUP BY bucket, symbol;
```

---

## 10) Equix-Specific Knowledge

### Q21. Tóm tắt sản phẩm và tech stack của Equix Technologies?

**A:**
- EN: Equix Technologies (Melbourne, Australia — offices in VN, Singapore) builds fintech solutions for banks, brokers, and asset managers. Founded 2008 (as Quantedge), 18+ years, 1.5M+ transactions/year, 50+ financial institutions, 95% client retention.
- VI: Equix Technologies (Melbourne) xây dựng giải pháp fintech cho banks, brokers, asset managers. Thành lập 2008, 18+ năm, 1.5M+ giao dịch/năm.

Products:
```
SELL-SIDE:
  ├── Equix White Label Trading Platform
  │     5000+ TPS, 100K concurrent users, 10+ markets
  │     Real-time market data, TradingView charting
  │     Go live in 2 weeks (white-label)
  │
  ├── OneWalleX OMS (Order Management System)
  │     End-to-end order lifecycle management
  │
  └── Trading & Risk Suite
        Multi-asset, multi-venue, FIX connectivity
        Risk controls, advisory tools

BANKING:
  ├── Night Vision FX — Real-time FX trading (Techcombank, VietinBank)
  ├── Vision Swap — Derivatives trading automation
  └── Vision GOLD — Precious metals trading

BUY-SIDE:
  └── HarmoniX — Unified portfolio management
        Cross-asset analytics, AI-powered insights

OTHER:
  ├── Finsight — Market Data as a Service (cloud-native microservices)
  └── Offshore IT Services
```

Partners: OpenMarkets, Iress, FinClear, Tiger Trade (Australian market ecosystem)

Clients (known): Techcombank, VietinBank, LPBank, Sacombank, Trade for Good

---

### Q22. Câu hỏi behavioral thường gặp khi phỏng vấn fintech company?

**A:**
- EN: Common behavioral questions at fintech companies focus on: working under pressure (market hours = no downtime), handling production incidents (trading system outage = money loss), regulatory awareness, collaboration between dev and traders/business, and experience with financial domain complexity.
- VI: Câu hỏi behavioral ở fintech: làm việc dưới áp lực, xử lý incident production, hiểu biết regulatory, collab dev-business, kinh nghiệm domain finance.

Prepare STAR stories for:

1. **Production incident during trading hours**
   - "Tell me about a time you fixed a critical bug in production"
   - Key: response time matters, financial impact awareness

2. **Working with tight deadlines**
   - "How do you prioritize when multiple urgent tasks compete?"
   - Key: market deadlines are hard (exchange opens at X, no delay)

3. **Cross-functional collaboration**
   - "How do you work with non-technical stakeholders (traders, compliance)?"
   - Key: translate technical concepts, understand business impact

4. **Learning new domain quickly**
   - "How do you approach a domain you're unfamiliar with?"
   - Key: proactive learning, asking questions, building domain vocabulary

5. **System reliability**
   - "What's your approach to ensuring 99.99% uptime?"
   - Key: monitoring, alerting, runbooks, chaos engineering

---

## Flash Cards

| # | Question | Key Answer |
|---|----------|-----------|
| 1 | Trading platform components | Market Data, OMS, Execution, Risk, Position/P&L, Back Office |
| 2 | White-label challenge | Multi-tenancy, data isolation, configurable rules per tenant |
| 3 | FIX protocol | Industry-standard messaging for electronic trading (35=D, 35=8) |
| 4 | FIX sequence gap | ResendRequest for missed range, PossDupFlag for duplicates |
| 5 | Order lifecycle | New → Pending → Open → Partial Fill → Filled/Cancelled |
| 6 | Pre-trade risk | Buying power, position limit, fat finger, price reasonability |
| 7 | SOR | Smart Order Routing — best execution across venues |
| 8 | Market data pipeline | Feed Handler → Ticker Plant → Distribution (pub/sub) |
| 9 | FX vs Equity | OTC, 24/5, currency pairs, multiple LPs, T+2 settlement |
| 10 | WebSocket for trading | Full-duplex, server push, low overhead vs REST polling |
| 11 | Scale 100K WS | Epoll, horizontal + sticky LB, Redis Pub/Sub fan-out |
| 12 | Kafka in trading | High-throughput events, ordered per partition, replay/audit |
| 13 | DB for trading | PostgreSQL (ACID), TimescaleDB (OHLCV), Redis (cache) |
| 14 | Equix products | White-label platform, OneWalleX OMS, Night Vision FX, Vision Swap, HarmoniX |
| 15 | Australian regulation | ASIC, AFSL, Best Execution, AML/KYC, 7-year audit retention |
