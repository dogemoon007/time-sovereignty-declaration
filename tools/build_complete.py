#!/usr/bin/env python3
"""Build 《时间主权宣言 · 完整版》/ The Sovereignty of Time: Complete Edition.

Canonical sources (UTF-8 Markdown): manifesto_zh.md, manifesto_en.md, series_0{1..5}_{zh,en}.md.
The colophon lists the SHA-256 of all twelve. Cover and body are rendered by Chromium and merged.
"""
import hashlib, html, re
from pathlib import Path
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)

VERSION = "v1.1"
DATE = "2026-11-06"
EDITION_ZH, EDITION_EN = "完整版", "Complete Edition"

FILES = ["manifesto_zh.md", "manifesto_en.md"] + [f"series_0{i}_{l}.md" for l in ("zh", "en") for i in range(1, 6)]
SRC = {f: (HERE / f).read_bytes() for f in FILES}
SHA = {f: hashlib.sha256(b).hexdigest() for f, b in SRC.items()}

LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITAL = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")

def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = BOLD.sub(r"<b>\1</b>", s)
    s = ITAL.sub(r"<i>\1</i>", s)
    return s

def parse(md: str):
    """Tiny markdown subset -> list of (kind, text|list)."""
    blocks, para, items, quote = [], [], [], []
    def flush():
        nonlocal para, items, quote
        if para: blocks.append(("p", " ".join(para))); para = []
        if items: blocks.append(("ul", items)); items = []
        if quote: blocks.append(("quote", " ".join(quote))); quote = []
    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip(): flush(); continue
        if line.startswith("### "): flush(); blocks.append(("h3", line[4:].strip()))
        elif line.startswith("## "): flush(); blocks.append(("h2", line[3:].strip()))
        elif line.startswith("# "): flush(); blocks.append(("h1", line[2:].strip()))
        elif line.startswith("@ "): flush(); blocks.append(("mark", line[2:].strip()))
        elif line.strip() == "---": flush(); blocks.append(("hr", ""))
        elif line.startswith("> "):
            if para or items: flush()
            quote.append(line[2:].strip())
        elif line.startswith("- "):
            if para or quote: flush()
            items.append(line[2:].strip())
        else:
            if items or quote: flush()
            para.append(line.strip())
    flush()
    return blocks

def render(blocks, h3_as="h3"):
    out = []
    for kind, val in blocks:
        if kind == "h1": out.append(f"<h1>{inline(val)}</h1>")
        elif kind == "h2": out.append(f"<h2>{inline(val)}</h2>")
        elif kind == "h3": out.append(f"<{h3_as}>{inline(val)}</{h3_as}>")
        elif kind == "mark": out.append(f'<div class="mark">{inline(val)}</div>')
        elif kind == "quote": out.append(f'<blockquote>{inline(val)}</blockquote>')
        elif kind == "hr": out.append('<div class="sep">— · —</div>')
        elif kind == "ul": out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in val) + "</ul>")
        else: out.append(f"<p>{inline(val)}</p>")
    return "".join(out)

def split_h2(blocks):
    parts, cur, buf = {}, "head", []
    for b in blocks:
        if b[0] == "h2": parts[cur] = buf; cur, buf = b[1], []
        else: buf.append(b)
    parts[cur] = buf
    return parts

def essay_html(fname, lang):
    """A series essay: title + subtitle + epigraph + sections + sources, as one page block."""
    blocks = parse(SRC[fname].decode("utf-8"))
    title = next(v for k, v in blocks if k == "h1")
    rest = [b for b in blocks if b[0] != "h1"]
    # first paragraph after h1 is the subtitle line
    sub = ""
    if rest and rest[0][0] == "p": sub = rest.pop(0)[1]
    body = []
    for kind, val in rest:
        if kind == "h2" and val in ("来源", "Sources"):
            body.append(f'<h3 class="src">{inline(val)}</h3>')
        elif kind == "h2":
            body.append(f"<h3>{inline(val)}</h3>")
        else:
            body.append(render([(kind, val)]))
    cls = "page essay" + (" en" if lang == "en" else "")
    return f'<div class="{cls}"><div class="ehead"><h1>{inline(title)}</h1><p class="sub">{inline(sub)}</p></div>{"".join(body)}</div>'

zh = split_h2(parse(SRC["manifesto_zh.md"].decode("utf-8")))
en = split_h2(parse(SRC["manifesto_en.md"].decode("utf-8")))

CSS = """
@page { size: A4; margin: 24mm 26mm 26mm 26mm; }
html, body { margin: 0; padding: 0; }
body { font-family: "Noto Sans CJK SC", "Noto Sans SC", sans-serif; color: #161616; background: #fff;
       font-size: 10.5pt; line-height: 1.9; font-kerning: normal; text-rendering: optimizeLegibility; }
p { margin: 0 0 0.9em 0; text-align: justify; text-justify: inter-ideograph; hanging-punctuation: allow-end; orphans: 3; widows: 3; }
.en p, .en li, .en blockquote { text-align: left; line-height: 1.62; hyphens: none; }
a { color: inherit; text-decoration: none; border-bottom: 0.5pt solid #bbb; }
h1, h2, h3 { font-weight: 700; margin: 0; letter-spacing: 0.02em; break-after: avoid; page-break-after: avoid; }
h2 { font-size: 11pt; color: #6b6b6b; font-weight: 500; letter-spacing: 0.22em; margin: 0 0 1.6em 0; text-transform: uppercase; }
h3 { font-size: 13.5pt; margin: 1.9em 0 0.8em 0; padding-top: 0.9em; border-top: 0.6pt solid #cfcfcf; }
h3.src { font-size: 10.5pt; color: #6b6b6b; letter-spacing: 0.16em; margin-top: 2.4em; }
.mark { text-align: center; font-weight: 700; font-size: 10.5pt; letter-spacing: 0.3em; color: #333; margin: 1.05em 0 0.45em 0; }
blockquote { margin: 0 0 1.6em 0; padding: 0 0 0 1.1em; border-left: 1.5pt solid #161616; color: #333; font-size: 10.2pt; line-height: 1.75; }
.en blockquote { font-style: italic; }
.sep { text-align: center; color: #999; letter-spacing: 0.4em; margin: 1.8em 0 1.2em 0; font-size: 9pt; }
ul { margin: 0 0 1em 0; padding-left: 1.2em; }
li { margin: 0 0 0.35em 0; font-size: 9.2pt; line-height: 1.55; color: #333; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
.lede { font-size: 14pt; line-height: 1.75; font-weight: 500; margin-bottom: 2.4em; }
.en .lede { font-size: 13.5pt; line-height: 1.5; }
.onepage { font-size: 9.6pt; line-height: 1.66; }
.onepage p { margin-bottom: 0.4em; }
.onepage h2 { margin-bottom: 1em; }
.onepage .mark { margin: 0.5em 0 0.15em 0; line-height: 1.25; font-size: 9.8pt; }
.fullhead { margin: 0.4em 0 2.2em 0; }
.fullhead h1 { font-size: 24pt; line-height: 1.3; }
.fullhead .sub, .ehead .sub { font-size: 11pt; color: #555; margin: 0.4em 0 0 0; text-align: left; line-height: 1.5; }
.fullhead .by { font-size: 9.5pt; color: #6b6b6b; letter-spacing: 0.08em; margin: 0.6em 0 0 0; text-align: left; }
.ehead { margin: 0.4em 0 1.8em 0; }
.ehead h1 { font-size: 24pt; line-height: 1.3; }
.ehead .sub { font-size: 9.5pt; color: #6b6b6b; letter-spacing: 0.06em; }
.essay h3:first-of-type { margin-top: 0.4em; }
.halftitle { padding-top: 34mm; }
.halftitle h1 { font-size: 30pt; line-height: 1.25; }
.halftitle .sub { font-size: 14pt; color: #444; margin: 0.5em 0 0 0; text-align: left; }
.halftitle .by { font-size: 10pt; color: #6b6b6b; letter-spacing: 0.1em; margin: 1.2em 0 0 0; text-align: left; }
.halftitle .rule { width: 42mm; border-top: 1.2pt solid #161616; margin: 10mm 0 0 0; }
.toc h2 { margin-bottom: 2em; }
.toc .grp { font-size: 9.5pt; color: #6b6b6b; letter-spacing: 0.2em; margin: 1.6em 0 0.5em 0; }
.toc .it { margin: 0 0 0.35em 0; text-align: left; font-size: 10.5pt; }
.toc .it i { color: #666; font-style: normal; margin-left: 0.6em; font-size: 9.5pt; }
.colophon { font-size: 8.9pt; line-height: 1.55; }
.colophon h2 { margin-bottom: 1.2em; }
.colophon dl { margin: 0; }
.colophon dt { font-weight: 700; margin-top: 0.8em; }
.colophon dd { margin: 0.15em 0 0 0; }
.colophon code, .colophon td.h { font-family: "DejaVu Sans Mono", "Liberation Mono", monospace; font-size: 7.2pt; letter-spacing: 0; word-break: break-all; }
.colophon table { border-collapse: collapse; width: 100%; margin: 0.4em 0 0 0; }
.colophon td { padding: 0.05em 0.6em 0.05em 0; vertical-align: top; font-size: 7.9pt; line-height: 1.35; }
.colophon .small { color: #6b6b6b; }
"""

COVER_CSS = CSS + """
.cover { padding-top: 58mm; }
.cover .over { font-size: 9.5pt; letter-spacing: 0.32em; color: #6b6b6b; margin-bottom: 14mm; }
.cover h1 { font-size: 44pt; line-height: 1.15; letter-spacing: 0.06em; }
.cover .ed { font-size: 16pt; color: #161616; margin: 3mm 0 0 0; letter-spacing: 0.3em; font-weight: 500; }
.cover .sub { font-size: 14pt; color: #333; margin: 7mm 0 0 0; text-align: left; letter-spacing: 0.02em; }
.cover .rule { width: 42mm; border-top: 1.4pt solid #161616; margin: 14mm 0 10mm 0; }
.cover .by { font-size: 12pt; letter-spacing: 0.12em; margin: 0; text-align: left; }
.cover .ver { font-size: 10pt; color: #6b6b6b; letter-spacing: 0.1em; margin: 0.5em 0 0 0; text-align: left; }
.cover .foot { position: absolute; bottom: 0; left: 0; right: 0; font-size: 8.5pt; color: #6b6b6b; line-height: 1.6; }
body { position: relative; min-height: 243mm; }
"""

cover_html = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8"><style>{COVER_CSS}</style></head>
<body><div class="cover">
<div class="over">宣言与五篇 · THE DECLARATION AND FIVE ESSAYS</div>
<h1>时间主权宣言</h1>
<div class="ed">{EDITION_ZH}</div>
<p class="sub">The Sovereignty of Time: A Declaration · {EDITION_EN}</p>
<div class="rule"></div>
<p class="by">Titan</p>
<p class="ver">{VERSION} · 2026 年 11 月 · CC BY-ND 4.0</p>
<div class="foot">宣言四层与"时间盗窃"系列五篇，中文在前，英文在后。十二个规范文本的 SHA-256 见版权页；本文件的 SHA-256 记录于比特币区块链（OpenTimestamps），原文托管于 SSRN。<br>
The four-layer declaration and the five essays of "The Theft of Time," Chinese first, English second. The colophon carries the SHA-256 of the twelve canonical files; the SHA-256 of this file is timestamped on the Bitcoin blockchain (OpenTimestamps) and the text is hosted on SSRN.</div>
</div></body></html>"""

ZH_ESSAYS = ["三重盗窃", "分配", "一种协议", "梯度", "终局"]
EN_ESSAYS = ["Three Thefts", "Distribution", "A Protocol", "Gradient", "Endgame"]

toc_html = '<div class="page toc"><h2>目录 · Contents</h2>' \
    + '<div class="grp">中文</div>' \
    + '<p class="it">一句话 · 一段话</p><p class="it">一页版</p><p class="it">完整宣言<i>一、时间 · 二、三重盗窃 · 三、梯度 · 四、分配 · 五、协议 · 六、终局 · 七、选择</i></p>' \
    + "".join(f'<p class="it">时间盗窃系列 · {"一二三四五"[i]} · {t}</p>' for i, t in enumerate(ZH_ESSAYS)) \
    + '<div class="grp">ENGLISH</div>' \
    + '<p class="it">One sentence · One paragraph</p><p class="it">The Declaration<i>I. Time · II. Three Thefts · III. Gradient · IV. Distribution · V. A Protocol · VI. Endgame · VII. Choice</i></p>' \
    + "".join(f'<p class="it">The Theft of Time · Part {i+1} · {t}</p>' for i, t in enumerate(EN_ESSAYS)) \
    + '<div class="grp">—</div><p class="it">版权页 · Colophon</p></div>'

def sect(key, d): return render(d[key])

body = [toc_html]
body.append(f'<div class="page"><h2>一句话</h2><div class="lede">{sect("一句话", zh)}</div><h2>一段话</h2>{sect("一段话", zh)}</div>')
body.append(f'<div class="page onepage"><h2>一页版</h2>{sect("一页版", zh)}</div>')
body.append(f'<div class="page"><div class="fullhead"><h1>时间主权宣言</h1><p class="sub">The Sovereignty of Time: A Declaration</p><p class="by">Titan · {VERSION} · 2026 年 11 月</p></div>{sect("完整宣言", zh)}</div>')
for i in range(1, 6): body.append(essay_html(f"series_0{i}_zh.md", "zh"))
body.append(f'<div class="page en halftitle"><h1>The Sovereignty of Time</h1><p class="sub">A Declaration · {EDITION_EN}</p><p class="by">Titan · {VERSION} · November 2026</p><div class="rule"></div></div>')
body.append(f'<div class="page en"><h2>One sentence</h2><div class="lede">{sect("One sentence", en)}</div><h2>One paragraph</h2>{sect("One paragraph", en)}</div>')
body.append(f'<div class="page en"><h2>The Declaration</h2>{sect("The Declaration", en)}</div>')
for i in range(1, 6): body.append(essay_html(f"series_0{i}_en.md", "en"))

rows = "".join(f'<tr><td>{f}</td><td class="h">{SHA[f]}</td></tr>' for f in FILES)
body.append(f"""<div class="page colophon">
<h2>版权页 · Colophon</h2>
<dl>
<dt>时间主权宣言 · {EDITION_ZH} — The Sovereignty of Time: A Declaration · {EDITION_EN}</dt>
<dd>作者 Author：Titan</dd>
<dd>版本 Version：{VERSION} · {DATE}</dd>
<dd>内容 Contents：宣言四层（一句话、一段话、一页版、完整宣言）与"时间盗窃"系列五篇（三重盗窃、分配、一种协议、梯度、终局），中英双语。The four-layer declaration and the five essays of "The Theft of Time," in Chinese and English.</dd>

<dt>规范文本 Canonical text（UTF-8 Markdown，SHA-256）</dt>
<dd><table>{rows}</table></dd>
<dd class="small">本 PDF 由以上十二个文件生成。任何人可用 <code>sha256sum</code> 核对。宣言两个文件的哈希与单行本（v1.1，2026-11-06）一致。<br>
This PDF is generated from the twelve files above; anyone can verify them with <code>sha256sum</code>. The two declaration files carry the same hashes as the stand-alone edition (v1.1, 2026-11-06).</dd>

<dt>时间戳与存档 Timestamp and archive</dt>
<dd>本 PDF 的 SHA-256 经 OpenTimestamps 记录于比特币区块链，证明其至迟存在于记录之日；原文托管于 SSRN。核验以哈希为准：无论从何处取得本文件，只要 SHA-256 与发布时公布的一致，即为原文；本页列出的规范文本哈希同理。</dd>
<dd class="small">The SHA-256 of this PDF is timestamped on the Bitcoin blockchain via OpenTimestamps, proving it existed no later than the recorded date; the text is hosted on SSRN. Verification is by hash: any copy whose SHA-256 matches the published value is the original, and likewise for the canonical files listed on this page.</dd>

<dt>版本历史 History</dt>
<dd>2026-01 · v1 草稿《熵减与主权：时间领主宣言（图文终极版）》，已停止流通。</dd>
<dd>2026-11-01 · v0.2 · 重构为嵌套宣言：一句话 / 一段话 / 一页版 / 完整宣言。</dd>
<dd>2026-11-01 · v0.3 · 协议改为第三方视角；增加"换一种货币，不够"一节；英文版。</dd>
<dd>2026-11-03 · 宣言 v1.0 定稿（单行本）。</dd>
<dd>2026-11-03 · {EDITION_ZH} v1.0 · 加入"时间盗窃"系列五篇，中英双语。</dd>
<dd>2026-11-06 · {EDITION_ZH} v1.1 · 更正协议的时间表述（宣言第五节、系列三）：起始年份 2022 年改为 2023 年，“四年”改为“近四年”；系列五一句随存档方式调整；存档方式由 Arweave 改为 OpenTimestamps 时间戳加 SSRN 托管。</dd>

<dt>许可 License</dt>
<dd>© 2026 Titan · CC BY-ND 4.0。可自由复制、转载与分发（含商业用途），须署名并注明来源；不得改写、节译或制作衍生作品。<br>
<span class="small">© 2026 Titan · Creative Commons Attribution-NoDerivatives 4.0 International. Copy, redistribute and share freely, with attribution; no adaptations, abridgements or derivative works.</span><br>
<code>https://creativecommons.org/licenses/by-nd/4.0/</code></dd>
</dl>
</div>""")

body_html = f'<!doctype html><html lang="zh"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(body)}</body></html>'
(OUT / "complete_cover.html").write_text(cover_html, encoding="utf-8")
(OUT / "complete_body.html").write_text(body_html, encoding="utf-8")

FOOTER = ("<div style=\"width:100%; font-family:'Noto Sans CJK SC', sans-serif; font-size:7.5pt; color:#7a7a7a; "
          "padding:0 26mm; box-sizing:border-box; display:flex; justify-content:space-between;\">"
          f"<span>时间主权宣言 · {EDITION_ZH} · The Sovereignty of Time · {VERSION}</span><span class=\"pageNumber\"></span></div>")

with sync_playwright() as p:
    browser = p.chromium.launch(); page = browser.new_page()
    page.set_content(cover_html, wait_until="load")
    page.pdf(path=str(OUT / "complete_cover.pdf"), format="A4", print_background=True, prefer_css_page_size=True)
    page.set_content(body_html, wait_until="load")
    page.pdf(path=str(OUT / "complete_body.pdf"), format="A4", print_background=True, prefer_css_page_size=True,
             display_header_footer=True, header_template="<div></div>", footer_template=FOOTER,
             margin={"top": "24mm", "bottom": "26mm", "left": "26mm", "right": "26mm"})
    browser.close()

writer = PdfWriter()
for f in ("complete_cover.pdf", "complete_body.pdf"):
    for pg in PdfReader(OUT / f).pages: writer.add_page(pg)
writer.add_metadata({"/Title": f"时间主权宣言 · {EDITION_ZH} — The Sovereignty of Time: {EDITION_EN}", "/Author": "Titan",
                     "/Subject": f"{VERSION} · {DATE} · CC BY-ND 4.0", "/Creator": "build_complete.py (Chromium print)"})
final = OUT / f"时间主权宣言_{EDITION_ZH}_{VERSION}.pdf"
with open(final, "wb") as fh: writer.write(fh)
for f in FILES: print(SHA[f], f)
print("pdf", final, final.stat().st_size, "bytes, pages:", len(PdfReader(final).pages))
