#!/usr/bin/env python3
"""根据 summary.json 生成 DOCX 提案；无实测数据时输出“待实测”占位。"""
import argparse
import json
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


def style_font(style, size=10.5):
    style.font.name = "Times New Roman"
    style.font.size = Pt(size)
    rfonts = style.element.get_or_add_rPr().get_or_add_rFonts()
    rfonts.set(qn("w:eastAsia"), "宋体")


def heading_font(paragraph):
    for run in paragraph.runs:
        run.font.name = "Times New Roman"
        run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "黑体")


def add_table(doc, headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    for index, header in enumerate(headers):
        cell = table.rows[0].cells[index]
        cell.text = str(header)
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.bold = True
    for row in rows:
        cells = table.add_row().cells
        for index, value in enumerate(row):
            cells[index].text = "" if value is None else str(value)
    return table


def fmt(value, digits=3):
    return "待实测" if value is None else f"{value:.{digits}f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", default="results/summary.json")
    ap.add_argument("--chart", default="results/psnr_chart.png")
    ap.add_argument("--output", default="proposal_file/ASC26_Task2_Proposal.docx")
    ap.add_argument("--team", default="TeamName")
    ap.add_argument("--colab-link", default="待填写")
    args = ap.parse_args()

    summary_path = Path(args.summary)
    data = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else []

    doc = Document()
    style_font(doc.styles["Normal"])
    for name in ("Heading 1", "Heading 2", "Title"):
        if name in doc.styles:
            style_font(doc.styles[name], 14 if name != "Title" else 18)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("ASC26 赛题二：具身世界模型推理优化与复现")
    run.bold = True
    run.font.size = Pt(18)
    run._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "黑体")

    team = doc.add_paragraph()
    team.alignment = WD_ALIGN_PARAGRAPH.CENTER
    team.add_run(f"参赛队伍：{args.team}    Colab 链接：{args.colab_link}")

    doc.add_heading("一、复现目标", level=1)
    heading_font(doc.paragraphs[-1])
    doc.add_paragraph(
        "基于 UnifoLM-WMA-0 世界模型，选择 unitree_z1_dual_arm_cleanup_pencils 与 "
        "unitree_z1_dual_arm_stackbox 两个场景，每个场景 4 个 case，复现官方推理流程；"
        "在保证每个样本 PSNR ≥ 25 的前提下压缩推理时间，并对比优化前后的单样本推理耗时。"
    )

    doc.add_heading("二、实验环境", level=1)
    heading_font(doc.paragraphs[-1])
    add_table(
        doc,
        ["项目", "配置"],
        [
            ["算力平台", "Colab GPU（待填写具体型号）"],
            ["操作系统 / 运行时", "Linux + Python 3.10 + PyTorch (CUDA)"],
            ["模型仓库", "unitreerobotics/unifolm-world-model-action"],
            ["模型权重", "unitreerobotics/UnifoLM-WMA-0-Dual"],
            ["输入数据", "ASC-Competition/ASC26-Embodied-World-Model-Optimizations"],
            ["评测指标", "单样本推理时间、PSNR（阈值 25）"],
        ],
    )

    doc.add_heading("三、复现流程", level=1)
    heading_font(doc.paragraphs[-1])
    for text in [
        "1. 克隆官方仓库并按 README 安装依赖；",
        "2. 通过 HuggingFace 下载 UnifoLM-WMA-0-Dual 权重；",
        "3. 下载 5 个场景、20 个样本的初始条件与参考视频，放置到仓库目录，并在 configs/inference/world_model_interaction.yaml 中设置 data_dir 绝对路径；",
        "4. 执行 bash {scenario}/{case_id}/run_world_model_interaction.sh，从输出日志读取 real time 作为单样本推理时间；",
        "5. 使用 PSNR 评估脚本对比生成视频与参考视频，逐样本记录 PSNR。",
    ]:
        doc.add_paragraph(text)

    doc.add_heading("四、优化方法", level=1)
    heading_font(doc.paragraphs[-1])
    doc.add_paragraph(
        "优化点：将扩散采样步数从官方默认值降低到 25 步，并将 ddim_eta 设为 0（确定性 DDIM 采样）。"
        "采样步数是视频生成推理的主要计算开销来源，减少步数可以线性压缩 UNet 前向次数；"
        "通过 PSNR ≥ 25 的约束确认画质损失在可接受范围内。"
    )
    doc.add_paragraph(
        "实现方式：code/prepare_opt_config.py 读取官方配置，自动定位采样步数字段并生成 "
        "world_model_interaction_opt.yaml；run_case.sh 在 optimized 模式下临时替换官方配置，"
        "运行结束后恢复原配置，保证 baseline 与 optimized 使用同一套代码和输入。"
    )
    doc.add_paragraph(
        "未计入结果的后续优化方向：torch.compile、FP16/FP8 推理、xformers 注意力、帧分块推理。"
        "这些方案需要修改模型代码，须在真实权重上验证 PSNR 后再纳入对比。"
    )

    doc.add_heading("五、推理时间对比", level=1)
    heading_font(doc.paragraphs[-1])
    time_rows = []
    for item in data:
        before = item.get("time_before_optim")
        after = item.get("time_after_optim")
        speedup = f"{before / after:.2f}×" if before and after else "待实测"
        time_rows.append([
            item.get("scenario", ""),
            f'case{item.get("case_id")}',
            fmt(before),
            fmt(after),
            speedup,
        ])
    if not time_rows:
        time_rows = [["待实测", "待实测", "待实测", "待实测", "待实测"]]
    add_table(doc, ["场景", "样本", "优化前(s)", "优化后(s)", "加速比"], time_rows)

    doc.add_heading("六、PSNR 评估", level=1)
    heading_font(doc.paragraphs[-1])
    psnr_rows = []
    for item in data:
        psnr = item.get("psnr")
        passed = "待实测" if psnr is None else ("是" if psnr >= 25 else "否")
        psnr_rows.append([item.get("scenario", ""), f'case{item.get("case_id")}', fmt(psnr, 4), passed])
    if not psnr_rows:
        psnr_rows = [["待实测", "待实测", "待实测", "待实测"]]
    add_table(doc, ["场景", "样本", "PSNR(dB)", "是否 ≥ 25"], psnr_rows)

    chart = Path(args.chart)
    if chart.exists():
        doc.add_paragraph("各样本 PSNR（红色虚线为 25 分阈值）：")
        doc.add_picture(str(chart), width=Cm(16))
    else:
        doc.add_paragraph("PSNR 可视化图表待实测数据生成（code/plot_psnr.py）。")

    doc.add_heading("七、结论与后续工作", level=1)
    heading_font(doc.paragraphs[-1])
    doc.add_paragraph(
        "当前仓库已完成可执行的复现与评测管线；真实推理需要权重与输入数据就位后在 Colab 上运行，"
        "并按 results/README.md 的要求回填日志、视频、summary.json 与 PSNR 图表。"
        "若任一样本 PSNR 低于 25，将回退采样步数或调整优化策略后重新评测。"
    )

    doc.add_heading("八、提交说明", level=1)
    heading_font(doc.paragraphs[-1])
    doc.add_paragraph(f"代码：submission/TeamName_worldmodel/code/")
    doc.add_paragraph(f"结果：submission/TeamName_worldmodel/results/（summary.json + 8 个 case 目录）")
    doc.add_paragraph(f"Colab 共享链接：{args.colab_link}")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    print(f"已生成 {output}")


if __name__ == "__main__":
    main()
