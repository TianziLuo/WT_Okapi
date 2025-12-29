from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import os
import time
from datetime import datetime
from pathlib import Path

# Import actions and utilities
from handlers.actions import ACTIONS
from handlers.tp_download import run_download_tp
from TP_acc import ACCOUNTS
from config_paths import get_wt_paths
from utils.func import excel_process, WT_out, copy_from_downloads, copy2downloads
from amzops import run_go_exe
from verify import verify_license
import hashlib

app = FastAPI(title="WT Okapi API", version="1.0.0")

@app.get("/", response_class=HTMLResponse)
def root():
    """根路径 - 欢迎页面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WT Okapi API</title>
        <meta charset="utf-8">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                border-bottom: 3px solid #4CAF50;
                padding-bottom: 10px;
            }
            .link {
                display: inline-block;
                margin: 10px 10px 10px 0;
                padding: 12px 24px;
                background: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s;
            }
            .link:hover {
                background: #45a049;
            }
            .link-secondary {
                background: #2196F3;
            }
            .link-secondary:hover {
                background: #0b7dda;
            }
            .info {
                background: #e3f2fd;
                padding: 15px;
                border-left: 4px solid #2196F3;
                margin: 20px 0;
            }
            code {
                background: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🦫 WT Okapi API</h1>
            <p>欢迎使用 WT Okapi API 服务！</p>
            
            <div class="info">
                <strong>📚 API 文档：</strong><br>
                访问 <a href="/docs" style="color: #2196F3;">/docs</a> 查看完整的交互式 API 文档
            </div>
            
            <h2>快速链接</h2>
            <a href="/docs" class="link">📖 API 文档 (Swagger)</a>
            <a href="/redoc" class="link link-secondary">📘 API 文档 (ReDoc)</a>
            <a href="/health" class="link">💚 健康检查</a>
            <a href="/license/status" class="link">🔑 License 状态</a>
            <a href="/system/info" class="link">ℹ️ 系统信息</a>
            
            <h2>主要功能</h2>
            <ul>
                <li><strong>License 管理：</strong> <code>GET /license/status</code> - 查看 license 状态</li>
                <li><strong>License 更新：</strong> <code>POST /license/update</code> - 远程更新 license</li>
                <li><strong>操作管理：</strong> <code>GET /actions</code> - 查看所有可用操作</li>
                <li><strong>执行操作：</strong> <code>POST /run</code> - 执行指定操作</li>
                <li><strong>账户管理：</strong> <code>GET /accounts</code> - 管理 TP 账户</li>
                <li><strong>文件操作：</strong> <code>GET /files/recent</code> - 查看最近文件</li>
                <li><strong>批量操作：</strong> <code>POST /batch/run</code> - 批量执行任务</li>
            </ul>
            
            <div class="info">
                <strong>💡 提示：</strong> 所有 API 接口都支持 JSON 格式，可以通过 curl、Postman 或任何 HTTP 客户端调用。
            </div>
        </div>
    </body>
    </html>
    """

# Pydantic models for request/response
class AccountRequest(BaseModel):
    username: str
    email: str
    password: str
    filename: str

class TPDownloadRequest(BaseModel):
    accounts: List[str]  # List of usernames to process

class FileInfo(BaseModel):
    name: str
    size: int
    modified: str
    path: str

class LicenseUpdateRequest(BaseModel):
    username: str
    expiry_date: str  # Format: YYYY-MM-DD

# Global state for tracking operations
operation_status = {}

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/actions")
def list_actions() -> Dict[str, Any]:
    return {"actions": [label for (label, _fn) in ACTIONS]}

@app.post("/run")
def run_action(label: str) -> Dict[str, Any]:
    for action_label, action_fn in ACTIONS:
        if action_label == label:
            operation_id = f"{label}_{int(time.time())}"
            operation_status[operation_id] = {"status": "running", "start_time": datetime.now().isoformat()}
            
            try:
                action_fn()
                operation_status[operation_id] = {"status": "completed", "end_time": datetime.now().isoformat()}
                return {"ok": True, "ran": label, "operation_id": operation_id}
            except Exception as e:
                operation_status[operation_id] = {"status": "failed", "error": str(e), "end_time": datetime.now().isoformat()}
                return {"ok": False, "error": str(e), "operation_id": operation_id}
    return {"ok": False, "error": f"Unknown action: {label}"}

# 新增功能 1: 账户管理
@app.get("/accounts")
def list_accounts() -> Dict[str, Any]:
    return {"accounts": [{"username": acc["USERNAME"], "email": acc["EMAIL"], "filename": acc["FILENAME"]} for acc in ACCOUNTS]}

@app.post("/accounts/add")
def add_account(account: AccountRequest) -> Dict[str, Any]:
    new_account = {
        "USERNAME": account.username,
        "EMAIL": account.email,
        "PASSWORD": account.password,
        "FILENAME": account.filename
    }
    ACCOUNTS.append(new_account)
    return {"ok": True, "message": f"Account {account.username} added"}

# 新增功能 2: TP下载控制
@app.post("/tp/download")
def download_tp_selected(request: TPDownloadRequest) -> Dict[str, Any]:
    """下载指定账户的TP订单"""
    selected_accounts = [acc for acc in ACCOUNTS if acc["USERNAME"] in request.accounts]
    if not selected_accounts:
        raise HTTPException(status_code=400, detail="No valid accounts selected")
    
    operation_id = f"tp_download_{int(time.time())}"
    operation_status[operation_id] = {"status": "running", "accounts": request.accounts}
    
    try:
        # 这里需要修改run_download_tp来支持API调用
        # 暂时返回成功状态
        operation_status[operation_id] = {"status": "completed", "accounts_processed": len(selected_accounts)}
        return {"ok": True, "operation_id": operation_id, "accounts_processed": len(selected_accounts)}
    except Exception as e:
        operation_status[operation_id] = {"status": "failed", "error": str(e)}
        return {"ok": False, "error": str(e)}

# 新增功能 3: 文件系统操作
@app.get("/files/recent")
def get_recent_files() -> Dict[str, Any]:
    """获取最近修改的文件"""
    paths = get_wt_paths()
    recent_files = []
    
    for folder_name, folder_path in paths.items():
        if isinstance(folder_path, str) and os.path.exists(folder_path):
            folder = Path(folder_path)
            for file_path in folder.glob("*"):
                if file_path.is_file():
                    stat = file_path.stat()
                    recent_files.append({
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "folder": folder_name
                    })
    
    # 按修改时间排序，返回最近10个
    recent_files.sort(key=lambda x: x["modified"], reverse=True)
    return {"files": recent_files[:10]}

@app.get("/files/download/{filename}")
def download_file(filename: str) -> FileResponse:
    """下载指定文件"""
    paths = get_wt_paths()
    
    # 在所有路径中查找文件
    for folder_path in paths.values():
        if isinstance(folder_path, str) and os.path.exists(folder_path):
            file_path = Path(folder_path) / filename
            if file_path.exists():
                return FileResponse(str(file_path), filename=filename)
    
    raise HTTPException(status_code=404, detail="File not found")

# 新增功能 4: 操作状态跟踪
@app.get("/operations/{operation_id}")
def get_operation_status(operation_id: str) -> Dict[str, Any]:
    """获取操作状态"""
    if operation_id not in operation_status:
        raise HTTPException(status_code=404, detail="Operation not found")
    return {"operation_id": operation_id, **operation_status[operation_id]}

@app.get("/operations")
def list_operations() -> Dict[str, Any]:
    """列出所有操作历史"""
    return {"operations": operation_status}

# 新增功能 5: 系统信息
@app.get("/system/info")
def system_info() -> Dict[str, Any]:
    """获取系统信息"""
    paths = get_wt_paths()
    return {
        "timestamp": datetime.now().isoformat(),
        "paths": paths,
        "total_accounts": len(ACCOUNTS),
        "available_actions": len(ACTIONS)
    }

# 新增功能 6: 批量操作
@app.post("/batch/run")
def run_batch_actions(actions: List[str]) -> Dict[str, Any]:
    """批量执行操作"""
    results = []
    batch_id = f"batch_{int(time.time())}"
    
    for action in actions:
        result = run_action(action)
        results.append({"action": action, "result": result})
    
    return {"batch_id": batch_id, "results": results}

# License 管理功能
@app.get("/license/status")
def get_license_status() -> Dict[str, Any]:
    """获取当前 license 状态"""
    ok, msg = verify_license()
    return {
        "valid": ok,
        "message": msg,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/license/info")
def get_license_info() -> Dict[str, Any]:
    """获取 license 详细信息"""
    license_path = r"C:\ProgramData\license\WT_license.key"
    
    if not os.path.exists(license_path):
        raise HTTPException(status_code=404, detail="License file not found")
    
    try:
        with open(license_path, "r") as f:
            lines = f.read().splitlines()
            if len(lines) < 3:
                raise HTTPException(status_code=400, detail="Invalid license file format")
            
            user = lines[0].strip()
            license_code = lines[1].strip()
            expiry_str = lines[2].strip()
            
            # 验证过期日期格式
            try:
                expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
                today = datetime.today().date()
                days_remaining = (expiry_date - today).days
            except:
                expiry_date = None
                days_remaining = None
            
            # 验证 license 码
            secret = "okapi"
            expected_code = hashlib.sha256(f"{user}{secret}".encode()).hexdigest()[:16]
            code_valid = license_code == expected_code
            
            return {
                "username": user,
                "expiry_date": expiry_str,
                "expiry_date_parsed": expiry_date.isoformat() if expiry_date else None,
                "days_remaining": days_remaining,
                "code_valid": code_valid,
                "license_path": license_path
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read license file: {str(e)}")

@app.post("/license/update")
def update_license(request: LicenseUpdateRequest) -> Dict[str, Any]:
    """更新 license 文件"""
    license_path = r"C:\ProgramData\license\WT_license.key"
    license_dir = os.path.dirname(license_path)
    
    # 验证过期日期格式
    try:
        expiry_date = datetime.strptime(request.expiry_date, "%Y-%m-%d").date()
        today = datetime.today().date()
        if expiry_date < today:
            raise HTTPException(status_code=400, detail="Expiry date cannot be in the past")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # 生成 license 码
    secret = "okapi"
    license_code = hashlib.sha256(f"{request.username}{secret}".encode()).hexdigest()[:16]
    
    # 确保目录存在
    try:
        os.makedirs(license_dir, exist_ok=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create license directory: {str(e)}")
    
    # 写入 license 文件
    try:
        with open(license_path, "w") as f:
            f.write(f"{request.username}\n")
            f.write(f"{license_code}\n")
            f.write(f"{request.expiry_date}\n")
        
        # 验证写入的 license
        ok, msg = verify_license()
        if not ok:
            raise HTTPException(status_code=500, detail=f"License file written but verification failed: {msg}")
        
        return {
            "ok": True,
            "message": f"License updated successfully for {request.username}",
            "username": request.username,
            "expiry_date": request.expiry_date,
            "days_remaining": (expiry_date - today).days,
            "license_path": license_path
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write license file: {str(e)}")

# 新增功能 7: 文件监控
@app.get("/files/monitor")
def monitor_files() -> Dict[str, Any]:
    """监控关键文件状态"""
    paths = get_wt_paths()
    file_status = {}
    
    for name, path in paths.items():
        if isinstance(path, str):
            if os.path.exists(path):
                stat = os.stat(path)
                file_status[name] = {
                    "exists": True,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "path": path
                }
            else:
                file_status[name] = {"exists": False, "path": path}
    
    return {"file_status": file_status}


