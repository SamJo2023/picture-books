#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate voice-samples/index.html from the 54 mp3 files in this directory."""

import os
import html
from pathlib import Path

HERE = Path(__file__).parent

# Category definitions: (category_name, list_of_voice_ids)
# Only include voices we actually have mp3 files for.
CATEGORIES = [
    (
        "基础女声 / 基础男声（4 + 4）",
        [
            ("female-shaonv", "少女"),
            ("female-yujie", "御姐"),
            ("female-chengshu", "成熟"),
            ("female-tianmei", "甜妹"),
            ("male-qn-qingse", "青涩"),
            ("male-qn-jingying", "精英"),
            ("male-qn-badao", "霸道"),
            ("male-qn-daxuesheng", "大学生"),
        ],
    ),
    (
        "精品版（基础 + HD）",
        [
            ("female-shaonv-jingpin", "少女·精品"),
            ("female-yujie-jingpin", "御姐·精品"),
            ("female-chengshu-jingpin", "成熟·精品"),
            ("female-tianmei-jingpin", "甜妹·精品"),
            ("male-qn-qingse-jingpin", "青涩·精品"),
            ("male-qn-jingying-jingpin", "精英·精品"),
            ("male-qn-badao-jingpin", "霸道·精品"),
            ("male-qn-daxuesheng-jingpin", "大学生·精品"),
        ],
    ),
    (
        "童声 / 角色（适合绘本）",
        [
            ("cute_boy", "小男孩"),
            ("clever_boy", "机灵鬼"),
            ("lovely_girl", "可爱女孩"),
            ("cartoon_pig", "卡通猪"),
            ("tianxin_xiaoling", "甜心小玲"),
            ("qiaopi_mengmei", "俏皮萌妹"),
            ("diadia_xuemei", "嗲嗲学妹"),
            ("danya_xuejie", "淡雅学姐"),
            ("wumei_yujie", "妩媚御姐"),
            ("bingjiao_didi", "傲娇弟弟"),
            ("chunzhen_xuedi", "纯真学弟"),
            ("junlang_nanyou", "俊朗男友"),
            ("badao_shaoye", "霸道少爷"),
            ("lengdan_xiongzhang", "冷淡兄长"),
        ],
    ),
    (
        "Chinese (Mandarin) 系列 · 女士 / 女孩",
        [
            ("Chinese (Mandarin)_Soft_Girl", "软糯女孩"),
            ("Chinese (Mandarin)_Sweet_Lady", "甜美淑女"),
            ("Chinese (Mandarin)_Warm_Girl", "暖心姑娘"),
            ("Chinese (Mandarin)_Cute_Spirit", "元气少女"),
            ("Chinese (Mandarin)_Wise_Women", "知性姐姐"),
            ("Chinese (Mandarin)_Mature_Woman", "成熟女性"),
            ("Chinese (Mandarin)_Warm_Bestie", "暖心闺蜜"),
            ("Chinese (Mandarin)_Kind-hearted_Antie", "知心阿姨"),
            ("Chinese (Mandarin)_Kind-hearted_Elder", "慈祥长辈"),
            ("Chinese (Mandarin)_Lyrical_Voice", "抒情女声"),
            ("Chinese (Mandarin)_Radio_Host", "电台女主播"),
            ("Arrogant_Miss", "傲娇小姐"),
        ],
    ),
    (
        "Chinese (Mandarin) 系列 · 男士 / 男孩",
        [
            ("Chinese (Mandarin)_Gentle_Youth", "温润少年"),
            ("Chinese (Mandarin)_Sincere_Adult", "真诚青年"),
            ("Chinese (Mandarin)_Southern_Young_Man", "南方小哥"),
            ("Chinese (Mandarin)_Unrestrained_Young_Man", "洒脱青年"),
            ("Chinese (Mandarin)_Gentleman", "绅士"),
            ("Chinese (Mandarin)_Reliable_Executive", "稳重高管"),
            ("Chinese (Mandarin)_News_Anchor", "新闻主播"),
            ("Chinese (Mandarin)_Male_Announcer", "男播音员"),
            ("Chinese (Mandarin)_Humorous_Elder", "幽默老爷爷"),
            ("Chinese (Mandarin)_HK_Flight_Attendant", "HK 空少"),
            ("Chinese (Mandarin)_Stubborn_Friend", "倔强朋友"),
        ],
    ),
    (
        "其他（特殊角色）",
        [
            ("Robot_Armor", "机甲战士"),
        ],
    ),
]

# Sample text that all voices read — short, Chinese, picture-book-friendly
SAMPLE_TEXT = "从前，有一只小刺猬叫圆圆。有一天，他戴着红围巾，去森林里找朋友们玩。"

# Build HTML
parts = []
parts.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>mmx 中文语音试听 · 为女儿选一个温柔的童声</title>
  <style>
    :root {
      --bg-1: #fff5e6;
      --bg-2: #ffe8c2;
      --accent: #e8954a;
      --text: #4a2c1a;
      --soft: #8a5a3a;
      --card: #fffdf7;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
      background: radial-gradient(ellipse at top, var(--bg-2) 0%, var(--bg-1) 60%, #f5d9a8 100%);
      color: var(--text);
      min-height: 100vh;
      padding: 40px 20px 80px;
    }
    header {
      max-width: 1000px;
      margin: 0 auto 30px;
      text-align: center;
    }
    .badge {
      display: inline-block;
      padding: 6px 18px;
      background: var(--accent);
      color: white;
      border-radius: 999px;
      font-size: 13px;
      letter-spacing: 2px;
      margin-bottom: 14px;
    }
    h1 { font-size: 38px; font-weight: 800; letter-spacing: 4px; margin-bottom: 10px; }
    .subtitle { font-size: 15px; color: var(--soft); line-height: 1.7; max-width: 720px; margin: 0 auto; }
    .quote {
      margin: 18px auto 0;
      max-width: 720px;
      background: rgba(255,253,247,0.7);
      border-left: 4px solid var(--accent);
      padding: 12px 18px;
      border-radius: 8px;
      font-size: 14px;
      color: var(--soft);
      line-height: 1.7;
    }
    .quote b { color: var(--text); }
    main { max-width: 1000px; margin: 30px auto 0; }
    .category {
      background: rgba(255,253,247,0.6);
      border-radius: 18px;
      padding: 20px 22px 24px;
      margin-bottom: 24px;
    }
    .category h2 {
      font-size: 18px;
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px dashed rgba(232,149,74,0.3);
    }
    .category h2 .hint { font-size: 12px; color: var(--soft); font-weight: 400; margin-left: 8px; }
    .voice-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 14px;
    }
    .voice {
      background: var(--card);
      border-radius: 12px;
      padding: 12px 14px;
      box-shadow: 0 2px 8px rgba(74,44,26,0.06);
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .voice .row { display: flex; justify-content: space-between; align-items: center; }
    .voice .label { font-size: 15px; font-weight: 600; }
    .voice .id {
      font-size: 11px;
      color: var(--soft);
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      word-break: break-all;
      text-align: right;
      max-width: 50%;
    }
    .voice audio { width: 100%; height: 36px; }
    .missing {
      opacity: 0.45;
      background: #faf3e3;
    }
    .missing audio { display: none; }
    .missing .label::after {
      content: " · 未生成";
      font-size: 11px;
      color: #c66;
      font-weight: 400;
    }
    footer {
      max-width: 1000px;
      margin: 30px auto 0;
      text-align: center;
      color: var(--soft);
      font-size: 12px;
      opacity: 0.7;
    }
    @media (max-width: 600px) {
      h1 { font-size: 26px; letter-spacing: 2px; }
      .category { padding: 16px; }
      .voice-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <span class="badge">mmx 中文语音试听</span>
    <h1>挑一个温柔的声音</h1>
    <p class="subtitle">下方每张卡片是一段 10 秒左右的样音。挑出最适合给 3 岁小朋友讲睡前故事的那一款。</p>
    <div class="quote">
      所有样音朗读的是同一段：<b>""" + html.escape(SAMPLE_TEXT) + """</b>
    </div>
  </header>
""")

total_voices = 0
total_missing = 0
for cat_name, voices in CATEGORIES:
    parts.append('  <section class="category">\n')
    parts.append(f'    <h2>{html.escape(cat_name)}<span class="hint">共 {len(voices)} 个</span></h2>\n')
    parts.append('    <div class="voice-grid">\n')
    for vid, label in voices:
        total_voices += 1
        # Map voice id → filename
        # "Chinese (Mandarin)_Foo" → "Chinese__Mandarin__Foo.mp3"
        # Achieved by replacing each of "(", ")", and " " with "_"
        fname = vid.replace("(", "_").replace(")", "_").replace(" ", "_") + ".mp3"
        fpath = HERE / fname
        has_file = fpath.exists()
        if not has_file:
            total_missing += 1
        cls = "voice" + ("" if has_file else " missing")
        parts.append(f'      <div class="{cls}">\n')
        parts.append(f'        <div class="row"><span class="label">{html.escape(label)}</span><span class="id">{html.escape(vid)}</span></div>\n')
        parts.append(f'        <audio controls preload="none" src="{html.escape(fname)}"></audio>\n')
        parts.append('      </div>\n')
    parts.append('    </div>\n')
    parts.append('  </section>\n')

parts.append(f"""
  <footer>
    共 {total_voices} 个音色 · 已生成 {total_voices - total_missing} 段样音 · 缺 {total_missing} 段
  </footer>

  <script>
    // 同一时间只允许一段样音在播：新的开始播时，先停掉所有其他 audio
    (function () {{
      const audios = document.querySelectorAll('audio');
      audios.forEach((a) => {{
        a.addEventListener('play', () => {{
          audios.forEach((other) => {{
            if (other !== a && !other.paused) {{
              other.pause();
              other.currentTime = 0;
            }}
          }});
        }});
      }});
    }})();
  </script>
</body>
</html>
""")

out_path = HERE / "index.html"
out_path.write_text("".join(parts), encoding="utf-8")
print(f"OK: wrote {out_path} ({total_voices - total_missing}/{total_voices} voices have files)")
