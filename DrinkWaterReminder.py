# encoding=utf-8
"""
A water drinking reminder tool designed to help users hydrate regularly.
"""
import tkinter as tk
import time

# 全局变量配置
FONT_SIZE = 28  # 字号大小
TIMER_INTERVAL = 60 * 25  # 计时时间，单位为秒

# 创建一个根窗口
root = tk.Tk()
root.title("water drinking reminder")

# 移除窗口的标题栏
root.overrideredirect(True)

# 设置窗口背景为黑色
root.configure(bg="black")

# 创建一个标签来显示时间，设置文字为白色，字号为全局变量指定的大小
time_label = tk.Label(root, text="00:00:00", font=("Arial", FONT_SIZE), bg="black", fg="white")
time_label.pack()

# 初始化开始时间和暂停状态
start_time = time.time()
paused = False
pause_time = 0  # 暂停时刻的时间
time_adjustment = 0  # 时间调整，以秒为单位


# 定义一个函数来更新时间
def update_time():
    if not paused:
        # 计算经过的时间
        elapsed_time = time.time() - start_time + time_adjustment
        # 将时间格式化为 H:M:S
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        # 更新标签文本
        time_label.config(text=formatted_time)
        # 如果超过设定的计时时间，则将文本颜色更改为橙色
        if elapsed_time > TIMER_INTERVAL:
            time_label.config(fg="orange")
        else:
            time_label.config(fg="white")
    # 安排函数在100毫秒后再次调用
    root.after(100, update_time)


# 定义一个函数来重置计时器
def reset_timer(event):
    global start_time, time_adjustment
    start_time = time.time()
    time_adjustment = 0
    time_label.config(fg="white")


# 定义一个函数来调整计时器时间
def adjust_time(event):
    global time_adjustment
    if event.keysym == "plus":
        time_adjustment += 60
    elif event.keysym == "minus":
        time_adjustment -= 60


# 定义一个函数来暂停计时器
def pause_timer(event):
    global paused, pause_time, start_time
    if not paused:
        # 暂停计时器并记录暂停时刻
        paused = True
        pause_time = time.time()
    else:
        # 恢复计时器并调整开始时间
        paused = False
        start_time += time.time() - pause_time
    # 根据暂停状态设置窗口是否置顶
    root.attributes("-topmost", not paused)


# 定义一个函数来退出程序
def exit_program(event):
    root.destroy()


# 定义一个函数来移动窗口
def start_move(event):
    global x, y
    x = event.x
    y = event.y


def stop_move(event):
    global x, y
    x = None
    y = None


def on_move(event):
    global x, y
    deltax = event.x - x
    deltay = event.y - y
    x0 = root.winfo_x() + deltax
    y0 = root.winfo_y() + deltay
    root.geometry(f"+{x0}+{y0}")


# 绑定事件
root.bind("<Key-Escape>", exit_program)
root.bind("<Key-space>", pause_timer)
root.bind("<Key-plus>", adjust_time)
root.bind("<Key-minus>", adjust_time)
root.bind("<Key-Return>", reset_timer)  # 绑定Enter键到reset_timer函数
root.bind("<ButtonPress-1>", start_move)
root.bind("<ButtonRelease-1>", stop_move)
root.bind("<B1-Motion>", on_move)

# 设置窗口固定置于顶层
root.attributes("-topmost", True)


if __name__ == "__main__":

    # 开始时间更新循环
    update_time()

    # 运行主循环
    root.mainloop()

    pass
