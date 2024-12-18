import os

chat_language = os.getenv("INIT_LANGUAGE", default = "zh")

MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default = 7))
LANGUAGE_TABLE = {
  "zh": "哈囉！",
  "en": "Hello!"
}

# 使用環境變數來設置 AI_GUIDELINES，如果沒有設置則使用默認值
AI_GUIDELINES = os.getenv("AI_GUIDELINES", '你是一個AI助教，會用蘇格拉底教學法代替老師初步回應，如果有需要會提醒學生跟老師確認')

class Prompt:

    default_guideline = AI_GUIDELINES  # 動態管理規則

    def __init__(self):
        self.msg_list = []
        self.msg_list.append(
            {
                "role": "system", 
                "content": f"{LANGUAGE_TABLE[chat_language]}, {AI_GUIDELINES})"
             })    

    def add_msg(self, new_msg):
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            # 確保不刪除第一個系統訊息，改為刪除第二個訊息
            self.msg_list.pop(1)
        self.msg_list.append({"role": "user", "content": new_msg})

    def generate_prompt(self):
        return self.msg_list

    def reinit_(self, new_guideline=None):
        # 更新 default_guideline
        if new_guideline:
            Prompt.default_guideline = new_guideline
        # 重新初始化系統訊息
        self.msg_list[0] = {
            "role": "system",
            "content": f"{LANGUAGE_TABLE[chat_language]}, {Prompt.default_guideline}"
        }
        # 清空所有非系統訊息
        self.msg_list = [self.msg_list[0]]
