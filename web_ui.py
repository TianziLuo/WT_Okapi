"""
简单的Web界面来展示API功能
访问 http://127.0.0.1:8000/docs 查看完整API文档
"""
import requests
import json
from typing import Dict, Any

class WTAPIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
    
    def health_check(self) -> Dict[str, Any]:
        """检查API健康状态"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def list_actions(self) -> Dict[str, Any]:
        """获取所有可用操作"""
        response = requests.get(f"{self.base_url}/actions")
        return response.json()
    
    def run_action(self, action_label: str) -> Dict[str, Any]:
        """执行指定操作"""
        response = requests.post(f"{self.base_url}/run", params={"label": action_label})
        return response.json()
    
    def list_accounts(self) -> Dict[str, Any]:
        """获取所有账户"""
        response = requests.get(f"{self.base_url}/accounts")
        return response.json()
    
    def add_account(self, username: str, email: str, password: str, filename: str) -> Dict[str, Any]:
        """添加新账户"""
        data = {
            "username": username,
            "email": email,
            "password": password,
            "filename": filename
        }
        response = requests.post(f"{self.base_url}/accounts/add", json=data)
        return response.json()
    
    def get_recent_files(self) -> Dict[str, Any]:
        """获取最近修改的文件"""
        response = requests.get(f"{self.base_url}/files/recent")
        return response.json()
    
    def monitor_files(self) -> Dict[str, Any]:
        """监控文件状态"""
        response = requests.get(f"{self.base_url}/files/monitor")
        return response.json()
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        response = requests.get(f"{self.base_url}/system/info")
        return response.json()
    
    def run_batch_actions(self, actions: list) -> Dict[str, Any]:
        """批量执行操作"""
        response = requests.post(f"{self.base_url}/batch/run", json=actions)
        return response.json()

def demo_api_usage():
    """演示API使用方法"""
    client = WTAPIClient()
    
    print("🚀 WT Okapi API 功能演示")
    print("=" * 50)
    
    # 1. 健康检查
    print("\n1. 健康检查:")
    health = client.health_check()
    print(f"   状态: {health}")
    
    # 2. 系统信息
    print("\n2. 系统信息:")
    system_info = client.get_system_info()
    print(f"   账户数量: {system_info.get('total_accounts', 0)}")
    print(f"   可用操作: {system_info.get('available_actions', 0)}")
    
    # 3. 列出所有操作
    print("\n3. 可用操作:")
    actions = client.list_actions()
    for i, action in enumerate(actions.get('actions', []), 1):
        print(f"   {i}. {action}")
    
    # 4. 列出账户
    print("\n4. 当前账户:")
    accounts = client.list_accounts()
    for acc in accounts.get('accounts', []):
        print(f"   - {acc['username']} ({acc['email']})")
    
    # 5. 文件监控
    print("\n5. 文件状态监控:")
    file_status = client.monitor_files()
    for name, status in file_status.get('file_status', {}).items():
        if status.get('exists'):
            print(f"   ✅ {name}: {status['size']} bytes")
        else:
            print(f"   ❌ {name}: 文件不存在")
    
    # 6. 最近文件
    print("\n6. 最近修改的文件:")
    recent_files = client.get_recent_files()
    for file_info in recent_files.get('files', [])[:5]:  # 只显示前5个
        print(f"   - {file_info['name']} ({file_info['size']} bytes)")
    
    print("\n" + "=" * 50)
    print("💡 更多功能请访问: http://127.0.0.1:8000/docs")
    print("💡 或者使用 curl/Postman 调用API")

if __name__ == "__main__":
    try:
        demo_api_usage()
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器")
        print("请确保WT_main.py正在运行，并且FastAPI服务器已启动")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

