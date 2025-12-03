#任务:写一个 “计算器”（支持加减乘除）；

# 定义计算器类
class SimpleCalculator:
    def __init__(self):
        # 定义运算符优先级：乘除（2）比加减（1）高
        self.operator_priority = {'+': 1, '-': 1, '*': 2, '/': 2}

    def is_valid_number(self, s):
        """判断输入的字符串是不是合法数字（整数或小数）"""
        try:
            float(s)  # 尝试把字符串转成数字，成功就是合法的
            return True
        except:
            return False

    def infix_to_postfix(self, expression):
        """
        把表达式转成后缀
        比如 "1+2*3" 转成 ["1", "2", "3", "*", "+"]
        """
        postfix = []  # 存储转换后的后缀表达式
        operator_stack = []  # 临时存运算符的栈
        i = 0
        n = len(expression)

        while i < n:
            char = expression[i]
            # 1. 跳过空格（比如输入 "1 + 2" 也能识别）
            if char == ' ':
                i += 1
                continue
            # 2. 处理数字（包括小数）
            if char.isdigit() or char == '.':
                num_str = ''  # 用来拼接数字字符
                # 把连续的数字/小数点拼起来（比如 "3.14" 是一个完整数字）
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                postfix.append(num_str)  # 数字直接加入后缀表达式
                continue
            # 3. 处理左括号 "("，直接入栈
            if char == '(':
                operator_stack.append(char)
                i += 1
                continue
            # 4. 处理右括号 ")"，把栈里的运算符弹出来，直到遇到左括号
            if char == ')':
                found_left_bracket = False
                while operator_stack:
                    top_op = operator_stack.pop()  # 弹出栈顶运算符
                    if top_op == '(':
                        found_left_bracket = True
                        break
                    postfix.append(top_op)  # 运算符加入后缀表达式
                if not found_left_bracket:  # 没找到左括号，说明括号不匹配
                    return None, "错误：括号不匹配（少了左括号 '('）"
                i += 1
                continue
            # 5. 处理加减乘除运算符
            if char in self.operator_priority:
                # 把栈里优先级比当前运算符高/相等的，弹出来加入后缀表达式
                while (operator_stack and operator_stack[-1] != '(' and
                       self.operator_priority[operator_stack[-1]] >= self.operator_priority[char]):
                    postfix.append(operator_stack.pop())
                operator_stack.append(char)  # 当前运算符入栈
                i += 1
                continue
            # 6. 遇到不认识的字符（比如字母、特殊符号）
            return None, f"错误：有不认识的字符 '{char}'（只能输入数字、+-*/、括号）"
        # 7. 把栈里剩下的运算符全部弹出来
        while operator_stack:
            top_op = operator_stack.pop()
            if top_op == '(':  # 栈里还有左括号，说明括号不匹配
                return None, "错误：括号不匹配（少了右括号 ')'）"
            postfix.append(top_op)
        return postfix, ""  # 成功，返回后缀表达式和空错误信息
    def calculate_postfix(self, postfix):
        """
        计算后缀表达式的结果
        比如 ["1", "2", "3", "*", "+"] 计算过程：2*3=6，再 1+6=7
        """
        result_stack = []  # 存储计算过程的数字
        for token in postfix:
            if self.is_valid_number(token):  # 是数字就入栈
                result_stack.append(float(token))
            else:  # 是运算符，弹出两个数字计算
                if len(result_stack) < 2:  # 数字不够，说明表达式错了
                    return None, "错误：表达式写错了（比如 '1+' 这种）"
                num2 = result_stack.pop()  # 后弹出来的是第二个运算数（比如 1+2，先弹2）
                num1 = result_stack.pop()  # 先弹出来的是第一个运算数（再弹1）
                # 根据运算符计算
                if token == '+':
                    result = num1 + num2
                elif token == '-':
                    result = num1 - num2
                elif token == '*':
                    result = num1 * num2
                elif token == '/':
                    if num2 == 0:
                        return None, "错误：除数不能是0！"
                    result = num1 / num2
                result_stack.append(result)  # 计算结果入栈
        # 栈里最后应该只剩一个结果
        if len(result_stack) != 1:
            return None, "错误：表达式格式错了（比如 '1+2*'）"
        return result_stack[0], ""
    def calculate(self, expression):
        """对外提供的计算接口：输入表达式，返回结果或错误信息"""
        # 第一步：中缀转后缀
        postfix, error = self.infix_to_postfix(expression)
        if error:  # 转换出错，返回错误信息
            return error
        if not postfix:  # 转换失败
            return "错误：表达式无法识别"
        # 第二步：计算后缀表达式
        result, error = self.calculate_postfix(postfix)
        if error:  # 计算出错，返回错误信息
            return error

        # 处理结果：如果是整数（比如 7.0），转成整数显示；否则保留小数
        return int(result) if result.is_integer() else round(result, 6)


# ------------------- 小白怎么用？看这里！-------------------
if __name__ == "__main__":
    print("🎉 计算器（支持 +-*/ 和括号）")
    print("📌 示例：1+2*3、(1+2)*3、3.14+5.28、10/2-3")
    print("🔚 输入 'q' 或 'quit' 退出")
    print("-" * 50)

    calc = SimpleCalculator()  # 创建计算器实例
    while True:
        # 让用户输入表达式
        user_input = input("请输入计算表达式：")

        # 退出条件
        if user_input.lower() in ['q', 'quit']:
            print("👋 再见！")
            break

        # 调用计算器计算
        result = calc.calculate(user_input)

        # 输出结果
        print(f"结果：{result}\n")






