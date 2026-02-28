#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统信息获取工具

该模块提供了一系列函数，用于获取计算机系统的各种硬件和软件信息。
功能包括：
- 获取操作系统版本信息
- 获取CPU型号信息
- 获取NVIDIA显卡及显存信息
- 获取内存使用情况和占用内存最多的进程信息
- 特别关注Chrome浏览器的内存使用情况
"""

import platform
import psutil
import subprocess
import pynvml

# 1、获取当前操作系统版本
def get_operating_system_version():
    try:
        os_version = platform.platform()
    except Exception:
        os_version = '获取失败'
    print(f'1、操作系统：{os_version} \n')


# 2、获取CPU型号
def get_cpu_info():
    cpu_name = '获取失败'
    result = subprocess.run(['wmic', 'cpu', 'get', 'Name'], stdout=subprocess.PIPE, text=True)
    output = result.stdout
    lines = output.split('\n')
    for line in lines:
        if line.strip() and not line.startswith('Name'):
            cpu_name = line.strip()
    print(f'2、CPU型号：{cpu_name} \n')


# 3、获取当前显卡及显存大小
def get_gpu_memory_info():
    try:
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
    except:
        print("无法初始化 NVIDIA 驱动，请检查是否安装了 GPU 和 NVIDIA 驱动")
        return
    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        name = pynvml.nvmlDeviceGetName(handle)
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        print(f"3、显卡型号: {name}")
        print(f"   总显存: {mem_info.total / 1024**3:.2f} GB  已用显存: {mem_info.used / 1024**3:.2f} GB  可用显存: {mem_info.free / 1024**3:.2f} GB\n")


# 4、获取当前运行内存大小及占用前10
def get_running_memory_info():
    memory_info = psutil.virtual_memory()
    total_memory = f"{memory_info.total / (1024 ** 3):.2f} GB"
    used_memory = f"{memory_info.used / (1024 ** 3):.2f} GB"
    available_memory = f"{memory_info.available / (1024 ** 3):.2f} GB"
    print(f'4、内存大小：{total_memory}  已用内存：{used_memory}  可用内存：{available_memory}')

    # 只收集Chrome相关内存数据
    google_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            proc_name = proc.info['name']
            proc_info = proc.info['memory_info']
            if proc_name == "chrome.exe":
                google_processes.append((proc.info['pid'], proc.info['name'], proc_info.rss))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # 获取google chrome占用总内存及子进程排序
    google_memory_usage = 0
    google_processes.sort(key=lambda x: x[2], reverse=True)
    for i, (pid, name, rss) in enumerate(google_processes, 1):
        mem_gb = rss / (1024 ** 3)
        google_memory_usage += mem_gb
        print(f"   PID: {pid}  进程名: {name} 内存使用: {mem_gb:.2f} GB")
    print(f"   Google Chrome 累计内存使用：{google_memory_usage:.2f} GB")

    # 收集所有进程的内存信息
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            mem_info = proc.info['memory_info']
            if mem_info:
                processes.append((proc.info['pid'], proc.info['name'], mem_info.rss))  # 进程id、进程名称、进程占用
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    # 按内存占用排序并取前10
    processes.sort(key=lambda x: x[2], reverse=True)
    top_processes = processes[:5]

    for i, (pid, name, rss) in enumerate(top_processes, 1):
        mem_gb = rss / (1024 ** 3)
        print(f"   PID: {pid}  进程名: {name} 内存使用: {mem_gb:.2f} GB")


if __name__ == "__main__":
    print('='*80)
    get_operating_system_version()  # 获取操作系统版本
    get_cpu_info()  # 获取CPU信息
    get_gpu_memory_info()  # 获取GPU信息
    get_running_memory_info()  # 获取内存信息
    print('='*80 + '\n')
    input("按回车键退出...")