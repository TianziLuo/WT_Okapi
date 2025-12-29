# 🦫 WT Okapi API 进阶功能

## 概述

WT Okapi 现在支持完整的 REST API 和 WebSocket 实时通信功能，让你的本地应用变成强大的自动化平台！

## 🚀 新增功能

### 1. 基础API功能
- **健康检查**: `GET /health` - 检查API状态
- **系统信息**: `GET /system/info` - 获取系统配置和状态
- **操作列表**: `GET /actions` - 列出所有可用操作
- **执行操作**: `POST /run` - 执行指定操作

### 2. 账户管理
- **列出账户**: `GET /accounts` - 获取所有TP账户
- **添加账户**: `POST /accounts/add` - 动态添加新账户
- **TP下载控制**: `POST /tp/download` - 选择性下载指定账户的订单

### 3. 文件系统操作
- **文件监控**: `GET /files/monitor` - 监控关键文件状态
- **最近文件**: `GET /files/recent` - 获取最近修改的文件
- **文件下载**: `GET /files/download/{filename}` - 下载指定文件

### 4. 任务管理
- **创建任务**: `POST /tasks/create` - 创建后台任务
- **任务状态**: `GET /tasks/{task_id}` - 获取任务进度
- **任务列表**: `GET /tasks` - 列出所有任务
- **定时任务**: `POST /schedule/task` - 调度延迟任务

### 5. 批量操作
- **批量执行**: `POST /batch/run` - 批量执行多个操作
- **操作历史**: `GET /operations` - 查看操作历史记录

### 6. 实时通信
- **WebSocket**: `ws://127.0.0.1:8000/ws` - 实时任务状态更新
- **日志流**: `GET /logs/stream` - 实时日志流（SSE）
- **监控面板**: `GET /dashboard` - 可视化监控界面

### 7. 系统监控
- **系统状态**: `GET /monitor/system` - CPU、内存、磁盘使用率
- **任务统计**: 实时任务数量和状态统计
- **连接监控**: WebSocket连接数量监控

## 📋 使用方法

### 1. 启动服务
```bash
# 运行主程序（自动启动API服务器）
python WT_main.py

# 或者单独运行API服务器
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

### 2. 访问接口
- **API文档**: http://127.0.0.1:8000/docs
- **监控面板**: http://127.0.0.1:8000/dashboard
- **健康检查**: http://127.0.0.1:8000/health

### 3. 使用示例

#### Python客户端
```python
import requests

# 健康检查
response = requests.get("http://127.0.0.1:8000/health")
print(response.json())

# 执行操作
response = requests.post("http://127.0.0.1:8000/run", params={"label": "• WT Outbound"})
print(response.json())

# 创建任务
response = requests.post("http://127.0.0.1:8000/tasks/create", params={"name": "测试任务", "duration": 10})
task_id = response.json()["task_id"]
```

#### curl命令
```bash
# 健康检查
curl http://127.0.0.1:8000/health

# 列出操作
curl http://127.0.0.1:8000/actions

# 执行操作
curl -X POST "http://127.0.0.1:8000/run?label=•%20WT%20Outbound"

# 获取系统信息
curl http://127.0.0.1:8000/system/info
```

### 4. WebSocket连接
```javascript
const ws = new WebSocket('ws://127.0.0.1:8000/ws');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'task_update') {
        console.log('任务更新:', data.task);
    }
};
```

## 🔧 进阶功能

### 1. 自定义操作
```python
# 在handlers/actions.py中添加新操作
ACTIONS = [
    ("• 自定义操作", your_custom_function),
]
```

### 2. 任务队列
```python
# 创建长时间运行的任务
response = requests.post("http://127.0.0.1:8000/tasks/create", 
                        params={"name": "数据处理", "duration": 30})

# 监控任务进度
task_id = response.json()["task_id"]
status = requests.get(f"http://127.0.0.1:8000/tasks/{task_id}").json()
```

### 3. 定时任务
```python
# 调度延迟任务
response = requests.post("http://127.0.0.1:8000/schedule/task",
                        params={"name": "每日报告", "delay_seconds": 3600})
```

### 4. 批量处理
```python
# 批量执行操作
actions = ["• Open 2.1", "• WT Outbound", "• Copy 'Use' from Downloads"]
response = requests.post("http://127.0.0.1:8000/batch/run", json=actions)
```

## 📊 监控和调试

### 1. 实时监控面板
访问 http://127.0.0.1:8000/dashboard 查看：
- 系统资源使用情况
- 任务执行状态
- 实时日志流
- WebSocket连接状态

### 2. API文档
访问 http://127.0.0.1:8000/docs 查看：
- 完整的API接口文档
- 请求/响应示例
- 在线测试功能

### 3. 日志和调试
```python
# 获取操作历史
response = requests.get("http://127.0.0.1:8000/operations")

# 监控文件状态
response = requests.get("http://127.0.0.1:8000/files/monitor")
```

## 🛠️ 部署和打包

### 1. 依赖安装
```bash
pip install -r requirements.txt
```

### 2. PyInstaller打包
```bash
# 在spec文件中添加hidden-imports
pyinstaller --hidden-import=fastapi --hidden-import=uvicorn WT_main.spec
```

### 3. 生产环境
```python
# 修改WT_main.py中的服务器配置
uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, log_level="info")
```

## 🔒 安全考虑

### 1. 访问控制
- 默认绑定到127.0.0.1（仅本地访问）
- 生产环境建议添加认证机制

### 2. 数据安全
- 账户密码存储在内存中
- 敏感操作需要额外验证

### 3. 网络安全
- 使用HTTPS（生产环境）
- 配置防火墙规则

## 📈 性能优化

### 1. 异步处理
- 长时间运行的任务使用后台线程
- WebSocket实时通信
- 非阻塞API调用

### 2. 资源监控
- 实时CPU/内存监控
- 任务队列管理
- 连接池优化

### 3. 缓存策略
- 文件状态缓存
- 操作结果缓存
- 系统信息缓存

## 🎯 使用场景

### 1. 自动化工作流
- 定时执行重复任务
- 批量处理文件操作
- 远程控制应用功能

### 2. 监控和告警
- 文件变化监控
- 系统资源监控
- 任务执行状态监控

### 3. 集成开发
- 与其他系统集成
- 自定义前端界面
- 移动端控制

## 🚀 未来扩展

### 1. 数据库支持
- 操作历史持久化
- 用户权限管理
- 配置管理

### 2. 消息队列
- Redis/RabbitMQ集成
- 分布式任务处理
- 高可用性支持

### 3. 微服务架构
- 服务拆分
- 容器化部署
- 负载均衡

---

**开始使用**: 运行 `python demo_features.py` 查看完整功能演示！


