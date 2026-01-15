import os
import scipy.io
import numpy as np
from typing import Any, Dict, Optional

try:
    import h5py
except ImportError:
    h5py = None

def load_mat_file(file_path: str) -> Dict[str, Any]:
    """負責載入 .mat 檔案，自動切換 v7.3 與舊版格式。"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"找不到路徑: {file_path}")

    try:
        return scipy.io.loadmat(file_path, simplify_cells=True)
    except NotImplementedError:
        if h5py is None:
            raise ImportError("偵測到 v7.3 格式，但環境尚未安裝 'h5py'。")
        with h5py.File(file_path, 'r') as f:
            return _h5_to_dict(f)

def _h5_to_dict(h5_obj: Any) -> Dict[str, Any]:
    """將 HDF5 物件轉換為字典 (Recursive Functional Style)"""
    data = {}
    for key, item in h5_obj.items():
        if isinstance(item, h5py.Group):
            data[key] = _h5_to_dict(item)
        elif isinstance(item, h5py.Dataset):
            val = item[()]
            data[key] = val.T if isinstance(val, np.ndarray) and val.ndim > 1 else val
    return data

def preview_data(data: Any, rows: int = 10, cols: int = 10):
    """印出矩陣的前 rows * cols 內容"""
    if not isinstance(data, np.ndarray) or data.size == 0:
        return
    r, c = min(data.shape[0], rows), (min(data.shape[1], cols) if data.ndim > 1 else 1)
    print(f"   [Data Preview {r}x{c}]:")
    sub_matrix = data[:r] if data.ndim == 1 else data[:r, :c]
    print(np.array2string(sub_matrix, precision=4, separator=', '))

def inspect_structure(data: Any, name: str = "Root", indent: int = 0):
    """遞迴解析所有資訊"""
    spacing = "  " * indent
    if isinstance(data, (str, int, float, np.number)):
        print(f"{spacing}* {name} ({type(data).__name__}): {data}")
    elif isinstance(data, np.ndarray):
        print(f"{spacing}* {name} ({type(data).__name__}) | Shape: {data.shape}")
        if np.issubdtype(data.dtype, np.number):
            preview_data(data)
    elif isinstance(data, dict):
        print(f"{spacing}+ {name} (Directory/Struct)")
        for key, val in data.items():
            inspect_structure(val, key, indent + 1)
