# 18 - Tieto Interview Prep — Personalized English Q&A

Chuẩn bị phỏng vấn Tieto Tech Consulting, vị trí **C/C++ Software Engineer — 5G L2**.
Dựa trên CV của Manh Khieu Vu. Luyện nói TO TIẾNG trước khi vào phỏng vấn.

---

## PART 1: SELF-INTRODUCTION (Học thuộc, nói mượt)

---

### Q1. "Tell me about yourself" — 30 giây version

**A:**

```
"Hi, thanks so much for having me today. I'm Khieu.

I've been working as a software engineer for about 7 years 
now, mostly in C and C++ on Linux. I've had the chance to 
work on some pretty interesting things — database engines, 
embedded multimedia, and most recently enterprise printer 
platforms.

What I really enjoy is the system-level side of things — 
performance tuning, multi-process design, tracking down 
tricky concurrency bugs. That kind of problem-solving 
is what keeps me motivated.

And that's actually why I'm excited about this role — 
telecom and 5G bring those same real-time, performance-critical 
challenges, and I'd love to be part of that."
```

---

### Q2. "Tell me about yourself" — 1 phút version (chi tiết hơn)

**A:**

```
"Hi, thanks so much for this opportunity. I'm Khieu.

I've been doing C and C++ development on Linux for over 
7 years now, and I've been lucky to work on quite a range 
of projects.

Right now I'm at FPT Software, where I work on print workflow 
modules for a Japanese enterprise client. It involves job 
scheduling, talking to hardware, and dealing with concurrency 
across different printer models. I also handle market issues — 
basically owning bugs from investigation all the way to 
the fix and release.

Before that, I was at Toshiba Software for about 5 years. 
The highlight there was PGSpider — an open-source federated 
query engine on top of PostgreSQL. I built Foreign Data 
Wrappers to connect databases like MySQL, Oracle, and MongoDB, 
and worked on query pushdown to make distributed queries faster.

I also got to build an embedded multimedia system on a Toradex 
iMX board — we took it from Full HD 30fps up to 4K at 60fps 
using GStreamer and Wayland. That was a really fun challenge.

What draws me to telecom is that it's the same kind of work 
I love — real-time, performance-critical, close to the metal — 
but at a much larger scale. And with 6+ years working with 
Japanese teams, I'm used to international collaboration and 
high quality standards, which I think fits well with Tieto."
```

---

## PART 2: BEHAVIORAL QUESTIONS (STAR format)

---

### Q3. "Why do you want to join Tieto / work in telecom?"

**A:**

```
"There are three main reasons.

First, I want to work on systems where performance truly 
matters — microsecond-level timing, real-time constraints. 
Telecom L2 development is exactly that.

Second, I've spent over 6 years collaborating with international 
teams — specifically Japanese engineering teams with strict 
quality standards. I'm comfortable working in English in 
a global environment, which is important at Tieto.

Third, I see telecom as a long-term career path. 5G is still 
evolving, and the skills I build here — protocol stack 
implementation, multi-core real-time systems — will remain 
valuable for many years."
```

---

### Q4. "Tell me about a challenging bug you've fixed."

**A:**

```
Situation:
"At FPT Software, we received a market issue report where print 
jobs would randomly fail on a specific printer model — but only 
under heavy load."

Task:
"I was assigned to investigate and find the root cause."

Action:
"I started by reproducing the issue in our lab with a stress test 
— sending many print jobs simultaneously. I analyzed the logs 
and noticed a pattern: the failure happened when two jobs tried 
to access the finisher hardware at the same time.

I traced the code and found a race condition — two threads were 
accessing a shared resource without proper synchronization. The 
existing mutex was scoped too narrowly and didn't cover a critical 
section where the hardware state was being modified.

I extended the lock scope, added proper state validation before 
hardware access, and wrote a stress test to verify the fix."

Result:
"The fix resolved the issue completely. We deployed it to the 
market, and the failure rate dropped to zero. I also documented 
the pattern to help the team avoid similar issues in other models."
```

---

### Q5. "Tell me about your experience with open-source or large codebases."

**A:**

```
"At Toshiba, I contributed to PGSpider — an open-source 
PostgreSQL extension with 180+ stars on GitHub. It's a federated 
query engine that connects to multiple databases.

I implemented several Foreign Data Wrappers — for MySQL, Oracle, 
MongoDB, SQLite, InfluxDB, and others. Each integration required 
understanding the target database's query capabilities and mapping 
them to PostgreSQL's internal API.

One significant contribution was query pushdown optimization. 
Instead of pulling all data to PGSpider and filtering locally, 
I analyzed which operations — WHERE clauses, aggregations, 
ORDER BY — could be delegated to the child databases. This 
significantly improved performance for large datasets.

Working on a PostgreSQL-based codebase taught me how to navigate 
large, complex C projects — understanding code conventions, 
writing tests, and working with the open-source community."
```

---

### Q6. "Tell me about your experience with embedded / real-time systems."

**A:**

```
"At Toshiba, I developed a multimedia system on a Toradex Apalis 
iMX platform running embedded Linux. The system needed to display 
video, images, and text simultaneously.

The key challenge was scaling from Full HD 30fps to 4K 60fps. 
I optimized the GStreamer pipeline — used hardware-accelerated 
decoding, reduced memory copies by using DMA buffers, and 
integrated Wayland/Weston for GPU-accelerated compositing.

For the multi-process architecture, I designed the IPC using 
DBus — each service ran as a separate process, and they 
coordinated through message passing. This is similar to how 
telecom systems use message-based IPC between protocol layers.

I also optimized startup time and memory footprint — important 
for resource-constrained embedded targets. This experience 
directly relates to telecom embedded work where memory pools, 
zero-copy buffers, and real-time constraints are critical."
```

---

### Q7. "How do you handle working with international teams?"

**A:**

```
"I have over 6 years of experience working directly with 
Japanese engineering teams — at both Toshiba and FPT Software.

Japanese teams are known for very high quality standards and 
strict processes. I learned to communicate clearly and precisely 
— documenting everything, confirming requirements explicitly, 
and reporting progress proactively.

For example, at FPT, when handling market issues from Japanese 
clients, I own the full cycle: receive the bug report, 
investigate, communicate findings back to the client with 
evidence, propose a solution, and follow through to release. 
Clear communication is essential — especially when the root 
cause is complex and needs to be explained to non-technical 
stakeholders.

I believe this experience translates well to Tieto's 
international environment — working across teams in Finland, 
Sweden, Poland, and Vietnam."
```

---

### Q8. "What is your weakness?" / "What do you want to improve?"

**A:**

```
"My telecom domain knowledge is still developing. I haven't 
worked directly with 3GPP specifications or protocol stacks 
like MAC or RLC before.

However, I've been actively studying — I've gone through 
the 5G NR protocol stack architecture, learned about HARQ, 
scheduling algorithms, ASN.1 encoding, and SCTP. I also 
understand the CU/DU/RU split and how L2 fits in.

I'm a fast learner — when I joined the PostgreSQL project 
at Toshiba, I had no database internals experience, but 
within a few months I was implementing core features. 
I'm confident I can ramp up quickly on telecom specifics."
```

---

## PART 3: TECHNICAL QUESTIONS (Tieto 5G L2 focus)

---

### Q9. "Describe the 5G NR protocol stack. Where does L2 fit?"

**A:**

```
"The 5G NR protocol stack from bottom to top is:

- PHY (L1): physical layer — modulation, channel coding, OFDM
- MAC (L2): scheduling, HARQ, multiplexing, random access
- RLC (L2): segmentation, ARQ in acknowledged mode, reordering
- PDCP (L2): header compression, ciphering, integrity protection
- SDAP (L2): QoS flow to DRB mapping — new in 5G
- RRC (L3): connection management, mobility, bearer setup

L2 includes MAC, RLC, PDCP, and SDAP. In the O-RAN architecture, 
MAC and RLC run on the DU (Distributed Unit), while PDCP and 
SDAP run on the CU (Central Unit).

L2 is where most of the C development happens — scheduling 
runs every slot which can be as short as 0.125 milliseconds, 
so the code must be highly optimized."
```

---

### Q10. "What is HARQ and how does it work?"

**A:**

```
"HARQ stands for Hybrid Automatic Repeat reQuest. It combines 
forward error correction with retransmission.

When a receiver fails to decode a packet, it stores the received 
bits in a soft buffer and sends a NACK. The sender retransmits — 
either the same data (Chase Combining) or different redundancy 
bits (Incremental Redundancy). The receiver combines both 
transmissions for better decoding probability.

In 5G NR, there are up to 16 parallel HARQ processes running 
as a pipeline. This is important because we don't wait for 
ACK/NACK before sending the next data — we keep sending on 
different HARQ processes.

From a software perspective, HARQ is one of the most 
performance-critical modules — it runs every slot, manages 
soft buffer memory, and must handle ACK/NACK feedback 
with strict timing."
```

---

### Q11. "Explain the difference between RLC TM, UM, and AM modes."

**A:**

```
"RLC has three modes:

- TM (Transparent Mode): no processing, just passes data through. 
  Used for broadcast messages like System Information.

- UM (Unacknowledged Mode): does segmentation and reassembly 
  but no retransmission. Used for real-time traffic like VoLTE 
  where retransmission would add too much delay.

- AM (Acknowledged Mode): full reliability — segmentation, 
  ARQ with retransmission, reordering, and duplicate detection. 
  Used for data traffic where reliability is important.

In AM mode, the sender uses a polling mechanism to request 
status reports from the receiver. The receiver sends back 
a bitmap of ACKed and NACKed sequence numbers, and the sender 
retransmits any missing PDUs."
```

---

### Q12. "How does the MAC scheduler work?"

**A:**

```
"The MAC scheduler is the brain of the gNodeB. Every slot, 
it decides which UEs get radio resources — time and frequency.

Its inputs are: Buffer Status Reports from UEs, Channel Quality 
indicators (CQI), QoS requirements, and HARQ feedback.

Common scheduling algorithms include Proportional Fair — which 
balances throughput and fairness by dividing each UE's 
instantaneous rate by its average rate. The UE with the highest 
ratio gets scheduled first.

In 5G NR, the scheduler is more complex than LTE because of 
flexible numerology — different subcarrier spacings mean 
different slot durations. It also needs to handle mini-slot 
scheduling for URLLC traffic with very low latency requirements.

The scheduler must complete within the slot duration — which 
can be as short as 0.125 milliseconds. So the implementation 
must be very efficient."
```

---

### Q13. "How would you debug a memory-related issue in an embedded C system?"

**A:**

```
"My approach depends on the environment.

On a host build with Linux, I would use tools like Valgrind 
and AddressSanitizer to detect memory errors — buffer overflows, 
use-after-free, memory leaks.

On an embedded target where these tools aren't available, 
I would use techniques like:

- Memory pool guard patterns: put known byte patterns at the 
  head and tail of each allocated block, then periodically 
  check if they've been overwritten.

- Pool statistics: track allocation counts and high-water marks 
  to detect leaks.

- Logging: add trace logs around suspicious code paths, using 
  a ring buffer logger that doesn't block.

At my current job, I've debugged race conditions by adding 
assertions and stress testing under heavy load. I also use 
core dump analysis with GDB when crashes occur.

In telecom, I understand that malloc is not used at runtime — 
instead, pre-allocated memory pools with O(1) allocation are 
standard to avoid non-deterministic latency."
```

---

### Q14. "What is your experience with multi-threading and concurrency?"

**A:**

```
"I have significant experience with concurrency in C/C++.

At FPT Software, I work with multi-threaded print job processing 
— where multiple jobs run concurrently and access shared hardware 
resources. I've debugged and fixed race conditions involving 
mutexes, investigated deadlocks, and optimized lock granularity.

At Toshiba, I designed a multi-process architecture using DBus 
for IPC — each component ran as a separate process, communicating 
through message passing rather than shared memory. This is 
actually similar to the telecom approach where protocol layers 
communicate via message queues.

I'm also familiar with lock-free programming concepts — 
SPSC queues, memory barriers, atomic operations — from studying 
the C++ concurrency model. In telecom, I know these are critical 
for inter-core communication on multi-core DSP platforms."
```

---

### Q15. "What do you know about SCTP and why is it used in telecom?"

**A:**

```
"SCTP — Stream Control Transmission Protocol — is the transport 
protocol used for signaling in telecom, for example S1AP between 
eNodeB and MME.

It's preferred over TCP because it provides two key features:

Multi-homing: a single SCTP association can use multiple IP 
addresses, so if one network path fails, traffic automatically 
switches to the backup path. This is critical for carrier-grade 
reliability.

Multi-streaming: multiple independent streams within one 
association. If one stream has packet loss and needs 
retransmission, it doesn't block other streams — unlike TCP 
where head-of-line blocking affects everything.

SCTP also has built-in heartbeat for path monitoring and 
supports graceful shutdown."
```

---

## PART 4: QUESTIONS TO ASK THE INTERVIEWER

---

### Q16. Câu hỏi nên hỏi interviewer

**A:**

```
1. "Could you tell me more about the specific 5G L2 module 
    or layer the team is working on? Is it MAC, RLC, or PDCP?"

2. "What does the development environment look like — do you 
    work on host simulation builds, or directly on target 
    hardware?"

3. "How is the team structured? Is it organized by protocol 
    layer, or by feature?"

4. "What does the onboarding process look like for someone 
    transitioning from another domain into telecom?"

5. "What 3GPP release is the current product based on?"

6. "How does the team handle testing — do you have UE 
    simulators or use commercial test equipment?"
```

---

## PART 5: MANAGEMENT / HR INTERVIEW QUESTIONS

Management round thường không hỏi sâu kỹ thuật, mà tập trung vào: con người, cách làm việc, motivation, culture fit, expectation.

---

### Q17. "Why are you looking for a new job? / Why do you want to leave your current company?"

**A:**

```
"I've learned a lot at FPT Software — especially about working 
with Japanese clients and handling production issues end-to-end. 

But I feel like I've reached a point where I want a bigger 
technical challenge. The printer platform is mature, and 
I want to work on something with more real-time complexity 
and larger scale.

Telecom — especially 5G — is that for me. And Tieto has 
a strong reputation in this space with deep expertise. 
So it's more about moving toward something exciting than 
running away from anything."
```

Tip: KHÔNG BAO GIỜ nói xấu công ty cũ. Luôn frame là "moving toward", không phải "running from".

---

### Q18. "Where do you see yourself in 3-5 years?"

**A:**

```
"In 3 years, I want to be a solid contributor in telecom — 
deeply understanding the 5G protocol stack, owning complex 
features, and being someone the team can rely on for 
difficult debugging.

In 5 years, I'd like to grow into a technical lead or 
architect role — guiding design decisions, mentoring junior 
engineers, and helping shape the system architecture. 

I think Tieto is a great place for that kind of growth, 
given the scale and complexity of the projects here."
```

---

### Q19. "What is your expected salary?" / "What are your salary expectations?"

**A:**

```
"I'm open to discussing compensation. I'd love to understand 
the full picture — the role scope, benefits, and growth 
opportunities — before I give a specific number.

That said, I'm looking for something competitive for a senior 
engineer role in this domain. Could you share the range 
you have in mind for this position?"
```

Tips:
- Đừng nói con số đầu tiên nếu có thể — hỏi ngược lại range
- Nếu bị ép phải nói: research trước mức lương Tieto VN trên Glassdoor/LinkedIn
- Có thể nói: "Based on my research and experience, I'm looking at around [X] to [Y], but I'm flexible depending on the overall package."

---

### Q20. "How do you handle pressure / tight deadlines?"

**A:**

```
"I've worked under pressure quite a bit — both at FPT and 
Toshiba, where we had strict release cycles with Japanese 
clients. Missing a deadline was not an option.

My approach is: first, understand the priority — what 
absolutely must be done versus what's nice to have. Then 
break the work into small tasks and track progress daily.

If I see a risk of missing the deadline, I communicate early. 
I'd rather raise a flag early and adjust scope than surprise 
the team at the last minute.

For example, at FPT, we had a critical market issue that 
needed a fix within 3 days. I focused on the root cause first, 
proposed a minimal fix for the urgent release, and then 
followed up with a more thorough solution in the next sprint."
```

---

### Q21. "How do you handle disagreements with colleagues?"

**A:**

```
"I think disagreements are normal and actually healthy — 
they usually mean people care about the quality of the work.

My approach is to focus on the technical facts, not the person. 
I try to understand their perspective first — maybe they have 
context I'm missing. Then I share my reasoning with evidence — 
data, code examples, or spec references.

If we still can't agree, I'm happy to involve a senior 
engineer or architect to get a third opinion. At the end 
of the day, what matters is the best solution for the 
project, not who was right.

I had a situation at Toshiba where my colleague and I 
disagreed on a query optimization approach. We each 
prototyped our solution and benchmarked them. His approach 
was actually better for large datasets, so we went with 
that. No hard feelings — it was a good learning experience."
```

---

### Q22. "Tell me about a time you mentored or helped a teammate."

**A:**

```
"At FPT Software, a junior engineer joined our team and was 
assigned to investigate a printer hardware communication issue. 
He was struggling because the system involved multiple threads 
and it was hard to trace the execution flow.

I sat down with him and showed him my debugging approach — 
how to add targeted logging, how to use GDB to inspect thread 
states, and how to narrow down the problem by isolating 
components. I also shared some patterns for understanding 
race conditions.

After a couple of sessions, he was able to resolve the issue 
on his own. He later told me that the debugging methodology 
I showed him helped him with several other issues as well. 
That felt really rewarding."
```

---

### Q23. "Do you prefer working independently or in a team?"

**A:**

```
"I enjoy both, and I think a good balance is important.

For deep investigation work — like debugging a complex issue 
or reading a specification — I prefer focused, independent 
time. That's when I'm most productive.

But for design discussions, code reviews, and learning new 
domain knowledge, collaboration is essential. I learn a lot 
from my colleagues, and I think the best solutions come from 
shared perspectives.

In practice, my workflow is usually: understand the problem 
independently first, then discuss my approach with the team, 
then implement with regular check-ins."
```

---

### Q24. "What do you know about Tieto / TietoEvry?"

**A:**

```
"Tieto — or TietoEvry — is a Nordic technology company with 
about 13,000 employees globally. The headquarters are in 
Finland, with offices across the Nordics, Europe, and Asia 
including Vietnam.

For telecom specifically, Tieto Tech Consulting provides 
R&D engineering services — including 5G L2 development, 
network automation, and cloud-native solutions. I noticed 
on the careers page you have teams working on 5G L2 in C 
specifically, which is exactly what I'm interested in.

What attracted me is the combination of deep technical work 
with a global, collaborative environment. And the fact that 
Tieto works on the actual product development side of telecom 
— not just integration or testing — is very appealing."
```

---

### Q25. "Do you have any questions for us?"

**A:**

Luôn hỏi ít nhất 2-3 câu. Câu hỏi tốt cho management round:

```
1. "What does a typical career growth path look like for 
    an engineer at Tieto? How do people usually progress?"

2. "How would you describe the team culture? Is it more 
    autonomous or more structured?"

3. "What does the onboarding look like — especially for 
    someone coming from a non-telecom background?"

4. "What are the biggest challenges the team is facing 
    right now?"

5. "How does Tieto support professional development — 
    training, certifications, conferences?"

6. "What do you personally enjoy most about working here?"
    (← câu này tạo connection rất tốt)
```

---

## PART 6: LAST-MINUTE CHECKLIST

---

### Q26. Checklist trước khi vào phỏng vấn

**A:**

Pre-interview (1 giờ trước):
```
[ ] Đọc to self-intro 3 lần (Q1 + Q2)
[ ] Đọc to "Why Tieto" 2 lần (Q3)
[ ] Đọc to bug story 2 lần (Q4)
[ ] Review bảng pronunciation (Q31 trong file telecom)
[ ] Chuẩn bị giấy bút để vẽ diagram khi giải thích
[ ] Test camera, mic, internet
[ ] Mở sẵn file này để glance nếu cần
```

Mindset:
```
- Nói CHẬM và RÕ. Đừng vội.
- Nếu không hiểu → "Could you repeat that, please?"
- Nếu cần nghĩ → "That's a good question. Let me think..."
- Nếu không biết → "I haven't worked with that directly, 
  but based on my understanding of [related]..."
- Khi giải thích kỹ thuật → VẼ DIAGRAM
- Mỗi câu trả lời: 30-60 giây. Không nói quá dài.
- Cuối buổi: HỎI ÍT NHẤT 2 CÂU (Q16)
```

Key numbers to remember:
```
- 7+ years C/C++
- 6+ years working with Japanese teams
- PGSpider: 180+ stars, open-source PostgreSQL extension
- Scaled embedded video: FHD→4K, 30fps→60fps
- 5G NR: 16 HARQ processes, slot = 0.5ms (mu=1)
- Carrier-grade: 99.999% = 5 min downtime/year
```
