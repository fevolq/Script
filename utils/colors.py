#!-*- coding:utf-8 -*-
# python3.7
# CreateTime: 2022/11/4 18:06
# FileName: 颜色

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(30, 38)

# 加颜色函数
colorfy = lambda bold, color, target: "\033[%d;%dm%s\033[0m" % (bold, color, target)

# 高亮颜色函数
black = lambda target: colorfy(1, BLACK, target)
red = lambda target: colorfy(1, RED, target)
green = lambda target: colorfy(1, GREEN, target)
yellow = lambda target: colorfy(1, YELLOW, target)
blue = lambda target: colorfy(1, BLUE, target)
magenta = lambda target: colorfy(1, MAGENTA, target)
cyan = lambda target: colorfy(1, CYAN, target)
white = lambda target: colorfy(1, WHITE, target)

# 普通颜色函数
normal_black = lambda target: colorfy(0, BLACK, target)
normal_red = lambda target: colorfy(0, RED, target)
normal_green = lambda target: colorfy(0, GREEN, target)
normal_yellow = lambda target: colorfy(0, YELLOW, target)
normal_blue = lambda target: colorfy(0, BLUE, target)
normal_magenta = lambda target: colorfy(0, MAGENTA, target)
normal_cyan = lambda target: colorfy(0, CYAN, target)
normal_white = lambda target: colorfy(0, WHITE, target)

if __name__ == '__main__':
    print(red('hello'))
    pass
