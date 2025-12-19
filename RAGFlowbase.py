# 这个程序会远程在RAGflow对应聊天下创建一个会话，会话名称为***，有延迟，程序运行时RAGflow对应会话会卡，该程序无上下文增加上下文记忆请在程序中保持使用当前会话
import requests

# 1. 配置信息 - 请替换为您的实际信息
BASE_URL = "http://***********"  # 例如: "http://112.84.199.36:9380"
API_KEY = "**************************"  # 在RAGFlow用户设置中生成
CHAT_ID = "**************************"  # 可以从聊天->嵌入网站  中找到
def query_ragflow(question):
    """
    向RAGFlow发送问题并返回答案
    """
    # 2. 创建会话 (可选，但建议创建以管理对话历史)
    session_url = f"{BASE_URL}/api/v1/chats/{CHAT_ID}/sessions"
    session_headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    session_data = {
        "name": "优雅的企鹅"  # 会话名称，可自定义
    }
    
    try:
        session_response = requests.post(session_url, headers=session_headers, json=session_data)
        session_response.raise_for_status()  # 检查请求是否成功
        session_info = session_response.json()
        
        if session_info.get('code') != 0:
            print(f"创建会话失败: {session_info.get('message')}")
            return None
            
        session_id = session_info['data']['id']
        print(f"会话创建成功，ID: {session_id}")
        
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None

    # 3. 通过 completions 接口提问（此接口集成了检索和生成）
    chat_url = f"{BASE_URL}/api/v1/chats/{CHAT_ID}/completions"
    chat_headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    chat_data = {
        "question": question,  # 您要查询的问题
        "session_id": session_id,  # 上一步创建的会话ID
        "stream": False  # 设为 True 可开启流式输出，这里为简单起见设为 False
    }
    
    try:
        chat_response = requests.post(chat_url, headers=chat_headers, json=chat_data)
        chat_response.raise_for_status()
        chat_info = chat_response.json()
        
        if chat_info.get('code') == 0:
            answer = chat_info['data']['answer']
            print(f"问题: {question}")
            print(f"AI的回答")
            print(f"{answer}")
            return answer
        else:
            print(f"获取答案失败: {chat_info.get('message')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None

# 4. 使用示例
if __name__ == "__main__":
    user_question = "灭火器过期未更换"  # 您可以在这里输入任何问题
    result = query_ragflow(user_question)