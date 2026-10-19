#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""데이터베이스 설계 강의자료 — 주차별 구조 빌드
   index.html (다른 HTML로 링크하지 않음)
   week1|week2|week3|week4/{index.html, 01~05.html, answers.html}

   OUT_DIR 환경변수로 출력 폴더를 바꿀 수 있습니다(기본 docs/).
"""
import os, re, json, html, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, os.environ.get("OUT_DIR", "docs"))
CSS  = open(os.path.join(ROOT, "assets/base.css"), encoding="utf-8").read()
JS   = open(os.path.join(ROOT, "assets/base.js"), encoding="utf-8").read()
CHARS= json.load(open(os.path.join(ROOT, "assets/chars.json"), encoding="utf-8"))
from talk import DIALOGUES, talk_html
IMGREG = json.load(open(os.path.join(ROOT, "assets/img.json"), encoding="utf-8"))

def im(name, cls="", alt=""):
    return "{{IMG:%s|%s|%s}}" % (name, cls, alt)

HERO_IMG = {"week1": "hero_week1", "week2": "hero_week2", "week3": "hero_week3", "week4": "hero_week4"}
FIG_IMG = {
 "week2/01_data_and_information.html": ("fig_2_01_data_info", "데이터에서 정보로 — 수집한 값이 판단의 근거가 되기까지"),
 "week2/02_database_definition.html":  ("fig_2_02_definition", "데이터베이스의 네 조건 — 공유 · 통합 · 저장 · 운영"),
 "week2/03_data_classification.html":  ("fig_2_03_classify", "형태에 따른 분류 — 정형 · 반정형 · 비정형"),
 "week2/04_python_lab.html":           ("fig_2_04_pylab", "같은 데이터를 담는 네 가지 그릇 — 리스트 · 튜플 · 딕셔너리 · 데이터프레임"),
 "week3/01_file_system.html":          ("fig_3_01_filesystem", "주소 하나가 세 개의 파일에 흩어져 있는 상태"),
 "week3/02_why_dbms.html":             ("fig_3_02_why", "다섯 가지 문제가 DBMS를 불렀다"),
 "week3/03_dbms_functions.html":       ("fig_3_03_functions", "정의 · 조작 · 제어 — DBMS의 세 가지 기능"),
 "week3/04_dbms_values.html":          ("fig_3_04_values", "DBMS가 주는 것과 잃는 것 — 장점과 단점의 저울"),
 "week3/05_dbms_generations.html":     ("fig_3_05_generations", "계층형에서 NoSQL까지 — 네 세대의 발전사"),
 "week4/01_db_system.html":            ("fig_4_01_system", "데이터베이스 시스템의 구성 — 사전 · 사용자 · 언어 · 처리기"),
 "week4/02_data_modeling.html":        ("fig_4_02_modeling", "현실 세계를 개체와 관계로 옮기기"),
 "week4/03_erd_practice.html":         ("fig_4_03_erd", "쇼핑몰 ERD — 다섯 개체와 세 개의 관계"),
 "week4/04_relational_model.html":     ("fig_4_04_keys", "키 다섯 종류의 관계 — 슈퍼 · 후보 · 기본 · 대체 · 외래"),
 "week4/05_rpg_case.html":             ("fig_4_05_rpg", "RPG 용사의 전설 — 데이터베이스 설계 실무 프로젝트"),
 "week1/01_everyday_database.html":    ("fig_1_01_everyday", "우리 생활 속 데이터베이스 — 편의점 · 은행 · 도서관 · 교통카드"),
 "week1/02_db_vs_spreadsheet.html":    ("fig_1_02_vs_sheet", "스프레드시트 vs 데이터베이스 — 값이 어긋나는 표와 규칙이 잠긴 표"),
 "week1/03_db_tools.html":             ("fig_1_03_tools", "데이터베이스를 구현하는 도구 — 서버형과 내장형, 그리고 공통어 SQL"),
 "week1/04_habits_and_security.html":  ("fig_1_04_habits", "코딩보다 먼저 — 수집 · 분류 · 정리 습관"),
}
SEC_IMG = [
 ("week3/01_file_system.html", "m1", "dia_fs_vs_dbms", "파일 시스템 vs DBMS — 같은 데이터, 다른 관리 방식"),
 ("week2/04_python_lab.html",  "lab", "shot_pandas", "pandas DataFrame 출력 화면"),
 ("week3/05_dbms_generations.html", "prompt", "shot_psql", "psql 콘솔 실행 결과"),
 ("week4/01_db_system.html",   "m2", "dia_3level", "외부 · 개념 · 내부 스키마와 두 개의 사상(Mapping)"),
 ("week4/02_data_modeling.html", "m1", "dia_modeling_3step", "현실 세계 → 개념 세계 → 컴퓨터 세계"),
 ("week4/03_erd_practice.html", "m5", "dia_erd_legend", "ERD 표기법 범례 — 개체 · 속성 · 관계"),
 ("week4/03_erd_practice.html", "m5", "shot_mysql_workbench", "MySQL Workbench에서 ERD 그리기"),
 ("week4/05_rpg_case.html",    "m1", "rpg_concept", "프로젝트 세계관 컨셉아트"),
 ("week4/05_rpg_case.html",    "m6", "rpg_schema", "캐릭터 · 아이템 · 인벤토리 관계도"),
 ("week4/05_rpg_case.html",    "m9", "dia_index_scan", "풀 스캔 vs B-Tree 인덱스 탐색"),
 ("week4/05_rpg_case.html",    "m9", "rpg_dashboard", "인덱스 적용 전후 응답시간"),
 ("week1/01_everyday_database.html", "m1", "dia_1_flow", "바코드 스캔 → 판매 기록 → 재고 차감 → 발주 목록 자동 등록"),
 ("week1/03_db_tools.html", "m1", "dia_1_tools_map", "두 축으로 본 도구 지도 — 서버형/내장형 × 관계형/비관계형"),
 ("week1/03_db_tools.html", "m5", "dia_1_py_vs_db", "파이썬은 손, 데이터베이스는 창고 — 질의(SQL)와 결과로 이어집니다"),
 ("week1/03_db_tools.html", "m5", "shot_sqlite", "sqlite3로 테이블을 만들고 조회한 실행 화면"),
]
ICO_IMG = [
 ("week2/01_data_and_information.html", "m1", "ico_data"),
 ("week2/01_data_and_information.html", "m2", "ico_info"),
 ("week2/02_database_definition.html",  "m3", "ico_db"),
 ("week2/04_python_lab.html",           "lab", "ico_lab"),
 ("week4/03_erd_practice.html",         "m5", "ico_erd"),
 ("week4/04_relational_model.html",     "m4", "ico_key"),
 ("week4/05_rpg_case.html",             "m9", "ico_index"),
 ("week1/02_db_vs_spreadsheet.html",    "m1", "ico_sheet"),
 ("week1/03_db_tools.html",             "m1", "ico_tool"),
]

def figblock(name, cap):
    return ('<div class="figwrap">%s<div class="cap">%s<span>%s</span></div></div>'
            % (im(name, "figimg", cap), im("ico_quiz", "capico", "확인 문제"), cap))

def heroblock(name):
    return im(name, "heroimg", "주차 대표 이미지")

def diagblock(name, cap):
    return '<div class="diaimg">%s<div class="cap">%s</div></div>' % (im(name, "", cap), cap)

def icotag(name):
    return im(name, "ph-ico", "")

def insert_in_section(body, sid, html):
    m = re.search(r'<section class="part"[^>]*id="%s"[^>]*>\s*<div class="wrap">' % re.escape(sid), body)
    if not m: return body, False
    return body[:m.end()] + "\n" + html + body[m.end():], True

def insert_in_parthead(body, sid, html):
    m = re.search(r'(<section class="part"[^>]*id="%s".*?<div class="part-head">)' % re.escape(sid), body, re.S)
    if not m: return body, False
    return body[:m.end()] + html + body[m.end():], True

def decorate(body, key, week, is_index=False):
    if is_index and week["key"] in HERO_IMG:
        body = body.replace("</header>", "\n" + heroblock(HERO_IMG[week["key"]]) + "\n</header>", 1)
    if key in FIG_IMG:
        n, c = FIG_IMG[key]
        body = body.replace("</header>", "\n</header>\n" + figblock(n, c), 1)
    for pg, sid, n, c in SEC_IMG:
        if pg == key:
            body, ok = insert_in_section(body, sid, diagblock(n, c))
            if not ok: raise SystemExit("SEC_IMG miss %s #%s" % (key, sid))
    for pg, sid, n in ICO_IMG:
        if pg == key:
            body, ok = insert_in_parthead(body, sid, icotag(n))
            if not ok: raise SystemExit("ICO miss %s #%s" % (key, sid))
    return body

def esc(t): return html.escape(t, quote=True)

# ─────────────────────────── 소스 파트 추출 ───────────────────────────
def load_sections(fname):
    s = open(os.path.join(SRC, fname), encoding="utf-8").read()
    s = re.sub(r'<header class="hero".*?</header>', '', s, count=1, flags=re.S)
    out, order, pos = {}, [], 0
    while True:
        m = re.search(r'<section class="part"[^>]*id="([^"]+)"[^>]*>', s[pos:])
        if not m: break
        sid = m.group(1); start = pos + m.start()
        i = pos + m.end(); depth = 1
        while depth > 0:
            no = s.find('<section', i); nc = s.find('</section>', i)
            if nc < 0: break
            if 0 <= no < nc: depth += 1; i = no + 8
            else: depth -= 1; i = nc + 10
        out[sid] = s[start:i]; order.append(sid); pos = i
    return out, order

def take_divs(s, cls):
    res = []
    for m in re.finditer(r'<div class="%s">' % cls, s):
        start, i, depth = m.start(), m.end(), 1
        while depth > 0:
            no = s.find('<div', i); nc = s.find('</div>', i)
            if nc < 0: break
            if 0 <= no < nc: depth += 1; i = no + 5
            else: depth -= 1; i = nc + 6
        res.append(s[start:i])
    return res

def gl_entries(glossary_html):
    """gl-card id -> (제목, 비유, 뜻)"""
    d = {}
    for m in re.finditer(r'<div class="gl-card" id="g-([^"]+)">(.*?)</div>', glossary_html, re.S):
        key, body = m.group(1), m.group(2)
        t = re.search(r'<b>(.*?)</b>', body, re.S)
        a = re.search(r'<p class="gl-an">(.*?)</p>', body, re.S)
        n = re.search(r'<p class="gl-mean">(.*?)</p>', body, re.S)
        def txt(x):
            return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x)).strip() if x else ""
        d[key] = (txt(t.group(1)) if t else key, txt(a.group(1)) if a else "", txt(n.group(1)) if n else "")
    return d

def inline_terms(h, entries):
    def rep(m):
        tag = m.group(0)
        g = re.search(r'data-g="([^"]+)"', tag)
        if not g: return tag
        key = g.group(1)
        key = key[2:] if key.startswith("g-") else key
        e = entries.get(key)
        if not e: return tag
        return tag[:-1] + ' data-t="%s" data-a="%s" data-m="%s">' % (esc(e[0]), esc(e[1]), esc(e[2]))
    return re.sub(r'<span[^>]*class="term"[^>]*>', rep, h)

# ─────────────────────────── 공통 조각 ───────────────────────────
def hero(crumb, h1, lead, keys, btns):
    b = "".join('<a class="pbtn%s" href="%s">%s</a>' % (" primary" if p else "", href, lab) for lab, href, p in btns)
    k = "".join('<span class="kchip">%s</span>' % x for x in keys)
    return ('<header class="hero" id="top">\n  <div class="hwrap">\n'
            '    <div class="crumb">%s</div>\n    <h1>%s</h1>\n    <p class="lead">%s</p>\n'
            '    <div class="hbtns">%s</div>\n    <div class="hero-keys">%s</div>\n  </div>\n</header>\n'
            % (crumb, h1, lead, b, k))

FOOTER = """
<footer>
  <div class="wrap">
    <div>
      <b>데이터베이스 설계</b> · 야간 연구실 교육 자료<br>
      <span style="font-size:12.5px">글: 안상선 ((주)M-Robo 대표) · logix44@hanmail.net</span>
    </div>
    <div class="lic">© 2025 데이터베이스 설계 강의 | 안상선<br>CC BY-NC 4.0 — 비상업적 이용, 출처 표기 필수</div>
  </div>
</footer>
<button class="btn totop" type="button" style="position:fixed;right:18px;bottom:18px;z-index:70;opacity:0;transition:.25s">↑ 위로</button>
"""

def toc_items(body):
    out = []
    for m in re.finditer(r'<section class="part"[^>]*id="([^"]+)"[^>]*>(.*?)</section>', body, re.S):
        sid, chunk = m.group(1), m.group(2)
        hm = re.search(r"<h2[^>]*>(.*?)</h2>", chunk, re.S)
        if not hm: continue
        t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", hm.group(1))).strip()
        pm = re.search(r'<div class="part-no">(.*?)</div>', chunk, re.S)
        no = re.sub(r"<[^>]+>", "", pm.group(1)).strip() if pm else ""
        out.append((sid, no, t))
    return out

def topbar(week, cur, items):
    links = []
    links.append('<a class="tb-l%s" href="index.html">표지</a>' % (" on" if cur == "index.html" else ""))
    for i, p in enumerate(week["pages"], 1):
        links.append('<a class="tb-l%s" href="%s">%02d</a>' % (" on" if cur == p["out"] else "", p["out"], i))
    links.append('<a class="tb-l%s" href="answers.html">정답</a>' % (" on" if cur == "answers.html" else ""))
    toc = []
    if items:
        toc.append('<div class="toc-h">이 페이지 목차</div>')
        for sid, no, t in items:
            toc.append('<a href="#%s"><i>%s</i><span>%s</span></a>' % (sid, no or "•", html.escape(t)))
    toc.append('<div class="toc-h">%s 구성</div>' % week["nav"])
    toc.append('<a href="index.html"><i>표지</i><span>%s — %s</span></a>' % (week["nav"], html.escape(week["title"])))
    for i, p in enumerate(week["pages"], 1):
        toc.append('<a href="%s"><i>%02d</i><span>%s</span></a>' % (p["out"], i, html.escape(p["title"])))
    toc.append('<a href="answers.html"><i>✓</i><span>정답과 채점 기준</span></a>')
    return ('<div class="topbar">\n  <div class="tb">\n'
            '    <span class="brand"><span class="dot"></span>DB&nbsp;DESIGN<small>%s · %s</small></span>\n'
            '    <span class="tb-sp"></span>\n    %s\n'
            '    <button class="tocbtn" type="button" aria-expanded="false" aria-controls="tocmenu">목차 ▾</button>\n'
            '  </div>\n  <div class="tocmenu" id="tocmenu">%s</div>\n  <div class="prog"></div>\n</div>'
            % (week["nav"], html.escape(week["title"]), "".join(links), "".join(toc)))

def pager(week, cur):
    seq = [("index.html", "%s 표지" % week["nav"])] + [(p["out"], p["title"]) for p in week["pages"]] + [("answers.html", "정답과 채점 기준")]
    k = [i for i, (o, _) in enumerate(seq) if o == cur]
    if not k: return ""
    k = k[0]; parts = []
    if k > 0: parts.append('<a class="pbtn" href="%s">← %s</a>' % (seq[k-1][0], html.escape(seq[k-1][1])))
    else:     parts.append('<span class="pbtn" style="opacity:.45">%s의 처음</span>' % week["nav"])
    if k < len(seq) - 1: parts.append('<a class="pbtn primary" href="%s">%s →</a>' % (seq[k+1][0], html.escape(seq[k+1][1])))
    else: parts.append('<a class="pbtn primary" href="index.html">%s 표지로 →</a>' % week["nav"])
    return '<div class="pager">%s</div>' % "".join(parts)

def page_html(week, cur, title, desc, body):
    body = re.sub(r"\{\{IMG:([^|]+)\|([^|]*)\|([^}]*)\}\}",
                  lambda m: '<img class="%s" src="%s" alt="%s">' % (m.group(2), IMGREG[m.group(1)], html.escape(m.group(3))),
                  body)
    used = sorted(set(re.findall(r'data-src="([^"]+)"', body)))
    sub = {k: CHARS[k] for k in used if k in CHARS}
    items = toc_items(body)
    return """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s | 데이터베이스 설계 · %s</title>
<meta name="description" content="%s">
<meta name="author" content="안상선 ((주)M-Robo 대표)">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;600;700&display=swap">
<style>
%s
</style>
</head>
<body>
%s
%s
%s
<script>
window.IMG=%s;
%s
</script>
</body>
</html>
""" % (esc(title), esc(week["nav"]), esc(desc), esc(title), esc(desc), CSS,
       topbar(week, cur, items), body, FOOTER + pager(week, cur),
       json.dumps(sub, separators=(",", ":")), JS)

# 전체 15주차 가운데 이 자료의 위치와 다음 주제
TOTAL_WEEKS = 15
WEEK_NEXT = {
    "week1": "데이터와 데이터베이스",
    "week2": "데이터베이스 관리 시스템",
    "week3": "데이터베이스 시스템과 설계",
    "week4": "정규화와 이상현상",
}

# ─────────────────────────── 주차 정의 ───────────────────────────
WEEKS = [
dict(key="week1", dir="week1", nav="1주차", title="오리엔테이션 — 데이터베이스와 첫 만남",
 src=["w1_1.body.html","w1_2.body.html","w1_3.body.html","w1_4.body.html"],
 hero=dict(crumb='데이터베이스 설계 · <b>1주차</b> · 표지',
   h1='데이터베이스는<br>어디에나 <em>있었습니다</em>',
   lead='오리엔테이션은 코드로 시작하지 않습니다. 편의점 재고, 은행 잔고, 도서관 대출 — 이미 매일 쓰고 있는 데이터베이스를 찾아내고, 엑셀·구글 시트와 무엇이 다른지, 어떤 도구로 만들며, <b>무엇보다 어떤 습관이 필요한지</b>를 봅니다.',
   keys=['일상 속 데이터베이스','시트와의 차이','MySQL·PostgreSQL·Oracle','파이썬과의 관계','정리·보안 의식'],
   btns=[('01 우리 생활 속 DB','01_everyday_database.html',True),('03 도구 살펴보기','03_db_tools.html',False),('정답과 채점 기준','answers.html',False)]),
 goals=['편의점·은행·도서관 같은 <b>일상 사례</b>에서 데이터베이스를 찾아낼 수 있다',
        '엑셀·구글 시트와 데이터베이스의 차이를 <b>보장</b> 관점에서 설명할 수 있다',
        'MySQL·MariaDB·PostgreSQL·Oracle·SQLite의 위치를 구분할 수 있다',
        '파이썬과 데이터베이스의 <b>역할 차이</b>를 말할 수 있다',
        '프로그래밍보다 먼저 필요한 <b>수집·분류·정리 습관</b>과 보안 의식을 갖춘다'],
 pages=[
  dict(out="01_everyday_database.html", nav="우리 생활 속 DB", title="우리 생활 속에서 보는 데이터베이스", short="일상 속 DB",
       desc="편의점 재고와 발주, 은행 잔고와 이체, 도서관·병원·교통카드. 이미 매일 쓰고 있는 데이터베이스를 찾아내고 공통 구조를 뽑아냅니다.",
       secs=[("w1_1.body.html","problem"),("w1_1.body.html","m1"),("w1_1.body.html","m2"),("w1_1.body.html","m3"),("w1_1.body.html","m4")],
       crumb='데이터베이스 설계 · 1주차 · <b>01 우리 생활 속 데이터베이스</b>',
       h1='데이터베이스는<br>어디에나 <em>있었습니다</em>',
       lead='편의점 알바 첫날 밤 11시에서 출발합니다. 재고는 어디에 적혀 있고, 은행 잔고는 저장된 값일까 계산된 값일까. 일상 사례 여덟 곳에서 같은 뼈대를 찾아냅니다.',
       keys=['편의점 재고·발주','은행 잔고·이체','일상 사례 8곳','개체·기록·조회·규칙'],
       btns=[('도입 문제','#problem',True),('편의점','#m1',False),('은행','#m2',False)]),
  dict(out="02_db_vs_spreadsheet.html", nav="시트와의 차이", title="데이터베이스와 엑셀·구글 시트", short="시트와의 차이",
       desc="시트가 잘하는 일과, 여러 사람이 오래 쓰기 시작할 때 무너지는 다섯 지점. 그리고 도구를 고르는 네 가지 판단 기준.",
       secs=[("w1_2.body.html","m1"),("w1_2.body.html","m2"),("w1_2.body.html","m3"),("w1_2.body.html","m4")],
       crumb='데이터베이스 설계 · 1주차 · <b>02 데이터베이스와 엑셀·구글 시트</b>',
       h1='같은 표인데<br><em>무엇이 다른가</em>',
       lead='시트는 즉시성이 강하고 데이터베이스는 보장이 강합니다. 동시 편집 충돌, 형식 강제 없음, 중복 방지 불가, 규모 상한, 거친 권한 — 다섯 지점을 확인하고 판단 기준을 세웁니다.',
       keys=['동시 편집 충돌','형식 강제','중복 방지','규모 상한','판단 기준 4가지'],
       btns=[('시트가 잘하는 것','#m1',True),('무너지는 순간','#m2',False),('판단 기준','#m4',False)]),
  dict(out="03_db_tools.html", nav="도구 살펴보기", title="데이터베이스를 구현하는 도구", short="도구 살펴보기",
       desc="MySQL·MariaDB·PostgreSQL·Oracle·SQLite를 두 축으로 정리하고, 파이썬과 데이터베이스가 어떻게 다른지 sqlite3 예제로 확인합니다.",
       secs=[("w1_3.body.html","m1"),("w1_3.body.html","m2"),("w1_3.body.html","m3"),("w1_3.body.html","m4"),("w1_3.body.html","m5")],
       crumb='데이터베이스 설계 · 1주차 · <b>03 데이터베이스를 구현하는 도구</b>',
       h1='도구는 많지만<br><em>축은 둘뿐</em>',
       lead='서버형과 내장형, 관계형과 비관계형. 두 축으로 다섯 도구를 정리하고, MySQL과 MariaDB가 왜 갈라졌는지, 파이썬이 데이터베이스와 어떤 관계인지 봅니다.',
       keys=['MySQL · MariaDB','PostgreSQL','Oracle · SQLite','파이썬 vs DB','SQL은 공통어'],
       btns=[('도구 지도','#m1',True),('PostgreSQL','#m3',False),('파이썬과의 차이','#m5',False)]),
  dict(out="04_habits_and_security.html", nav="습관과 보안", title="프로그래밍 지식이 꼭 필요할까?", short="습관과 보안",
       desc="쓰는 일과 만드는 일은 다릅니다. 코딩보다 먼저 필요한 수집·분류·정리 습관, 보안 의식 다섯 원칙, 중복을 만들지 않는 정리 의식.",
       secs=[("w1_4.body.html","m1"),("w1_4.body.html","m2"),("w1_4.body.html","m3"),("w1_4.body.html","m4")],
       crumb='데이터베이스 설계 · 1주차 · <b>04 프로그래밍 지식이 꼭 필요할까?</b>',
       h1='코딩보다 먼저<br><em>정리하는 습관</em>',
       lead='데이터베이스를 쓰는 일에는 대부분 프로그래밍이 필요하지 않습니다. 필요한 것은 무엇을 기록할지 정하는 힘, 지키는 보안 의식, 그리고 중복을 만들지 않는 정리 의식입니다.',
       keys=['쓰는 일 vs 만드는 일','수집·분류·정리','보안 다섯 원칙','중복 만들지 않기'],
       btns=[('프로그래밍이 필요한가','#m1',True),('코딩보다 먼저','#m2',False),('보안 의식','#m3',False)]),
 ]),

dict(key="week2", dir="week2", nav="2주차", title="데이터와 데이터베이스",
 src=["2.body.html"],
 hero=dict(crumb='데이터베이스 설계 · <b>2주차</b> · 표지',
   h1='데이터에서 데이터베이스까지<br><em>세 걸음</em>',
   lead='영수증 한 장에서 시작해, 값이 정보가 되고 정보가 표가 되고 그 표가 데이터베이스가 되는 과정을 따라갑니다.',
   keys=['데이터 ↔ 정보','DB의 네 조건','정형·반정형·비정형','네 가지 척도','파이썬 실습'],
   btns=[('01 데이터와 정보','01_data_and_information.html',True),('04 파이썬 실습','04_python_lab.html',False),('정답과 채점 기준','answers.html',False)]),
 goals=['데이터와 정보를 <b>가공 여부</b>로 구분해 설명할 수 있다',
        '데이터베이스의 네 가지 정의(공유·통합·저장·운영)를 말할 수 있다',
        '정형·반정형·비정형, 범주형·수치형의 분류 기준을 구분할 수 있다',
        '명목·순서·등간·비율 네 가지 척도를 예와 함께 설명할 수 있다',
        '파이썬 자료구조로 같은 데이터를 옮겨 보며 릴레이션과 비교할 수 있다'],
 pages=[
  dict(out="01_data_and_information.html", nav="데이터와 정보", title="데이터와 정보", short="데이터와 정보",
       desc="영수증 한 장으로 시작합니다. 값과 정보를 가르는 기준은 '가공했는가'입니다. 정보처리와 정보시스템까지 이어서 봅니다.",
       secs=[("2.body.html","problem"),("2.body.html","m1"),("2.body.html","m2")],
       crumb='데이터베이스 설계 · 2주차 · <b>01 데이터와 정보</b>',
       h1='데이터는 그냥 값,<br>정보는 <em>쓸 수 있게 만든 값</em>',
       lead='영수증 한 장에서 출발합니다. 같은 값도 가공하면 의사결정에 쓸 수 있는 정보가 됩니다. 데이터와 정보를 가르는 기준, 정보처리, 정보시스템을 차례로 정리합니다.',
       keys=['데이터 ↔ 정보','정보처리','정보시스템','DIKW'],
       btns=[('도입 문제','#problem',True),('데이터와 정보','#m1',False),('정보시스템','#m2',False)]),
  dict(out="02_database_definition.html", nav="정의·특징", title="데이터베이스의 정의와 특징", short="정의와 특징",
       desc="공유·통합·저장·운영 네 조건과 네 가지 특징(실시간 접근·계속 변화·동시 공유·내용 참조)을 표로 정리합니다.",
       secs=[("2.body.html","m3"),("2.body.html","m4")],
       crumb='데이터베이스 설계 · 2주차 · <b>02 데이터베이스의 정의와 특징</b>',
       h1='데이터베이스는<br><em>네 조건</em>을 만족하는 데이터의 모음',
       lead='아무 파일이나 모아 두면 데이터베이스가 아닙니다. 공유·통합·저장·운영이라는 네 조건과, 그 조건이 만들어 내는 네 가지 특징을 확인합니다.',
       keys=['공유 데이터','통합 데이터','저장 데이터','운영 데이터'],
       btns=[('네 가지 정의','#m3',True),('네 가지 특징','#m4',False),('다음: 데이터의 분류','03_data_classification.html',False)]),
  dict(out="03_data_classification.html", nav="데이터 분류", title="데이터의 분류", short="데이터의 분류",
       desc="형태에 따라 정형·반정형·비정형으로, 특성에 따라 명목·순서·등간·비율로 나눕니다. 척도마다 할 수 있는 계산이 다릅니다.",
       secs=[("2.body.html","m5"),("2.body.html","m6")],
       crumb='데이터베이스 설계 · 2주차 · <b>03 데이터의 분류</b>',
       h1='데이터를 <em>나누는 두 가지 기준</em>',
       lead='형태로 나누면 정형·반정형·비정형, 특성으로 나누면 범주형과 수치형입니다. 특히 네 가지 척도는 어떤 통계를 쓸 수 있는지를 결정합니다.',
       keys=['정형·반정형·비정형','명목·순서','등간·비율','척도와 계산'],
       btns=[('형태에 따른 분류','#m5',True),('특성에 따른 분류','#m6',False),('다음: 파이썬 실습','04_python_lab.html',False)]),
  dict(out="04_python_lab.html", nav="파이썬 실습", title="파이썬 실습과 코드 가이드", short="실습·코드",
       desc="리스트·튜플·딕셔너리·집합으로 같은 고객 데이터를 옮겨 보고, MySQL·PostgreSQL·파이썬·AI 프롬프트 네 갈래 코드 가이드를 봅니다.",
       secs=[("2.body.html","lab"),("2.body.html","prompt")],
       crumb='데이터베이스 설계 · 2주차 · <b>04 파이썬 실습과 코드 가이드</b>',
       h1='파이썬으로 <em>표를 흉내 내 보기</em>',
       lead='데이터베이스가 없던 시절의 도구들로 같은 데이터를 옮겨 봅니다. 자료구조마다 무엇이 되고 무엇이 안 되는지가 곧 데이터베이스의 필요성입니다.',
       keys=['리스트·튜플·딕셔너리','pandas DataFrame','MySQL 가이드','PostgreSQL 가이드'],
       btns=[('파이썬 실습','#lab',True),('코드 가이드 4종','#prompt',False),('정답 보기','answers.html',False)]),
 ]),

dict(key="week3", dir="week3", nav="3주차", title="데이터베이스 관리 시스템",
 src=["3.body.html"],
 hero=dict(crumb='데이터베이스 설계 · <b>3주차</b> · 표지',
   h1='파일로 관리하면<br>왜 <em>무너지는가</em>',
   lead='파일 시스템의 다섯 가지 한계에서 출발해 DBMS의 정의·기능·장단점, 그리고 계층형에서 NoSQL까지 네 세대의 발전사를 따라갑니다.',
   keys=['데이터 중복·종속','롤백과 저널','정의·조작·제어','ACID','네 세대 발전사'],
   btns=[('01 파일 시스템','01_file_system.html',True),('03 DBMS의 기능','03_dbms_functions.html',False),('정답과 채점 기준','answers.html',False)]),
 goals=['파일 시스템에서 데이터 중복이 왜 문제가 되는지 <b>판단 비용</b> 관점에서 설명할 수 있다',
        '데이터 종속성과 롤백·저널의 역할을 말할 수 있다',
        'DBMS의 세 가지 기능(정의·조작·제어)을 예와 함께 구분할 수 있다',
        'DBMS의 장점과 단점을 업무 상황에 맞춰 비교할 수 있다',
        '계층형·네트워크형·관계형·객체지향/NoSQL의 차이를 설명할 수 있다'],
 pages=[
  dict(out="01_file_system.html", nav="파일 시스템", title="파일 시스템의 데이터 관리", short="파일 시스템",
       desc="중복된 데이터 파일을 관리한다는 것의 실제 비용. 주소 하나를 바꿨을 때 어디까지 반영해야 하는지를 따라갑니다.",
       secs=[("3.body.html","problem"),("3.body.html","m1")],
       crumb='데이터베이스 설계 · 3주차 · <b>01 파일 시스템</b>',
       h1='주소 하나를 바꿨더니<br><em>열 곳을 고쳐야 한다</em>',
       lead='파일 시스템의 문제는 저장이 아니라 관리입니다. 중복을 판단하는 비용, 값이 바뀔 때 따라다니는 수정, 구조가 바뀌면 프로그램이 깨지는 종속성까지.',
       keys=['중복 데이터','위치 참조 ↔ 내용 참조','데이터 종속성','저널과 롤백'],
       btns=[('도입 문제','#problem',True),('파일 시스템의 한계','#m1',False),('다음: DBMS의 등장','02_why_dbms.html',False)]),
  dict(out="02_why_dbms.html", nav="DBMS 등장", title="DBMS의 등장 배경", short="DBMS 등장 배경",
       desc="중복·종속·동시 공유·보안·회복 — 다섯 가지 문제를 하나씩 짚고, 각각을 DBMS가 어떻게 받아내는지 봅니다.",
       secs=[("3.body.html","m2")],
       crumb='데이터베이스 설계 · 3주차 · <b>02 DBMS의 등장 배경</b>',
       h1='다섯 가지 문제가<br><em>DBMS를 불렀다</em>',
       lead='데이터 중복, 데이터 종속성, 동시 공유의 어려움, 보안, 회복. 파일 시스템이 감당하지 못한 다섯 문제가 DBMS의 등장 이유입니다.',
       keys=['데이터 중복','종속성','동시 공유','보안·회복'],
       btns=[('다섯 가지 문제','#m2',True),('이전: 파일 시스템','01_file_system.html',False),('다음: DBMS의 기능','03_dbms_functions.html',False)]),
  dict(out="03_dbms_functions.html", nav="DBMS의 기능", title="DBMS의 정의와 주요 기능", short="정의와 기능",
       desc="정의(DDL)·조작(DML)·제어(DCL) 세 기능과, 그 위에서 돌아가는 질의처리기·저장데이터 관리자의 역할.",
       secs=[("3.body.html","m3")],
       crumb='데이터베이스 설계 · 3주차 · <b>03 DBMS의 정의와 주요 기능</b>',
       h1='정의·조작·제어<br><em>세 가지 기능</em>',
       lead='DBMS는 데이터를 만들고(정의), 다루고(조작), 지킵니다(제어). 세 기능이 각각 어떤 명령과 대응하는지 정리합니다.',
       keys=['DDL · DML · DCL','질의처리기','저장데이터 관리자','무결성·동시성·회복'],
       btns=[('세 가지 기능','#m3',True),('이전: 등장 배경','02_why_dbms.html',False),('다음: 핵심 가치','04_dbms_values.html',False)]),
  dict(out="04_dbms_values.html", nav="가치와 사례", title="DBMS가 제공하는 핵심 가치와 실무 사례", short="가치·사례",
       desc="무결성·동시성·회복·보안이 주는 것과, 비용·복잡성·중앙관리 취약점처럼 잃는 것. 그리고 세 기업의 실제 선택.",
       secs=[("3.body.html","m4"),("3.body.html","case")],
       crumb='데이터베이스 설계 · 3주차 · <b>04 핵심 가치와 실무 사례</b>',
       h1='DBMS가 주는 것과<br><em>잃는 것</em>',
       lead='DBMS는 공짜가 아닙니다. 데이터 중복을 통제하고 독립성을 확보하는 대신 비용과 복잡성, 중앙관리 취약점을 안고 갑니다. 장단점을 나란히 놓고 봅니다.',
       keys=['데이터 독립성','무결성·동시성','비용·복잡성','쿠팡·메타·X'],
       btns=[('핵심 가치','#m4',True),('실무 사례','#case',False),('다음: 발전사','05_dbms_generations.html',False)]),
  dict(out="05_dbms_generations.html", nav="발전사", title="DBMS 세대별 발전사와 코드 가이드", short="발전사·코드",
       desc="계층형 → 네트워크형 → 관계형 → 객체지향·NoSQL. 각 세대가 앞 세대의 무엇을 해결했는지, 그리고 네 갈래 코드 가이드.",
       secs=[("3.body.html","m5"),("3.body.html","prompt")],
       crumb='데이터베이스 설계 · 3주차 · <b>05 세대별 발전사와 코드 가이드</b>',
       h1='계층형에서 NoSQL까지<br><em>네 세대</em>',
       lead='계층형은 다대다를 표현하지 못했고, 네트워크형이 그래프로 보완했고, 관계형이 표로 정리했고, NoSQL이 유연한 스키마로 확장했습니다.',
       keys=['계층형·네트워크형','관계형','객체지향·NoSQL','코드 가이드 4종'],
       btns=[('네 세대 발전사','#m5',True),('코드 가이드 4종','#prompt',False),('정답 보기','answers.html',False)]),
 ]),

dict(key="week4", dir="week4", nav="4주차", title="데이터베이스 시스템과 설계",
 src=["4.body.html","5.body.html","6.body.html","7.body.html"],
 hero=dict(crumb='데이터베이스 설계 · <b>4주차</b> · 표지',
   h1='시스템을 알고,<br>현실을 <em>표로 옮긴다</em>',
   lead='3단계 구조와 데이터 독립성으로 시스템을 이해하고, 데이터 모델링과 관계 모델로 설계의 뼈대를 세운 뒤, RPG 실무 프로젝트로 전체를 통과합니다.',
   keys=['3단계 스키마','데이터 독립성','E-R 모델','키와 무결성','RPG 실무 사례'],
   btns=[('01 데이터베이스 시스템','01_db_system.html',True),('05 RPG 실무 사례','05_rpg_case.html',False),('정답과 채점 기준','answers.html',False)]),
 goals=['외부·개념·내부 스키마와 두 가지 사상을 그림으로 설명할 수 있다',
        '논리적·물리적 데이터 독립성을 구분하고 예를 들 수 있다',
        '개체·속성·관계를 찾아 ERD로 표현하고 릴레이션으로 옮길 수 있다',
        '키 다섯 종류와 두 가지 무결성 제약을 적용할 수 있다',
        '실무 프로젝트 흐름(설계 → 인덱스 → 장애 → 회고)을 설명할 수 있다'],
 pages=[
  dict(out="01_db_system.html", nav="DB 시스템", title="데이터베이스 시스템과 3단계 구조", short="DB 시스템·3단계",
       desc="데이터 사전, 사용자와 데이터베이스 언어, 외부·개념·내부 스키마와 두 사상, 그리고 데이터 독립성 애니메이션.",
       secs=[("4.body.html","m1"),("4.body.html","m2"),("4.body.html","anim3"),("4.body.html","m3"),("4.body.html","prompt")],
       crumb='데이터베이스 설계 · 4주차 · <b>01 데이터베이스 시스템과 3단계 구조</b>',
       h1='이름을 바꾸면<br><em>테이블을 고쳐야 할까?</em>',
       lead='같은 데이터베이스를 사용자·설계자·시스템이 서로 다른 눈높이로 봅니다. 외부·개념·내부 세 스키마와 그 사이를 잇는 두 개의 사상이 데이터 독립성을 만듭니다.',
       keys=['3단계 스키마','외부/개념 사상','논리적 독립성','물리적 독립성'],
       btns=[('시스템의 구성','#m1',True),('3단계 구조','#m2',False),('독립성 애니메이션','#anim3',False)]),
  dict(out="02_data_modeling.html", nav="데이터 모델링", title="데이터 모델링과 개체·속성·관계", short="모델링·개체",
       desc="현실 세계 → 개념 세계 → 컴퓨터 세계. 개체와 인스턴스, 속성의 여섯 갈래, 일대일·일대다·다대다 관계.",
       secs=[("5.body.html","problem"),("5.body.html","m1"),("5.body.html","m2"),("5.body.html","m3")],
       crumb='데이터베이스 설계 · 4주차 · <b>02 데이터 모델링과 개체·속성·관계</b>',
       h1='현실 세계를<br><em>개체와 관계</em>로 옮기기',
       lead='"고객이 상품을 주문한다"는 한 문장을 표로 바꾸는 일이 데이터 모델링입니다. 무엇이 개체이고 무엇이 속성이며 둘 사이가 어떤 관계인지 찾아냅니다.',
       keys=['개체·인스턴스','속성 6종','1:1 · 1:N · N:M','ERD 표기법'],
       btns=[('도입 문제','#problem',True),('개체와 속성','#m2',False),('관계의 유형','#m3',False)]),
  dict(out="03_erd_practice.html", nav="ERD 실습", title="논리적 데이터 모델과 쇼핑몰 ERD", short="ERD·논리모델",
       desc="계층·네트워크·관계 모델을 비교하고, 쇼핑몰 ERD를 직접 그려 릴레이션으로 옮깁니다. 코드 가이드 4종 포함.",
       secs=[("5.body.html","m4"),("5.body.html","m5"),("5.body.html","prompt")],
       crumb='데이터베이스 설계 · 4주차 · <b>03 논리적 데이터 모델과 쇼핑몰 ERD</b>',
       h1='그린 ERD를<br><em>표로 옮기기</em>',
       lead='개체는 테이블이 되고, 관계는 외래키나 별도 테이블이 됩니다. 쇼핑몰 다섯 테이블을 직접 그려 보며 1:N과 N:M의 처리 차이를 확인합니다.',
       keys=['계층·네트워크·관계 모델','N쪽에 외래키','N:M 분해','쇼핑몰 ERD'],
       btns=[('논리적 데이터 모델','#m4',True),('쇼핑몰 ERD','#m5',False),('코드 가이드 4종','#prompt',False)]),
  dict(out="04_relational_model.html", nav="관계 모델", title="관계 데이터 모델 — 릴레이션·키·무결성", short="키·무결성",
       desc="릴레이션의 일곱 용어와 네 가지 특징, 키 다섯 종류, 개체 무결성과 참조 무결성. 위반 데이터를 실제로 넣어 봅니다.",
       secs=[("6.body.html","m1"),("6.body.html","m4"),("6.body.html","prompt")],
       crumb='데이터베이스 설계 · 4주차 · <b>04 관계 데이터 모델</b>',
       h1='표를 <em>단단하게</em> 만드는<br>키와 무결성',
       lead='릴레이션은 그냥 표가 아닙니다. 튜플의 유일성, 순서의 무의미, 속성의 원자성이라는 규칙을 지키는 표입니다. 키와 무결성이 그 규칙을 강제합니다.',
       keys=['릴레이션·튜플·도메인','차수 · 카디널리티','키 5종','개체·참조 무결성'],
       btns=[('기본 용어','#m1',True),('키의 종류','#m4',False),('코드 가이드 4종','#prompt',False)]),
  dict(out="05_rpg_case.html", nav="RPG 실무 사례", title="실무 프로젝트 — RPG 용사의 전설", short="RPG 실무 사례",
       desc="파일 시스템의 한계를 겪은 게임 개발팀이 DBMS를 도입하고 캐릭터·아이템·전투·퀘스트를 설계하기까지, 열 단계 실무 기록.",
       secs=[("7.body.html","m1"),("7.body.html","m2"),("7.body.html","m5"),("7.body.html","m6"),
             ("7.body.html","m7"),("7.body.html","m8"),("7.body.html","m9"),("7.body.html","m10"),
             ("7.body.html","prompt")],
       crumb='데이터베이스 설계 · 4주차 사례 · <b>05 RPG 용사의 전설</b>',
       h1='RPG 용사의 전설 —<br><em>설계자의 실무 기록</em>',
       lead='캐릭터·아이템·전투·퀘스트. 대규모 게임의 데이터를 어떻게 표로 옮겼는지, 어디서 장애가 났고 무엇으로 고쳤는지까지 실제 프로젝트 흐름 그대로 정리했습니다.',
       keys=['10단계 설계','3단계 아키텍처','N:M → 중간 테이블','인덱싱 전략','3초 → 0.1초'],
       btns=[('프로젝트 개요','#m1',True),('성능 최적화','#m9',False),('회고와 교훈','#m10',False)]),
 ]),
]

# ─────────────────────────── 정답 페이지 ───────────────────────────
def quiz_items(fname):
    s = open(os.path.join(SRC, fname), encoding="utf-8").read()
    marks = []
    for m in re.finditer(r'<div class="lbl">(.*?)</div>', s, re.S):
        marks.append((m.start(), "lbl", re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', m.group(1))).strip()))
    for m in re.finditer(r'<div class="q" data-ok="(\d+)" data-ex="(.*?)">(.*?)(?=<div class="q" |\Z)', s, re.S):
        body = m.group(3)
        qt = re.search(r'<p class="qt">(.*?)</p>', body, re.S)
        opts = re.findall(r'<button[^>]*data-i="\d+"[^>]*>(.*?)</button>', body, re.S)
        cl = lambda x: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x)).strip()
        marks.append((m.start(), "q", dict(q=cl(qt.group(1)) if qt else "", opts=[cl(o) for o in opts],
                                            ok=int(m.group(1)), ex=cl(html.unescape(m.group(2))))))
    marks.sort(key=lambda x: x[0])
    out, group = [], ""
    for _, kind, val in marks:
        if kind == "lbl": group = val
        else: val["group"] = group; out.append(val)
    return out

def ans_block(items, start_no=1):
    h, last = [], None
    for i, it in enumerate(items, start_no):
        if it["group"] and it["group"] != last:
            h.append('      <div class="ans-group">%s</div>' % esc(it["group"])); last = it["group"]
        h.append('      <div class="ans">')
        h.append('        <p class="aq"><span class="qn">%02d</span><span>%s</span></p>' % (i, esc(it["q"])))
        h.append('        <ul class="ao">')
        for k, o in enumerate(it["opts"]):
            h.append('          <li%s>%s%s</li>' % (' class="correct"' if k == it["ok"] else "", esc(o), " ✔ 정답" if k == it["ok"] else ""))
        h.append('        </ul>')
        h.append('        <div class="ae"><b>해설</b> %s</div>' % esc(it["ex"]))
        h.append('        <div class="score">배점 2점 · 정답을 고르고 이유를 한 문장으로 말하면 2점, 정답만 고르면 1점, 오답이어도 해설의 핵심 이유를 말하면 1점.</div>')
        h.append('      </div>')
    return "\n".join(h)

SCORE_RULE = """
<section class="part" id="how">
  <div class="wrap">
    <div class="part-head"><div class="part-no">안내</div>
      <h2>채점 기준<span class="en">Scoring</span></h2>
      <p>문항당 2점입니다. 정답만 고른 학습자보다 <b>이유를 말한 학습자</b>를 더 높게 봅니다.</p></div>
    <div class="grid">
      <div class="card span">
        <div class="lbl"><span class="no">1</span>문항당 배점</div>
        <ul class="checklist">
          <li><b>2점</b> — 정답을 고르고, 그 이유를 해설의 핵심 논리로 한 문장 설명함</li>
          <li><b>1점</b> — 정답만 고름 (이유를 말하지 못함)</li>
          <li><b>1점</b> — 오답이지만 해설의 핵심 이유를 말함</li>
          <li><b>0점</b> — 무응답이거나, 오답이고 이유도 다른 개념을 가리킴</li>
        </ul>
        <div class="callout key"><b>왜 오답에도 1점인가</b> — 이 자료의 확인 문제는 암기 시험이 아니라 <b>설계 판단 훈련</b>입니다. 근거를 말할 수 있으면 개념은 잡힌 것이므로 부분 점수를 줍니다.</div>
      </div>
      <div class="card span">
        <div class="lbl"><span class="no">2</span>이 주차 배점표</div>
        <table class="t"><thead><tr><th>구분</th><th>문항</th><th>배점</th></tr></thead><tbody>%s
        <tr><td><b>합계</b></td><td><b>%d</b></td><td><b>%d점</b></td></tr></tbody></table>
      </div>
    </div>
  </div>
</section>
"""

LABS = {
"week1": [
 ("L1", "1주차 실습 — 내 주변의 데이터베이스 한 곳을 골라 네 가지 질문에 답하기",
  """편의점·은행·도서관·병원·배달 앱 가운데 <b>하나</b>를 골라, 네 가지 질문에 표로 답합니다.
  <ul class="checklist">
    <li><b>무엇을 다루나(개체)</b> — 편의점이라면 상품, 회원, 점포</li>
    <li><b>무엇을 남기나(속성)</b> — 바코드 · 이름 · 가격 · 수량 · 판매 시각</li>
    <li><b>어떻게 연결되나(관계)</b> — 상품이 재고에, 판매가 상품에 연결됩니다</li>
    <li><b>무엇을 지키나(제약)</b> — 재고보다 많이 팔 수 없다, 없는 상품은 팔 수 없다</li>
  </ul>
  <b>채점 포인트</b> — 사례를 나열하는 것만으로는 부족합니다. <b>"이 값은 어느 개체에 속하는가"</b>를 스스로 판단했는지가 핵심입니다. 예를 들어 '주문 당시의 가격'을 상품이 아니라 주문 항목에 둔 이유를 설명하면 만점입니다."""),
 ("L2", "1주차 실습 — 같은 표를 시트와 데이터베이스로 각각 적어 보기",
  """고객 5명과 주문 10건을 <b>시트 한 장</b>과 <b>데이터베이스 세 테이블</b>로 각각 적어 보고, 두 방식의 차이를 관찰합니다.
  <ul class="checklist">
    <li><b>시트 한 장</b> — 고객 정보가 주문 줄마다 반복됩니다. 고객이 이사하면 여러 줄을 고쳐야 합니다.</li>
    <li><b>데이터베이스</b> — 고객·주문·주문항목으로 나눕니다. 이사하면 고객 표 한 줄만 고칩니다.</li>
    <li><b>형식 강제</b> — 가격 열에 '무료' 같은 문자를 넣어 보고, 데이터베이스가 거부하는지 확인합니다.</li>
    <li><b>중복</b> — 같은 고객번호를 두 번 넣어 보고, 기본키가 막아 주는지 확인합니다.</li>
  </ul>
  <b>채점 포인트</b> — "데이터베이스가 더 편하다"는 결론만으로는 부족합니다. <b>어느 지점에서 도구가 대신 막아 주었는지</b>(형식·중복)를 구체적으로 말해야 만점입니다."""),
],
"week2": [("L1", "2주차 실습 — 파이썬의 데이터 구조로 같은 고객 데이터 표현하기",
  """같은 고객 한 명을 네 가지 구조로 옮겨 보고, 각 구조가 무엇을 흉내 내는지 말할 수 있어야 합니다.
  <ul class="checklist">
    <li><b>튜플</b> — (고객번호, 이름, 이메일)처럼 순서가 고정된 한 건의 레코드. <b>행 하나</b>에 대응합니다.</li>
    <li><b>리스트</b> — 튜플들을 담은 목록. 곧 <b>테이블(튜플의 집합)</b>이며, 순서가 있다는 점이 릴레이션의 '튜플 무순서'와 다릅니다.</li>
    <li><b>딕셔너리</b> — 값에 <b>이름표(키)</b>가 붙은 형태. 데이터 안에 구조 설명이 들어 있으므로 <b>반정형</b>에 해당합니다.</li>
    <li><b>집합</b> — 중복을 자동으로 제거합니다. 고객번호 목록에서 중복을 없애는 일은 곧 <b>키의 유일성</b>을 확인하는 일입니다.</li>
    <li><b>pandas DataFrame</b> — 열 이름과 값이 2차원 표로 정리되어 릴레이션과 가장 가깝습니다. 열 이름 = 속성, 인덱스 = 튜플.</li>
  </ul>
  <b>채점 포인트</b> — 네 구조를 나열하는 것만으로는 부족합니다. "딕셔너리는 이름표를 스스로 들고 있어 반정형, DataFrame은 2차원 표라 릴레이션에 가깝다"처럼 <b>대응 관계</b>를 말하면 만점입니다.""")],
"week3": [("L2", "3주차 실습 — 파일 시스템과 DBMS를 같은 업무로 비교하기",
  """같은 '고객 주소 변경' 업무를 파일 시스템과 DBMS 두 방식으로 적어 보고, 무엇이 달라지는지 정리합니다.
  <ul class="checklist">
    <li><b>파일 시스템</b> — 고객 파일, 주문 파일, 배송 파일에 주소가 흩어져 있으면 세 곳을 모두 찾아 고쳐야 합니다. 하나를 빠뜨리면 <b>불일치</b>가 생기고, 그 불일치를 찾는 비용이 계속 듭니다.</li>
    <li><b>DBMS</b> — 주소는 고객 테이블 한 곳에만 있고, 주문·배송은 고객번호를 참조합니다. 한 행만 고치면 끝나고, <b>참조 무결성</b>이 어긋난 상태를 막아 줍니다.</li>
    <li><b>트랜잭션</b> — 변경 도중 실패하면 롤백으로 되돌립니다. 파일 시스템에서는 어디까지 반영됐는지 사람이 판단해야 합니다.</li>
    <li><b>동시 공유</b> — 두 사람이 같은 고객을 동시에 고칠 때 DBMS는 잠금과 동시성 제어로 순서를 정합니다.</li>
  </ul>
  <b>채점 포인트</b> — "DBMS를 쓰면 편하다"는 결론만으로는 부족합니다. <b>중복·종속·동시 공유·보안·회복</b> 다섯 문제 중 어느 것이 어떤 방식으로 해결되는지 짝지어 말해야 만점입니다.""")],
"week4": [
 ("L3", "4주차 실습 — 쇼핑몰 ERD를 릴레이션으로 옮기기",
  """개체는 테이블로, 관계는 <b>N쪽의 외래키</b> 또는 <b>별도 테이블</b>로 옮깁니다.
  <ul class="checklist">
    <li><b>category</b>(카테고리번호 PK, 이름)</li>
    <li><b>customer</b>(고객번호 PK, 이름, 이메일, 주소)</li>
    <li><b>product</b>(상품번호 PK, 이름, 가격, 카테고리번호 FK → category) — 1:N이므로 <b>N쪽</b>에 1쪽의 키를 넣습니다.</li>
    <li><b>orders</b>(주문번호 PK, 고객번호 FK → customer, 주문일, 상태)</li>
    <li><b>order_item</b>(주문번호 + 상품번호 PK, 수량, 단가) — 주문과 상품은 <b>N:M</b>이라 별도 테이블로 분해하고, 수량·단가 같은 <b>관계의 속성</b>을 여기에 둡니다.</li>
  </ul>
  <b>채점 포인트</b> — ① N:M을 order_item으로 분해했는가 ② 외래키 방향(N쪽에 FK)을 맞게 잡았는가 ③ 수량을 상품 테이블이 아니라 order_item에 두었는가."""),
 ("L4", "4주차 실습 — 적재 전 키·무결성 위반 점검",
  """데이터를 넣기 전에 아래 순서로 점검하고, 위반은 <b>정책을 정해서</b> 고칩니다.
  <ul class="checklist">
    <li><b>개체 무결성</b> — 기본키에 NULL이나 중복이 있는지. 고객번호가 비어 있으면 그 행은 개체로 성립하지 않습니다.</li>
    <li><b>참조 무결성</b> — orders.고객번호가 customer에 없는 값을 가리키는지(고아 레코드). 임시 고객을 만들지, 적재를 보류할지 정해야 합니다.</li>
    <li><b>도메인 제약</b> — 가격에 음수, 이메일에 형식 위반 값이 들어오는지.</li>
    <li><b>순환 참조</b> — 서로를 참조하는 두 테이블은 <b>지연(deferrable) 제약</b>으로 검사를 커밋 시점까지 미룹니다.</li>
  </ul>
  <b>채점 포인트</b> — 위반을 찾는 것보다 "어느 정책이 업무에 맞는가"를 근거와 함께 정하는 것이 목표입니다. 정책 없이 "삭제하면 됩니다"라고만 답하면 절반 점수입니다."""),
 ("L5", "4주차 사례 실습 — RPG 데이터베이스 설계 10단계와 인덱스 효과",
  """파일 시스템의 한계 인식 → DBMS 도입 → 3단계 구조 → 개체 도출 → 관계 정리 → 인덱스·운영 순으로 답이 이어져야 합니다.
  <ul class="checklist">
    <li><b>개체</b> — game_character, character_stat, item, inventory, battle_log. 캐릭터와 아이템은 <b>N:M</b>이므로 inventory로 분해하고 수량을 그곳에 둡니다.</li>
    <li><b>캐릭터·스탯 분리</b> — 자주 조회되는 기본 정보와 자주 바뀌지 않는 상세 스탯을 나누는 <b>성능 최적화</b> 목적입니다. 레벨업 갱신은 트랜잭션으로 묶습니다.</li>
    <li><b>인덱스</b> — 활성 퀘스트 조회에는 <b>player_id + status 복합 인덱스</b>. 선행/후행 관계는 그래프로, 선택 기록은 JSON으로 관리합니다.</li>
    <li><b>장애와 개선</b> — 동시접속 5만 명 상황에서 인벤토리 조회 지연으로 서비스가 마비되었고, 인덱스 추가와 조회 로직 개선으로 <b>3초 → 0.1초</b>로 줄었습니다.</li>
    <li><b>대규모 로그</b> — battle_log는 기간별 <b>파티셔닝</b>으로 관리합니다.</li>
    <li><b>회고</b> — "가장 중요한 것은 미래의 확장성." 업데이트를 견디는 유연한 구조가 결론입니다.</li>
  </ul>
  <b>채점 포인트</b> — 표를 몇 개 만들었는지보다 <b>관계를 어떻게 풀었는지</b>와 <b>왜 그 인덱스를 골랐는지</b>가 점수의 대부분입니다."""),
]}

def build_answers(week, secs_by_src, gl_all):
    qsets = []
    for fname in week["src"]:
        qsets += quiz_items(fname)
    rows = []
    total = len(qsets)
    for fname in week["src"]:
        n = len(quiz_items(fname))
        if n: rows.append('<tr><td>%s</td><td>%d</td><td>%d점</td></tr>' % (esc(week["nav"]), n, n*2))
    rows.append('<tr><td colspan="3" style="color:var(--dim)">이 주차 정답은 아래에 이어집니다.</td></tr>') if False else None
    h = [hero(week["hero"]["crumb"].replace("표지", "<b>정답과 채점 기준</b>"),
              '확인 문제 <em>정답과 채점 기준</em>',
              '학습자라면 각 편의 확인 문제를 먼저 풀어 본 뒤 여세요. 강사·튜터는 정답과 해설, 문항당 배점, 실습 과제의 모범 답안을 수업에 맞게 조정해 쓰면 됩니다.',
              ['%d문항' % total, '%d점 만점' % (total*2), '실습 모범 답안 %d종' % len(LABS[week["key"]])],
              [('채점 기준', '#how', True), ('정답', '#a1', False), ('실습 모범 답안', '#lab', False)])]
    h.append(SCORE_RULE % ("\n        ".join(r for r in rows if r), total, total*2))
    h.append('<section class="part" id="a1"><div class="wrap">')
    h.append('  <div class="part-head"><div class="part-no">정답</div><h2>%s 확인 문제 정답<span class="en">Answer Key</span></h2>'
             '<p>%d문항 · 문항당 2점 · 총 %d점</p></div>' % (esc(week["nav"]), total, total*2))
    h.append('  <div class="anslist">')
    h.append(ans_block(qsets))
    h.append('  </div></div></section>')
    h.append('<section class="part" id="lab"><div class="wrap">')
    h.append('  <div class="part-head"><div class="part-no">실습</div><h2>실습 과제 모범 답안<span class="en">Lab Notes</span></h2>'
             '<p>실습은 정답이 하나로 고정되지 않습니다. 아래는 <b>설계 판단의 근거</b> 중심의 채점 참고안입니다.</p></div>')
    h.append('  <div class="anslist">')
    for code, title, body in LABS[week["key"]]:
        h.append('    <div class="ans"><p class="aq"><span class="qn">%s</span><span>%s</span></p>'
                 '<div class="ae"><b>모범 답안 요점</b> — %s</div></div>' % (code, esc(title), body))
    h.append('  </div></div></section>')
    h.append('<section class="part" id="grade"><div class="wrap">')
    h.append('  <div class="part-head"><div class="part-no">채점</div><h2>오답이 몰리는 지점<span class="en">Common Mistakes</span></h2>'
             '<p>%s에서 특히 자주 틀리는 곳입니다.</p></div>' % esc(week["nav"]))
    h.append('  <div class="grid">%s</div>' % "".join('<div class="card"><div class="lbl"><span class="no">%d</span>%s</div><p>%s</p></div>' % (i, t, d) for i, (t, d) in enumerate(TRAPS[week["key"]], 1)))
    h.append('  <div class="callout key"><b>출처 표기</b> — 이 자료는 안상선 ((주)M-Robo 대표)의 강의 자료를 바탕으로 제작되었으며 <b>CC BY-NC 4.0</b>을 따릅니다. 비상업적 이용은 자유이고, 출처를 반드시 표기해야 합니다.</div>')
    h.append('</div></section>')
    body = "\n".join(x for x in h if x)
    return page_html(week, "answers.html", "%s 정답과 채점 기준" % week["nav"],
                     "%s 확인 문제 정답·해설·배점과 실습 모범 답안" % week["nav"], body)

# ─────────────────────────── 주차 표지(index) ───────────────────────────
def scope_note(week):
    pos = [w["key"] for w in WEEKS].index(week["key"]) + 1
    s = ' 전체 <b>%d주차</b> 가운데 <b>%d주차</b>입니다.' % (TOTAL_WEEKS, pos)
    nxt = WEEK_NEXT.get(week["key"])
    if nxt:
        s += ' 다음 주 주제는 <b>%s</b>입니다.' % nxt
    return s

def build_week_index(week, secs_by_src, gl_all):
    hp = week["hero"]
    h = [hero(hp["crumb"], hp["h1"], hp["lead"], hp["keys"], hp["btns"])]
    h.append('<section class="part" id="goal"><div class="wrap">')
    h.append('  <div class="part-head"><div class="part-no">GOAL</div><h2>이 주차에서 할 수 있게 되는 것<span class="en">Learning Goals</span></h2>'
             '<p>%s의 학습 목표입니다. 아래 세부 페이지를 차례로 따라가면 자연스럽게 채워집니다.%s</p></div>'
             % (esc(week["nav"]), scope_note(week)))
    h.append('  <div class="grid"><div class="card span"><ul class="checklist">%s</ul></div></div>'
             % "".join('<li>%s</li>' % g for g in week["goals"]))
    h.append('  <div class="part-head" style="margin-top:34px"><div class="part-no">MAP</div><h2>이 주차의 구성<span class="en">Contents</span></h2>'
             '<p>이번 주에 다루는 주제를 순서대로 정리했습니다. 위에서부터 차례로 따라가면 됩니다.</p></div>')
    cards = []
    for i, p in enumerate(week["pages"], 1):
        cards.append('<div class="card"><div class="lbl"><span class="no">%02d</span>%s</div><h3><a href="%s">%s</a></h3><p class="sub">%s</p></div>'
                     % (i, esc(p["nav"]), p["out"], esc(p["title"]), esc(p["desc"])))
    cards.append('<div class="card"><div class="lbl"><span class="no">✓</span>정답</div><h3><a href="answers.html">정답과 채점 기준</a></h3>'
                 '<p class="sub">확인 문제 정답·해설·배점과 실습 모범 답안. 학습자는 문제를 먼저 푼 뒤에 여세요.</p></div>')
    h.append('  <div class="grid">%s</div>' % "".join(cards))
    _t = DIALOGUES.get(week["key"] + "/index.html")
    if _t: h.append(talk_html(_t))
    h.append('</div></section>')
    # 용어 사전 (주차 통합)
    gl_groups = []
    for k, fname in enumerate(week["src"], 1):
        secs, _ = secs_by_src[fname]
        g = secs.get("glossary")
        if not g: continue
        for grp in take_divs(g, "gl-group"):
            gl_groups.append(grp.replace('id="g-', 'id="g%d-' % k))
    if gl_groups:
        h.append('<section class="part" id="glossary"><div class="wrap">')
        h.append('  <div class="part-head"><div class="part-no">Aa</div><h2>%s 용어 사전 — 비유로 보기<span class="en">Glossary</span></h2>'
                 '<p>본문에서 점선 밑줄이 있는 낱말을 누르면 같은 비유가 그 자리에서 뜹니다. 여기서는 한꺼번에 훑어볼 수 있습니다.</p></div>' % esc(week["nav"]))
        h.append("  " + "\n  ".join(gl_groups))
        h.append('</div></section>')
    # 저자 + 아웃트로
    first = secs_by_src[week["src"][0]][0]
    for sid in ("author-sec", "outro"):
        if sid in first: h.append(first[sid])
    body = "\n".join(h)
    return page_html(week, "index.html", "%s — %s" % (week["nav"], week["title"]),
                     "%s %s 표지 — 학습 목표, 세부 페이지 안내, 용어 사전" % (week["nav"], week["title"]), body)

# ─────────────────────────── OVERVIEW (링크 없음) ───────────────────────────
OV_HERO = """<header class="hero" id="top">
  <div class="hwrap">
    <div class="crumb">데이터베이스 설계 · <b>OVERVIEW</b> · 전체 안내</div>
    <h1>데이터베이스 설계<br><em>야간 연구실</em> 교육 자료</h1>
    <p class="lead">오리엔테이션부터 시작해 데이터베이스가 되기까지 — 일상 사례에서 파일 시스템의 한계, 관계 데이터 모델까지를 <b>주차별로 나눠</b> 담았습니다. 아래에서 주차별 내용과 전체 로드맵, 그리고 이 자료를 보는 법을 한눈에 확인할 수 있습니다.</p>
    <div class="hbtns">
      <a class="pbtn primary" href="#files">파일 구성 안내</a>
      <a class="pbtn" href="#map">주차별 내용</a>
      <a class="pbtn" href="#road">15챕터 로드맵</a>
      <a class="pbtn" href="#how">이렇게 보면 좋아요</a>
    </div>
    <div class="hero-keys">
      <span class="kchip">일상 사례에서 관계 모델까지</span>
      <span class="kchip">표 · 키 · 제약으로 만드는 설계</span>
      <span class="kchip">확인 문제 58문항</span>
      <span class="kchip">MySQL · PostgreSQL · 파이썬 코드 가이드</span>
      <span class="kchip">단계 애니메이션 · 용어 사전</span>
    </div>
  </div>
</header>
"""

OV_FILES = """
<section class="part" id="files">
  <div class="wrap">
    <div class="part-head"><div class="part-no">FILES</div>
      <h2>자료 구성<span class="en">File Layout</span></h2>
      <p>각 주차 폴더에 어떤 파일이 들어 있는지 정리했습니다. 이 자료는 <b>전체 15주차 가운데 1~4주차</b>까지를 다루며, 5주차 이후는 주차별 폴더로 이어서 열립니다.</p></div>
    <div class="grid">
      <div class="card span">
        <div class="lbl"><span class="no">A</span>폴더 구조</div>
        <div class="calc">index.html                         ← 전체 안내

week1/                            1주차 — 오리엔테이션 (데이터베이스와 첫 만남)
  ├─ index.html                     표지
  ├─ 01_everyday_database.html      우리 생활 속에서 보는 데이터베이스
  ├─ 02_db_vs_spreadsheet.html      데이터베이스와 엑셀·구글 시트
  ├─ 03_db_tools.html               데이터베이스를 구현하는 도구
  ├─ 04_habits_and_security.html    프로그래밍 지식이 꼭 필요할까?
  └─ answers.html                   정답과 채점 기준

week2/                            2주차 — 데이터와 데이터베이스
  ├─ index.html                     표지 (학습 목표 · 세부 안내 · 용어 사전)
  ├─ 01_data_and_information.html   데이터와 정보
  ├─ 02_database_definition.html    데이터베이스의 정의와 특징
  ├─ 03_data_classification.html    데이터의 분류
  ├─ 04_python_lab.html             파이썬 실습과 코드 가이드
  └─ answers.html                   정답과 채점 기준

week3/                            3주차 — 데이터베이스 관리 시스템
  ├─ index.html                     표지
  ├─ 01_file_system.html            파일 시스템의 데이터 관리
  ├─ 02_why_dbms.html               DBMS의 등장 배경
  ├─ 03_dbms_functions.html         DBMS의 정의와 주요 기능
  ├─ 04_dbms_values.html            핵심 가치와 실무 사례
  ├─ 05_dbms_generations.html       세대별 발전사와 코드 가이드
  └─ answers.html                   정답과 채점 기준

week4/                            4주차 — 데이터베이스 시스템과 설계
  ├─ index.html                     표지
  ├─ 01_db_system.html              데이터베이스 시스템과 3단계 구조
  ├─ 02_data_modeling.html          데이터 모델링과 개체·속성·관계
  ├─ 03_erd_practice.html           논리적 데이터 모델과 쇼핑몰 ERD
  ├─ 04_relational_model.html       관계 데이터 모델 — 릴레이션·키·무결성
  ├─ 05_rpg_case.html               실무 프로젝트 — RPG 용사의 전설
  └─ answers.html                   정답과 채점 기준

week5 이후                         이후 주차 — 같은 구성으로 차례로 이어집니다</div>
      </div>
      <div class="card"><div class="lbl"><span class="no">B</span>이 자료에서 할 수 있는 것</div>
        <ul class="checklist">
          <li>확인 문제는 보기를 누르면 즉시 채점되고 해설이 뜹니다.</li>
          <li>코드 블록은 복사 버튼으로 그대로 가져다 실행할 수 있습니다.</li>
          <li>용어에 마우스를 올리면 비유와 뜻이 그 자리에서 뜹니다.</li>
        </ul>
      </div>
      <div class="card"><div class="lbl"><span class="no">C</span>인쇄</div>
        <p>모든 페이지가 인쇄용 스타일을 갖추고 있어, 브라우저 인쇄에서 <b>PDF로 저장</b>하면 배포용 유인물로 쓸 수 있습니다. 배경색을 끄고 인쇄해도 본문과 표는 그대로 읽힙니다.</p>
      </div>
    </div>
  </div>
</section>
"""

OV_OUTRO = """
<section class="part" id="outro">
  <div class="wrap outro">
    <h2>이 OVERVIEW에서 할 일은 끝났습니다</h2>
    <p>일상에서 데이터베이스를 찾아내고, 표로 옮기고, 키와 제약으로 단단하게 만드는 과정을 차례로 담았습니다. 각 주차 표지에서 학습 목표를 확인한 뒤 이어지는 페이지를 따라가면 됩니다.</p>
    <div class="callout key" style="text-align:left;max-width:760px;margin:18px auto 0"><b>교재</b> — 김연희, 『데이터베이스 개론』(3판)에서 커리큘럼의 순서 및 주요 용어의 정의, 예시의 설명 등을 참고했습니다. 이 자료는 안상선 ((주)M-Robo 대표)의 강의 자료이며 <b>CC BY-NC 4.0</b>을 따릅니다.</div>
  </div>
</section>
"""

def build_overview():
    s = open(os.path.join(SRC, "index.body.html"), encoding="utf-8").read()
    s = re.sub(r'<header class="hero".*?</header>', OV_HERO.strip(), s, count=1, flags=re.S)
    # 1) 링크 제거
    s = re.sub(r'<a[^>]*href="[^"]*\.html"[^>]*>(.*?)</a>', r'\1', s, flags=re.S)
    s = re.sub(r'<a[^>]*href="(?:https?://)[^"]*"[^>]*>(.*?)</a>', r'\1', s, flags=re.S)
    # 2) 파일 구성 안내 삽입
    s = s.replace('<section class="part" id="how">', OV_FILES.strip() + '\n\n<section class="part" id="how">', 1)

    # 3) 아웃트로 교체
    s = re.sub(r'<section class="part" id="outro">.*?</section>', OV_OUTRO.strip(), s, count=1, flags=re.S)
    # 4) 문구 정리
    s = s.replace('여섯 편을 차례로', '세 주차를 차례로').replace('여섯 편', '세 주차')
    s = s.replace('<p>2주차부터 4주차까지의 실제 강의 내용을 여섯 편으로 나눴습니다. 각 편은 앞 편의 결론에서 시작합니다.</p>',
                  '<p>각 주차에서 무엇을 배우는지 정리했습니다.</p>')
    s = s.replace('<h2>연구 지도 — 세 주차를 차례로<span class="en">Research Map</span></h2>',
                  '<h2>주차별 내용<span class="en">Weekly Map</span></h2>')
    body = s
    # overview 전용 가짜 week (topbar/pager 없이)
    fake = dict(nav="OVERVIEW", title="전체 안내")
    return page_html(fake, "__none__", "OVERVIEW — 데이터베이스 설계 전체 안내",
                     "데이터베이스 설계 야간 연구실 교육 자료 전체 안내. 다른 HTML 파일로 연결하지 않습니다.", body).replace(
        re.search(r'<div class="topbar">.*?</div>\s*<div class="prog"></div>\s*</div>', "", flags=re.S) and "", "")


OV_MAP = """
<section class="part" id="map">
  <div class="wrap">
    <div class="part-head"><div class="part-no">MAP</div>
      <h2>주차별 내용<span class="en">Weekly Map</span></h2>
      <p>각 주차에서 무엇을 배우는지 정리했습니다.</p></div>
    <div class="grid">
      <div class="card"><div class="lbl"><span class="no">1주차</span>오리엔테이션 — 데이터베이스와 첫 만남</div>
        <p class="sub">코드 없이 시작합니다. 편의점 재고, 은행 잔고, 도서관 대출에서 데이터베이스를 찾아내고, 시트와의 차이·도구의 종류·필요한 습관을 봅니다.</p>
        <div class="facts">
          <div class="fact"><span>세부 4개</span>01 우리 생활 속 DB · 02 시트와의 차이 · 03 도구 살펴보기 · 04 습관과 보안</div>
          <div class="fact"><span>확인 문제</span>20문항 · 실습 모범 답안 2종</div>
        </div>
      </div>
      <div class="card"><div class="lbl"><span class="no">2주차</span>데이터와 데이터베이스</div>
        <p class="sub">값과 정보를 가르는 기준, 데이터베이스의 네 조건과 네 가지 특징, 형태·특성에 따른 분류와 네 가지 척도.</p>
        <div class="facts">
          <div class="fact"><span>세부 4개</span>01 데이터와 정보 · 02 정의와 특징 · 03 데이터의 분류 · 04 파이썬 실습</div>
          <div class="fact"><span>확인 문제</span>8문항 · 실습 모범 답안 1종</div>
        </div>
      </div>
      <div class="card"><div class="lbl"><span class="no">3주차</span>데이터베이스 관리 시스템</div>
        <p class="sub">파일 시스템이 무너지는 다섯 지점에서 DBMS의 등장 배경을 읽고, 정의·조작·제어 세 기능과 네 세대 발전사를 따라갑니다.</p>
        <div class="facts">
          <div class="fact"><span>세부 5개</span>01 파일 시스템 · 02 DBMS 등장 · 03 정의와 기능 · 04 가치와 사례 · 05 발전사</div>
          <div class="fact"><span>확인 문제</span>6문항 · 실습 모범 답안 1종</div>
        </div>
      </div>
      <div class="card"><div class="lbl"><span class="no">4주차</span>데이터베이스 시스템과 설계</div>
        <p class="sub">3단계 스키마와 데이터 독립성으로 시스템을 이해하고, 데이터 모델링과 관계 모델로 설계의 뼈대를 세운 뒤 RPG 실무 프로젝트로 통과합니다.</p>
        <div class="facts">
          <div class="fact"><span>세부 5개</span>01 DB 시스템 · 02 데이터 모델링 · 03 쇼핑몰 ERD · 04 관계 모델 · 05 RPG 사례</div>
          <div class="fact"><span>확인 문제</span>24문항 · 실습 모범 답안 3종</div>
        </div>
      </div>
      <div class="card span"><div class="lbl"><span class="no">전체</span>이어지는 주차</div>
        <p class="sub">정규화와 이상현상, SQL, 인덱스와 물리적 저장 구조, 트랜잭션과 동시성 제어, 회복과 보안, 분산 데이터베이스로 이어집니다.</p>
        <div class="callout info" style="margin-bottom:0"><b>이어지는 내용</b> — 5주차부터는 정규화와 이상현상, SQL, 인덱스와 저장 구조, 트랜잭션과 동시성 제어, 회복과 보안, 분산 데이터베이스로 이어집니다.</div>
      </div>
    </div>
  </div>
</section>
"""

def build_overview2():
    s = open(os.path.join(SRC, "index.body.html"), encoding="utf-8").read()
    s = re.sub(r'<header class="hero".*?</header>', OV_HERO.strip(), s, count=1, flags=re.S)
    s = re.sub(r'<a[^>]*href="[^"]*\.html"[^>]*>(.*?)</a>', r'\1', s, flags=re.S)
    s = re.sub(r'<a[^>]*href="(?:https?://)[^"]*"[^>]*>(.*?)</a>', r'\1', s, flags=re.S)
    s = s.replace('<section class="part" id="how">', OV_FILES.strip() + '\n\n<section class="part" id="how">', 1)
    _a = s.find('<section class="part" id="map">')
    if _a >= 0:
        _b = s.find('</section>', _a)
        if _b > _a:
            s = s[:_a] + OV_MAP.strip() + s[_b + len('</section>'):]
    s = re.sub(r'<section class="part" id="outro">.*?</section>', OV_OUTRO.strip(), s, count=1, flags=re.S)
    s = s.replace('여섯 편', '세 주차')
    s = s.replace('<p>2주차부터 4주차까지의 실제 강의 내용을 세 주차로 나눴습니다. 각 편은 앞 편의 결론에서 시작합니다.</p>',
                  '<p>각 주차에서 무엇을 배우는지 정리했습니다.</p>')
    s = s.replace('<h2>연구 지도 — 세 주차를 차례로<span class="en">Research Map</span></h2>',
                  '<h2>주차별 내용<span class="en">Weekly Map</span></h2>')
    items = toc_items(s)
    used = sorted(set(re.findall(r'data-src="([^"]+)"', s)))
    sub = {k: CHARS[k] for k in used if k in CHARS}
    links = []
    for i, w in enumerate(WEEKS, 1):
        links.append('<a class="tb-l%s" href="#">%s</a>' % ("", esc(w["nav"])))
    toc = ['<div class="toc-h">이 페이지 목차</div>']
    for sid, no, t in items:
        toc.append('<a href="#%s"><i>%s</i><span>%s</span></a>' % (sid, no or "•", html.escape(t)))

    bar = ('<div class="topbar">\n  <div class="tb">\n'
           '    <span class="brand"><span class="dot"></span>DB&nbsp;DESIGN<small>OVERVIEW · 전체 안내</small></span>\n'
           '    <span class="tb-sp"></span>\n    %s\n'
           '    <button class="tocbtn" type="button" aria-expanded="false" aria-controls="tocmenu">목차 ▾</button>\n'
           '  </div>\n  <div class="tocmenu" id="tocmenu">%s</div>\n  <div class="prog"></div>\n</div>'
           % ("", "".join(toc)))
    return """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>OVERVIEW — 데이터베이스 설계 전체 안내</title>
<meta name="description" content="데이터베이스 설계 야간 연구실 교육 자료 전체 안내. 다른 HTML 파일로 연결하지 않습니다.">
<meta name="author" content="안상선 ((주)M-Robo 대표)">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;600;700&display=swap">
<style>
%s
</style>
</head>
<body>
%s
%s
%s
<script>
window.IMG=%s;
%s
</script>
</body>
</html>
""" % (CSS, bar, s, FOOTER, json.dumps(sub, separators=(",", ":")), JS)

TRAPS = {
"week1": [
 ("시트 vs 데이터베이스의 진짜 차이", "속도가 아니라 '보장'입니다. 형식·중복·동시 편집을 도구가 책임지는지가 갈림길입니다."),
 ("POS와 종이 장부", "POS는 팔린 그 순간에 정보가 만들어집니다. 종이는 하루가 끝나야 합계가 나옵니다."),
 ("잔고를 저장된 값으로 오해", "거래내역에서 계산되는 값으로 이해하게 지도합니다. 이체는 트랜잭션으로 묶입니다."),
 ("파이썬 vs 데이터베이스", "둘은 경쟁 관계가 아니라 손과 창고의 관계입니다. 파이썬이 질의하고 결과로 계산합니다."),
 ("SQL 인젝션", "값을 문장에 이어 붙이지 않고 자리표시자(?)로 넘긴다는 원칙을 반복 확인합니다."),
],
"week2": [
 ("데이터 ↔ 정보의 경계", "'평균 구매액'처럼 계산·집계한 결과인지로 판단하게 지도합니다. 가격표에 적힌 값은 데이터, 그것을 모아 계산한 값은 정보입니다."),
 ("명목 ↔ 순서 ↔ 등간 ↔ 비율", "'2배'가 말이 되는지, 절대 영점이 있는지를 기준으로 묻습니다. IQ와 섭씨는 등간, 나이·무게·거리는 비율입니다."),
 ("정형 ↔ 반정형", "JSON은 값과 함께 이름표(키)를 들고 있으므로 반정형입니다. 구조 설명이 데이터 밖에 있으면 정형, 데이터 안에 있으면 반정형입니다."),
 ("자료구조 ↔ 릴레이션", "리스트는 순서가 있고 릴레이션의 튜플은 순서가 없다는 점, 집합의 중복 제거가 곧 키의 유일성이라는 점을 연결해 지도합니다."),
],
"week3": [
 ("중복의 '판단' 비용", "중복 데이터가 나쁜 이유는 저장 공간이 아니라, 같은 값인지 판단하고 관리하는 프로세스가 계속 필요하기 때문입니다."),
 ("위치 참조 ↔ 내용 참조", "파일 번호·블록 주소로 찾으면 위치 참조, '이름이 김철수인 고객'처럼 값의 조건으로 찾으면 내용 참조입니다."),
 ("롤백 ↔ 회복", "롤백은 오류 시 저널 파일로 이전 상태로 되돌리는 것, 회복(redo)은 앞으로 복구하는 것입니다. 방향이 반대입니다."),
 ("DBMS의 장점 ↔ 단점", "'중복을 통제할 수 있다'는 장점, '비용 증가·백업 복잡·중앙관리 취약'은 단점입니다. 장단점을 뒤섞어 고르는 오답이 많습니다."),
 ("세대별 한계", "계층형은 다대다 관계를 표현하지 못합니다. 네트워크형이 그래프 구조로 보완했다는 순서를 기억하게 합니다."),
],
"week4": [
 ("논리적 ↔ 물리적 독립성", "어느 스키마 '사이'의 이야기인지 확인합니다. 개념↔외부가 논리적, 내부↔개념이 물리적입니다."),
 ("차수 ↔ 카디널리티", "'차수=열, 카디널리티=행'으로 고정해 익히게 합니다."),
 ("후보키의 최소성", "(이름+이메일)은 유일하지만 이메일만으로도 구별되므로 후보키가 아닙니다. 유일성만 보고 고르는 오답이 많습니다."),
 ("1:N 변환 방향", "외래키는 항상 N쪽에 둡니다. 1쪽에 두면 한 칸에 여러 값이 생겨 원자성이 깨집니다."),
 ("유도 속성", "나이는 생년월일에서 계산되므로 유도 속성입니다. 값을 저장하지 않고 계산으로 얻는 속성을 구분하게 합니다."),
 ("인덱스 선택", "'활성 퀘스트 목록 조회'에는 player_id + status 복합 인덱스가 맞습니다. 단일 컬럼 인덱스로는 부족한 이유를 조회 조건에서 읽게 합니다."),
],
}

# ─────────────────────────── 실행 ───────────────────────────
def main():
    if os.path.isdir(DIST): shutil.rmtree(DIST)
    os.makedirs(DIST)
    allsecs = {}
    srcfiles = []
    for w in WEEKS:
        for fn in w["src"]:
            if fn not in srcfiles: srcfiles.append(fn)
    for fname in srcfiles:
        allsecs[fname] = load_sections(fname)
    # 주차별 용어 인라인용 사전
    total = 0
    for week in WEEKS:
        entries = {}
        for fname in week["src"]:
            secs, _ = allsecs[fname]
            if "glossary" in secs: entries.update(gl_entries(secs["glossary"]))
        outdir = os.path.join(DIST, week["dir"]); os.makedirs(outdir, exist_ok=True)
        # 표지
        idx = build_week_index(week, allsecs, entries)
        idx = decorate(idx, week["key"] + "/index.html", week, is_index=True)
        idx = re.sub(r"\{\{IMG:([^|]+)\|([^|]*)\|([^}]*)\}\}",
                     lambda m: '<img class="%s" src="%s" alt="%s">' % (m.group(2), IMGREG[m.group(1)], html.escape(m.group(3))), idx)
        open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(idx); total += 1
        print("%-34s %7.1f KB" % (week["dir"] + "/index.html", len(idx.encode())/1024))
        # 세부
        for p in week["pages"]:
            body = [hero(p["crumb"], p["h1"], p["lead"], p["keys"], p["btns"])]
            for _k, (fname, sid) in enumerate(p["secs"]):
                secs, _ = allsecs[fname]
                if sid not in secs: raise SystemExit("MISSING %s #%s" % (fname, sid))
                body.append(secs[sid])
                if _k == 0:
                    _t = DIALOGUES.get(week["key"] + "/" + p["out"])
                    if _t: body.append(talk_html(_t))
            body = inline_terms("\n".join(body), entries)
            body = decorate(body, week["key"] + "/" + p["out"], week)
            html_out = page_html(week, p["out"], p["title"], p["desc"], body)
            open(os.path.join(outdir, p["out"]), "w", encoding="utf-8").write(html_out); total += 1
            print("%-34s %7.1f KB" % (week["dir"] + "/" + p["out"], len(html_out.encode())/1024))
        # 정답
        ans = build_answers(week, allsecs, entries)
        open(os.path.join(outdir, "answers.html"), "w", encoding="utf-8").write(ans); total += 1
        print("%-34s %7.1f KB" % (week["dir"] + "/answers.html", len(ans.encode())/1024))
    ov = build_overview2()
    ov = ov.replace("</header>", "\n" + heroblock("hero_overview") + "\n</header>", 1)
    ov = re.sub(r"\{\{IMG:([^|]+)\|([^|]*)\|([^}]*)\}\}",
                lambda m: '<img class="%s" src="%s" alt="%s">' % (m.group(2), IMGREG[m.group(1)], html.escape(m.group(3))), ov)
    open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(ov); total += 1
    print("%-34s %7.1f KB" % ("index.html", len(ov.encode())/1024))
    print("총 %d개 파일" % total)

if __name__ == "__main__":
    main()
