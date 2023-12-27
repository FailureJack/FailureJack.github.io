---
title: Linux:远程服务器基本配置
cover: /cover/Linux远程服务器基本配置.png
date: 2023-12-27 20:02:14
comments: False
feature: False
abstracts: 这篇文章详细介绍了如何在本地计算机和远程Linux服务器之间进行高效稳定的文件传输，提供了多种方法，如VPN跳板机访问内网服务器、ssh免密登录和文件传输等。同时，文章还解释了如何使用VSCode进行拖拽式文件传输，并建议使用ssh连接的服务器端开发。此外，文章还涉及了其他网络问题的解决方案。
categories: 工程技术
tags:
- 远程服务器
- Markdown
- 文件传输
mathjax: true
---

# 基本配置

## Linux 远程服务器

### 通过跳板机访问内网服务器

本地机器的配置详见下面的文件：

注意**跳板机 IP 地址**和**服务器 IP 地址**不一样，跳板机作用是让本地机器访问内网，因此配置 VPN 这里需要填入**跳板机的 IP 地址**。预共享密钥和密码不是同一个东西，这里我的预共享密钥是 lab505，用户名是 zkyh，密码是 ac3bdf92。密码用于服务器的登录等。

连接上 vpn 后，用终端连接服务器，这里推进 vscode 的 Remote-SSH 插件，接下来也基于该插件讲解。

<p align="center"><img src="/img/Linux远程服务器基本配置/U9Clbkb2loVoI3xkiEmckkvhnTf.png" ></p>

初次连接时，会要求配置 config 文件，在目录 `C:\Users\用户名\.ssh` 下，其内容如下：

<p align="center"><img src="/img/Linux远程服务器基本配置/ROjkb2d54ollymxOrZdcPe6wnZI.png" ></p>

Host 和 HostName 都配置成**服务器的 IP 地址，**User 就是用户名 zkyh。选择服务器系统 linux，配置完后完成连接。

### ssh 免密登录

假设需要使用 Windows 客户机 A 免密登录远程 Linux 服务器 B，其本质就是在 A 上生成 rsa 公私钥对，将公钥添加到服务器 B 上即可。

生成公私钥：

```bash
ssh-keygen -t rsa -C "1536454795@qq.com"
```

与后面 git 内容保持一致，一般用邮箱进行注释，执行命令后需要进行 3 次或 4 次确认：

<p align="center"><img src="/img/Linux远程服务器基本配置/DrFMbQRWToV6MQxAc0rcFOBonXb.png" ></p>

在 B 的~/.ssh/目录下输入命令：

```bash
# ID_RSA.PUB是A上的公钥id_rsa.pub的内容，将该内容追加进文件authorized_keys（没有该文件会新建）
echo "ID_RSA.PUB" >> authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCoJkMyoTQ58Bn9EXzzesPI9GCifSwhoJy+wzsrG7hGqQ1FtdZ/kzxWypO5rbmp7MNb7LP/01bINI/I1n2bF6N6eA0tJglN9i100t21TsmfuWe6X+FyTj7qyLX2rpeAa3O6n+XoklGtMsIZATMx8Jw4LPZYEq46I9l191kt/QSO6eNE3U+KLhvFXAzS/6Ok8ay9Qo4JXTaUjJCocTCMHpZsq1rw8OMowQUAtKyjRMZvHPg5QLyGAypAWWIn6yNH1aiU4OyyOJjOD8u3gg/44dqbFiiV7JT++zM7JwHD4HlkoO0/5D6n8NPI+PMtXcfTDHVjAekj44KaomIoYpG2vqMGUztyI46qQGmJGC/RZTtMDjZMB6l+i1ZlZ4Wck/hIZiiuzHaWnXBZBsNgfxKdOPWQYRx1rtl8awHICvd2XFteFw8xyzHHrH9SqZwSYM5ImuJWLxwPzMKZsVmRvQ50ICKfOYjjHyl60m5PUV8S7d1BzT1uMOPJqPpEHf4PfoA75rU= 1536454795@qq.com"  >> authorized_keys
```

### 文件传输

文件传输有许多方法，如果本地机器有图形化界面，推荐使用 vscode 进行传输，否则还是基于 ssh 加密的两种方法：`scp` 和 `sftp`。本次 terminal 中的命令示例都是基于本地服务器 Windows 和远程服务器为 Linux 的情况，可以从命令中路径的间隔符判别是 Windows 的路径还是 Linux 的路径（Windows 是反斜杠 `\`，Linux 是正斜杠 `/`）。所有 terminal 的命令都是在 Windows 上发起的，因此 Windows 路径都是相对 terminal 工作目录的，而 Linux 则是相对用户目录 `~` 的。

指定远程 Linux 服务器都会使用**< 用户名 >@<IP 地址 >**的形式，本小节遵循该方式。

本小节分大文件和小文件的传输讨论传输手段，由于内网穿透原因，大文件的传输可能不稳定。如何界定大文件和小文件本身是一件模糊的事情，这里经过本人的实验，小于等于 512MB 的文件是可以通过 scp 稳定传输的 ，因此认为是小文件，大于 512MB 的文件传输不稳定，认为是大文件。**注意大文件小文件的界定是根据网络情况来的**，如果没有内网穿透可能不存在传输不稳定问题。

#### 小文件的传输

文件传输建立在上述 **ssh 免密登录**的前提下，使用 scp 命令进行文件的拷贝：

```bash
**scp** -r file zkyh@10.77.110.155:upload/
```

- `file` 代表待上传的文件或文件夹
- `-r` 代表允许传输文件夹
- `zkyh` 代表用户名
- `10.77.110.155` 代表服务器 IP 地址
- `upload` 代表相对于 `~` 的上传位置（目标路径）

相应地，将服务器上的文件（夹）下载至本机即可使用下面的命令：

```bash
**scp** -r zkyh@10.77.110.155:file download\
```

- `file` 代表相对于 `~` 的待下载文件（夹）
- `-r` 代表允许传输文件夹
- `zkyh` 代表用户名
- `10.77.110.155` 代表服务器 IP 地址
- `.\download` 代表下载到本机的目录

#### 大文件的传输

大文件的传输推荐使用 sftp 命令（没有试过 scp，应该也可以），需要先建立 sftp 连接，再使用 put 和 get 方法进行文件的传输：

```bash
# 建立sftp连接
**sftp** zkyh@10.77.110.155
# 使用put上传文件，上传file到Linux的upload目录
**put** -r file upload/
# 使用get下载文件，下载file到Windows的download目录
**get** -r file download\
```

值得注意的是 sftp 是支持断点续传的，因此网络不稳定，出现 broken pipe 的错误也没有问题，只需要重新建立 sftp 连接，使用 reput/reget 命令即可：

```bash
# 建立sftp连接
**sftp** zkyh@10.77.110.155
# 使用reput实现断点续传
**reput** -r file upload/
```

可以看下面的示例：

<p align="center"><img src="/img/Linux远程服务器基本配置/I8OIbvx5koCq6XxNOa1cUoa8n8b.png" ></p>

#### vscode 直接拖拽

直接基于 GUI 的方式将文件（可以是大文件）拖入已经建立 ssh 连接的 vscode 文件导航栏中，vscode 会在后台完成复制。这种方式似乎只能由客户端向服务端上传文件/文件夹，但是连接比较稳定。

#### 文件暂存网站

国内国外有许多提供文件暂存服务的网站，这是一个文件传输的很好的中转站，其对于拥有图形化界面拥有浏览器的 Linux 系统比较方便，但是若没有图形化界面，似乎不可用：因为这些网站的上传下载都是基于 javascript 的，需要自行写请求体。至于能否使用 curl、wget 等下载工具去下载还有待研究。

使用 aria2 进行下载：

### 使用 vscode 进行服务器端开发

除了上述使用 vscode 连接远程服务器，vscode 还可以进行服务器端的开发，只需要在服务器端安装插件即可：

<p align="center"><img src="/img/Linux远程服务器基本配置/OBTqbJQdloelZxxAFuPcdifPnpf.png" ></p>

上述图中的 `LOCAL-INSTALLED` 表示的是本地的插件，可以点击 `Install in SSH：10.77.110.155` 安装到服务器端，这样在下面的 `SSH：10.77.110.155-INSTALLED` 能够显示。

ssh 连接后，vscode 的插件的运算负载就会被放在服务器上而不是本地，甚至 vscode 本身的一些功能，比如左侧栏的全局替换和全局搜索，负责实际去计算的也是服务器。

## 其他网络问题

### 虚拟机“掉网”

有时候虚拟机会在某次开启后，无法连接互联网，这个现象我个人称之为“掉网”，从经验的角度来看，出现了一次“掉网”后频繁发生。原因未明，重新安装虚拟机可能永久解决这一现象，暂时解决可以允许下面的脚本：

```bash
#!/bin/bash
sudo service network-manager stop
sudo cp /var/lib/NetworkManager/NetworkManager.state  /var/lib/NetworkManager/NetworkManager.state.back
sudo rm /var/lib/NetworkManager/NetworkManager.state
sudo service network-manager start
# 如果不能联网就重启一下
reboot
```
