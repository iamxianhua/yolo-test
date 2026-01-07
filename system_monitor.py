#!/usr/bin/env python3
"""
系统监控脚本 - System Monitor Script
实时监控 CPU、内存、磁盘、网络等系统资源
"""

import psutil
import time
import os
import platform
from datetime import datetime


class SystemMonitor:
    """系统监控类"""

    def __init__(self):
        self.hostname = platform.node()
        self.system = platform.system()
        self.release = platform.release()

    def get_system_info(self):
        """获取系统基本信息"""
        print("=" * 60)
        print(f"系统监控 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print(f"主机名: {self.hostname}")
        print(f"系统: {self.system} {self.release}")
        print(f"处理器: {platform.processor()}")
        print("=" * 60)

    def get_cpu_info(self):
        """获取 CPU 信息"""
        print("\n[CPU 信息]")
        cpu_percent = psutil.cpu_percent(interval=1, percpu=False)
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()

        print(f"  物理核心数: {cpu_count}")
        print(f"  逻辑核心数: {cpu_count_logical}")
        print(f"  CPU 使用率: {cpu_percent}%")
        if cpu_freq:
            print(f"  CPU 频率: {cpu_freq.current:.2f} MHz")

        # 每个核心的使用率
        per_cpu = psutil.cpu_percent(interval=1, percpu=True)
        for i, percentage in enumerate(per_cpu):
            bar = self._get_progress_bar(percentage, 20)
            print(f"  核心 {i}: {bar} {percentage}%")

    def get_memory_info(self):
        """获取内存信息"""
        print("\n[内存信息]")
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()

        print(f"  总内存: {self._bytes_to_gb(mem.total):.2f} GB")
        print(f"  已使用: {self._bytes_to_gb(mem.used):.2f} GB ({mem.percent}%)")
        print(f"  可用: {self._bytes_to_gb(mem.available):.2f} GB")
        print(f"  {self._get_progress_bar(mem.percent, 30)}")

        print(f"\n  交换内存总量: {self._bytes_to_gb(swap.total):.2f} GB")
        print(f"  交换内存已使用: {self._bytes_to_gb(swap.used):.2f} GB ({swap.percent}%)")

    def get_disk_info(self):
        """获取磁盘信息"""
        print("\n[磁盘信息]")
        partitions = psutil.disk_partitions()

        for partition in partitions:
            print(f"\n  设备: {partition.device}")
            print(f"  挂载点: {partition.mountpoint}")
            print(f"  文件系统: {partition.fstype}")

            try:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"  总容量: {self._bytes_to_gb(usage.total):.2f} GB")
                print(f"  已使用: {self._bytes_to_gb(usage.used):.2f} GB ({usage.percent}%)")
                print(f"  可用: {self._bytes_to_gb(usage.free):.2f} GB")
                print(f"  {self._get_progress_bar(usage.percent, 30)}")
            except PermissionError:
                print(f"  无权限访问")

    def get_network_info(self):
        """获取网络信息"""
        print("\n[网络信息]")
        net_io = psutil.net_io_counters()

        print(f"  发送数据: {self._bytes_to_gb(net_io.bytes_sent):.2f} GB")
        print(f"  接收数据: {self._bytes_to_gb(net_io.bytes_recv):.2f} GB")
        print(f"  发送包数: {net_io.packets_sent:,}")
        print(f"  接收包数: {net_io.packets_recv:,}")

        # 网络接口信息
        print("\n  网络接口:")
        addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in addrs.items():
            print(f"\n    接口: {interface_name}")
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    print(f"      IP 地址: {address.address}")
                    print(f"      子网掩码: {address.netmask}")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    print(f"      MAC 地址: {address.address}")

    def get_process_info(self, top_n=5):
        """获取进程信息"""
        print(f"\n[进程信息 - 前 {top_n} 个 CPU 占用]")
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        # 按 CPU 使用率排序
        processes = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)

        print(f"  {'PID':<8} {'进程名':<25} {'CPU %':<10} {'内存 %':<10}")
        print("  " + "-" * 55)
        for proc in processes[:top_n]:
            pid = proc['pid']
            name = proc['name'][:24]
            cpu = proc['cpu_percent'] or 0
            mem = proc['memory_percent'] or 0
            print(f"  {pid:<8} {name:<25} {cpu:<10.1f} {mem:<10.1f}")

    def get_system_uptime(self):
        """获取系统运行时间"""
        print("\n[系统运行时间]")
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_str = self._seconds_to_dhms(uptime_seconds)

        boot_datetime = datetime.fromtimestamp(boot_time)
        print(f"  启动时间: {boot_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  运行时长: {uptime_str}")

    def monitor_continuous(self, interval=5):
        """持续监控模式"""
        print("\n持续监控模式 (按 Ctrl+C 退出)")
        print(f"刷新间隔: {interval} 秒\n")

        try:
            while True:
                os.system('clear' if os.name == 'posix' else 'cls')
                self.display_all()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n监控已停止")

    def display_all(self):
        """显示所有监控信息"""
        self.get_system_info()
        self.get_cpu_info()
        self.get_memory_info()
        self.get_disk_info()
        self.get_network_info()
        self.get_process_info()
        self.get_system_uptime()

    def save_to_log(self, filename="system_monitor.log"):
        """保存监控信息到日志文件"""
        import sys
        from io import StringIO

        # 重定向输出到字符串
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        self.display_all()

        # 获取输出内容
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        # 写入文件
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(output)
            f.write("\n" + "=" * 60 + "\n\n")

        print(f"监控信息已保存到: {filename}")

    # 辅助方法
    def _bytes_to_gb(self, bytes_value):
        """字节转 GB"""
        return bytes_value / (1024 ** 3)

    def _get_progress_bar(self, percentage, length=20):
        """生成进度条"""
        filled = int(length * percentage / 100)
        bar = '█' * filled + '░' * (length - filled)
        return f"[{bar}]"

    def _seconds_to_dhms(self, seconds):
        """秒转换为天时分秒"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        parts = []
        if days > 0:
            parts.append(f"{days}天")
        if hours > 0:
            parts.append(f"{hours}小时")
        if minutes > 0:
            parts.append(f"{minutes}分钟")
        parts.append(f"{secs}秒")

        return " ".join(parts)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='系统监控脚本')
    parser.add_argument('-c', '--continuous', action='store_true',
                       help='持续监控模式')
    parser.add_argument('-i', '--interval', type=int, default=5,
                       help='持续监控的刷新间隔（秒），默认 5 秒')
    parser.add_argument('-l', '--log', type=str,
                       help='保存监控信息到日志文件')
    parser.add_argument('-s', '--simple', action='store_true',
                       help='简化输出（仅显示关键信息）')

    args = parser.parse_args()

    monitor = SystemMonitor()

    if args.continuous:
        monitor.monitor_continuous(args.interval)
    elif args.log:
        monitor.save_to_log(args.log)
    elif args.simple:
        monitor.get_system_info()
        monitor.get_cpu_info()
        monitor.get_memory_info()
    else:
        monitor.display_all()


if __name__ == "__main__":
    main()
