
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gdb_app.gdb_script import gdb_debugger
import os

# 允许跨域访问, POST请求
@csrf_exempt
def upload_cpp_file(request):
    """上传CPP文件并编译生成可执行文件

    Args:
        cpp_file (file): 上传的CPP文件
        executable_file_name (string): 可执行文件名/算法代号或名称
    Returns:
        json: 编译结果
    """
    if request.method == 'POST':
        cpp_file = request.FILES.get('cpp_file')
        if cpp_file:
            cpp_file_name = cpp_file.name
            executable_file_name = request.POST.get('executable_file_name')
            path = os.path.abspath(os.path.dirname(__file__)) + '/gdb_script'
            # 查看与manage.py同级目录下的cpp_files文件夹是否存在
            print(path, cpp_file_name, executable_file_name)
            # if not os.path.exists(path + '/cpp_files'):
            #     # 不存在则创建
            #     os.mkdir(path + '/cpp_files')
                
            # 保存CPP文件到gdb_app的cpp_files中
            with open(path + '/cpp_files/' + cpp_file.name, 'wb') as file:
                for chunk in cpp_file.chunks():
                    file.write(chunk)
            # 执行编译
            compile_result = gdb_debugger.compile(gdb_debugger.cpp_file_path + cpp_file_name, gdb_debugger.executable_path + executable_file_name)
            print(compile_result)
            if compile_result == 0:
                return JsonResponse({'message': '文件编译成功', 'status':200}, status=200, charset='utf-8')
            else:
                return JsonResponse({'message': '文件编译失败', 'status':505}, status=400, charset='utf-8')
        else:
            return JsonResponse({'message': '未找到上传的文件', 'status':400}, status=400, charset='utf-8')
    else:
        return JsonResponse({'message': '仅支持POST请求', 'status':405}, status=405, charset='utf-8')
    
    
def hello_world(request):
    return JsonResponse({'message': 'Hello, World!'})


