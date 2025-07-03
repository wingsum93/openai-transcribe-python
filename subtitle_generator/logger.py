import os
import datetime

class Logger:
    def __init__(self, log_folder="logs"):
        self.log_folder = log_folder
        self.action_timings = {}  # 儲存動作開始時間
        self.current_log_file = None

    def get_log_file_name(self):
        now = datetime.datetime.now()
        file_name = f"{now.year}-{now.month}-{now.day}.log"
        return os.path.join(self.log_folder, file_name)

    def ensure_log_file_exists(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        if self.current_log_file is None:
            self.current_log_file = self.get_log_file_name()
        if not os.path.exists(self.current_log_file):
            with open(self.current_log_file, 'w', encoding='utf-8') as file:
                pass  # 建立空白檔案
    
    def addLog(self, message):
        try:
            self.ensure_log_file_exists()
            with open(self.current_log_file, 'a', encoding='utf-8') as file:
                now = datetime.datetime.now()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"[{timestamp}] {message}"
                file.write(log_entry + '\n')
            print(f'✅ 已紀錄：{message}')
        except Exception as e:
            print(f'❌ 記錄日誌時出錯：{str(e)}')

    def logStartAction(self, action_name):
        start_time = datetime.datetime.now()
        self.action_timings[action_name] = start_time  # 存储开始时间
        message = f"開始動作「{action_name}」，時間：{start_time.strftime('%Y-%m-%d %H:%M:%S')}"
        self.addLog(message)

    def logEndAction(self, action_name):
        end_time = datetime.datetime.now()
        start_time = self.action_timings.get(action_name)
        if start_time:
            duration = end_time - start_time
            message = (
                f"完成動作「{action_name}」，時間：{end_time.strftime('%Y-%m-%d %H:%M:%S')}，"
                f"耗時：{duration}"
            )
            self.addLog(message)
        else:
            print(f"⚠️ 無法找到「{action_name}」嘅開始時間，無法紀錄耗時")

# 示例用法：
if __name__ == "__main__":
    # 创建 Logger 实例，默认使用"logs"文件夹
    logger = Logger()

    # 记录开始动作和结束动作
    logger.logStartAction("动作1")
    # 执行动作1的代码
    logger.logEndAction("动作1")

    logger.logStartAction("动作2")
    # 执行动作2的代码
    logger.logEndAction("动作2")
