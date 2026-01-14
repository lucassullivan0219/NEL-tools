# filename: mat_tools.py
import scipy.io
import h5py
import numpy as np
import os
from typing import Any, Dict

def load_mat_file(file_path: str) -> Dict[str, Any]:
    """
    負責載入 .mat 檔案，自動判斷是舊版 (scipy) 還是 v7.3 (h5py)。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"找不到檔案: {file_path}")

    try:
        # 嘗試使用 scipy (適用於 v5, v6, v7.2 以前)
        return scipy.io.loadmat(file_path)
    except NotImplementedError:
        print(f"偵測到 v7.3 格式 (HDF5)，切換至 h5py 解析...")
        try:
            with h5py.File(file_path, 'r') as f:
                return _h5_to_dict(f)
        except Exception as e:
            raise RuntimeError(f"無法解析 v7.3 檔案: {e}")
    except Exception as e:
        raise RuntimeError(f"讀取失敗: {e}")

def _h5_to_dict(h5_obj) -> Dict[str, Any]:
    """Helper function: 將 h5py 物件遞迴轉換為 Python dictionary"""
    data = {}
    for key, item in h5_obj.items():
        if isinstance(item, h5py.Group):
            data[key] = _h5_to_dict(item)
        elif isinstance(item, h5py.Dataset):
            data[key] = item[()] 
    return data

def inspect_variable(name: str, value: Any, indent: int = 0):
    """遞迴分析並印出變數的型態、維度與摘要"""
    prefix = "  " * indent
    
    if name in ['__header__', '__version__', '__globals__']:
        # print(f"{prefix}[Metadata] {name}") # Optional: 減少雜訊
        return

    type_name = type(value).__name__
    shape_info = getattr(value, 'shape', 'Scalar')
    
    summary = ""
    if isinstance(value, np.ndarray):
        if value.size < 5:
            summary = f"Values: {value.flatten()}"
        else:
            if np.issubdtype(value.dtype, np.number):
                summary = f"Mean: {np.mean(value):.2f}, Max: {np.max(value):.2f}"
            
    print(f"{prefix}- {name} | Type: {type_name} | Shape: {shape_info} | {summary}")

    if isinstance(value, np.ndarray) and value.dtype.names:
        print(f"{prefix}  [Nested Struct Detected]")
        for field_name in value.dtype.names:
            field_val = value[field_name][0, 0] if value.shape == (1, 1) else value[field_name]
            inspect_variable(field_name, field_val, indent + 1)
            
    elif isinstance(value, dict):
         for sub_key, sub_val in value.items():
             inspect_variable(sub_key, sub_val, indent + 1)

def print_summary(filepath: str):
    """主程序：協調載入與分析流程 (方便快速除錯用)"""
    print(f"--- 開始解析: {filepath} ---")
    try:
        data = load_mat_file(filepath)
        print(f"\n[檔案內容摘要]")
        for key, value in data.items():
            inspect_variable(key, value)
        print("\n--- 解析完成 ---")
    except Exception as e:
        print(f"錯誤: {e}")