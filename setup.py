
from setuptools import setup, find_packages

setup(
    name="nel_tools",                # 套件名稱 (pip install 時顯示的名字)
    version="0.1.0",                 # 版本號
    packages=find_packages(),        # 自動偵測你的 mat_tools 資料夾
    install_requires=[               # 自動安裝依賴套件 (Robustness)
        "numpy",
        "scipy",
        "h5py"
    ],
    author="Lucas Sullivan",         # 你的名字 (可選)
    description="A simple tool for loading .mat files with v7.3 support",
    python_requires='>=3.6',
)
