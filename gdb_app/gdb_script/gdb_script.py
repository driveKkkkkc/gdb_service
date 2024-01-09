import gdb
import json

list = []
filter_list = [
    "{",
    "}",
    "return 0",
    "int main",
    "int argc",
    "char *argv[]"
    "return",
]

# 需要步入的函数参数，默认为空
# step_into = []
# print("arg0: ", arg0)
# print("step_into: ", step_into)

step_into = step_into
print("step_into: ", step_into)
print("type:", type(step_into))

def is_filter_code(code):
    for filter in filter_list:
        if filter in code:
            return True
    return False


def is_step_into(frame):
    for func in step_into:
        if func in frame.split("\n")[1]:
            return True
    return False

def main():
    # 设置断点在主函数的入口处
    gdb.execute('break main')
    # 启动程序
    gdb.execute('run')
    frame = gdb.execute('frame', to_string=True)
    # 记录步数
    step = 0
    # 进入单步执行循环
    while True:
        execute_flag = False
        # 执行步入，检查是否在需要步入的函数中
        # if 'main' in frame: # 主函数中默认需要步入 TODO：待确认
        #     gdb.execute('step')
        #     execute_flag = True
        # 判断是否步入
        if is_step_into(frame):
            gdb.execute('step')
            execute_flag = True
        # 判断是否步过
        if not execute_flag:
            gdb.execute('next')
            
        frame = gdb.execute('frame', to_string=True)
        # 获取frame的第二行，代表行号和具体代码
        info = frame.split("\n")[1]
        code = info.split("\t")[1].replace(" ", "")
        line = info.split("\t")[0]
        #  过滤无意义代码
        if is_filter_code(code):
            continue
        
        step += 1
        # 构造为dict，包括行号和指令
        code_dict = {
            "step": step,
            "line": line,
            "code": code
        }
        list.append(code_dict)
        # line = gdb.execute('list', to_string=True)
        
        # 判断是否在主函数中
        if 'main' in frame and "return 0" in frame:
            break
        # 可以添加其他条件来跳出单步执行循环

    # 在主函数返回后继续执行
    # gdb.execute('continue')

if __name__ == '__main__':
    main()
    # 把list 转换为json写入文件
    with open('frame.json', 'w') as f:
        json.dump(list, f)
    # 重置参数
    step_into = []
    gdb.execute('quit')
    gdb.execute('y')