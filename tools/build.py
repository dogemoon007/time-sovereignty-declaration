#!/usr/bin/env python3
"""Build the bilingual PDF of 时间主权宣言 from the two canonical markdown files.

Cover is rendered without a footer; the body carries a running footer with page numbers;
the two are merged with pypdf. Hashes of the canonical sources are printed on the colophon.
"""
import hashlib, html, re, sys, datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

VERSION = "v1.1"
STATUS_ZH = "定稿"
STATUS_EN = "final"
DATE = "2026-11-06"

zh_src = (HERE / "manifesto_zh.md").read_bytes()
en_src = (HERE / "manifesto_en.md").read_bytes()
zh_sha = hashlib.sha256(zh_src).hexdigest()
en_sha = hashlib.sha256(en_src).hexdigest()


def parse(md: str):
    """Very small markdown subset -> list of (kind, text). kind in h1,h2,h3,mark,p."""
    blocks, para = [], []
    def flush():
        nonlocal para
        if para:
            blocks.append(("p", " ".join(para)))
            para = []
    for raw in md.splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush(); continue
        if line.startswith("### "):
            flush(); blocks.append(("h3", line[4:].strip()))
        elif line.startswith("## "):
            flush(); blocks.append(("h2", line[3:].strip()))
        elif line.startswith("# "):
            flush(); blocks.append(("h1", line[2:].strip()))
        elif line.startswith("@ "):
            flush(); blocks.append(("mark", line[2:].strip()))
        else:
            para.append(line.strip())
    flush()
    return blocks


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def render_blocks(blocks, split_on_h2=True):
    """Return dict h2-title -> html of the blocks under it (plus 'head' for pre-h2 blocks)."""
    parts, cur, buf = {}, "head", []
    for kind, text in blocks:
        if kind == "h2" and split_on_h2:
            parts[cur] = "".join(buf); cur, buf = text, []
            continue
        if kind == "h1":
            buf.append(f'<h1>{esc(text)}</h1>')
        elif kind == "h2":
            buf.append(f'<h2>{esc(text)}</h2>')
        elif kind == "h3":
            buf.append(f'<h3>{esc(text)}</h3>')
        elif kind == "mark":
            buf.append(f'<div class="mark">{esc(text)}</div>')
        else:
            buf.append(f'<p>{esc(text)}</p>')
    parts[cur] = "".join(buf)
    return parts


zh = render_blocks(parse(zh_src.decode("utf-8")))
en = render_blocks(parse(en_src.decode("utf-8")))

CSS = """
@page { size: A4; margin: 24mm 26mm 26mm 26mm; }
html, body { margin: 0; padding: 0; }
body { font-family: "Noto Sans CJK SC", "Noto Sans SC", sans-serif; color: #161616; background: #fff;
       font-size: 10.5pt; line-height: 1.9; font-kerning: normal; text-rendering: optimizeLegibility; }
p { margin: 0 0 0.9em 0; text-align: justify; text-justify: inter-ideograph; hanging-punctuation: allow-end; }
.en p { text-align: left; line-height: 1.62; hyphens: none; }
h1, h2, h3 { font-weight: 700; margin: 0; letter-spacing: 0.02em; }
h2 { font-size: 11pt; color: #6b6b6b; font-weight: 500; letter-spacing: 0.22em; margin: 0 0 1.6em 0; text-transform: uppercase; }
h3 { font-size: 13.5pt; margin: 1.9em 0 0.8em 0; padding-top: 0.9em; border-top: 0.6pt solid #cfcfcf; }
h3:first-of-type { margin-top: 0.6em; }
.mark { text-align: center; font-weight: 700; font-size: 10.5pt; letter-spacing: 0.3em; color: #333; margin: 1.05em 0 0.45em 0; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
.lede { font-size: 14pt; line-height: 1.75; font-weight: 500; margin-bottom: 2.4em; }
.en .lede { font-size: 13.5pt; line-height: 1.5; }
.onepage { font-size: 9.6pt; line-height: 1.66; }
.onepage p { margin-bottom: 0.4em; }
.onepage h2 { margin-bottom: 1em; }
.onepage .mark { margin: 0.5em 0 0.15em 0; line-height: 1.25; font-size: 9.8pt; }
h3 { break-after: avoid; page-break-after: avoid; }
p { orphans: 3; widows: 3; }
.fullhead { margin: 0.4em 0 2.2em 0; }
.fullhead h1 { font-size: 24pt; line-height: 1.3; }
.fullhead .sub { font-size: 12pt; color: #444; margin: 0.35em 0 0 0; text-align: left; }
.fullhead .by { font-size: 9.5pt; color: #6b6b6b; letter-spacing: 0.08em; margin: 0.6em 0 0 0; text-align: left; }
.halftitle { padding-top: 34mm; }
.halftitle h1 { font-size: 30pt; line-height: 1.25; }
.halftitle .sub { font-size: 14pt; color: #444; margin: 0.5em 0 0 0; text-align: left; }
.halftitle .by { font-size: 10pt; color: #6b6b6b; letter-spacing: 0.1em; margin: 1.2em 0 0 0; text-align: left; }
.halftitle .rule { width: 42mm; border-top: 1.2pt solid #161616; margin: 10mm 0 0 0; }
.colophon { font-size: 9.5pt; line-height: 1.75; }
.colophon h2 { margin-bottom: 1.2em; }
.colophon dl { margin: 0; }
.colophon dt { font-weight: 700; margin-top: 1.1em; }
.colophon dd { margin: 0.15em 0 0 0; }
.colophon code { font-family: "DejaVu Sans Mono", "Liberation Mono", monospace; font-size: 8.4pt; letter-spacing: 0.01em; word-break: break-all; }
.colophon .small { color: #6b6b6b; }
"""

COVER_CSS = CSS + """
.cover { padding-top: 58mm; }
.cover .over { font-size: 9.5pt; letter-spacing: 0.32em; color: #6b6b6b; margin-bottom: 14mm; }
.cover h1 { font-size: 44pt; line-height: 1.15; letter-spacing: 0.06em; }
.cover .sub { font-size: 15pt; color: #333; margin: 7mm 0 0 0; text-align: left; letter-spacing: 0.02em; }
.cover .rule { width: 42mm; border-top: 1.4pt solid #161616; margin: 16mm 0 12mm 0; }
.cover .by { font-size: 12pt; letter-spacing: 0.12em; margin: 0; text-align: left; }
.cover .ver { font-size: 10pt; color: #6b6b6b; letter-spacing: 0.1em; margin: 0.5em 0 0 0; text-align: left; }
.cover .foot { position: absolute; bottom: 0; left: 0; right: 0; font-size: 8.5pt; color: #6b6b6b; line-height: 1.6; }
body { position: relative; min-height: 243mm; }
"""

cover_html = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8"><style>{COVER_CSS}</style></head>
<body><div class="cover">
<div class="over">宣言 · DECLARATION</div>
<h1>时间主权宣言</h1>
<p class="sub">The Sovereignty of Time: A Declaration</p>
<div class="rule"></div>
<p class="by">Titan</p>
<p class="ver">{VERSION}（{STATUS_ZH} / {STATUS_EN}）· 2026 年 11 月</p>
<div class="foot">中文在前，英文在后。规范文本的 SHA-256 见版权页；本文件的 SHA-256 记录于比特币区块链（OpenTimestamps），原文托管于 SSRN。<br>
Chinese first, English second. The colophon carries the SHA-256 of the canonical text; the SHA-256 of this file is timestamped on the Bitcoin blockchain (OpenTimestamps) and the text is hosted on SSRN.</div>
</div></body></html>"""

body_html = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8"><style>{CSS}</style></head><body>

<div class="page">
<h2>一句话</h2>
<div class="lede">{zh['一句话']}</div>
<h2>一段话</h2>
{zh['一段话']}
</div>

<div class="page onepage">
<h2>一页版</h2>
{zh['一页版']}
</div>

<div class="page">
<div class="fullhead"><h1>时间主权宣言</h1><p class="sub">The Sovereignty of Time: A Declaration</p><p class="by">Titan · {VERSION} · 2026 年 11 月</p></div>
{zh['完整宣言']}
</div>

<div class="page en halftitle">
<h1>The Sovereignty of Time</h1>
<p class="sub">A Declaration</p>
<p class="by">Titan · {VERSION} · November 2026</p>
<div class="rule"></div>
</div>

<div class="page en">
<h2>One sentence</h2>
<div class="lede">{en['One sentence']}</div>
<h2>One paragraph</h2>
{en['One paragraph']}
</div>

<div class="page en">
<h2>The Declaration</h2>
{en['The Declaration']}
</div>

<div class="page colophon">
<h2>版权页 · Colophon</h2>
<dl>
<dt>时间主权宣言 · The Sovereignty of Time: A Declaration</dt>
<dd>作者 Author：Titan</dd>
<dd>版本 Version：{VERSION}（{STATUS_ZH} / {STATUS_EN}）· {DATE}</dd>

<dt>规范文本 Canonical text（UTF-8 Markdown）</dt>
<dd>中文 manifesto_zh.md · SHA-256<br><code>{zh_sha}</code></dd>
<dd>English manifesto_en.md · SHA-256<br><code>{en_sha}</code></dd>
<dd class="small">本 PDF 由上述两个文件生成。任何人可用 <code>sha256sum</code> 核对文件是否与此处一致。<br>This PDF is generated from the two files above; anyone can verify them with <code>sha256sum</code>.</dd>

<dt>时间戳与存档 Timestamp and archive</dt>
<dd>本 PDF 的 SHA-256 经 OpenTimestamps 记录于比特币区块链，证明其至迟存在于记录之日；原文托管于 SSRN。核验以哈希为准：无论从何处取得本文件，只要 SHA-256 与发布时公布的一致，即为原文；本页列出的规范文本哈希同理。</dd>
<dd class="small">The SHA-256 of this PDF is timestamped on the Bitcoin blockchain via OpenTimestamps, proving it existed no later than the recorded date; the text is hosted on SSRN. Verification is by hash: any copy whose SHA-256 matches the published value is the original, and likewise for the canonical files listed on this page.</dd>

<dt>版本历史 History</dt>
<dd>2026-01 · v1 草稿《熵减与主权：时间领主宣言（图文终极版）》，已停止流通。</dd>
<dd>2026-11-01 · v0.2 · 重构为嵌套宣言：一句话 / 一段话 / 一页版 / 完整宣言。</dd>
<dd>2026-11-01 · v0.3 · 协议改为第三方视角；增加“换一种货币，不够”一节；英文版。</dd>
<dd>2026-11-03 · v1.0 · 定稿。许可 CC BY-ND 4.0。</dd>
<dd>2026-11-06 · v1.1 · 更正第五节对协议的时间表述：起始年份 2022 年改为 2023 年，“四年”改为“近四年”；存档方式由 Arweave 改为 OpenTimestamps 时间戳加 SSRN 托管。</dd>

<dt>许可 License</dt>
<dd>© 2026 Titan · CC BY-ND 4.0。可自由复制、转载与分发（含商业用途），须署名并注明来源；不得改写、节译或制作衍生作品。<br>
<span class="small">© 2026 Titan · Creative Commons Attribution-NoDerivatives 4.0 International. Copy, redistribute and share freely, with attribution; no adaptations, abridgements or derivative works.</span><br>
<code>https://creativecommons.org/licenses/by-nd/4.0/</code></dd>
</dl>
</div>

</body></html>"""

(OUT / "cover.html").write_text(cover_html, encoding="utf-8")
(OUT / "body.html").write_text(body_html, encoding="utf-8")

FOOTER = ("<div style=\"width:100%; font-family:'Noto Sans CJK SC', sans-serif; font-size:7.5pt; color:#7a7a7a; "
          "padding:0 26mm; box-sizing:border-box; display:flex; justify-content:space-between;\">"
          f"<span>时间主权宣言 · The Sovereignty of Time · {VERSION}</span><span class=\"pageNumber\"></span></div>")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(cover_html, wait_until="load")
    page.pdf(path=str(OUT / "cover.pdf"), format="A4", print_background=True, prefer_css_page_size=True)
    page.set_content(body_html, wait_until="load")
    page.pdf(path=str(OUT / "body.pdf"), format="A4", print_background=True, prefer_css_page_size=True,
             display_header_footer=True, header_template="<div></div>", footer_template=FOOTER,
             margin={"top": "24mm", "bottom": "26mm", "left": "26mm", "right": "26mm"})
    browser.close()

writer = PdfWriter()
for f in ("cover.pdf", "body.pdf"):
    for pg in PdfReader(OUT / f).pages:
        writer.add_page(pg)
writer.add_metadata({"/Title": "时间主权宣言 · The Sovereignty of Time: A Declaration", "/Author": "Titan",
                     "/Subject": f"{VERSION} {STATUS_EN} · {DATE}", "/Creator": "build.py (Chromium print)"})
final = OUT / f"时间主权宣言_{VERSION}.pdf"
with open(final, "wb") as fh:
    writer.write(fh)
print("zh sha256", zh_sha)
print("en sha256", en_sha)
print("pdf", final, final.stat().st_size, "bytes, pages:", len(PdfReader(final).pages))
