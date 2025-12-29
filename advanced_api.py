"""
高级API功能扩展
包括WebSocket实时通信、任务队列、定时任务等
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse
import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

# 任务状态枚举
class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    id: str
    name: str
    status: TaskStatus
    created_at: datetime
    started_at: datetime = None
    completed_at: datetime = None
    progress: int = 0
    result: Any = None
    error: str = None

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.websocket_connections: List[WebSocket] = []
    
    async def add_task(self, task_id: str, name: str) -> Task:
        task = Task(
            id=task_id,
            name=name,
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )
        self.tasks[task_id] = task
        await self.broadcast_task_update(task)
        return task
    
    async def update_task_status(self, task_id: str, status: TaskStatus, progress: int = None, result: Any = None, error: str = None):
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = status
            
            if status == TaskStatus.RUNNING:
                task.started_at = datetime.now()
            elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                task.completed_at = datetime.now()
            
            if progress is not None:
                task.progress = progress
            if result is not None:
                task.result = result
            if error is not None:
                task.error = error
            
            await self.broadcast_task_update(task)
    
    async def get_task(self, task_id: str) -> Task:
        return self.tasks.get(task_id)
    
    async def list_tasks(self) -> List[Task]:
        return list(self.tasks.values())
    
    async def add_websocket(self, websocket: WebSocket):
        self.websocket_connections.append(websocket)
    
    async def remove_websocket(self, websocket: WebSocket):
        if websocket in self.websocket_connections:
            self.websocket_connections.remove(websocket)
    
    async def broadcast_task_update(self, task: Task):
        message = {
            "type": "task_update",
            "task": {
                "id": task.id,
                "name": task.name,
                "status": task.status.value,
                "progress": task.progress,
                "created_at": task.created_at.isoformat(),
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "result": task.result,
                "error": task.error
            }
        }
        
        # 发送给所有连接的WebSocket客户端
        disconnected = []
        for websocket in self.websocket_connections:
            try:
                await websocket.send_text(json.dumps(message))
            except:
                disconnected.append(websocket)
        
        # 清理断开的连接
        for ws in disconnected:
            await self.remove_websocket(ws)

# 全局任务管理器
task_manager = TaskManager()

# 模拟长时间运行的任务
async def simulate_long_task(task_id: str, duration: int = 10):
    """模拟长时间运行的任务"""
    await task_manager.update_task_status(task_id, TaskStatus.RUNNING, progress=0)
    
    for i in range(duration):
        await asyncio.sleep(1)
        progress = int((i + 1) / duration * 100)
        await task_manager.update_task_status(task_id, TaskStatus.RUNNING, progress=progress)
    
    await task_manager.update_task_status(task_id, TaskStatus.COMPLETED, progress=100, result="任务完成")

# WebSocket连接管理
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await task_manager.add_websocket(websocket)
    
    try:
        while True:
            # 保持连接活跃
            await websocket.receive_text()
    except WebSocketDisconnect:
        await task_manager.remove_websocket(websocket)

# 任务相关API
@app.post("/tasks/create")
async def create_task(name: str, duration: int = 10):
    """创建新任务"""
    task_id = f"task_{int(time.time())}"
    task = await task_manager.add_task(task_id, name)
    
    # 在后台运行任务
    asyncio.create_task(simulate_long_task(task_id, duration))
    
    return {"task_id": task_id, "status": "created"}

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """获取任务状态"""
    task = await task_manager.get_task(task_id)
    if not task:
        return {"error": "Task not found"}
    
    return {
        "id": task.id,
        "name": task.name,
        "status": task.status.value,
        "progress": task.progress,
        "created_at": task.created_at.isoformat(),
        "started_at": task.started_at.isoformat() if task.started_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "result": task.result,
        "error": task.error
    }

@app.get("/tasks")
async def list_tasks():
    """列出所有任务"""
    tasks = await task_manager.list_tasks()
    return {"tasks": [
        {
            "id": task.id,
            "name": task.name,
            "status": task.status.value,
            "progress": task.progress,
            "created_at": task.created_at.isoformat()
        } for task in tasks
    ]}

# 实时日志流
@app.get("/logs/stream")
async def stream_logs():
    """实时日志流（SSE）"""
    from fastapi.responses import StreamingResponse
    
    async def generate_logs():
        while True:
            # 模拟日志数据
            log_data = {
                "timestamp": datetime.now().isoformat(),
                "level": "INFO",
                "message": f"系统运行正常 - {datetime.now().strftime('%H:%M:%S')}"
            }
            yield f"data: {json.dumps(log_data)}\n\n"
            await asyncio.sleep(1)
    
    return StreamingResponse(generate_logs(), media_type="text/plain")

# 定时任务调度
scheduled_tasks = {}

@app.post("/schedule/task")
async def schedule_task(name: str, delay_seconds: int):
    """调度延迟任务"""
    task_id = f"scheduled_{int(time.time())}"
    
    async def delayed_task():
        await asyncio.sleep(delay_seconds)
        task = await task_manager.add_task(task_id, name)
        await task_manager.update_task_status(task_id, TaskStatus.RUNNING)
        # 执行实际任务逻辑
        await asyncio.sleep(5)  # 模拟任务执行
        await task_manager.update_task_status(task_id, TaskStatus.COMPLETED, result="定时任务完成")
    
    asyncio.create_task(delayed_task())
    scheduled_tasks[task_id] = {"name": name, "scheduled_at": datetime.now(), "delay": delay_seconds}
    
    return {"task_id": task_id, "scheduled": True, "delay_seconds": delay_seconds}

@app.get("/schedule/tasks")
async def list_scheduled_tasks():
    """列出所有定时任务"""
    return {"scheduled_tasks": scheduled_tasks}

# 系统监控
@app.get("/monitor/system")
async def system_monitor():
    """系统监控数据"""
    import psutil
    
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "active_tasks": len([t for t in task_manager.tasks.values() if t.status == TaskStatus.RUNNING]),
        "total_tasks": len(task_manager.tasks),
        "websocket_connections": len(task_manager.websocket_connections)
    }

# 简单的Web界面
@app.get("/dashboard")
async def dashboard():
    """简单的监控面板"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WT Okapi 监控面板</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .card { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .task { background: #f5f5f5; padding: 10px; margin: 5px 0; border-radius: 3px; }
            .running { background: #e3f2fd; }
            .completed { background: #e8f5e8; }
            .failed { background: #ffebee; }
            .progress-bar { width: 100%; height: 20px; background: #ddd; border-radius: 10px; overflow: hidden; }
            .progress-fill { height: 100%; background: #4caf50; transition: width 0.3s; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🦫 WT Okapi 监控面板</h1>
            
            <div class="card">
                <h3>系统状态</h3>
                <div id="system-status">加载中...</div>
            </div>
            
            <div class="card">
                <h3>任务列表</h3>
                <div id="tasks-list">加载中...</div>
            </div>
            
            <div class="card">
                <h3>实时日志</h3>
                <div id="logs" style="height: 200px; overflow-y: auto; background: #f9f9f9; padding: 10px; font-family: monospace;"></div>
            </div>
        </div>
        
        <script>
            // WebSocket连接
            const ws = new WebSocket('ws://127.0.0.1:8000/ws');
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.type === 'task_update') {
                    updateTasksList();
                }
            };
            
            // 更新系统状态
            async function updateSystemStatus() {
                try {
                    const response = await fetch('/monitor/system');
                    const data = await response.json();
                    document.getElementById('system-status').innerHTML = `
                        <p>CPU: ${data.cpu_percent}% | 内存: ${data.memory_percent}% | 磁盘: ${data.disk_usage}%</p>
                        <p>活跃任务: ${data.active_tasks} | 总任务: ${data.total_tasks} | WebSocket连接: ${data.websocket_connections}</p>
                    `;
                } catch (error) {
                    console.error('更新系统状态失败:', error);
                }
            }
            
            // 更新任务列表
            async function updateTasksList() {
                try {
                    const response = await fetch('/tasks');
                    const data = await response.json();
                    let html = '';
                    data.tasks.forEach(task => {
                        const statusClass = task.status;
                        html += `
                            <div class="task ${statusClass}">
                                <strong>${task.name}</strong> (${task.id})
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${task.progress}%"></div>
                                </div>
                                <small>状态: ${task.status} | 进度: ${task.progress}%</small>
                            </div>
                        `;
                    });
                    document.getElementById('tasks-list').innerHTML = html || '<p>暂无任务</p>';
                } catch (error) {
                    console.error('更新任务列表失败:', error);
                }
            }
            
            // 创建测试任务
            async function createTestTask() {
                try {
                    await fetch('/tasks/create?name=测试任务&duration=10', {method: 'POST'});
                    updateTasksList();
                } catch (error) {
                    console.error('创建任务失败:', error);
                }
            }
            
            // 定时更新
            setInterval(updateSystemStatus, 5000);
            setInterval(updateTasksList, 2000);
            
            // 初始加载
            updateSystemStatus();
            updateTasksList();
            
            // 添加测试按钮
            document.body.innerHTML += '<button onclick="createTestTask()" style="margin: 20px; padding: 10px;">创建测试任务</button>';
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html_content)

