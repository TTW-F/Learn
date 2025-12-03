#任务: 写一个 “质数判断工具”（输入数字，判断是否为质数）。
import math

#质数（也叫素数）指：大于 1 的整数，除了 1 和它自己，再也没有其他能整除它的数。
class Prime_number_judgment_tool:
    def __init__(self):
        pass
    def judge(self, num):
        if num == 2 or num == 3:
            print(num,"是素数")
            return
        if num <= 1:
            print("输入必须大于1")
            return
        if num % 2 == 0:
            print(num, "不是素数")
            return
        if num % 3 == 0:
            print(num,"不是素数")
            return
        #核心判断：检查到 num 的平方根
        max_divisor = int(math.sqrt(num))  # 取平方根，转成整数
        # 步长为2：只查奇数
        for i in range(5, max_divisor + 1, 2):
            if num % i == 0:  # 能被其他数整除，不是素数
                print(num, "不是素数")
                return

        # 所有情况都检查完，没找到其他因数 → 是素数
        print(num, "是素数")



if __name__ == "__main__":
    print("🎉 素数判断工具")
    # 创建类的实例
    prime_tool = Prime_number_judgment_tool()
    while True:
        # 让用户输入数字
        user_input = input("请输入一个整数：")
        # 退出条件
        if user_input.lower() in ['q', 'quit']:
            print("👋 再见！")
            break
        try:
            num = int(user_input)  # 把输入转成整数
        except:
            print("❌ 错误：请输入合法的整数（比如 2、7、10 等）\n")
            continue

        prime_tool.judge(num)
        print()