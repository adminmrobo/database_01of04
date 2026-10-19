/* =========================================================
   데이터베이스 설계 강의자료 — 공통 인터랙션
   © 2025 데이터베이스 설계 강의 | 안상선  (CC BY-NC 4.0)
   ========================================================= */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- 1. 목차 드롭다운 ---------- */
  var tocBtn = $(".tocbtn"), tocMenu = $(".tocmenu");
  if (tocBtn && tocMenu) {
    tocBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      tocMenu.classList.toggle("on");
      tocBtn.setAttribute("aria-expanded", String(tocMenu.classList.contains("on")));
    });
    document.addEventListener("click", function () { tocMenu.classList.remove("on"); });
    tocMenu.addEventListener("click", function (e) { e.stopPropagation(); });
  }

  /* ---------- 2. 읽기 진행률 ---------- */
  var bar = $(".prog");
  if (bar) {
    var upd = function () {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
    };
    window.addEventListener("scroll", upd, { passive: true });
    window.addEventListener("resize", upd);
    upd();
  }

  /* ---------- 3. 확인 문제 채점 ---------- */
  $$(".quiz .q").forEach(function (q) {
    var ok = parseInt(q.getAttribute("data-ok"), 10);
    var ex = q.getAttribute("data-ex") || "";
    var fb = $(".fb", q);
    $$(".opts button", q).forEach(function (b) {
      b.addEventListener("click", function () {
        var i = parseInt(b.getAttribute("data-i"), 10);
        $$(".opts button", q).forEach(function (x) { x.classList.remove("ok", "no"); x.disabled = true; });
        var right = (i === ok);
        b.classList.add(right ? "ok" : "no");
        if (!right) { var t = $$(".opts button", q)[ok]; if (t) t.classList.add("ok"); }
        if (fb) {
          fb.className = "fb on " + (right ? "ok" : "no");
          fb.innerHTML = (right ? "✅ 맞았습니다. " : "❌ 다시 볼까요. ") + ex;
        }
        // 진행 점수 갱신
        var box = q.closest(".quiz"), tot = box ? $$(".q", box).length : 0;
        if (box && tot) {
          if (!box.dataset.done) box.dataset.done = "0";
          if (!box.dataset.scored) box.dataset.scored = "";
          if (box.dataset.scored.indexOf(i + "-" + (q.dataset.idx || $$(".q", box).indexOf(q))) < 0) {
            box.dataset.scored += i + "-" + (q.dataset.idx || $$(".q", box).indexOf(q)) + ",";
            if (right) box.dataset.done = String(parseInt(box.dataset.done, 10) + 1);
          }
          var sc = $(".qscore", box);
          if (sc) sc.textContent = "이 카드 점수 " + box.dataset.done + " / " + tot;
        }
      });
    });
  });

  /* ---------- 4. 코드 복사 / 프롬프트 복사·저장 ---------- */
  function copyText(txt, btn) {
    var done = function () {
      var old = btn.textContent;
      btn.textContent = "복사됨 ✓"; btn.classList.add("done");
      setTimeout(function () { btn.textContent = old; btn.classList.remove("done"); }, 1600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(txt).then(done, function () { fallback(txt, done); });
    } else { fallback(txt, done); }
  }
  function fallback(txt, done) {
    var ta = document.createElement("textarea");
    ta.value = txt; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); done(); } catch (e) { alert("복사에 실패했습니다. 직접 선택해 주세요."); }
    document.body.removeChild(ta);
  }
  function dl(name, txt) {
    var b = new Blob([txt], { type: "text/plain;charset=utf-8" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(b); a.download = name;
    document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 800);
  }
  $$("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var pre = document.getElementById(btn.getAttribute("data-copy"));
      if (pre) copyText(pre.innerText, btn);
    });
  });
  $$("[data-pcopy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var box = btn.closest(".promptbox") || document;
      var pre = $("pre", box);
      if (pre) copyText(pre.innerText, btn);
    });
  });
  $$("[data-ptxt]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var box = btn.closest(".promptbox") || document;
      var pre = $("pre", box);
      if (!pre) return;
      var nm = btn.getAttribute("data-ptxt") || "prompt.txt";
      dl(nm, pre.innerText);
    });
  });
  $$("[data-save]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var pre = document.getElementById(btn.getAttribute("data-save"));
      if (pre) dl((pre.getAttribute("data-name") || "code") + ".sql", pre.innerText);
    });
  });

  /* ---------- 5. 탭 ---------- */
  $$(".tabs").forEach(function (bar2) {
    var tabs = $$(".tab", bar2);
    tabs.forEach(function (t) {
      t.addEventListener("click", function () {
        tabs.forEach(function (x) { x.setAttribute("aria-selected", String(x === t)); });
        var scope = bar2.parentNode;
        $$(".tabpanel", scope).forEach(function (p) { p.classList.remove("on"); });
        var tgt = document.getElementById("tab-" + t.getAttribute("data-tab"));
        if (tgt) tgt.classList.add("on");
      });
    });
  });

  /* ---------- 6. 캐릭터 표정 전환 ---------- */
  $$("img[data-src]").forEach(function (img) {
    var k = img.getAttribute("data-src");
    if (window.IMG && window.IMG[k]) img.src = window.IMG[k];
  });
  $$(".mem").forEach(function (m) {
    var img = $("img", m), btns = $$(".pose button", m);
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        var key = b.getAttribute("data-src");
        if (img && window.IMG && window.IMG[key]) {
          img.src = window.IMG[key];
          img.alt = (m.getAttribute("data-name") || "캐릭터") + " — " + b.textContent;
        }
        btns.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
      });
    });
  });

  /* ---------- 7. 용어 툴팁 ---------- */
  var tip = null;
  function ensureTip() {
    if (!tip) { tip = document.createElement("div"); tip.id = "gttip"; document.body.appendChild(tip); }
    return tip;
  }
  $$(".term").forEach(function (t) {
    var id = t.getAttribute("data-g");
    var card = id ? document.getElementById(id) : null;
    var show = function (e) {
      var box = card ? card : null;
      var tt = ensureTip();
      var title = t.getAttribute("data-t") || (box ? $("b", box).textContent : t.textContent);
      var an = box ? ($(".gl-an", box) || { innerText: "" }).innerText : (t.getAttribute("data-a") || "");
      var mn = box ? ($(".gl-mean", box) || { innerText: "" }).innerText : (t.getAttribute("data-m") || "");
      tt.innerHTML = "<b>" + title + "</b>" + (an ? "<div style='color:#ffb8d6;margin-bottom:5px'>" + an + "</div>" : "") +
        (mn ? "<div style='color:#cfe9ee'>" + mn + "</div>" : "");
      tt.style.display = "block";
      var r = t.getBoundingClientRect();
      var tw = tt.offsetWidth, th = tt.offsetHeight;
      var left = Math.min(Math.max(8, r.left + r.width / 2 - tw / 2), window.innerWidth - tw - 8);
      var top = r.top - th - 10;
      if (top < 8) top = r.bottom + 10;
      tt.style.left = left + "px"; tt.style.top = top + "px";
    };
    t.addEventListener("mouseenter", show);
    t.addEventListener("focus", show);
    t.addEventListener("click", show);
    t.setAttribute("tabindex", "0");
    var hide = function () { if (tip) tip.style.display = "none"; };
    t.addEventListener("mouseleave", hide);
    t.addEventListener("blur", hide);
    document.addEventListener("scroll", hide, { passive: true });
  });

  /* ---------- 8. 단계 애니메이션 ---------- */
  $$(".anim").forEach(function (box) {
    var layers = $$(".anim-layer", box), steps = $$(".anim-steps li", box);
    var prev = $("[data-anim-prev]", box), next = $("[data-anim-next]", box), play = $("[data-anim-play]", box);
    var txt = $(".step-txt", box), i = 0, timer = null;
    var n = layers.length || steps.length;
    if (!n) return;
    function render() {
      layers.forEach(function (l, k) { l.classList.toggle("on", k === i); });
      steps.forEach(function (s, k) { s.classList.toggle("on", k === i); });
      if (txt) txt.textContent = (i + 1) + " / " + n;
    }
    function go(d) { i = (i + d + n) % n; render(); }
    if (prev) prev.addEventListener("click", function () { stop(); go(-1); });
    if (next) next.addEventListener("click", function () { stop(); go(1); });
    function stop() { if (timer) { clearInterval(timer); timer = null; if (play) play.textContent = "▶ 자동 재생"; } }
    if (play) play.addEventListener("click", function () {
      if (timer) { stop(); return; }
      play.textContent = "❚❚ 멈춤";
      timer = setInterval(function () { go(1); }, 2400);
    });
    render();
  });

  /* ---------- 9. 슬라이더 → 계산값 ---------- */
  $$("[data-calc]").forEach(function (box) {
    var out = $("[data-calc-out]", box);
    var inputs = $$("input[type=range]", box);
    function upd() {
      var v = {};
      inputs.forEach(function (x) { v[x.name] = parseFloat(x.value); });
      if (out) out.innerHTML = box.getAttribute("data-calc").replace(/\{(\w+)\}/g, function (_, k) {
        return (v[k] !== undefined ? (Math.round(v[k] * 100) / 100).toLocaleString("ko-KR") : "");
      });
      $$("[data-out]", box).forEach(function (el) {
        var k = el.getAttribute("data-out");
        if (v[k] !== undefined) el.textContent = Math.round(v[k] * 100) / 100;
      });
    }
    inputs.forEach(function (x) { x.addEventListener("input", upd); });
    upd();
  });

  /* ---------- 10. 상단으로 ---------- */
  var top = $(".totop");
  if (top) {
    top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
    window.addEventListener("scroll", function () {
      top.style.opacity = window.scrollY > 600 ? "1" : "0";
    }, { passive: true });
  }
})();
