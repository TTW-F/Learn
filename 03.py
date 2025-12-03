#任务: 判断水仙花数。
#水仙花数是指 一个 n 位整数，它的每个位上的数字的 n 次幂之和，等于它本身。


class NarcissisticNumberTool:
    def __init__(self):
        pass
    def is_narcissistic(self, num):
        """
        判断单个数字是不是水仙花数
        参数 num：要判断的整数
        返回：True（是）/ False（不是）
        """
        # 第一步：排除负数和0-9的个位数（水仙花数是n≥3位的整数）
        if num < 100:
            return False

        # 第二步：把数字转成字符串，获取每一位数字
        num_str = str(num)
        n = len(num_str)  # 获取数字的位数（n位）

        # 第三步：计算每一位数字的n次幂之和
        total = 0
        for digit_char in num_str:
            digit = int(digit_char)  # 把字符转成数字（比如 '5' → 5）
            total += digit ** n  # 计算n次幂，累加到总和

        # 第四步：判断总和是否等于原数字
        return total == num

    def find_narcissistic_in_range(self, start, end):
        """
        查找[start, end]范围内的所有水仙花数
        参数：start（范围开始）、end（范围结束）
        返回：水仙花数列表
        """
        narcissistic_list = []
        # 遍历范围内的每个整数
        for num in range(start, end + 1):
            if self.is_narcissistic(num):
                narcissistic_list.append(num)
        return narcissistic_list


if __name__ == "__main__":
    print("🎉 水仙花数判断工具")
    print("📌 水仙花数定义：n位整数，每位数字的n次幂之和 = 本身（n≥3）")
    print("📌 功能选项：")
    print("   1. 判断单个数字是不是水仙花数")
    print("   2. 查找指定范围内的所有水仙花数")
    print("🔚 输入 'q' 或 'quit' 退出")
    print("-" * 50)

    # 创建工具实例
    narc_tool = NarcissisticNumberTool()

    while True:
        # 选择功能
        choice = input("请选择功能（输入 1 或 2）：")

        # 退出条件
        if choice.lower() in ['q', 'quit']:
            print("👋 再见！")
            break

        # 功能1：判断单个数字
        if choice == '1':
            user_input = input("请输入一个整数：")
            try:
                num = int(user_input)
            except:
                print("❌ 错误：请输入合法的整数！\n")
                continue

            if narc_tool.is_narcissistic(num):
                print(f"✅ {num} 是水仙花数！\n")
            else:
                print(f"❌ {num} 不是水仙花数（或小于3位）！\n")

        # 功能2：查找范围内的水仙花数
        elif choice == '2':
            print("请输入查找范围（比如 100 999 查找3位水仙花数）")
            start_input = input("范围开始：")
            end_input = input("范围结束：")

            try:
                start = int(start_input)
                end = int(end_input)
            except:
                print("❌ 错误：请输入合法的整数！\n")
                continue

            # 确保范围合法（开始≤结束，且至少从100开始）
            if start > end:
                print("❌ 错误：范围开始不能大于结束！\n")
                continue
            if end < 100:
                print("❌ 错误：水仙花数至少是3位数，请输入≥100的范围！\n")
                continue

            # 查找并输出结果
            result = narc_tool.find_narcissistic_in_range(start, end)
            if result:
                print(f"✅ 在 [{start}, {end}] 范围内的水仙花数有：{result}\n")
            else:
                print(f"❌ 在 [{start}, {end}] 范围内没有找到水仙花数！\n")

        # 输入无效功能
        else:
            print("❌ 错误：请输入 1 或 2 选择功能！\n")