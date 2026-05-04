import os
import csv
import shutil
import random
import pandas as pd
import gradio as gr

EN_US = os.getenv("LANG") != "zh_CN.UTF-8"
TMP_DIR = os.path.join(os.path.dirname(__file__), "__pycache__")
ZH2EN = {
    "输入参与者数量": "Number of participants",
    "输入分组比率 (格式为用:隔开的数字，生成随机分组数据)": "Grouping ratio (numbers separated by : to generate randomized controlled trial)",
    "状态栏": "Status",
    "下载随机分组数据 CSV": "Download data CSV",
    "随机分组数据预览": "Data preview",
    "随机对照试验生成": "RCT Generator",
}


def _L(zh_txt: str):
    return ZH2EN[zh_txt] if EN_US else zh_txt


def list_to_csv(list_of_dicts: list, filename: str):
    keys = dict(list_of_dicts[0]).keys()
    # 将列表中的字典写入 CSV 文件
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for data in list_of_dicts:
            writer.writerow(data)


def random_allocate(participants: int, ratio: list, out_csv: str):
    splits = [0]
    total = sum(ratio)
    for i, r in enumerate(ratio):
        splits.append(splits[i] + int(1.0 * r / total * participants))

    splits[-1] = participants
    partist = list(range(1, participants + 1))
    random.shuffle(partist)
    allocation = []
    groups = len(ratio)
    for i in range(groups):
        start = splits[i]
        end = splits[i + 1]
        for participant in partist[start:end]:
            allocation.append({"id": participant, "group": i + 1})

    sorted_data = sorted(allocation, key=lambda x: x["id"])
    list_to_csv(sorted_data, out_csv)
    return out_csv, pd.DataFrame(sorted_data)


def clean_dir(dir_path: str):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

    os.makedirs(dir_path)


# outer func
def infer(participants: float, ratios: str, cache=TMP_DIR):
    ratio = []
    status = "Success"
    out_csv = previews = None
    try:
        ratio_list = ratios.split(":")
        clean_dir(cache)
        for r in ratio_list:
            current_ratio = float(r.strip())
            if current_ratio > 0:
                ratio.append(current_ratio)

        out_csv, previews = random_allocate(
            int(participants), ratio, f"{cache}/output.csv"
        )

    except Exception as e:
        status = f"{e}"

    return status, out_csv, previews


def main():
    return gr.Interface(
        fn=infer,
        inputs=[
            gr.Number(label=_L("输入参与者数量"), value=10),
            gr.Textbox(
                label=_L("输入分组比率 (格式为用:隔开的数字，生成随机分组数据)"),
                value="8:1:1",
            ),
        ],
        outputs=[
            gr.Textbox(label=_L("状态栏"), buttons=["copy"]),
            gr.File(label=_L("下载随机分组数据 CSV")),
            gr.Dataframe(label=_L("随机分组数据预览")),
        ],
        flagging_mode="never",
        title=_L("随机对照试验生成"),
    )


if __name__ == "__main__":
    main().launch(css="#gradio-share-link-button-0 { display: none; }", ssr_mode=False)
