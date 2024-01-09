from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gdb_app.gdb_script import gdb_debugger
import json

def hello_world(request):
    return HttpResponse("Hello, World!")

# 允许跨域访问
@csrf_exempt
def get_gdb_result(request):
    """获取GDB调试结果

    Args:
        executable_file_name (string): 可执行文件名

    Returns:
        json: GDB调试栈帧
    TODO: 检查是否存在可执行文件（依据数据库）
    """
    # 从post请求的body中获取参数
    body = json.loads(request.body)
    print(body)
    executable_file_name = body['executable_file_name'] # 可执行文件名
    step_in_list = body['step_in_list'] # 要步入的函数列表
    print(executable_file_name, step_in_list)
    
    result = gdb_debugger.debug(gdb_debugger.executable_path + executable_file_name, step_in_list)
    return HttpResponse(result)