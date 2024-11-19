import json
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def get_average(file_path, input_method, input_text, input_type):
    game = game_var.get()
    gi_standard_char = ["莫娜", "琴", "迪盧克", "迪希雅", "七七", "提納里", "刻晴"] 
    hsr_standard_char = ["瓦爾特", "姬子", "彥卿", "布洛妮婭", "克拉拉", "白露", "傑帕德"] 
    gi_standard_weapon = ["阿莫斯之弓", "天空之翼", "和璞鳶", "天空之脊", "四風原典", "天空之卷", "狼的末路", "天空之傲", "風鷹劍", "天空之刃"] 
    hsr_standard_weapon = ["但戰鬥還未結束", "如泥酣眠", "以世界之名", "無可取代的東西", "銀河鐵道之夜", "時節不居", "致勝的瞬間"] 
    standard_char = gi_standard_char if game == "原神" else hsr_standard_char 
    standard_weapon = gi_standard_weapon if game == "原神" else hsr_standard_weapon

    characters, weapons, standard = [], [], []
    limit_char, limit_weapon = [], []

    category_map = {
        "standard": {"type": "200" if game == "原神" else "1", "list": standard},
        "character": {"type": ["301", "400"] if game == "原神" else ["11"], "list": characters, "limit_list": limit_char},
        "weapon": {"type": "302" if game == "原神" else "12", "list": weapons, "limit_list": limit_weapon}
    }

    if file_path:
        with open(file_path, "r", encoding="utf8") as file:
            data = json.load(file)

        if (data["list"][0]['gacha_type'] in ["200", "301", "400", "302"] and game == "崩鐵") or (data["list"][0]['gacha_type'] in ["1", "11", "12"] and game == "原神"):
            messagebox.showerror("Error", "導入錯誤的遊戲資料")
            return

        for item in data["list"]:
            for category, details in category_map.items():
                if (isinstance(details["type"], list) and item['gacha_type'] in details["type"]) or item['gacha_type'] == details["type"]:
                    details["list"].append(item['name'])
                    if category in ["character", "weapon"] and item['rank_type'] == "5" and item['name'] not in (standard_char if category == "character" else standard_weapon):
                        details["limit_list"].append(item['name'])

        result_text = (
        f"限定池抽數：{len(characters)}, 限定角色數：{len(limit_char)}, 平均限定金：{round(len(characters) / len(limit_char),2)}\n"
        f"武器池抽數：{len(weapons)}, 限定武器數：{len(limit_weapon)}, 平均限定金：{round(len(weapons) / len(limit_weapon),2)}\n"
        f"常駐池抽數：{len(standard)}"
    )
    

    else:
        items = input_text.split('\n')
        total = 0
        limit = []
        standard_items = standard_char if input_type == "角色" else standard_weapon
        for item in items:
            parts = re.findall(r'\D+|\d+', item.strip())
            if len(parts) == 2:
                name, count = parts[0], int(parts[1])
                total += count
                if name not in standard_items:
                    limit.append(name)

        result_text = (
        f"總抽數：{total}, 限定數：{len(limit)}, 平均限定金：{round(total / len(limit), 2)}"
    )

    result_label.config(text=result_text)

def select_file(game, input_method):
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        get_average(file_path, input_method, "", "")

def manual_input():
    input_method = input_method_var.get()
    input_text = manual_input_text.get("1.0", "end").strip()
    input_type = input_type_var.get()
    get_average("", input_method, input_text, input_type)

def choose_input_method():
    input_method = input_method_var.get()
    game = game_var.get()
    if game not in ["原神", "崩鐵"]:
        messagebox.showerror("Error", "請選擇有效的遊戲名稱（原神或崩鐵）")
        return
    if input_method == "手動輸入":
        manual_input_frame.pack(pady=10)
        start_button.pack_forget()
    else:
        manual_input_frame.pack_forget()
        start_button.pack(pady=20)
        select_file(game, input_method)

root = tk.Tk()
root.title("Gacha Data Analysis")
root.geometry("800x600")  # 設置視窗大小
root.resizable(False, False)  # 禁止改變視窗大小

style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))
style.configure("TRadiobutton", font=("Arial", 12))

# 選擇遊戲名稱部分
game_frame = ttk.Frame(root)
game_frame.pack(pady=10)

ttk.Label(game_frame, text="請選擇遊戲名稱：").pack(side="left", padx=10)
game_var = tk.StringVar(value="原神")
ttk.Radiobutton(game_frame, text="原神", variable=game_var, value="原神").pack(side="left")
ttk.Radiobutton(game_frame, text="崩鐵", variable=game_var, value="崩鐵").pack(side="left")

# 添加分隔符
separator = ttk.Label(root, text="------------------------")
separator.pack(pady=10)

# 選擇輸入方式部分
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="請選擇輸入方式：").pack(side="left", padx=10)
input_method_var = tk.StringVar(value="選擇JSON檔案")
ttk.Radiobutton(input_frame, text="手動輸入", variable=input_method_var, value="手動輸入", command=lambda: [manual_input_frame.pack(pady=10), start_button.pack_forget()]).pack(side="left")
ttk.Radiobutton(input_frame, text="選擇JSON檔案", variable=input_method_var, value="選擇JSON檔案", command=lambda: [manual_input_frame.pack_forget(), start_button.pack(pady=20)]).pack(side="left")

manual_input_frame = ttk.Frame(root)

ttk.Label(manual_input_frame, text="請選擇類型：").pack(side="left", padx=10)
input_type_var = tk.StringVar(value="角色")
ttk.Radiobutton(manual_input_frame, text="角色", variable=input_type_var, value="角色").pack(side="left")
ttk.Radiobutton(manual_input_frame, text="武器", variable=input_type_var, value="武器").pack(side="left")

# 新增的提示行
ttk.Label(manual_input_frame, text="每個角色/武器以下列格式輸入 '角色名稱 抽數'").pack()

manual_input_text = tk.Text(manual_input_frame, height=10, width=50)
manual_input_text.pack(pady=10)
manual_input_text.insert("1.0", "")

ttk.Button(manual_input_frame, text="計算", command=manual_input).pack(pady=10)

start_button = ttk.Button(root, text="開始", command=choose_input_method)
start_button.pack(pady=20)

result_label = ttk.Label(root, text="", justify="left")
result_label.pack(pady=10, side=tk.BOTTOM, anchor="s")

root.mainloop()
