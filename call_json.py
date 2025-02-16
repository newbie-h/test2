import json
import requests

def call_api_with_json(json_str, url, http_method='POST', timeout=10):
    """
    将JSON字符串转换为字典并用其中的字段作为参数调用Web接口

    Args:
        json_str (str): 需要转换的JSON格式字符串
        url (str): 目标API的URL地址
        http_method (str): HTTP方法，支持GET/POST（默认POST）
        timeout (int): 请求超时时间（秒，默认10）

    Returns:
        dict: 包含响应结果和状态的字典结构：
            {
                'success': bool,     # 是否成功
                'response': dict,     # 响应内容（JSON自动转换）
                'error': str,         # 错误信息（如有）
                'status_code': int   # HTTP状态码
            }
    """
    result = {
        'success': False,
        'response': None,
        'error': None,
        'status_code': None
    }

    try:
        # 将JSON字符串转换为字典
        params_dict = json.loads(json_str)
    except json.JSONDecodeError as e:
        result['error'] = f'JSON解析失败: {str(e)}'
        return result
    except Exception as e:
        result['error'] = f'参数处理异常: {str(e)}'
        return result

    try:
        # 根据请求方法发送HTTP请求
        http_method = http_method.upper()
        if http_method == 'GET':
            response = requests.get(
                url,
                params=params_dict,
                timeout=timeout
            )
        elif http_method == 'POST':
            response = requests.post(
                url,
                json=params_dict,  # 自动设置Content-Type为application/json
                timeout=timeout
            )
        else:
            result['error'] = f'不支持的HTTP方法: {http_method}'
            return result

        # 记录状态码
        result['status_code'] = response.status_code

        # 检查HTTP状态码
        response.raise_for_status()

        # 尝试解析JSON响应
        try:
            result['response'] = response.json()
        except json.JSONDecodeError:
            result['response'] = response.text

        result['success'] = True

    except requests.exceptions.RequestException as e:
        result['error'] = f'请求失败: {str(e)}'
        if hasattr(e, 'response') and e.response is not None:
            result['status_code'] = e.response.status_code
    except Exception as e:
        result['error'] = f'未知错误: {str(e)}'

    return result

# 示例调用
if __name__ == '__main__':
    # 测试数据
    test_json = '''{
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }'''

    # 调用API（测试使用httpbin.org的示例接口）
    api_result = call_api_with_json(
        json_str=test_json,
        url='https://httpbin.org/post',
        http_method='POST'
    )

    # 处理结果
    if api_result['success']:
        print("API调用成功！")
        print("响应数据:", api_result['response'])
    else:
        print("API调用失败")
        print("错误信息:", api_result['error'])
        print("状态码:", api_result['status_code'])