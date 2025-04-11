import os
import shutil
import subprocess
from subprocess import run

def get_allure_cmd():
    """获取正确的allure命令路径"""
    if os.name == 'nt':  # Windows系统
        try:
            # 使用where命令找到allure.cmd的位置
            result = subprocess.check_output('where allure', shell=True, text=True)
            paths = result.strip().split('\n')
            for path in paths:
                if path.endswith('.cmd'):
                    return path
            # 如果没找到.cmd文件，返回默认的npm位置
            return r"C:\Users\{}\AppData\Roaming\npm\allure.cmd".format(os.getenv('USERNAME'))
        except:
            return r"C:\Users\{}\AppData\Roaming\npm\allure.cmd".format(os.getenv('USERNAME'))
    return 'allure'  # 非Windows系统直接返回allure

def clean_reports():
    """清理旧的报告数据"""
    print("正在清理旧的报告数据...")
    paths_to_clean = [
        'Reports/allure-results',
        'Reports/html'
    ]
    
    for path in paths_to_clean:
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                print(f"已清理: {path}")
            except Exception as e:
                print(f"清理 {path} 时出错: {str(e)}")
    
    # 重新创建目录
    for path in paths_to_clean:
        os.makedirs(path, exist_ok=True)
    print("清理完成！")

def run_tests():
    try:
        # 获取正确的allure命令路径
        allure_cmd = get_allure_cmd()
        print(f"使用Allure命令: {allure_cmd}")
        
        # 清理旧报告
        clean_reports()
        
        # 运行测试并生成allure结果
        print("开始运行测试...")
        pytest_result = subprocess.run(['pytest', '-v', '--alluredir=Reports/allure-results'], 
                                    capture_output=True, 
                                    text=True)
        print(pytest_result.stdout)
        
        # 生成报告
        print("正在生成Allure报告...")
        generate_result = subprocess.run([allure_cmd, 'generate', 'Reports/allure-results', 
                                       '-o', 'Reports/html', '--clean'],
                                      capture_output=True,
                                      text=True,
                                      shell=True)  # 添加shell=True
        
        if generate_result.returncode == 0:
            print("报告生成成功！")
            # 打开报告
            subprocess.run([allure_cmd, 'open', 'Reports/html'], shell=True)
        else:
            print("报告生成失败！")
            print("错误信息:", generate_result.stderr)
        
    except FileNotFoundError as e:
        print(f"错误：未找到Allure命令行工具。请确保已安装Allure并添加到环境变量中。")
        print(f"详细错误：{str(e)}")
    except Exception as e:
        print(f"发生错误：{str(e)}")
        print("请确保已正确安装Node.js版本的allure-commandline：")
        print("npm install -g allure-commandline")

if __name__ == "__main__":
    run_tests()