"""Generate the bilingual case-study site into <profile repo>/docs."""
import html
import pathlib
import shutil
import sys

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[2] / "docs"
GH = "https://github.com/feizaodemon"
MTRI = f"{GH}/magnetic-trajectory-robot-interface"
DEMO = "https://feizaodemon.github.io/magnetic-trajectory-robot-interface/"

PAGES = ["index", "mtri", "gp", "job-tracker", "coursework"]

UI = {
    "en": {
        "lang": "en", "other": "zh", "other_label": "中文", "home": "Projects",
        "name": "Xiaowei Rong", "glance": "At a glance", "problem": "The problem",
        "how": "How it works", "decisions": "Key decisions", "results": "Results",
        "role": "My part", "limits": "Limits and what is next", "back": "All projects",
        "private": "Private repository. This page describes the work without the code.",
        "chosen": "Chosen", "instead": "Instead of", "cost": "Trade-off",
        "footer": "Every number on this site comes from the project's own repository. Where a repository does not record something, the page says so.",
        "read": "Read the case study",
    },
    "zh": {
        "lang": "zh-CN", "other": "en", "other_label": "English", "home": "项目",
        "name": "Xiaowei Rong", "glance": "概览", "problem": "要解决的问题",
        "how": "系统结构", "decisions": "关键设计决策", "results": "结果",
        "role": "我负责的部分", "limits": "局限与下一步", "back": "全部项目",
        "private": "私有仓库。本页只介绍工作内容，不公开代码。",
        "chosen": "选择", "instead": "放弃", "cost": "取舍",
        "footer": "本站所有数字都来自各项目自己的仓库；仓库里没有记录的内容，页面上会直接说明。",
        "read": "阅读案例",
    },
}


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- diagrams
class Diagram:
    def __init__(self, w, h, label):
        self.w, self.h, self.label, self.parts = w, h, label, []

    def box(self, x, y, w, h, title, sub="", kind="node"):
        self.parts.append(f'<rect class="d-{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>')
        cy = y + h / 2 + (-7 if sub else 5)
        self.parts.append(f'<text class="d-t" x="{x + w / 2}" y="{cy}" text-anchor="middle">{esc(title)}</text>')
        if sub:
            for i, line in enumerate(sub.split("\n")):
                self.parts.append(
                    f'<text class="d-s" x="{x + w / 2}" y="{cy + 18 + 15 * i}" text-anchor="middle">{esc(line)}</text>')

    def arrow(self, pts, kind="arr"):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        self.parts.append(f'<path class="d-{kind}" d="{d}" marker-end="url(#ah)"/>')

    def note(self, x, y, text, anchor="start", kind="d-n"):
        self.parts.append(f'<text class="{kind}" x="{x}" y="{y}" text-anchor="{anchor}">{esc(text)}</text>')

    def band(self, x, y, w, h, text):
        self.parts.append(f'<rect class="d-band" x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>')
        self.parts.append(f'<text class="d-k" x="{x + 14}" y="{y + 22}">{esc(text)}</text>')

    def svg(self):
        defs = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="d-head"/></marker></defs>')
        body = "".join(self.parts)
        return (f'<div class="diagram"><svg viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(self.label)}">'
                f'{defs}{body}</svg></div>')


def t(lang, en, zh):
    return en if lang == "en" else zh


def mtri_diagram(L):
    d = Diagram(960, 360, t(L, "MTRI architecture: task path with confirmation and teleop path through one Cartesian core",
                            "MTRI 结构：带确认的任务路径，以及经由同一笛卡尔核心的遥操作路径"))
    d.band(10, 10, 940, 190, t(L, "TASK mode · a recognized symbol runs a task", "TASK 模式 · 识别出的符号触发任务"))
    d.box(30, 70, 130, 70, t(L, "Board / mouse", "画板 / 鼠标"), t(L, "one stroke", "一笔轨迹"), "io")
    d.box(195, 70, 150, 70, t(L, "Recognizer", "识别节点"), t(L, "DTW bank +\nconfidence/margin gates", "DTW 模板库 +\n置信度/差距门限"))
    d.box(380, 70, 150, 70, t(L, "Dashboard", "仪表盘"), t(L, "operator presses\nC Confirm", "操作员按下\nC 确认"), "gate")
    d.box(565, 70, 150, 70, t(L, "Dispatcher", "调度节点"), t(L, "only publisher of\n/colmag/task_command", "唯一发布\n/colmag/task_command"), "gate")
    d.box(755, 40, 175, 56, t(L, "Gazebo bridge", "Gazebo 桥接"), t(L, "simulated Panda", "仿真 Panda"), "io")
    d.box(755, 114, 175, 56, t(L, "FR3 adapter (C++)", "FR3 适配器（C++）"), t(L, "allowlists, bounds, freshness", "白名单、限位、时效检查"), "io")
    d.arrow([(160, 105), (191, 105)])
    d.arrow([(345, 105), (376, 105)])
    d.arrow([(530, 105), (561, 105)])
    d.arrow([(715, 95), (735, 95), (735, 68), (751, 68)])
    d.arrow([(715, 115), (735, 115), (735, 142), (751, 142)])
    d.note(270, 168, t(L, "/colmag/symbol_candidates", "/colmag/symbol_candidates"), "middle")
    d.note(455, 168, t(L, "/colmag/confirmed_label", "/colmag/confirmed_label"), "middle")
    d.band(10, 215, 940, 135, t(L, "TELEOP mode · continuous Cartesian control", "TELEOP 模式 · 连续笛卡尔控制"))
    d.box(30, 260, 130, 70, t(L, "Keyboard / board", "键盘 / 画板"), t(L, "velocity or position", "速度或位置输入"), "io")
    d.box(195, 260, 335, 70, t(L, "Fr3CartesianTeleopCore (C++)", "Fr3CartesianTeleopCore（C++）"),
          t(L, "bounded targets · damped-least-squares IK\nworkspace and joint limits · finite-output checks",
            "有界目标 · 阻尼最小二乘逆运动学\n工作空间与关节限位 · 输出有限性检查"))
    d.box(565, 260, 365, 70, t(L, "Gazebo Panda  ·  Franka FR3", "Gazebo Panda  ·  Franka FR3"),
          t(L, "the same core drives both", "同一核心驱动两台机器人"), "io")
    d.arrow([(160, 295), (191, 295)])
    d.arrow([(530, 295), (561, 295)])
    return d.svg()


def gp_diagram(L):
    d = Diagram(960, 380, t(L, "GP torque compensation: online loop and offline staged programme",
                            "高斯过程力矩补偿：在线回路与离线分阶段实验流程"))
    d.band(10, 10, 940, 210, t(L, "In the controller (every cycle)", "控制器内（每个控制周期）"))
    d.box(30, 60, 150, 70, t(L, "Robot state", "机器人状态"), t(L, "7 joint positions +\n7 desired velocities", "7 个关节位置 +\n7 个期望速度"), "io")
    d.box(215, 45, 170, 50, t(L, "Per-joint GPs", "逐关节 GP"), t(L, "local / cloud-like", "本地 / 类云端"))
    d.box(215, 105, 170, 50, t(L, "Historical residual DB", "历史残差数据库"), t(L, "hist_db source", "hist_db 来源"))
    d.box(420, 60, 150, 70, t(L, "Source switch", "来源开关"), t(L, "GP or hist_db\nfrozen: no online update", "GP 或 hist_db\n冻结：关闭在线更新"), "gate")
    d.box(605, 60, 150, 70, t(L, "Scale × clip", "缩放 × 限幅"), t(L, "small scale, Nm clip\njoint 7 disabled", "小比例，按 Nm 限幅\n第 7 关节不补偿"), "gate")
    d.box(790, 60, 140, 70, t(L, "+ impedance τ", "+ 阻抗力矩"), t(L, "off by default", "默认关闭"), "io")
    d.arrow([(180, 85), (198, 85), (198, 70), (211, 70)])
    d.arrow([(180, 105), (198, 105), (198, 130), (211, 130)])
    d.arrow([(385, 70), (400, 70), (400, 88), (416, 88)])
    d.arrow([(385, 130), (400, 130), (400, 102), (416, 102)])
    d.arrow([(570, 95), (601, 95)])
    d.arrow([(755, 95), (786, 95)])
    d.note(30, 190, t(L, "Before any GP-on run: a 14-D joint-space support check, so the model is never asked to extrapolate.",
                      "每次开启 GP 之前：先做 14 维关节空间覆盖检查，避免模型外推。"))
    d.band(10, 235, 940, 135, t(L, "Around the lab (every stage)", "实验室之外（每个阶段）"))
    steps = [
        (t(L, "Plan", "计划"), t(L, "one question per stage", "每阶段只回答一个问题")),
        (t(L, "Sim first", "先仿真"), t(L, "MuJoCo + fake hardware", "MuJoCo + 假硬件")),
        (t(L, "Lab run", "真机实验"), t(L, "checklist, logged CSV", "检查清单，记录 CSV")),
        (t(L, "Offline analysis", "离线分析"), t(L, "scripts, not re-runs", "用脚本分析，不盲目重跑")),
        (t(L, "Report", "报告"), t(L, "result + caveats", "结果 + 局限说明")),
    ]
    x = 30
    for i, (a, b) in enumerate(steps):
        d.box(x, 280, 158, 64, a, b, "gate" if i == 3 else "node")
        if i < 4:
            d.arrow([(x + 158, 312), (x + 180, 312)])
        x += 184
    return d.svg()


def jt_diagram(L):
    d = Diagram(960, 340, t(L, "Job-search workbench architecture", "求职工作台结构"))
    d.box(30, 40, 200, 80, t(L, "Chrome extension (MV3)", "Chrome 扩展（MV3）"),
          t(L, "click → preview → save Job\nactiveTab · scripting · storage", "点击 → 预览 → 保存岗位\nactiveTab · scripting · storage"), "io")
    d.box(30, 190, 200, 80, t(L, "React web app", "React 网页"),
          t(L, "applications, timeline,\nimport, calendar", "投递、时间线、\n导入、日历"), "io")
    d.box(300, 100, 190, 110, t(L, "Fastify API", "Fastify API"),
          t(L, "34 /v1 routes\nZod contracts\none process serves\nAPI + built web", "34 个 /v1 路由\nZod 校验契约\n单进程同时提供\nAPI 与网页"))
    d.box(560, 100, 170, 110, t(L, "application · domain", "application · domain"),
          t(L, "domain: no DB,\nno framework\napplication: no HTTP", "domain 不依赖\n数据库和框架\napplication 不依赖 HTTP"))
    d.box(790, 60, 150, 190, t(L, "SQLite", "SQLite"),
          t(L, "jobs\napplications\n(current_status)\napplication_events\n\nsnapshot + event\nin one transaction", "jobs\napplications\n（current_status）\napplication_events\n\n快照与事件\n同一事务写入"), "gate")
    d.arrow([(230, 80), (265, 80), (265, 135), (296, 135)])
    d.arrow([(230, 230), (265, 230), (265, 175), (296, 175)])
    d.arrow([(490, 155), (556, 155)])
    d.arrow([(730, 155), (786, 155)])
    d.note(30, 312, t(L, "Runs on a private server, bound to 127.0.0.1 and reachable only over Tailscale; no public port.",
                      "部署在私有服务器上，只监听 127.0.0.1，仅能通过 Tailscale 访问，没有公网端口。"))
    d.note(232, 152, t(L, "saves Jobs only", "只保存岗位"), "start", "d-n")
    return d.svg()


def cw_diagram(L):
    d = Diagram(960, 360, t(L, "Coursework: teach-and-replay pipeline and RCM task-priority stack",
                            "课程项目：示教回放流程与远心点任务优先级结构"))
    d.band(10, 10, 940, 150, t(L, "Erasing by demonstration (Franka FR3)", "示教擦除（Franka FR3）"))
    steps = [
        (t(L, "Hand-guide", "手动拖动示教"), t(L, "gravity compensation", "重力补偿")),
        (t(L, "Record", "录制"), t(L, "ros2 bag → CSV\n13,833 samples / 13.8 s", "ros2 bag → CSV\n13,833 个采样 / 13.8 s")),
        (t(L, "Replay", "回放"), t(L, "τ = K(q_goal − q) − D·q̇", "τ = K(q_goal − q) − D·q̇")),
        (t(L, "Safety layer", "安全层"), t(L, "NaN → 0, clamp size\nand rate per joint", "NaN 置零，逐关节\n限制幅值和变化率")),
    ]
    x = 30
    for i, (a, b) in enumerate(steps):
        d.box(x, 55, 205, 80, a, b, "gate" if i == 3 else "node")
        if i < 3:
            d.arrow([(x + 205, 95), (x + 232, 95)])
        x += 232
    d.band(10, 175, 940, 175, t(L, "Remote center of motion (Franka FR3)", "远心点约束（Franka FR3）"))
    rows = [
        ("1", t(L, "RCM constraint: the tool must pass through the trocar point", "远心点约束：器械必须穿过套管点")),
        ("2", t(L, "Tool-tip tracking, in the null space of priority 1", "工具尖端跟踪，位于优先级 1 的零空间")),
        ("3", t(L, "Joint-limit centering, in the remaining null space", "关节限位居中，位于剩余零空间")),
    ]
    for i, (n, txt) in enumerate(rows):
        y = 210 + i * 42
        d.box(30, y, 40, 34, n, "", "gate")
        d.box(80, y, 560, 34, txt, "")
    d.box(670, 210, 260, 118, t(L, "8th virtual joint η", "第 8 个虚拟关节 η"),
          t(L, "insertion depth: moves the\ntrocar point, not the tip\nDLS damping 1e-3\nJacobians checked vs. finite diff.",
            "插入深度：移动套管点，\n不移动工具尖端\nDLS 阻尼 1e-3\n雅可比与有限差分对照测试"))
    return d.svg()


# ---------------------------------------------------------------- content
def chip(s):
    return f'<span class="chip">{s}</span>'


def stats(items):
    return '<div class="stats">' + "".join(
        f'<div class="stat"><div class="v">{v}</div><div class="k">{k}</div></div>' for v, k in items) + "</div>"


def decision(n, title, chosen, instead, cost, L):
    u = UI[L]
    return (f'<article class="dec"><div class="num">{n:02d}</div><div><h3>{title}</h3><dl>'
            f'<dt>{u["chosen"]}</dt><dd>{chosen}</dd><dt>{u["instead"]}</dt><dd>{instead}</dd>'
            f'<dt>{u["cost"]}</dt><dd>{cost}</dd></dl></div></article>')


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


PROJECTS = {}


def mtri(L):
    T = lambda en, zh: t(L, en, zh)
    return {
        "title": T("Magnetic Trajectory Robot Interface", "磁性轨迹机器人交互系统"),
        "kicker": T("Open source · live demo · ROS1 Noetic", "开源 · 在线演示 · ROS1 Noetic"),
        "lede": T("Draw a symbol on a magnetic board or with the mouse. The system recognizes it, the operator confirms it, and only then does the robot run the matching task.",
                  "在磁性画板上或用鼠标画一个符号，系统识别后由操作员确认，确认之后机器人才执行对应任务。"),
        "links": [(T("Try the recognizer", "在线试用识别器"), DEMO, True), (T("Source code", "源代码"), MTRI, False),
                  (T("Design decisions", "设计决策（英文）"), f"{MTRI}/blob/main/docs/DESIGN_DECISIONS.md", False)],
        "public": True,
        "stats": [("100%", T("leave-one-out Top-1 on the bank", "模板库留一法 Top-1")),
                  ("~83 ms", T("median per query, pure Python", "单次识别中位数，纯 Python")),
                  ("124 · 8", T("templates · symbols", "模板 · 符号")),
                  ("~495", T("pytest cases, plus C++ tests", "个 pytest 用例，另有 C++ 测试"))],
        "media": f'<figure><img src="{"../" if L == "zh" else ""}assets/mtri-task-gazebo.gif" alt="{T("A drawn 2 is recognized, confirmed, and the Gazebo robot runs the task", "画出的 2 被识别、确认，Gazebo 中的机器人执行任务")}" loading="lazy"><figcaption>{T("TASK mode in Gazebo: a mouse-drawn “2” is recognized, confirmed on the C dwell button, and the robot runs the mapped motion. Simulation, not hardware footage.", "Gazebo 中的 TASK 模式：鼠标画的“2”被识别，在 C 停留按钮上确认后，机器人执行对应动作。这是仿真画面，不是真机录像。")}</figcaption></figure>',
        "problem": T("<p>A gesture interface for a robot arm has two jobs that pull against each other. It should feel quick, but a wrong guess must never move the robot. The project also had to run the same way against a simulated Panda and a real Franka FR3, and keep working when the input came from a serial magnetic board instead of a mouse.</p>",
                     "<p>机械臂的手势交互有两个相互牵制的目标：要反应快，但识别错了绝不能让机器人动。同一套系统还要既能接 Gazebo 里的仿真 Panda，也能接真实的 Franka FR3，而且输入既可以是鼠标，也可以是串口磁性画板。</p>"),
        "diagram": mtri_diagram(L),
        "how": T("<p>Recognition, confirmation, dispatch and execution are four separate ROS nodes. The recognizer only publishes ranked candidates. The dashboard publishes a label only after the operator confirms it. The dispatcher maps that label to a fixed task vocabulary and is the only node that can command the robot. A second mode, TELEOP, sends keyboard or board input through one C++ Cartesian core that drives both robots.</p>",
                 "<p>识别、确认、调度、执行是四个独立的 ROS 节点。识别节点只发布排序后的候选；仪表盘只有在操作员确认后才发布标签；调度节点把标签映射到固定的任务表，并且是唯一能给机器人下指令的节点。另一个模式 TELEOP 把键盘或画板输入送进同一个 C++ 笛卡尔核心，由它驱动两台机器人。</p>"),
        "decisions": [
            (T("A DTW template bank, benchmarked against five alternatives", "DTW 模板库，并与 5 种替代方法对比"),
             T("Strokes are normalized, resampled to 64 points and ranked by DTW against 124 templates. Confidence and margin gates reject unclear input.", "笔迹归一化、重采样为 64 点后，与 124 个模板做 DTW 排序；置信度和差距门限拒绝不清楚的输入。"),
             T("Derivative DTW, windowed DTW, Protractor ($1), $P and feature k-NN, all implemented behind one interface and compared offline.", "导数 DTW、加窗 DTW、Protractor（$1）、$P、特征 k-NN，全部用同一接口实现并离线对比。"),
             T("On clean data every method scores 100%. Under synthetic noise and rotation Protractor matches or beats DTW at about 1/200 of the cost; DTW holds up better on truncated strokes. The runtime stayed on DTW, and the comparison is documented rather than hidden.", "干净数据上所有方法都是 100%。在合成噪声和旋转下，Protractor 与 DTW 持平或更好，耗时约为 1/200；截断笔迹上 DTW 更稳。运行时仍用 DTW，对比结果如实写进文档。")),
            (T("A human confirmation step between recognition and motion", "识别和运动之间必须有人确认"),
             T("Only the dispatcher publishes /colmag/task_command, and only after an explicit confirm. Candidates from an earlier sample cannot be confirmed for the current one.", "只有调度节点发布 /colmag/task_command，而且必须在明确确认之后；上一笔的候选不能被确认到当前这一笔上。"),
             T("Letting a confident recognizer trigger the task directly.", "让高置信度的识别结果直接触发任务。"),
             T("Every task costs one extra click. In exchange, a misrecognition cannot move the robot. Bad dispatcher configuration now stops the node instead of silently falling back to a default mapping.", "每个任务多一次点击，换来误识别无法单独让机器人运动。调度配置写错时节点会直接停止，而不是悄悄退回默认映射。")),
            (T("One C++ Cartesian core for simulation and hardware", "仿真和真机共用一个 C++ 笛卡尔核心"),
             T("Fr3CartesianTeleopCore owns target filtering, damped-least-squares IK, workspace and joint bounds, and finite-output checks. The Gazebo Panda and the FR3 adapter both link it.", "Fr3CartesianTeleopCore 负责目标滤波、阻尼最小二乘逆运动学、工作空间与关节限位、输出有限性检查；Gazebo Panda 和 FR3 适配器都链接它。"),
             T("Separate teleop code per backend.", "每个后端各写一套遥操作代码。"),
             T("Gazebo runs and the ROS-free C++ tests exercise the same code the FR3 route uses. Keyboard input was first routed through the board's point-to-point filter, which cruised at about 0.03 m/s and overshot about 11 cm on a direction change; it became a velocity command with acceleration and jerk limits.", "Gazebo 运行和不依赖 ROS 的 C++ 测试覆盖的就是 FR3 路线用的同一份代码。键盘输入最初走画板的点到点滤波，巡航速度约 0.03 m/s，换向时过冲约 11 cm；后来改成带加速度和加加速度限制的速度指令。")),
            (T("Mode ownership is not hardware authorization", "模式切换不等于授权硬件"),
             T("A latched TASK/TELEOP mode decides which path owns the command. Switching mode never starts a backend or enables physical commands, and invalid mode state fails closed.", "锁存的 TASK/TELEOP 模式只决定哪条路径拥有指令权；切换模式不会启动后端，也不会开启实机指令；模式状态无效时按关闭处理。"),
             T("A single “enable robot” toggle tied to the mode.", "用一个与模式绑定的“启用机器人”开关。"),
             T("More states to reason about, but the CI Gazebo smoke test checks the gating on every pull request: TASK rejects gripper commands, TELEOP moves, TASK rejects again.", "需要考虑的状态更多，但 CI 中的 Gazebo 冒烟测试每个 PR 都会验证：TASK 下拒绝夹爪指令，TELEOP 下可以运动，切回 TASK 再次拒绝。")),
        ],
        "results": T("""<table><thead><tr><th>Measure</th><th>Result</th></tr></thead><tbody>
<tr><td>Leave-one-out over 124 templates, 8 symbols</td><td>Top-1 100%, Top-3 100%</td></tr>
<tr><td>Queries accepted by the runtime gates</td><td>100%, all correct</td></tr>
<tr><td>Recognition time, pure-Python DTW</td><td>83 ms median, 118 ms p95, one core</td></tr>
<tr><td>Robustness, DTW vs. Protractor (noise σ=0.12 / 45° rotation / 30% truncation)</td><td>95.2 / 84.1 / 38.7% vs. 100 / 100 / 18.5%</td></tr>
<tr><td>Automated checks</td><td>about 495 pytest tests, 7 C++ test programs, CI with a headless Gazebo smoke test</td></tr>
</tbody></table>""", """<table><thead><tr><th>指标</th><th>结果</th></tr></thead><tbody>
<tr><td>124 个模板、8 个符号的留一法评测</td><td>Top-1 100%，Top-3 100%</td></tr>
<tr><td>通过运行时门限的查询</td><td>100%，全部正确</td></tr>
<tr><td>识别耗时（纯 Python DTW）</td><td>中位数 83 ms，p95 118 ms，单核</td></tr>
<tr><td>鲁棒性：DTW 对比 Protractor（噪声 σ=0.12 / 旋转 45° / 截断 30%）</td><td>95.2 / 84.1 / 38.7% 对比 100 / 100 / 18.5%</td></tr>
<tr><td>自动化检查</td><td>约 495 个 pytest 用例、7 个 C++ 测试程序，CI 含无界面 Gazebo 冒烟测试</td></tr>
</tbody></table>"""),
        "role": T("<p>The repository is my portfolio copy of a collaborative project. My parts: the board orientation clutch and the board and mouse profiles; the DTW recognition path, gates, tracked bank and evaluation tools; the shared dashboard and confirmation flow; integration of the dispatcher, Gazebo bridge and FR3 adapter; TASK/TELEOP ownership and the shared Cartesian core; Docker packaging, CI and tests; and the architecture, safety and validation docs.</p>",
                  "<p>这个仓库是一个合作项目的作品集版本。我负责的部分：画板的方向离合和画板/鼠标两套交互配置；DTW 识别路径、门限、模板库和评测工具；共用仪表盘和确认流程；调度节点、Gazebo 桥接和 FR3 适配器的集成；TASK/TELEOP 指令权和共用笛卡尔核心；Docker 打包、CI 和测试；以及架构、安全和验证文档。</p>"),
        "limits": ul([
            T("All 124 templates were drawn with a mouse by one person. The accuracy is an upper bound for one writer, not a measured accuracy for new users or for the magnetic board.", "124 个模板全部由同一个人用鼠标画出。准确率只是单人数据上的上限，不代表新用户或磁性画板上的实际准确率。"),
            T("The robustness perturbations are synthetic; real board error has not been recorded.", "鲁棒性评测里的扰动是合成的，还没有录制真实画板误差。"),
            T("The Real-FR3 adapters compile and are in the launch graph, but physical Real-FR3 TELEOP has not been run.", "真机 FR3 适配器能编译，也在 launch 图里，但真机 TELEOP 还没有实际运行过。"),
            T("Next: collect strokes from other writers and on the board, then re-run the same evaluation.", "下一步：收集其他人和画板上的笔迹，用同样的评测脚本重新测一遍。"),
        ]),
        "card": T("Gesture-to-task robot interface with a confirmation gate and one C++ teleop core for Gazebo and FR3.", "手势到任务的机器人交互：识别后需确认，一个 C++ 遥操作核心同时驱动 Gazebo 和 FR3。"),
        "card_stats": ["100% LOO Top-1", "~83 ms", T("live demo", "在线演示")],
    }


def gp(L):
    T = lambda en, zh: t(L, en, zh)
    return {
        "title": T("GP torque compensation", "高斯过程力矩补偿"),
        "kicker": T("Team research project · ROS 2 · Python", "团队科研项目 · ROS 2 · Python"),
        "lede": T("Learning the residual joint torque of a Franka Panda with Gaussian processes, and feeding a small, clipped share of the prediction back into an impedance controller.",
                  "用高斯过程学习 Franka Panda 的关节力矩残差，并把经过缩放和限幅的一小部分预测反馈给阻抗控制器。"),
        "links": [], "public": False,
        "stats": [("9", T("design decisions documented", "条设计决策有记录")),
                  ("Stage 1–5", T("plus GOAL1, GOAL2, GOAL12", "以及 GOAL1、GOAL2、GOAL12")),
                  ("14-D", T("support check before GP-on", "开启 GP 前的覆盖检查")),
                  ("0", T("compensation by default", "默认补偿量（默认关闭）"))],
        "media": "",
        "problem": T("<p>An impedance controller leaves a residual between the torque it expects and the torque the robot needs. A GP can predict part of that residual, but feeding a learned prediction into a torque loop on real hardware is risky, and an online-updating model makes any before/after comparison hard to attribute. The work was to make GP compensation testable on the real robot without losing control of the risk.</p>",
                     "<p>阻抗控制器预期的力矩和机器人实际需要的力矩之间存在残差。GP 可以预测其中一部分，但把学习到的预测送进真机的力矩回路有风险；而模型一边运行一边在线更新，就很难判断前后差异到底来自哪里。这项工作要做的，是让 GP 补偿在真机上变得可测试，同时把风险控制住。</p>"),
        "diagram": gp_diagram(L),
        "how": T("<p>The GP model, training pipeline and the original controller are earlier team work. On top of that, experiment switches pick the compensation source, freeze the model, and set a scale and an Nm clip; compensation is off unless a run turns it on. Each stage of testing has a written plan, a lab checklist, a run, an offline analysis script and a result summary.</p>",
                 "<p>GP 模型、训练流程和原始控制器是团队更早的工作。在此基础上，实验开关负责选择补偿来源、冻结模型、设置缩放比例和 Nm 限幅；只有某次实验明确打开时补偿才生效。每个测试阶段都有书面计划、实验检查清单、一次实验、离线分析脚本和结果总结。</p>"),
        "decisions": [
            (T("Evaluate a frozen GP behind explicit switches", "用显式开关评估冻结的 GP"),
             T("Switches for online update, model directory, compensation source, scale and clip. Test runs turn online update off.", "增加在线更新、模型目录、补偿来源、缩放和限幅等开关；测试时关闭在线更新。"),
             T("Testing with the original online-updating GP, whose model changes during the run being measured.", "直接用原来在线更新的 GP 测试，模型在被测的那次运行中不断变化。"),
             T("No adaptation during a run, but every on/off comparison is attributable to one fixed model. Default behaviour is unchanged.", "运行中不再自适应，但每次开/关对比都能归因到同一个固定模型；默认行为保持不变。")),
            (T("Small scale with a clip, raised one step at a time", "小比例加限幅，一步一步加大"),
             T("Start at a small scale with a tight Nm clip, at 50 Hz, and move up only after the previous step is stable.", "从小比例、严格的 Nm 限幅、50 Hz 开始，上一步稳定了才往上加。"),
             T("No-clip or unlimited GP-on runs.", "不限幅或不设上限地开启 GP。"),
             T("Slower progress and a small effect size, in exchange for staying inside a known torque bound.", "进展更慢、效果幅度更小，换来始终处在已知的力矩范围内。")),
            (T("Check joint-space support before turning GP on", "开启 GP 前先检查关节空间覆盖"),
             T("A 14-D support preflight over joint positions and velocities, and a no-GP logging run first.", "对关节位置和速度做 14 维覆盖预检，并先跑一次不开 GP 的记录实验。"),
             T("Continuing after a conservative gate passed, or fixing only the one joint that looked out of range.", "保守门限通过后就继续，或者只修看起来越界的那一个关节。"),
             T("It blocks some trajectories that might have worked, but the GP is never asked to extrapolate. Joint 7 stays out of compensation.", "会拦下一些本来可能可行的轨迹，但保证 GP 不会外推；第 7 关节不参与补偿。")),
            (T("Compensation goes through the controller, not a replay node", "补偿走控制器，而不是回放节点"),
             T("For formal comparisons the trajectory is a reference to the impedance controller, so one torque pipeline applies GP compensation through the existing gates.", "正式对比时把轨迹作为阻抗控制器的参考输入，由同一条力矩管线经过已有的门控施加 GP 补偿。"),
             T("A joint-space replay node as the final torque publisher, which bypassed the compensation gate.", "用关节空间回放节点直接发布最终力矩，这样会绕过补偿开关。"),
             T("The direct replay route was stopped after it triggered a communication-constraint fault on the real robot; it was treated as an architecture problem, not something to retry.", "直接回放路线在真机上触发通信约束故障后被停用；这被当作架构问题处理，而不是反复重试。")),
            (T("Simulation before the lab, and offline analysis as the record", "先仿真再进实验室，以离线分析为准"),
             T("MuJoCo kinematic replay, then fake-hardware replay in RViz, then the lab. After each run, analysis scripts and a written summary with its caveats.", "先用 MuJoCo 做运动学回放，再在 RViz 里跑假硬件回放，然后才上真机；每次实验后用分析脚本和带局限说明的书面总结记录结果。"),
             T("Going straight to the robot with a new trajectory, or re-running the robot without a plan.", "新轨迹直接上真机，或者没有计划地反复重跑。"),
             T("Fewer robot runs and slower turnaround. Simulation proves only kinematics and wiring, and each conclusion is scoped to one run.", "真机实验次数更少、周期更长；仿真只能证明运动学和话题连线，每个结论只对应一次实验。")),
        ],
        "results": T("<p>The stage reports compare a strict no-GP baseline with GP-on runs and compare the online GPs with a historical residual database. Those real-robot numbers come from single runs in a lab and are not published on this site. In an interview I can walk through the reports and what each one does and does not show.</p>",
                     "<p>各阶段报告对比了严格的无 GP 基线和开启 GP 的实验，也对比了在线 GP 和历史残差数据库。这些真机数字来自实验室里的单次实验，本站不公开。面试时我可以逐份讲解这些报告，以及每份报告能说明什么、不能说明什么。</p>"),
        "role": T("<p>A team project at a university robotics lab. My part: code development, including the experiment switches that made frozen-GP tests possible and safety work in the controller (guarded startup, session-relative trajectory anchors); real-robot testing in the lab alongside the team; the staged test programme with a plan and report for each stage; and the offline analysis that compared the online GPs with a historical residual database. The GP model and training pipeline are earlier team work.</p>",
                  "<p>大学机器人实验室的团队项目。我负责的部分：代码开发，包括让冻结 GP 测试成为可能的实验开关，以及控制器里的安全改进（带保护的启动、会话相对轨迹锚点）；和团队一起在实验室做真机测试；分阶段实验计划，每个阶段都有计划和报告；以及对比在线 GP 和历史残差数据库的离线分析。GP 模型和训练流程是团队更早的工作。</p>"),
        "limits": ul([
            T("Every real-robot conclusion rests on one run, so none of it is a statistical result.", "每个真机结论都只基于一次实验，都不是统计意义上的结果。"),
            T("Simulation covered kinematics and topic wiring only: no dynamics or torque-safety claims.", "仿真只覆盖了运动学和话题连线，不涉及动力学和力矩安全的结论。"),
            T("The session-relative anchor is work in progress; no validated real run after the last fix is recorded.", "会话相对锚点还在开发中，最后一次修复之后还没有记录到经过验证的真机运行。"),
        ]),
        "card": T("Frozen-GP and historical-database torque residual compensation on a Franka Panda, tested in stages on the real robot.", "在 Franka Panda 上做冻结 GP 与历史数据库的力矩残差补偿，分阶段在真机上测试。"),
        "card_stats": [T("team project", "团队项目"), T("real-robot tests", "真机测试"), "ROS 2"],
    }


def jt(L):
    T = lambda en, zh: t(L, en, zh)
    return {
        "title": T("Job-search workbench", "求职工作台"),
        "kicker": T("Personal tool · TypeScript · Fastify · React · SQLite", "个人工具 · TypeScript · Fastify · React · SQLite"),
        "lede": T("A self-hosted tracker I use every day instead of a spreadsheet, with a Chrome extension that saves a job from the page I am reading.",
                  "自己部署、每天在用的求职管理工具，替代了 Excel 表格，配一个能从正在看的招聘页保存岗位的 Chrome 扩展。"),
        "links": [], "public": False,
        "stats": [("34", T("/v1 API routes", "个 /v1 API 路由")),
                  ("420+", T("Vitest cases in 66 files", "个 Vitest 用例，66 个测试文件")),
                  ("6 · 10", T("SQLite tables · indexes", "张表 · 个索引")),
                  ("3", T("extension permissions", "个扩展权限"))],
        "media": "",
        "problem": T("<p>A spreadsheet loses history: when a status cell is overwritten, the timeline is gone, and saving a posting and applying to it end up as the same row. I wanted a tool that keeps every status change as an event, separates “saved” from “applied”, and captures a posting in one click without giving a browser extension broad access.</p>",
                     "<p>表格会丢历史：状态单元格一改，时间线就没了；“收藏了岗位”和“已经投递”也挤在同一行里。我想要一个工具：每次状态变化都保留为事件，把“已保存”和“已投递”分开，并且能一键保存岗位，同时不给浏览器扩展过大的权限。</p>"),
        "diagram": jt_diagram(L),
        "how": T("<p>A pnpm monorepo: a Fastify API with Zod contracts, a React web app and a Manifest V3 extension, over SQLite with Drizzle. The domain layer has no database or framework dependency, and the application layer has no HTTP dependency. One Node process serves both the API and the built web app.</p>",
                 "<p>pnpm monorepo：Fastify API 配 Zod 契约、React 网页、Manifest V3 扩展，数据存在 SQLite（Drizzle）。domain 层不依赖数据库和框架，application 层不依赖 HTTP；一个 Node 进程同时提供 API 和构建好的网页。</p>"),
        "decisions": [
            (T("Jobs and applications are separate records", "岗位和投递分开存"),
             T("A Job is a saved posting; an Application is one attempt at it. Saving a job never creates an application.", "Job 是保存的岗位，Application 是针对它的一次求职流程；保存岗位绝不隐式创建投递。"),
             T("One row per posting with a status column.", "每个岗位一行，用一列表示状态。"),
             T("Two concepts to explain, but re-applying or applying through another channel works, and a second open application for the same job is rejected inside the transaction (HTTP 409).", "多了一个概念，但可以重新投递或换渠道投递；同一岗位已有进行中的投递时，第二次创建会在事务内被拒绝（HTTP 409）。")),
            (T("A status snapshot plus an event, in one transaction", "状态快照和事件在同一事务里写入"),
             T("current_status is a snapshot for lists; application_events is the source of truth for the timeline, statistics and calendar. Corrections append events instead of rewriting history.", "current_status 是给列表用的快照；application_events 是时间线、统计和日历的事实来源。更正也是追加事件，不改写历史。"),
             T("Updating the status in place.", "直接原地改状态。"),
             T("One extra row per change, in exchange for a timeline that can always be traced.", "每次变化多写一行，换来永远可追溯的时间线。")),
            (T("Frozen specs and append-only migrations", "冻结规格，migration 只追加"),
             T("The DDL, API contract and import format were written and frozen before the code. A test checks that runtime migrations match the frozen DDL byte for byte.", "DDL、API 契约和导入格式先写成文档并冻结，再写代码；测试会检查运行时 migration 与冻结的 DDL 逐字节一致。"),
             T("Letting the schema drift with the code.", "让 schema 跟着代码随意变化。"),
             T("A protocol change needs its own versioned document, but docs, code and tests can be checked against each other automatically, and old exports still import.", "改协议要单独出一版文档，但文档、代码和测试之间可以自动核对，旧的导出文件也仍能导入。")),
            (T("A narrow extension that only saves jobs", "权限很窄、只保存岗位的扩展"),
             T("The extension reads the current page only after a click (activeTab + scripting), shows a preview, checks for duplicates, and saves a job. Application status is only edited in the web app.", "扩展只有在用户点击后才读取当前页面（activeTab + scripting），先预览、查重，再保存岗位；投递状态只在网页里修改。"),
             T("<all_urls>, background scraping, cookie access, or editing applications from the popup.", "<all_urls>、后台抓取、读取 Cookie，或在弹窗里直接修改投递。"),
             T("You cannot advance an application from the job page, but there is one path for status changes and the extension needs only 3 permissions and one host.", "不能在招聘页上直接推进投递，但状态变化只有一条路径，扩展也只需要 3 个权限和一个 host。")),
            (T("Import with a preview, then one transaction", "导入先预览，再单事务写入"),
             T("CSV/JSON import first classifies every row as new, duplicate, possible duplicate or invalid; after confirmation it writes everything in one transaction with an idempotency key.", "CSV/JSON 导入先把每行分成新建、完全重复、疑似重复、无效；确认后带幂等键在一个事务内全部写入。"),
             T("Silent overwrite or automatic merging of possible duplicates.", "静默覆盖，或自动合并疑似重复。"),
             T("One more step for the user; a preview expires after 15 minutes and goes stale if the data changes.", "用户多一步确认；预览 15 分钟后失效，数据变化后旧预览也会失效。")),
        ],
        "results": T("<p>I use it every day in place of a spreadsheet. CI runs the 420+ Vitest cases on every pull request, including the byte-for-byte migration check and a WCAG AA contrast test across light and dark themes. Real browser checks of the extension stay manual, because automation cannot stand in for a real toolbar click.</p>",
                     "<p>我每天都在用它替代表格。CI 在每个 PR 上运行 420+ 个 Vitest 用例，包括 migration 逐字节校验，以及浅色/深色主题下的 WCAG AA 对比度测试。扩展的真实浏览器检查保留为人工验收，因为自动化无法代替真实的工具栏点击。</p>"),
        "role": T("<p>A personal project: I designed and built it, and I run it.</p>", "<p>个人项目：从设计、开发到部署运行都由我负责。</p>"),
        "limits": ul([
            T("Single user by design. Sharing with other people would need a separate decision with authentication, isolation and deletion in place first.", "按单用户设计。如果要给别人用，需要先单独决策，并补齐认证、隔离和删除机制。"),
            T("Direction tagging uses fixed keywords, so results may need a manual check.", "方向自动归类用的是固定关键词，结果可能需要人工复核。"),
            T("Screenshots are not shown here because the app holds personal data.", "因为应用里有个人数据，这里不放截图。"),
        ]),
        "card": T("Self-hosted tracker with an audited application timeline and a one-click, 3-permission job-capture extension.", "自托管的求职管理工具：可追溯的投递时间线，加一个只需 3 个权限的一键保存扩展。"),
        "card_stats": ["34 routes", "420+ tests", "MV3"],
    }


def cw(L):
    T = lambda en, zh: t(L, en, zh)
    return {
        "title": T("Robot manipulation coursework", "机器人操作课程项目"),
        "kicker": T("Group projects, team of 4 · ROS 2 · C++", "4 人小组项目 · ROS 2 · C++"),
        "lede": T("Four projects on a UR5e, a Franka Panda and a Franka FR3: drawing from an SVG, teaching and replaying a motion, pressing a lit button found by a camera, and moving a tool through a fixed point.",
                  "在 UR5e、Franka Panda 和 Franka FR3 上完成的四个项目：按 SVG 绘图、示教并回放动作、用相机找到亮起的按钮并按下、让工具始终穿过一个固定点运动。"),
        "links": [], "public": False,
        "stats": [("4", T("projects, 3 robots", "个项目，3 种机器人")),
                  ("77 s → ~180 s", T("drawing time, sim vs. real", "绘图耗时，仿真对比真机")),
                  ("13,833", T("taught samples over 13.8 s", "个示教采样，共 13.8 s")),
                  ("3", T("priority levels in the RCM solver", "层 RCM 任务优先级"))],
        "media": "",
        "problem": T("<p>Each project put a different part of manipulation on a real robot: offline programming and its timing, torque-level replay of a human demonstration, perception that has to be trusted near contact, and redundancy resolution under a hard constraint.</p>",
                     "<p>每个项目把操作中的一个环节放到真机上：离线编程及其节拍、人类示教在力矩层面的回放、接近接触时仍要可信的感知，以及硬约束下的冗余求解。</p>"),
        "diagram": cw_diagram(L),
        "how": T("<p>The drawing project is programmed offline in RoboDK and exported to URScript. The other three are ROS 2 Humble packages on top of franka_ros2: a joint-impedance torque controller for replay, a perception node plus a custom contact controller for the button press, and a task-priority inverse-kinematics solver publishing joint velocities for the RCM project.</p>",
                 "<p>绘图项目在 RoboDK 中离线编程并导出为 URScript。其余三个是基于 franka_ros2 的 ROS 2 Humble 包：回放用的关节阻抗力矩控制器、按按钮用的感知节点加自定义接触控制器，以及 RCM 项目里发布关节速度的任务优先级逆运动学求解器。</p>"),
        "decisions": [
            (T("Replay with a joint-impedance torque controller", "用关节阻抗力矩控制器回放"),
             T("The taught CSV is interpolated and tracked with τ = K(q_goal − q) − D·q̇ through the effort interface, after a warm-start move to the first sample.", "对示教 CSV 插值，先热启动到第一个采样点，再通过力矩接口用 τ = K(q_goal − q) − D·q̇ 跟踪。"),
             T("A position controller.", "位置控制器。"),
             T("Compliant replay, so a software safety layer sits in front: non-finite torques become zero and each joint is clamped in magnitude and rate. It does not replace Franka's own safety.", "回放是柔顺的，因此前面加了一层软件安全层：非有限值置零，逐关节限制幅值和变化率；它不替代 Franka 自身的安全机制。")),
            (T("Vision decides which button; taught poses decide where to press", "视觉决定按哪个，示教位姿决定按在哪"),
             T("HSV colour and brightness thresholding finds the lit button; the press itself uses taught positions.", "用 HSV 颜色和亮度阈值找到亮起的按钮，按压动作本身使用示教位置。"),
             T("Fully visual 3D pressing, and MoveIt free-space trajectories that were too large for the compact board.", "完全依赖视觉的三维按压，以及在紧凑面板上轨迹过大的 MoveIt 自由空间规划。"),
             T("Small calibration or execution errors are not trusted during contact, but the press is only validated at the taught board placement.", "接触时不依赖小的标定或执行误差，但按压只在示教时的面板位置上验证过。")),
            (T("Strict task priority with an 8th virtual joint", "严格任务优先级加第 8 个虚拟关节"),
             T("Insertion depth is a virtual prismatic joint η. The RCM constraint comes first, tool-tip tracking runs in its null space, and joint-limit centering in what is left, with damped least squares (1e-3).", "插入深度建模为虚拟移动关节 η；RCM 约束优先，工具尖端跟踪在其零空间中，关节限位居中在剩余零空间中，求解用阻尼最小二乘（1e-3）。"),
             T("Weighted, non-strict priorities.", "加权的非严格优先级。"),
             T("When the tasks conflict, the tip yields to the RCM. Analytical Jacobians are checked against finite differences in a unit test.", "任务冲突时工具尖端让位于 RCM；解析雅可比在单元测试中与有限差分对照验证。")),
            (T("Measure simulated vs. real time instead of assuming it", "实测仿真和真机节拍，而不是想当然"),
             T("SVG paths sampled at about 5 mm with a 1 mm blend radius, then timed in simulation and on the UR5e.", "SVG 路径约 5 mm 采样、1 mm 过渡半径，然后分别在仿真和 UR5e 上计时。"),
             T("Not documented.", "未记录。"),
             T("The circle took 44 s simulated vs. about 60 s real, the robot drawing 77 s vs. about 180 s. The gap is attributed to many short segments, acceleration limits and the small blend radius; a run to confirm that explanation is not recorded.", "画圆仿真 44 s、真机约 60 s；画机器人图案仿真 77 s、真机约 180 s。差距归因于大量短线段、加速度限制和很小的过渡半径；验证这个解释的实验没有记录。")),
        ],
        "results": T("<p>The RCM controller ran on a physical FR3. The teach-and-replay and button-press controllers ran on the lab robots. After the course, the repository gained CI that builds and tests the RCM package and runs the perception tests.</p>",
                     "<p>RCM 控制器在真实 FR3 上运行过；示教回放和按按钮控制器在实验室机器人上运行过。课程结束后，仓库补上了 CI：构建并测试 RCM 包，并运行感知部分的测试。</p>"),
        "role": T("<p>Group coursework in a team of 4. I worked on code development and real-robot testing in all four projects. All course commits used a shared team account, so the history cannot show who wrote which part; I describe my role and do not claim any project as mine alone.</p>",
                  "<p>4 人小组的课程项目。四个项目我都参与了代码开发和真机测试。课程期间的提交都用的是共享的团队账号，提交历史无法区分每个人写了哪部分；因此我只描述自己的角色，不把任何一个项目说成是我一个人完成的。</p>"),
        "limits": ul([
            T("No numeric RCM error summary is recorded; the errors are in a result plot only.", "RCM 没有记录数值误差汇总，误差只在结果图里。"),
            T("Button detection accuracy and lighting robustness were not measured.", "按钮检测准确率和光照鲁棒性没有测量。"),
            T("The timing explanation for the drawing project was not confirmed with a second run.", "绘图项目节拍差异的解释没有用第二次实验验证。"),
        ]),
        "card": T("UR5e drawing, Franka teach-and-replay with a torque controller, vision-triggered button press, and task-priority IK under an RCM constraint.", "UR5e 绘图、Franka 力矩控制器示教回放、视觉触发按钮按压，以及远心点约束下的任务优先级逆运动学。"),
        "card_stats": [T("team of 4", "4 人小组"), "FR3 · Panda · UR5e", "ROS 2"],
    }


BUILDERS = {"mtri": mtri, "gp": gp, "job-tracker": jt, "coursework": cw}


# ---------------------------------------------------------------- pages
def page(L, slug, title, desc, body):
    u = UI[L]
    root = "../" if L == "zh" else ""
    other_href = ("../" if L == "zh" else "zh/") + (f"{slug}.html" if slug != "index" else "")
    return f"""<!doctype html>
<html lang="{u['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="alternate" hreflang="{UI[u['other']]['lang']}" href="{other_href}">
<link rel="stylesheet" href="{root}assets/site.css">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="./"><span class="dot"></span>{u['name']}</a>
<nav><a href="{GH}">GitHub</a><a class="lang" href="{other_href}" hreflang="{UI[u['other']]['lang']}">{u['other_label']}</a></nav>
</div></header>
<main class="wrap">
{body}
</main>
<footer class="wrap foot"><p>{u['footer']}</p><p><a href="{GH}">github.com/feizaodemon</a></p></footer>
</body>
</html>
"""


def project_page(L, slug):
    u = UI[L]
    p = BUILDERS[slug](L)
    links = "".join(
        f'<a class="btn{" primary" if prim else ""}" href="{h}">{esc(lbl)}</a>' for lbl, h, prim in p["links"])
    note = "" if p["public"] else f'<p class="private"><span class="lock" aria-hidden="true"></span>{u["private"]}</p>'
    decs = "".join(decision(i + 1, *d, L) for i, d in enumerate(p["decisions"]))
    body = f"""<p class="crumb"><a href="./">← {u['back']}</a></p>
<section class="hero proj">
<p class="kicker">{esc(p['kicker'])}</p>
<h1>{esc(p['title'])}</h1>
<p class="lede">{esc(p['lede'])}</p>
{f'<div class="actions">{links}</div>' if links else ''}
{note}
</section>
<h2 class="sr">{u['glance']}</h2>
{stats(p['stats'])}
{p['media']}
<section><h2>{u['problem']}</h2>{p['problem']}</section>
<section><h2>{u['how']}</h2>{p['how']}{p['diagram']}</section>
<section><h2>{u['decisions']}</h2><div class="decs">{decs}</div></section>
<section><h2>{u['results']}</h2>{p['results']}</section>
<section><h2>{u['role']}</h2>{p['role']}</section>
<section><h2>{u['limits']}</h2>{p['limits']}</section>
<p class="crumb end"><a href="./">← {u['back']}</a></p>"""
    title = f"{p['title']} · {u['name']}"
    return page(L, slug, title, p["lede"], body)


def index_page(L):
    u = UI[L]
    T = lambda en, zh: t(L, en, zh)
    root = "../" if L == "zh" else ""
    cards = []
    for slug in ["mtri", "gp", "job-tracker", "coursework"]:
        p = BUILDERS[slug](L)
        feat = slug == "mtri"
        img = (f'<img src="{root}assets/mtri-task-gazebo.gif" alt="" loading="lazy">' if feat else "")
        tag = T("Open source", "开源") if p["public"] else T("Private", "私有")
        chips = "".join(chip(esc(s)) for s in p["card_stats"])
        cards.append(f"""<a class="card{' feat' if feat else ''}" href="{slug}.html">
{img}<div class="cbody"><p class="kicker"><span class="tag{' pub' if p['public'] else ''}">{tag}</span>{esc(p['kicker'].split(' · ', 1)[1] if p['public'] else p['kicker'])}</p>
<h3>{esc(p['title'])}</h3><p>{esc(p['card'])}</p><div class="chips">{chips}</div>
<span class="more">{u['read']} →</span></div></a>""")
    body = f"""<section class="hero home">
<svg class="loop" viewBox="0 0 400 160" aria-hidden="true"><path d="M20,120 C80,10 160,10 190,80 C220,150 300,150 340,60 C360,20 390,30 385,70"/><circle cx="385" cy="70" r="6"/></svg>
<p class="kicker">{T("Robot software · control · full-stack tools", "机器人软件 · 控制 · 全栈工具")}</p>
<h1>{u['name']}</h1>
<p class="lede">{T("I build robot software end to end: recognition and supervision logic, Cartesian and torque controllers on Franka arms, and the experiments and tests that show whether they work. When a spreadsheet stops being enough, I build the tool myself.", "我做端到端的机器人软件：识别与监督逻辑、Franka 机械臂上的笛卡尔控制和力矩控制，以及验证它们是否真正有效的实验和测试。表格不够用的时候，我会自己写工具。")}</p>
<div class="actions"><a class="btn primary" href="{DEMO}">{T("Try the gesture recognizer", "在线试用手势识别器")}</a><a class="btn" href="{GH}">GitHub</a></div>
</section>
<section><h2>{T("Case studies", "项目案例")}</h2>
<p class="sub">{T("One project is open source. The other three are private because they are team work, coursework or hold personal data, so each case study explains the problem, the design and the trade-offs without the code.", "其中一个项目是开源的；另外三个是团队项目、课程作业或含有个人数据，所以仓库是私有的。每个案例都讲清问题、设计和取舍，但不公开代码。")}</p>
<div class="cards">{''.join(cards)}</div></section>"""
    title = T("Xiaowei Rong · Robot software case studies", "Xiaowei Rong · 机器人软件项目案例")
    return page(L, "index", title, T("Case studies of four robotics and software projects.", "四个机器人与软件项目的案例介绍。"), body)


def main():
    here = pathlib.Path(__file__).parent
    (OUT / "zh").mkdir(parents=True, exist_ok=True)
    (OUT / "assets").mkdir(exist_ok=True)
    shutil.copy(here / "site.css", OUT / "assets/site.css")
    shutil.copy(here / "favicon.svg", OUT / "assets/favicon.svg")
    for L in ("en", "zh"):
        d = OUT if L == "en" else OUT / "zh"
        (d / "index.html").write_text(index_page(L))
        for slug in BUILDERS:
            (d / f"{slug}.html").write_text(project_page(L, slug))
    (OUT / ".nojekyll").write_text("")


main()
