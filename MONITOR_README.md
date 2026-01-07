# 系统监控脚本使用指南

## 功能特性

✅ **实时监控系统资源**
- CPU 使用率（总体 + 每个核心）
- 内存使用情况（物理内存 + 交换内存）
- 磁盘空间使用
- 网络流量统计
- 进程信息（CPU/内存占用 Top N）
- 系统运行时间

✅ **多种运行模式**
- 单次快照
- 持续监控
- 简化输出
- 日志记录

✅ **可视化显示**
- 进度条显示使用率
- 彩色输出（终端支持）
- 清晰的分类信息

---

## 安装依赖

```bash
pip3 install psutil
```

---

## 使用方法

### 1. 完整监控（单次）
显示所有系统信息：
```bash
python3 system_monitor.py
```

### 2. 简化输出
仅显示关键信息（CPU、内存）：
```bash
python3 system_monitor.py -s
# 或
python3 system_monitor.py --simple
```

### 3. 持续监控模式
每隔 5 秒自动刷新（按 Ctrl+C 退出）：
```bash
python3 system_monitor.py -c
# 或
python3 system_monitor.py --continuous
```

自定义刷新间隔（例如每 10 秒）：
```bash
python3 system_monitor.py -c -i 10
# 或
python3 system_monitor.py --continuous --interval 10
```

### 4. 保存到日志文件
将监控信息保存到文件：
```bash
python3 system_monitor.py -l system_log.txt
# 或
python3 system_monitor.py --log system_log.txt
```

### 5. 组合使用
持续监控并每次保存到日志（需要自定义脚本逻辑）：
```bash
# 示例：每 60 秒记录一次
watch -n 60 "python3 system_monitor.py -l monitor_$(date +\%Y\%m\%d_\%H\%M\%S).log"
```

---

## 输出示例

```
============================================================
系统监控 - 2026-01-07 05:53:34
============================================================
主机名: runsc
系统: Linux 4.4.0
处理器: x86_64
============================================================

[CPU 信息]
  物理核心数: 16
  逻辑核心数: 16
  CPU 使用率: 15.3%
  CPU 频率: 2600.00 MHz
  核心 0: [███░░░░░░░░░░░░░░░░░] 15.0%
  核心 1: [████░░░░░░░░░░░░░░░░] 20.5%
  ...

[内存信息]
  总内存: 21.00 GB
  已使用: 8.45 GB (40.2%)
  可用: 12.55 GB
  [████████████░░░░░░░░░░░░░░░░░░]

[磁盘信息]
  设备: /dev/sda1
  挂载点: /
  文件系统: ext4
  总容量: 500.00 GB
  已使用: 125.30 GB (25.1%)
  可用: 374.70 GB
  [███████░░░░░░░░░░░░░░░░░░░░░░]

[网络信息]
  发送数据: 2.35 GB
  接收数据: 15.67 GB
  ...

[进程信息 - 前 5 个 CPU 占用]
  PID      进程名                     CPU %      内存 %
  -------------------------------------------------------
  1234     python3                   45.2       5.3
  5678     chrome                    12.8       8.9
  ...

[系统运行时间]
  启动时间: 2026-01-05 08:30:15
  运行时长: 1天 21小时 23分钟 19秒
```

---

## 命令行参数

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| --continuous | -c | 持续监控模式 | `-c` |
| --interval | -i | 刷新间隔（秒） | `-i 10` |
| --log | -l | 保存到日志文件 | `-l output.log` |
| --simple | -s | 简化输出 | `-s` |
| --help | -h | 显示帮助信息 | `-h` |

---

## 实用场景

### 场景 1：性能调试
在运行 YOLO 检测时监控系统资源：
```bash
# 终端 1：运行监控
python3 system_monitor.py -c -i 2

# 终端 2：运行 YOLO 检测
python3 yolo-test.py
```

### 场景 2：服务器巡检
定期记录服务器状态：
```bash
# 添加到 crontab，每小时记录一次
0 * * * * /usr/bin/python3 /path/to/system_monitor.py -l /var/log/system_monitor.log
```

### 场景 3：故障排查
快速查看当前系统状态：
```bash
python3 system_monitor.py -s
```

### 场景 4：长期监控
运行在后台，持续记录：
```bash
nohup python3 system_monitor.py -c -i 300 > monitor_output.log 2>&1 &
```

---

## 监控指标说明

### CPU
- **使用率**：当前 CPU 负载百分比
- **核心数**：物理核心数 vs 逻辑核心数（超线程）
- **频率**：当前运行频率

### 内存
- **总内存**：系统总物理内存
- **已使用**：当前使用的内存
- **可用**：可供分配的内存
- **交换内存**：虚拟内存使用情况

### 磁盘
- **总容量**：分区总大小
- **已使用**：已占用空间
- **可用**：剩余可用空间

### 网络
- **发送/接收数据**：累计流量
- **包数**：网络包统计
- **IP 地址**：网络接口配置

### 进程
- **PID**：进程 ID
- **进程名**：程序名称
- **CPU %**：CPU 占用率
- **内存 %**：内存占用率

---

## 注意事项

⚠️ **权限问题**
- 某些信息可能需要 root 权限
- 使用 `sudo python3 system_monitor.py` 获取完整信息

⚠️ **兼容性**
- 支持 Linux、macOS、Windows
- 某些功能在不同系统上可能有差异

⚠️ **性能影响**
- 监控本身会占用少量系统资源
- 刷新间隔建议 ≥ 2 秒

---

## 扩展功能

如需添加自定义功能，可修改 `SystemMonitor` 类：

```python
# 添加 GPU 监控
def get_gpu_info(self):
    # 使用 GPUtil 或 nvidia-smi
    pass

# 添加告警功能
def check_alerts(self):
    if cpu_usage > 80:
        send_alert("CPU 使用率过高")
```

---

## 故障排查

**问题 1：ModuleNotFoundError: No module named 'psutil'**
```bash
pip3 install psutil
```

**问题 2：权限拒绝**
```bash
sudo python3 system_monitor.py
```

**问题 3：中文乱码**
- 确保终端支持 UTF-8 编码
- Linux: `export LANG=zh_CN.UTF-8`

---

## 更新日志

- **v1.0** (2026-01-07)
  - 初始版本
  - 支持 CPU、内存、磁盘、网络、进程监控
  - 多种运行模式
  - 日志记录功能

---

## 许可证

MIT License - 自由使用和修改
