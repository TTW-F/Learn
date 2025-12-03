import re


class TextExtractorTool:
    def __init__(self):
        pass

    def extract_phone_numbers(self, text):
        """
        从文本中提取手机号
        规则：11位数字，以 13/14/15/17/18/19 开头
        返回：去重后的手机号列表
        """
        phone_pattern = r'1[3-9]\d{9}'
        phones = re.findall(phone_pattern, text)
        unique_phones = list(set(phones))
        return unique_phones

    def extract_emails(self, text):
        """
        从文本中提取邮箱
        规则：支持 xxx@xxx.xxx 格式（字母、数字、下划线、点号、连字符）
        返回：去重后的邮箱列表
        """
        email_pattern = r'[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'
        emails = re.findall(email_pattern, text)
        unique_emails = list(set(emails))
        return unique_emails

    def extract_both(self, text):
        """
        同时提取手机号和邮箱
        返回：字典（包含手机号列表和邮箱列表）
        """
        phones = self.extract_phone_numbers(text)
        emails = self.extract_emails(text)
        return {
            "手机号": phones,
            "邮箱": emails
        }


# ------------------- 关键：下面的代码要和 class 同级缩进 -------------------
if __name__ == "__main__":
    print("🎉 文本提取工具（提取手机号/邮箱）")
    print("📌 支持格式：")
    print("   - 手机号：11位（13/14/15/17/18/19开头）")
    print("   - 邮箱：xxx@qq.com、xxx@gmail.com 等主流格式")
    print("🔚 输入 'q' 或 'quit' 退出")
    print("-" * 50)

    # 创建工具实例（现在类已经定义完了，能正常找到）
    extractor = TextExtractorTool()

    while True:
        # 让用户输入要提取的文本
        user_input = input("请输入要提取的文本（可包含手机号、邮箱）：")

        # 退出条件
        if user_input.lower() in ['q', 'quit']:
            print("👋 再见！")
            break

        # 避免用户输入空文本
        if not user_input.strip():
            print("❌ 错误：请输入有效的文本！\n")
            continue

        # 同时提取手机号和邮箱
        result = extractor.extract_both(user_input)

        # 输出结果（友好展示）
        print("\n📊 提取结果：")
        # 输出手机号
        if result["手机号"]:
            print(f"手机号：{', '.join(result['手机号'])}")
        else:
            print("手机号：未提取到")
        # 输出邮箱
        if result["邮箱"]:
            print(f"邮箱：{', '.join(result['邮箱'])}")
        else:
            print("邮箱：未提取到")
        print("-" * 50 + "\n")