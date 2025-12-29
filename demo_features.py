"""
WT Okapi 进阶功能演示
展示所有新增的API功能
"""
import requests
import json
import time
import asyncio
from datetime import datetime

class WTAPIDemo:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def print_section(self, title):
        print(f"\n{'='*60}")
        print(f"🚀 {title}")
        print('='*60)
    
    def demo_basic_api(self):
        """演示基础API功能"""
        self.print_section("基础API功能")
        
        # 1. 健康检查
        print("1. 健康检查:")
        try:
            response = self.session.get(f"{self.base_url}/health")
            print(f"   状态: {response.json()}")
        except Exception as e:
            print(f"   ❌ 连接失败: {e}")
            return False
        
        # 2. 系统信息
        print("\n2. 系统信息:")
        try:
            response = self.session.get(f"{self.base_url}/system/info")
            info = response.json()
            print(f"   时间戳: {info.get('timestamp')}")
            print(f"   账户数量: {info.get('total_accounts')}")
            print(f"   可用操作: {info.get('available_actions')}")
        except Exception as e:
            print(f"   ❌ 获取系统信息失败: {e}")
        
        # 3. 列出操作
        print("\n3. 可用操作:")
        try:
            response = self.session.get(f"{self.base_url}/actions")
            actions = response.json().get('actions', [])
            for i, action in enumerate(actions, 1):
                print(f"   {i}. {action}")
        except Exception as e:
            print(f"   ❌ 获取操作列表失败: {e}")
        
        return True
    
    def demo_account_management(self):
        """演示账户管理功能"""
        self.print_section("账户管理功能")
        
        # 1. 列出当前账户
        print("1. 当前账户:")
        try:
            response = self.session.get(f"{self.base_url}/accounts")
            accounts = response.json().get('accounts', [])
            for acc in accounts:
                print(f"   - {acc['username']} ({acc['email']})")
        except Exception as e:
            print(f"   ❌ 获取账户列表失败: {e}")
        
        # 2. 添加新账户（演示）
        print("\n2. 添加新账户:")
        try:
            new_account = {
                "username": "demo_user",
                "email": "demo@example.com",
                "password": "demo_password",
                "filename": "demo_orders.csv"
            }
            response = self.session.post(f"{self.base_url}/accounts/add", json=new_account)
            result = response.json()
            print(f"   结果: {result}")
        except Exception as e:
            print(f"   ❌ 添加账户失败: {e}")
    
    def demo_file_operations(self):
        """演示文件操作功能"""
        self.print_section("文件操作功能")
        
        # 1. 文件监控
        print("1. 文件状态监控:")
        try:
            response = self.session.get(f"{self.base_url}/files/monitor")
            file_status = response.json().get('file_status', {})
            for name, status in file_status.items():
                if status.get('exists'):
                    print(f"   ✅ {name}: {status.get('size', 0)} bytes")
                else:
                    print(f"   ❌ {name}: 文件不存在")
        except Exception as e:
            print(f"   ❌ 文件监控失败: {e}")
        
        # 2. 最近文件
        print("\n2. 最近修改的文件:")
        try:
            response = self.session.get(f"{self.base_url}/files/recent")
            recent_files = response.json().get('files', [])
            for file_info in recent_files[:5]:  # 只显示前5个
                print(f"   - {file_info['name']} ({file_info['size']} bytes)")
        except Exception as e:
            print(f"   ❌ 获取最近文件失败: {e}")
    
    def demo_task_management(self):
        """演示任务管理功能"""
        self.print_section("任务管理功能")
        
        # 1. 创建任务
        print("1. 创建测试任务:")
        try:
            response = self.session.post(f"{self.base_url}/tasks/create", params={
                "name": "演示任务",
                "duration": 5
            })
            result = response.json()
            print(f"   任务ID: {result.get('task_id')}")
            task_id = result.get('task_id')
        except Exception as e:
            print(f"   ❌ 创建任务失败: {e}")
            return
        
        # 2. 监控任务进度
        print("\n2. 监控任务进度:")
        for i in range(10):  # 监控10次
            try:
                response = self.session.get(f"{self.base_url}/tasks/{task_id}")
                task_info = response.json()
                status = task_info.get('status', 'unknown')
                progress = task_info.get('progress', 0)
                print(f"   状态: {status} | 进度: {progress}%")
                
                if status in ['completed', 'failed']:
                    break
                    
                time.sleep(1)
            except Exception as e:
                print(f"   ❌ 获取任务状态失败: {e}")
                break
    
    def demo_batch_operations(self):
        """演示批量操作功能"""
        self.print_section("批量操作功能")
        
        # 1. 批量执行操作
        print("1. 批量执行操作:")
        try:
            actions = ["• Open 2.1", "• WT Outbound"]  # 示例操作
            response = self.session.post(f"{self.base_url}/batch/run", json=actions)
            result = response.json()
            print(f"   批量ID: {result.get('batch_id')}")
            print(f"   执行结果: {len(result.get('results', []))} 个操作")
        except Exception as e:
            print(f"   ❌ 批量操作失败: {e}")
    
    def demo_advanced_features(self):
        """演示高级功能"""
        self.print_section("高级功能")
        
        # 1. 定时任务
        print("1. 调度定时任务:")
        try:
            response = self.session.post(f"{self.base_url}/schedule/task", params={
                "name": "定时演示任务",
                "delay_seconds": 3
            })
            result = response.json()
            print(f"   任务ID: {result.get('task_id')}")
            print(f"   延迟: {result.get('delay_seconds')} 秒")
        except Exception as e:
            print(f"   ❌ 调度任务失败: {e}")
        
        # 2. 系统监控
        print("\n2. 系统监控:")
        try:
            response = self.session.get(f"{self.base_url}/monitor/system")
            monitor_data = response.json()
            print(f"   CPU使用率: {monitor_data.get('cpu_percent', 0)}%")
            print(f"   内存使用率: {monitor_data.get('memory_percent', 0)}%")
            print(f"   活跃任务: {monitor_data.get('active_tasks', 0)}")
        except Exception as e:
            print(f"   ❌ 系统监控失败: {e}")
    
    def demo_websocket_connection(self):
        """演示WebSocket连接"""
        self.print_section("WebSocket实时通信")
        
        try:
            import websocket
            import threading
            
            def on_message(ws, message):
                data = json.loads(message)
                if data.get('type') == 'task_update':
                    task = data.get('task', {})
                    print(f"   收到任务更新: {task.get('name')} - {task.get('status')} ({task.get('progress')}%)")
            
            def on_error(ws, error):
                print(f"   ❌ WebSocket错误: {error}")
            
            def on_close(ws, close_status_code, close_msg):
                print("   WebSocket连接已关闭")
            
            def on_open(ws):
                print("   ✅ WebSocket连接已建立")
            
            # 连接WebSocket
            ws_url = self.base_url.replace('http', 'ws') + '/ws'
            ws = websocket.WebSocketApp(ws_url,
                                     on_message=on_message,
                                     on_error=on_error,
                                     on_close=on_close,
                                     on_open=on_open)
            
            # 在后台运行WebSocket
            wst = threading.Thread(target=ws.run_forever)
            wst.daemon = True
            wst.start()
            
            print("   WebSocket连接已启动，等待任务更新...")
            time.sleep(5)  # 等待5秒
            
        except ImportError:
            print("   ⚠️ 需要安装websocket-client: pip install websocket-client")
        except Exception as e:
            print(f"   ❌ WebSocket连接失败: {e}")
    
    def run_full_demo(self):
        """运行完整演示"""
        print("🦫 WT Okapi 进阶功能演示")
        print("=" * 60)
        print("请确保WT_main.py正在运行，并且FastAPI服务器已启动")
        print("=" * 60)
        
        # 检查连接
        if not self.demo_basic_api():
            print("\n❌ 无法连接到API服务器，请检查:")
            print("   1. WT_main.py是否正在运行")
            print("   2. FastAPI服务器是否在127.0.0.1:8000启动")
            print("   3. 防火墙是否阻止了连接")
            return
        
        # 运行所有演示
        self.demo_account_management()
        self.demo_file_operations()
        self.demo_task_management()
        self.demo_batch_operations()
        self.demo_advanced_features()
        self.demo_websocket_connection()
        
        print(f"\n{'='*60}")
        print("🎉 演示完成！")
        print("💡 更多功能请访问:")
        print("   - API文档: http://127.0.0.1:8000/docs")
        print("   - 监控面板: http://127.0.0.1:8000/dashboard")
        print("   - WebSocket: ws://127.0.0.1:8000/ws")
        print("=" * 60)

if __name__ == "__main__":
    demo = WTAPIDemo()
    demo.run_full_demo()

