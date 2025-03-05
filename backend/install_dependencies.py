#!/usr/bin/env python
"""
安装所需的依赖包
"""

import subprocess
import sys

def install_dependencies():
    """安装所需的依赖包"""
    dependencies = [
        "pydantic-settings",  # 用于 BaseSettings
    ]
    
    print("正在安装依赖包...")
    for dep in dependencies:
        print(f"安装 {dep}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
    
    print("依赖包安装完成！")

if __name__ == "__main__":
    install_dependencies() 