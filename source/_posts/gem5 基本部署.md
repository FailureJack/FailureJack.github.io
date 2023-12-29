---
title: gem5 基本部署
cover: /cover/gem5 基本部署.png
date: 2023-12-29 15:09:04
comments: True
feature: False
abstracts: 这篇文章主要介绍了在Ubuntu上部署gem5的方法，包括系统调用和全系统模拟两种模式。详细讲述了如何搭建环境、安装依赖、克隆源码、编译源码、检验是否成功、解决内存不足问题和全系统模式搭建等内容。此外，文章还给出了详细的参数设置和组件安装流程，适合gem5初学者阅读参考。
categories: 工程技术
tags:
- Gem5
mathjax: true
---
# gem5 基本部署

本文档介绍如何在 Ubuntu 上部署 gem5，主要是系统调用和全系统模拟两种模式。[gem5 的官方文章](https://arxiv.org/abs/2007.03152)中介绍了这两种模式的异同，具体可以看下图：

<p align="center"><img src="/img/gem5 基本部署/EEO1bSFAPoVsOKxiizVcEntvnhg.png" ></p>

系统调用模式（SE，Syscall Emulation）将模拟的指令转化为系统调用，全系统模式（FS，Full System）模拟硬件并在模拟的硬件上建立客户操作系统，能够提供更加底层精细的统计，同时性能会更差。但因其 FS 模式更加全面，因此 FS 模式更常使用，是重点。

下面给出推荐的环境配置：

| **环境** | **要求**     | **原因**                                                                                                          |
| -------- | ------------ | ----------------------------------------------------------------------------------------------------------------- |
| Ubuntu   | 版本 >=18    | 按照官网建议的来，gem5 的版本和 Ubuntu 的版本需要搭配，否则难以编译 gem5；本人使用的是 Ubuntu20.04LTS+gem5 22.0。 |
| gem5     | 版本 >=20.0  |                                                                                                                   |
| Host 机  | 内存 >=8GB   | 编译 gem5 的时候很占内存，内存越大越好                                                                            |
| Host 机  | 硬盘 >=100GB | gem5 本身、全系统的 img 都不小，还可能创建 swap 分区                                                              |

## gem5 SE 模式搭建

此步骤建议按照[官方文档](https://www.gem5.org/documentation/learning_gem5/part1/building/)一步一步走，最后进行 Hello world 测试。也可参考[他人的博客](https://zhuanlan.zhihu.com/p/336017753)。

### 依赖安装

注意：整个安装过程可能需要等待较长时间。切记不要换源，阿里源、清华源均不可，否则会出现难以琢磨的未满足的依赖关系的问题。

执行下面的命令安装依赖：

```bash
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    python3-dev python-is-python3 libboost-all-dev pkg-config
```

### gem5 源码克隆

克隆 gem5 到目录 GEM5 中，要保证空间充足。

```bash
# 可以访问谷歌使用下面的克隆，应该是最新版本
git clone https://gem5.googlesource.com/public/gem5

# 可以访问github使用下面的克隆，应该是最新版本
git clone https://github.com/gem5/gem5.git

# 不能访问上面两种，克隆我本人的公开仓库，版本是22.0
git clone https://gitee.com/failurejack/gem5.git
```

### 编译源码

terminal 进入刚刚克隆的 gem5 目录，执行下面命令进行编译：

```bash
python3 `which scons` build/ARM/gem5.opt **-j9**
```

解释一下上面的命令：

- `ARM` 代表编译的模拟器的指令集是 arm 指令集，如果要编译 x86 指令集，只需要将 ARM 换成 X86，注意大写。
- `-j9` 代表编译使用的 CPU 数量为 9，具体的原理我也不太清楚，推荐编译使用的线程数是 CPU 核心数 +1，比如我的 CPU 是 4 核，那就写为 `-j5`，如果内存不够用，适当调小。

### 检验是否成功

在 gem5 目录中使用 se.py 中的 hello world 测试，控制台打印出 `Hello world!` 字样证明编译成功：

```bash
build/**ARM**/gem5.opt configs/example/se.py -c tests/test-progs/hello/bin/**arm**/linux/hello
```

### 问题：Python 报错

编译 gem5 的时候可能出现以下报错：

> Embedded python library 3.6 or newer required
> Checking for linker -Wl,–as-needed support… yes
> Checking for compiler -Wno-free-nonheap-object support… yes
> Checking for compiler -gz support… yes
> Checking for linker -gz support… yes
> Info: Using Python config: python-config
> Checking for C header file Python.h… yes
> Checking Python version… 2.7.18
> Error: Embedded python library 3.6 or newer required, found 2.7.18.

这里出现问题的可能一方面是版本问题；另一方面可能是 Python 的默认解释器还是 Python2。

版本问题其实就是 Python 和 SCons 的版本不匹配，按照官方建议的 gem5 版本和 Ubuntu 版本搭配，使用 apt-get 安装的 Python 和 SCons 的版本是匹配的。反过来说不匹配可以在输出中检查并更新（源码编译，添加源都可以）。

如果本身版本是匹配的，但是仍然编译报错，那就可能是

这个问题在我初次编译 gem5 的时候遇到过，尽管 Python 的版本都是对的，还是报错，那可能是 Python 的默认解释器还是 Python2，需要手动设置软连接：

```bash
cd /usr/bin/
sudo rm python
sudo ln -s  python3 python
```

**值得注意的是**，上述问题在本人第一次编译 gem5 的时候出现过，那时使用的就是 python 的命令，后来使用 python3 的命令编译后，在新的环境中也没有出现过问题。

### 问题：内存不足

较新版本的 gem5 编译非常占用内存空间，老一些的版本，如大约 2017 年的版本编译需要的内存开销明显较小。最新的 20.0+ 版本需要至少 8GB 以上的内存。

X86 和 ARM 两个指令集的 gem5 我都编译测试过，在 Ubuntu2004LTS 桌面版中，X86 的编译明显比 ARM 更快而且更节省内存，我在编译 X86 时内存够用，而在编译 ARM 内存不够（8GB 内存），调小 CPU 数也不够，就需要[创建 SWAP 分区](https://blog.csdn.net/u011897411/article/details/89742008)。创建分区时可能会遇到各种各样的错误 ，可以自行百度解决（这个网上资源非常多）。可以使用下面的命令：

```bash
# 从分区/dev/zero向目录/swapfile写入bs*count个字节的空间
sudo dd if=/dev/zero of=/swapfile bs=1G count=6
# 把刚才空间格式化成swap格式
sudo mkswap /swapfile
# 挂载分区  
sudo swapon /swapfile
```

如果上面的第一条命令报错：

> dd: failed to open '/swapfile': Text file busy

则执行 `sudo swapoff -a` 即可正常运行。

编译结束后如果硬盘吃紧可以删除该 swap 分区：

```bash
# 卸载分区
sudo swapoff /swapfile
#删除swap文件，减少空间占用
sudo rm /swapfile
```

## gem5 FS 模式搭建

gem5 的 FS 模式需要完全模拟操作系统，因此需要许多组件，基本的组件如下：

| 需要组件         | 作用 | 备注                                                            |
| ---------------- | ---- | --------------------------------------------------------------- |
| kernel           |      |                                                                 |
| img              |      |                                                                 |
| bootloader       |      |                                                                 |
| device tree blob |      | 在 20.0+ 的 gem5 版本中，默认能生成，不需要提供，除非有特殊需求 |

### 预构建组件

对于搭建 ARM 体系的 gem5 全系统模式，并不必要自行创建 kernel 和 disk，直接下载官方预编译的组件即可：

[gem5: Guest Binaries](https://www.gem5.org/documentation/general_docs/fullsystem/guest_binaries)

后缀中带有 img 的文件一般就是 disk 镜像，其他的则是预编译好的 kernel 和 bootloader 文件（其中有的包含 img）。

<p align="center"><img src="/img/gem5 基本部署/SHeabMBbXowsJVxYiAAc2unwnVg.png" ></p>

目前官网上所有预编译文件下载连接如下：

```bash
# kernel文件（可能包含img）
wget [http://dist.gem5.org/dist/v22-0/arm/aarch-system-20220707.tar.bz2](http://dist.gem5.org/dist/v22-0/arm/aarch-system-20220707.tar.bz2)
wget [http://dist.gem5.org/dist/current/arm/aarch-system-20170616.tar.xz](http://dist.gem5.org/dist/current/arm/aarch-system-20170616.tar.xz)
wget [http://dist.gem5.org/dist/current/arm/aarch-system-20180409.tar.xz](http://dist.gem5.org/dist/current/arm/aarch-system-20180409.tar.xz)
wget [http://dist.gem5.org/dist/current/arm/arm-system-dacapo-2011-08.tgz](http://dist.gem5.org/dist/current/arm/arm-system-dacapo-2011-08.tgz)
wget [http://dist.gem5.org/dist/current/arm/arm-system.tar.bz2](http://dist.gem5.org/dist/current/arm/arm-system.tar.bz2)
wget [http://dist.gem5.org/dist/current/arm/arm64-system-02-2014.tgz](http://dist.gem5.org/dist/current/arm/arm64-system-02-2014.tgz)
wget [http://dist.gem5.org/dist/current/arm/kitkat-overlay.tar.bz2](http://dist.gem5.org/dist/current/arm/kitkat-overlay.tar.bz2)
wget [http://dist.gem5.org/dist/current/arm/linux-arm-arch.tar.bz2](http://dist.gem5.org/dist/current/arm/linux-arm-arch.tar.bz2)
wget [http://dist.gem5.org/dist/current/arm/vmlinux-emm-pcie-3.3.tar.bz2](http://dist.gem5.org/dist/current/arm/vmlinux-emm-pcie-3.3.tar.bz2)
wget [http://dist.gem5.org/dist/current/arm/vmlinux.arm.smp.fb.3.2.tar.gz](http://dist.gem5.org/dist/current/arm/vmlinux.arm.smp.fb.3.2.tar.gz)

# img文件
wget [http://dist.gem5.org/dist/v22-0/arm/disks/ubuntu-18.04-arm64-docker.img.bz2](http://dist.gem5.org/dist/v22-0/arm/disks/ubuntu-18.04-arm64-docker.img.bz2)
wget [http://dist.gem5.org/dist/v22-0/arm/disks/aarch32-ubuntu-natty-headless.img.bz2](http://dist.gem5.org/dist/v22-0/arm/disks/aarch32-ubuntu-natty-headless.img.bz2)
wget [http://dist.gem5.org/dist/current/arm/disks/aarch64-ubuntu-trusty-headless.img.bz2](http://dist.gem5.org/dist/current/arm/disks/aarch64-ubuntu-trusty-headless.img.bz2)
wget [http://dist.gem5.org/dist/current/arm/disks/linaro-minimal-aarch64.img.bz2](http://dist.gem5.org/dist/current/arm/disks/linaro-minimal-aarch64.img.bz2)
wget [http://dist.gem5.org/dist/current/arm/disks/linux-aarch32-ael.img.bz2](http://dist.gem5.org/dist/current/arm/disks/linux-aarch32-ael.img.bz2)
```

值得一提的是最新的预编译文件中并不包含 dtb 文件，原因是官方不建议手动指定因为 gem5 20.0+ 版本能够自动生成，当然这个生成有一定的约束（VExpress_EMM 类型无法生成）。

下载最新的 kernel 和 bootloader 文件使用如下命令：

```bash
# 下载至当前目录（fullsystem）
wget [http://dist.gem5.org/dist/v22-0/arm/aarch-system-20220707.tar.bz2](http://dist.gem5.org/dist/v22-0/arm/aarch-system-20220707.tar.bz2)
# 解压至当前目录（包含两个文件夹binaries和disks）
tar jxvf aarch-system-20220707.tar.bz2
```

下载最新的 disk 镜像使用如下命令：

```bash
# 下载至当前目录（fullsystem）
wget [http://dist.gem5.org/dist/v22-0/arm/disks/ubuntu-18.04-arm64-docker.img.bz2](http://dist.gem5.org/dist/v22-0/arm/disks/ubuntu-18.04-arm64-docker.img.bz2)
# 解压至当前目录**并会删除原压缩文件**
bzip2 -d ubuntu-18.04-arm64-docker.img.bz2
```

值得注意的是选择镜像时，要考虑目标应用对操作系统的要求，在该下载页面，有许多 disk 中 Ubuntu 的版本是 14，如 **aarch64-ubuntu-trusty-headless.img.bz2**，这个我目前只能在进入了全系统模拟后从 terminal 中的输出看到。

### 自构建组件

### fs.py 常用参数

**详细参见文件 configs/common/Option.py**

#### Debug-flag

```cpp
$GEM5/build/ARM/**gem5.opt** **--debug-flags=PIM** $GEM5/configs/example/**fs.py** ...
```

[https://blog.csdn.net/qq_43381135/article/details/104433150](https://blog.csdn.net/qq_43381135/article/details/104433150)

### 简单全系统测试

建议[编写简单的 sh 脚本](https://www.cnblogs.com/carle-09/p/12582209.html)进行全系统运行，每次 terminal 打比较麻烦。

```bash
# 进入GEM5目录
vim fs.sh
```

输入 `i` 进入 INSERT 模式，粘贴下列命令：

```bash
#!/bin/bash
GEM5=~/GEM5/gem5
FS=~/GEM5/fullsystem
$GEM5/build/ARM/gem5.opt $GEM5/configs/example/fs.py --kernel $FS/binaries/vmlinux.arm64 --disk $FS/img/ubuntu-18.04-arm64-docker.img --bootloader $FS/binaries/boot.arm64 --mem-size=4096MB --num-cpus=4
```

按 `ESC` 退出 INSERT 模式，输入 `:wq` 写入磁盘保存

```bash
# 继续在当前目录下赋予执行权限
chmod +x fs.sh
# 运行全系统模式
./fs.sh
```

与此同时，新建一个 terminal 来连接本地全系统的控制台

```bash
telnet localhost 3456
```

如果机器允许使用 `make install` 命令安装软件，则进入到 gem5 的目录下输入如下命令：

```bash
# 进入gem5目录
cd ~/GEM/gem5/util/term
make
make install

# 使用m5term连接
m5term localhost 3456
```

#### 环境变量

我看网上许多教程都使用了环境变量 M5_PATH，以及官网也提了一下，应该是方便书写 shell 命令。指定 M5_PATH 的路径，系统会自动从此路径寻找相应的内核和镜像文件（从 binaries 找 kenerl，从 disk 找 img）。但是我个人觉得没有必要，写 sh 脚本时将 kernel 和 img 的绝对路径设置好就可以直接运行，也更加灵活。下面的环境变量方法仅供参考（没有试过）：

打开本人主机下的 `.bashrc` 文件，我的主机名叫 zkyh，不同的机器名称不一样

```bash
vi /home/zkyh/.bashrc
```

在最后一行添加 fullsystem 的路径：

```bash
export M5_PATH=$M5_PATH:/usr/fs-image
```

使环境变量生效：

```bash
source /home/zkyh/.bashrc
```

### 对 img 进行基本设置

#### 挂/卸载镜像

更改 img 中的文件需要使用 `mount` 命令使得 Host 机以访问文件夹的方式访问 img 系统文件。

GEM5 目录下创建脚本 mount.sh：

```bash
#!/bin/bash
GEM5=~/GEM5/gem5
MNT=~/GEM5/mnt
FS=~/GEM5/fullsystem
sudo $GEM5/util/gem5img.py mount $FS/img/ubuntu-18.04-arm64-docker.img $MNT
```

在进入全系统模式之前需要将镜像 `umount`，同目录下建立脚本 umount.sh：

```bash
#!/bin/bash
MNT=~/GEM5/mnt
sudo umount $MNT
```

执行 umount.sh 脚本，如果出现 `umount target is busy` 的问题，证明有进程占用了该分区，需要杀掉该进程。

目前杀掉进程主要有[两种方法](https://www.laobuluo.com/8258.html)，分别是使用 `lsof` 命令和 `fuser` 命令（虚拟机等很简单，重启就行），然而 `lsof` 命令我并没有在服务器上使用成功，有复杂的权限问题，而 `fuser` 命令（如果没有该命令需要安装包 `psmisc`）使用成功：

```bash
sudo fuser -km /home/zkyh/GEM5/mnt
```

#### 扩容

扩容有时非常必要，对于已经建立好的 img，因为种种原因空间不够用，需要进行扩容。

本节主要是对于镜像 **ubuntu-18.04-arm64-docker.img** 扩容，因其本身不装有任何软件，预留的空间又较小（1.8G），简单编译几个 workload 就占满了，扩容比较必要。

##### 图形化界面方式

先安装 gparted 工具：

```bash
# 先要安装分区软件（磁盘管理）
sudo apt-get install gparted
```

开始扩展：

```bash
# 向当前目录下的img写入1GB的空白空间
sudo dd if=/dev/zero bs=1M count=1024 >> ./ubuntu-18.04-arm64-docker.img
# 挂载img到分区
sudo udisksctl loop-setup -f ./ubuntu-18.04-arm64-docker.img
```

注意，`/dev/zero` 文件是一个特殊的字符设备文件，当我们使用或者读取它的时候，它会提供无限连续不断的空数据流（特殊的数据格式流）

挂载结果如下，知道挂载到了分区/dev/loop14

> Mapped file ./ubuntu-18.04-arm64-docker.img as /dev/loop14.

使用 gparted 管理该分区，并最后卸载分区：

```bash
# 用gparted把空闲空间加到image的sda1上，在图形化界面使用resize拉满即可
sudo gparted /dev/loop14
# 卸载该分区
sudo udisksctl loop-delete -b /dev/loop14
```

Gparted 的图形化界面如下所示：

##### 命令行方式

命令行的方式与图形化有些许不同，需要用到工具 `parted` 和 `resize2fs`（一般系统都默认安装）。

首先跟图形化安装类似，追加空白空间；其次对 `img` 使用 `parted` 工具管理：

```bash
# 向当前目录下的img写入1GB的空白空间
sudo dd if=/dev/zero bs=1M count=1024 >> ./ubuntu-18.04-arm64-docker.img
# 使用parted工具管理img
sudo parted ./ubuntu-18.04-arm64-docker.img
```

进入 `parted` 命令界面，进行分区表的扩容：

```bash
# 打印一下img的分区情况
(parted) print
# 控制台输出如下所示：
# GNU Parted 3.3
# Using /home/zkyh/GEM5/fullsystem/img/ubuntu-18.04-arm64-docker.img
# Welcome to GNU Parted! Type 'help' to view a list of commands.
# (parted) print                                                            
# Model:  (file)
# Disk /home/zkyh/GEM5/fullsystem/img/ubuntu-18.04-arm64-docker.img: 5221MB
# Sector size (logical/physical): 512B/512B
# Partition Table: msdos
# Disk Flags: 
# 
# Number  Start   End     Size    Type     File system  Flags
#  1      65.5kB  5221MB  5221MB  primary  ext4
# 对1号分区重新分配空间，使得其占满未使用的空间
(parted) resizepart 1 100%
# 重新打印一下img的分区情况确认
(parted) print
# 退出
(parted) quit
```

再进入目录 `~/GEM5` 下，进行扩容：

```bash
# 调用之前写好的脚本将img挂载
mount.sh
# 查看本机分区情况，找到img被挂载的分区
df -h
# 控制台打印如下：
# Filesystem      Size  Used Avail Use% Mounted on
# udev            184G     0  184G   0% /dev
# tmpfs            37G  3.0M   37G   1% /run
# ...
# /dev/loop17     4.8G  1.5G  3.1G  32% /home/zkyh/GEM5/mnt
# 对该/dev/loop17分区进行扩容
sudo resize2fs /dev/loop17
# 重新查看分区情况以确认
df -h
# 调用之前写好的脚本卸载img，结束扩容
umount.sh
```

#### 安装软件

对于预构建或者自行创建的 img 来说，文件系统中安装的包非常少，特别是上述使用的 ubuntu-18.04-arm64-docker 镜像，里面没有安装任何软件，连基本的 gcc 和 make 都没有，需要使用者自行安装。最好使用 chroot 的方式安装软件，不推荐在全系统模式下进行软件的安装，因为这会非常慢。

GEM5 目录下建立 app-install.sh 文件：

```bash
#!/bin/bash
MNT=~/GEM5/mnt
sudo /bin/mount -o bind /sys $MNT/sys
sudo /bin/mount -o bind /dev $MNT/dev
sudo /bin/mount -o bind /proc $MNT/proc
# 连接网络需要，域名解析
sudo cp /etc/resolv.conf $MNT/etc/
```

进入目录~/GEM5/mnt 当中，执行以下命令：

```bash
sudo chroot .
```

在 x86 的 Host 机下对 arm 架构的文件系统进行 `chroot` 命令，大概率会出现以下错误：

> chroot: failed to run command ‘/bin/bash’: Exec format error

**大概率**是 Host 机和 img 的架构不兼容，要么是 arm 和 x86 不兼容，要么就是 32 位和 64 位不兼容，32 位和 64 位不兼容好解决，下载位数对应的 img 即可，而 arm 和 x86 的不兼容需要进行一定设置。

比如使用 x86Host 机，arm64 架构的 img，需要安装 qemu-user-static，这是 QEMU 用户模式下的 arm 仿真器。通过 qemu-arm-static，可以在 x86 的 Host 机上模拟 arm 处理器，就像运行在 arm 上一样进行各种操作。

安装该软件，并将 **qemu-aarch64-static** 文件复制到 img 中：

```bash
sudo apt-get install qemu-user-static
# 64位执行下面命令
sudo cp /usr/bin/qemu-aarch64-static ~/GEM5/mnt/usr/bin
# 32位执行下面的命令
# sudo cp /usr/bin/qemu-arm-static ~/GEM5/mnt/usr/bin
```

现在可以正常 chroot。

完成 chroot 命令后进入到 img 的根目录中，需要对软件源做一些基本配置：

```bash
apt-get update
# 安装一些非常基本的命令，比如下面将要用到的add-apt-repository
apt-get install software-properties-common
add-apt-repository universe
apt-get update
```

在此基础上设置更新软件源并安装一些常用软件：

```bash
add-apt-repository ppa:ubuntu-toolchain-r/test
apt-get update
apt-get install gcc-9 g++-9 make wget git vim --fix-missing
```

上面在添加源的时候，可能会遇到添加失败的情况：

> ERROR: user or team does not exist

一般是证书出了问题，需要[重新安装](https://blog.csdn.net/leviopku/article/details/101060133)。

默认安装的 gcc 版本是 7，这里需要使用 gcc-9 才能安装 9 以上的版本，但是此操作会在环境变量中添加 gcc-9/g++-9 的命令而不是 gcc/g++ 本身，需要建立动态链接：

```bash
cd /usr/bin
# 如果之前安装了gcc/g++，要先删除
# rm gcc g++
# 建立动态链接，将gcc9/g++9链接至gcc/g++
ln -s gcc-9 gcc
ln -s g++-9 g++
```

安装完毕退出 chroot，umount 镜像。

修改 umount.sh 方便后面的执行：

```bash
#!/bin/bash
MNT=~/GEM5/mnt
sudo umount $MNT/proc
sudo umount $MNT/dev
sudo umount $MNT/sys
sudo umount $MNT
```

执行下列命令：

```bash
exit
./umount.sh
```

#### 配置代理

配置代理和普通 Ubuntu 配置类似，注意要安装 curl 工具（同时保证基本的联网），以及良好的开关 proxy 和服务的习惯

```bash
apt-get install curl --fix-missing
```

### CheckPoint
