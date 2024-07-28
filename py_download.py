import os
import random
import threading
import time
import tkinter as tk

import requests


class DownloaderGUI:
    def __init__(self, master):
        self.master = master
        master.title("资源下载器")
        master.resizable(False, False)  # 设置窗口不可最大化
        master.geometry("730x500")  # 设置窗口初始大小

        # 创建URL输入框和标签
        self.url_label = tk.Label(master, text="下载资源链接:")
        self.url_label.grid(row=0, column=0, sticky="w", padx=10, pady=0)
        self.url_input = tk.Text(master, height=20, width=100)
        self.url_input.grid(row=1, column=0, padx=10, pady=0)

        # 创建代理输入框和标签
        self.proxy_label = tk.Label(master, text="代理:")
        self.proxy_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.proxy_entry = tk.Entry(master, width=77)
        self.proxy_entry.insert(0, "http://127.0.0.1:6152")
        self.proxy_entry.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # 创建线程数输入框和标签
        self.threads_label = tk.Label(master, text="线程:")
        self.threads_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.threads_entry = tk.Entry(master, width=77)
        self.threads_entry.insert(0, "5")
        self.threads_entry.grid(row=5, column=0, sticky="w", padx=10, pady=5)

        # 创建下载按钮
        self.download_button = tk.Button(master, text="Download", command=self.start_download)
        self.download_button.grid(row=6, column=0, pady=5)

        # 创建状态栏
        self.status_label = tk.Label(master, text="")
        self.status_label.grid(row=7, column=0, pady=0)

    def start_download(self):
        threading.Thread(target=self.download).start()

    def download(self):
        urls = [url.strip() for url in self.url_input.get("1.0", tk.END).splitlines()]
        proxy = self.proxy_entry.get()
        threads = int(self.threads_entry.get())

        proxies = {
            'http': proxy,
            'https': proxy
        }

        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        ]

        # 启动多个线程下载文件
        threads_list = []
        for url in urls:
            thread = threading.Thread(target=self.download_url, args=(url, proxies, user_agents))
            thread.start()
            threads_list.append(thread)

        for thread in threads_list:
            thread.join()

        self.status_label.config(text="下载完毕！！！！")

    def download_url(self, url, proxies, user_agents):
        headers = {'User-Agent': random.choice(user_agents)}
        try:
            response = requests.get(url, headers=headers, proxies=proxies)
            file_name = os.path.basename(url)
            file_path = os.path.join("./", file_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            self.status_label.config(text=f"Downloaded {file_name}")
        except Exception as e:
            self.status_label.config(text=f"Error downloading {url}: {e}")
        time.sleep(3)


root = tk.Tk()
app = DownloaderGUI(root)
root.mainloop()
