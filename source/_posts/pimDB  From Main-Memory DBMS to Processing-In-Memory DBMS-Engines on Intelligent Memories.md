---
title: pimDB:From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories
cover: /cover/pimDB  From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories.png
date: 2023-11-28 19:02:22.098896
comments: True
abstracts: 研究内存数据库的处理方法，探讨布局、层次和迁移对性能的影响，结果提高计算效率，同时研究页面布局、内存层次和迁移对性能的影响。
mathjax: true
categories: 工程技术
tags:
- 页面布局
-  内存层次结构
-  数据迁移
---
# pimDB: From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories

## Motivation

- 仍然是 PIM 的动机，减少数据搬移
- 利用新硬件 UPMEM 构建 DBMS engine pimDB

## Design

<p align="center"><img src="/img/pimDB  From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories/G1iZb5GKCoNovcxbYTbcRqdJnwc.png" ></p>

- 内存数据库
- 既可以 CPU-DRAM 方式工作，也可以 DPU-UPMEM 方式工作
- 两种 Page Format：

<p align="center"><img src="/img/pimDB  From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories/EQ2UbXtWLo1DeTxs4DWcX00lnRc.png" ></p>

## Evaluation

- Intel Xeon Silver 4110 CPUs （16 核 32 线程）
- 125GB of DRAM（非 PIM）
- 20 PIM DIMMs（2560 DPUs，160GB memory)，因故障实际上只有 2496 DPUs 可用
- TPC-H orderline table

### TPC-H

- TPC-H 是用来评估在线分析处理的基准程序，主要模拟了供应商和采购商之间的交易行为，其中包含针对 8 张表的 22 条分析型**查询**
- TPC-H 模型是典型的雪花模型，一共有 8 张表，其中 nation（国家）和 region（区域）两张表的数据量是固定的，其余 6 张表的数据量跟**比例因子 SF（Scale Factor）**相关，可以指定为 1,100,1000 等，分别代表 1 GB、100GB、1000GB，根据指定的 SF 确定每张表的数据量
  | 实验 | CPU 线程 | DPU 个数       | Tasklet 数 | DMA Transfer size | Page format | SF   | operation       | selectivity        | attribute 个数 | 物化策略 |
  | ---- | -------- | -------------- | ---------- | ----------------- | ----------- | ---- | --------------- | ------------------ | -------------- | -------- |
  | 1    | 变量     | 变量(CPU 未知) | 11         | 没说              | 变量        | 变量 | scan-and-select | 50%                | 1              | /        |
  | 2    | 变量     | 变量(CPU 未知) | 11         | 没说              | 变量        | 1    | scan-and-select | 50%                | 1              | /        |
  | 3    | 32       | 64             | 11         | 变量              | 变量        | 变量 | scan-and-select | 50%                | 1              | /        |
  | 4    | 没说(32) | 变量           | 没说(11)   | 没说              | 变量        | 变量 | scan-and-select | 50%                | 没说(1)        | /        |
  | 5    | 没说(32) | 64             | 变量       | 变量              | 变量        | 8    | scan-and-select | 50%                | 没说(1)        | /        |
  | 6    | 没说(32) | 64             | 11         | 32B               | 变量        | 没说 | Aggregation     | 50%                | 变量           | /        |
  | 7    | 没说(32) | 64             | 11         | 64B               | 变量        | 1    | scan-and-select | 变量(DPU 变时 50%) |                | 变量     |
  | 8    |          | 变量           |            |                   | 变量        |      | 变量            |                    |                |          |
- 数据在 PIM 内存中是如何分布的？平均？
- DPU 的空间够吗？（640 个 DPU 怎么装 80GB）（8 个 DPU 怎么装 1GB）

### 实验 1 CPU vs PIM

| 实验 | CPU 线程 | DPU 个数       | Tasklet 数 | DMA Transfer size | Page format | SF   | operation       | selectivity | attribute 个数 | 物化策略 |
| ---- | -------- | -------------- | ---------- | ----------------- | ----------- | ---- | --------------- | ----------- | -------------- | -------- |
| 1    | 变量     | 变量(CPU 未知) | 11         | 没说              | 变量        | 变量 | scan-and-select | 50%         | 1              | /        |

<p align="center"><img src="/img/pimDB  From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories/OZ2Nb6Cgpoo4zNxyeI1cMn5tnqf.png" ></p>

- PIM 的成倍增加，性能几乎是成倍增加的；CPU 的成倍增加，在个数少时性能基本成倍增加，个数多时不然（shared nothing，减少竞争）
- 数据量的增加对于 PIM 的影响几乎线性；而对 CPU 性能影响较大（减少数据移动，或者高速化并行化数据移动）
- PAX 的方式优于 NSM 的方式（列存储适合 OLAP 的必然）

### 实验 2 Impact of Invocation

| 实验 | CPU 线程 | DPU 个数       | Tasklet 数 | DMA Transfer size | Page format | SF | operation       | selectivity | attribute 个数 | 物化策略 |
| ---- | -------- | -------------- | ---------- | ----------------- | ----------- | -- | --------------- | ----------- | -------------- | -------- |
| 2    | 变量     | 变量(CPU 未知) | 11         | 没说              | 变量        | 1  | scan-and-select | 50%         | 1              | /        |

<p align="center"><img src="/img/pimDB  From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories/ZWIpb0lQooSTh7x2unococSTnK3.png" ></p>

- 何为 invocation cost？个人认为，比如执行 select A from B where A > 30，传输 30 这个数据造成的开销就是
- 合理划分任务与数据的 UPMEM 应用中 invocation cost 忽略不计；invocation cost 是存在的，开发者需要合理分配任务
- 一个 DIMM 有两个 rank，每个 rank8 个 chip，每个 chip8 个 DPU，一个 DIMM 的并行计算能力优于 CPU

### 实验 3 Page Format、WRAM and Data Movement

| 实验 | CPU 线程 | DPU 个数 | Tasklet 数 | DMA Transfer size | Page format | SF   | operation       | selectivity | attribute 个数 | 物化策略 |
| ---- | -------- | -------- | ---------- | ----------------- | ----------- | ---- | --------------- | ----------- | -------------- | -------- |
| 3    | 32       | 64       | 11         | 变量              | 变量        | 变量 | scan-and-select | 50%         | 1              | /        |

<p align="center"><img src="/img/pimDB  From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories/Ad0jbOXjworOXnxJqFPcpxvznEe.png" ></p>

- 64B 一个 tuple
- 个人定性判断：DMA tansfer 所需的时钟还是多的，NSM 每次 DMA 传输的有效数据可供执行的指令非常少，整体来看 I/O 花费的时钟周期占比较大，因此 IPC 就低；而 PAX 每次 DMA 传输的有效数据非常多，一次 DMA 可以执行非常多的指令，整体来看用于计算的时钟周期占比较大。
- SF 的指标仍然是表现的扩展性和稳定性良好
- PAX 的方式需要更少的数据搬移，因此无论一次性传多少字节到 WRAM 中，数据远远足够，表现计算瓶颈
- NSM 的方式需要更多的数据搬移，表现为 IO 瓶颈（一次搬运的数据很小，计算占比很小，需要等下一次 I/O）

  - 32B 有最小的读放大
  - 64B 是一整个 tuple
  - 128B 是两个 tuple
- 合理设计数据布局提高数据搬移效率，合理调整 DMA transfer 大小

### 实验 4 Scalability and Constancy

| 实验 | CPU 线程 | DPU 个数 | Tasklet 数 | DMA Transfer size | Page format | SF   | operation       | selectivity | attribute 个数 | 物化策略 |
| ---- | -------- | -------- | ---------- | ----------------- | ----------- | ---- | --------------- | ----------- | -------------- | -------- |
| 4    | 没说(32) | 变量     | 没说(11)   | 没说              | 变量        | 变量 | scan-and-select | 50%         | 没说(1)        | /        |

<p align="center"><img src="/img/pimDB  From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories/R1sWbADZVov8AvxtPWucMJoeneb.png" ></p>

- 将数据量和 DPU 个数按照同样的比率增加，表现不变（数据平均分布）
- 将数据量恒定，将 DPU 个数按照一定的比率增加（2 倍），执行时间按照同样的比率减少
- 可扩展性和稳定性很好

### 实验 5 Tasklet

| 实验 | CPU 线程 | DPU 个数 | Tasklet 数 | DMA Transfer size | Page format | SF | operation       | selectivity | attribute 个数 | 物化策略 |
| ---- | -------- | -------- | ---------- | ----------------- | ----------- | -- | --------------- | ----------- | -------------- | -------- |
| 5    | 没说(32) | 64       | 变量       | 变量              | 变量        | 8  | scan-and-select | 50%         | 没说(1)        | /        |

<p align="center"><img src="/img/pimDB  From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories/WIqwb6bxZoJk1SxlbBWcWucznwe.png" ></p>

- PAX 模式由于计算瓶颈，因此 DMA transfer sizes 几乎没影响；DMA 对于 NSM 模式的影响与之前的 Page Format 类似，32B 相对最好，64B 最差，128B 次之
- 多 tasklet 能够充分利用 I/O 时间 interleave，提高计算效率
- PAX 模式于 12tasklet 饱和，NSM32B 于 8，NSM64B 和 NSM128B 都于 6 饱和
- tasklets 个数要合理，太多可能过分占用 WRAM 空间

### 实验 6 Projection and Aggregation

| 实验 | CPU 线程 | DPU 个数 | Tasklet 数 | DMA Transfer size | Page format | SF   | operation   | selectivity | attribute 个数 | 物化策略 |
| ---- | -------- | -------- | ---------- | ----------------- | ----------- | ---- | ----------- | ----------- | -------------- | -------- |
| 6    | 没说(32) | 64       | 11         | 32B               | 变量        | 没说 | Aggregation | 50%         | 变量           | /        |

<p align="center"><img src="/img/pimDB  From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories/GyP2b8Ii9oAe3OxDDmWcMlZ5nOO.png" ></p>

- 引入多个 attribute 并对每个 attribute 进行 aggregation
- 文中说到 NSM 能够一个 DMA Transfer 传输所有 attribute，因此增加 attribute 不会造成太大影响（I/O bounded），相反能够让 IPC 提高
- PAX 每次 DMA 拿到部分 mini page，要想完成上述计算就需要多次 I/O，但是每次 I/O 带来的计算任务还是足够多的，因此仍然是 computation bounded，IPC 会随 attribute 的增加减少，但减少的不多；此外，由于引入多 attribute 的 aggregation 增加了计算任务，对于 computation bounded 的 PAX 来说，仍然会造成性能的影响（多一个 attribute 多执行 6~8ms）
- 之前一直处于劣势的 NSM 反而在这种情况下的执行时间处于优势，这是 OLTP 和 OLAP 两种应用适用不同 page format 的必然，因此需要根据应用来设计程序，Trade off between computation and I/O

### 实验 7 Materialization

| 实验 | CPU 线程 | DPU 个数 | Tasklet 数 | DMA Transfer size | Page format | SF | operation       | selectivity        | attribute 个数 | 物化策略 |
| ---- | -------- | -------- | ---------- | ----------------- | ----------- | -- | --------------- | ------------------ | -------------- | -------- |
| 7    | 没说(32) | 64       | 11         | 64B               | 变量        | 1  | scan-and-select | 变量(DPU 变时 50%) |                | 变量     |

<p align="center"><img src="/img/pimDB  From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories/PvJFbNAHIokPVuxVzZkcq91tndo.png" ></p>

- Materialization，个人认为其意思是将一些复杂查询的结果持久化到硬盘中以便下次使用
- 增加 selectivity 会增加物化结果的大小（多少）
- 对于 BitVector，其只记载 tuple 的 location 而不记载真正的 tuple，在 WRAM 中缓存（不占内存）
- 对于 Full Materialization，需要记录所有 attribute，且在 MRAM 中缓存（占内存）
- 对 NSM，BitVector 方式几乎没有影响（I/O bounded），Full Materialization 方式会需要写入 MRAM，会有轻微影响（64B 刚好是一个 tuple）
- 对 PAX，BitVector 方式有轻微影响（computation bounded），Full Materialization 方式有着极大的影响，因为需要所有 attribute，而 PAX 只会缓存部分 mini page，因此需要 I/O 去读其他的 attribute
- Scalability 和之前一样

### 实验 8 Kernel deployment and invocation

<p align="center"><img src="/img/pimDB  From Main-Memory DBMS to Processing-In-Memory DBMS-Engines on Intelligent Memories/J1Mwba0KtoaxpfxhZwHcmvRVnng.png" ></p>

- 大的通用性高的 kernel（程序）vs 小的专用性高的 kernel（程序）
- 大的需要传额外的参数以判断操作类型，小的可能需要切换不同的 kernel 完成操作
- 文章认为 24KB 的 IRAM 足够放置大的通用性高的 kernel，传参数的开销小于传 kernel 的开销，但是如果应用条件允许的话，传 kernel 也是可以接受的选择

## Lessons

- How will PIM-capable memories be embedded into the memory hierarchy?
- Will they potentially co-exist with passive memories building a multi-tier main-memories or is it realistic to assume PIM-only memory?
- How will PIM-memories scale and what interconnect will they have, especially with view of novel cachecoherent interconnects such as CXL and protocols like CXL.mem?

## Contribution

- **We investigate the impact of different page layouts (NSM, PAX)** on PIM processing and scalability on a real system. We observe the necessity for custom PIM page layouts.
- **We investigate the scale and the different levels of PIM-parallelism**. Our exploration offers insights into the compute/bandwidth tradeoffs in PIM-processing and calls for compute/transfer interleaving primitives in PIM settings.
- **We investigate the effect of the in-situ/PIM memory hierarchy and configurable PIM data transfers** (as opposed to cachelinesized transfers) on assumptions in cache-aware processing and data layouts.
- **We investigate PIM allocation strategies**, as PIM mandates data/ operation co-placement and partitioning. In this context, we evaluate the kernel deployment and the PIM invocation overhead.
