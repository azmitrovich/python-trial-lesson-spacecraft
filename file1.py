# @title 🚀 Space Runner - Colab Setup
# Step 1: Create templates folder
!mkdir -p templates

# Step 2: Write the game HTML to a file
html_content = r'''
<!doctype html>
<html>
<head>
  <title>Space Runner</title>
  <meta charset="utf-8">
  <style>
    html, body {
      margin: 0; padding: 0;
      background: #000;
      overflow: hidden;
      font-family: 'Segoe UI', Arial, sans-serif;
      color: #9fdcff;
      user-select: none;
    }
    #wrap {
      position: relative;
      width: 100vw; height: 100vh;
      display: flex; align-items: center; justify-content: center;
    }
    canvas {
      display: block;
      box-shadow: 0 0 40px rgba(80, 180, 255, 0.4);
      border-radius: 6px;
      background: #000;
    }
    #hud {
      position: absolute;
      top: 12px; left: 12px;
      z-index: 3;
      font-size: 16px;
      line-height: 1.45;
      text-shadow: 0 0 8px #29a6ff;
      pointer-events: none;
    }
    #hudMode { font-family: Consolas, 'Courier New', monospace; font-size: 13px; letter-spacing: 1px; }
    #hudMode.bad { color: #ff8d8d; text-shadow: 0 0 8px #ff4040; }
    #codeBtn {
      position: absolute;
      top: 12px; right: 12px;
      z-index: 4;
      padding: 8px 14px;
      font-family: Consolas, 'Courier New', monospace;
      font-size: 13px;
      letter-spacing: 2px;
      color: #b6ff8a;
      background: #04140c;
      border: 1px solid #1f8f3a;
      border-radius: 4px;
      cursor: pointer;
      box-shadow: 0 0 14px rgba(80, 255, 120, 0.28);
    }
    #codeBtn:hover { background: #0c2a16; box-shadow: 0 0 18px rgba(80, 255, 120, 0.5); }
    .lang-switch { display: flex; gap: 6px; margin-bottom: 10px; }
    .lang-switch button {
      font-family: Consolas, 'Courier New', monospace;
      font-size: 12px;
      letter-spacing: 1px;
      padding: 4px 10px;
      border-radius: 999px;
      border: 1px solid rgba(90, 180, 255, 0.45);
      background: transparent;
      color: #9fdcff;
      cursor: pointer;
    }
    .lang-switch button.on {
      background: #0b2c5a;
      color: #7ce7ff;
      box-shadow: 0 0 12px rgba(41, 166, 255, 0.4);
    }
    #overlay {
      position: absolute;
      inset: 0;
      z-index: 5;
      display: flex;
      flex-direction: column;
      align-items: center;
      overflow: auto;
      padding: 22px 16px;
      background: rgba(0, 0, 16, 0.78);
      backdrop-filter: blur(4px);
    }
    .menu-card {
      width: min(980px, calc(100vw - 32px));
      max-width: 100%;
      margin: auto;
      display: flex;
      gap: 28px;
      align-items: stretch;
      box-sizing: border-box;
    }
    .menu-copy {
      flex: 0.9 1 0;
      text-align: left;
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-width: 0;
    }
    #overlay h1 {
      font-size: 38px;
      margin: 0 0 8px;
      color: #7ce7ff;
      text-shadow: 0 0 18px #29a6ff, 0 0 40px #0a6cff;
      letter-spacing: 3px;
    }
    #overlay p { margin: 6px 0; font-size: 15px; color: #cfe9ff; line-height: 1.45; }
    .modes {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin: 12px 0 8px;
    }
    .modes span {
      border: 1px solid rgba(90, 180, 255, 0.35);
      background: rgba(6, 20, 40, 0.72);
      border-radius: 999px;
      padding: 4px 10px;
      color: #d5ecff;
      font-size: 13px;
    }
    .modes b {
      color: #7ce7ff;
      font-family: Consolas, 'Courier New', monospace;
      font-weight: 600;
      margin-right: 6px;
    }
    .modes em { font-style: normal; }
    .note { color: #9fbcd8 !important; font-size: 13px !important; }
    #startBtn {
      margin-top: 16px;
      align-self: flex-start;
      padding: 12px 28px;
      font-size: 18px;
      border: 2px solid #2b8fff;
      background: #061225;
      color: #7ce7ff;
      border-radius: 30px;
      cursor: pointer;
      letter-spacing: 2px;
      transition: 0.2s;
    }
    #startBtn:hover {
      background: #0b2c5a;
      box-shadow: 0 0 20px #29a6ff;
    }
    .terminal {
      flex: 1.15 1 0;
      min-width: 0;
      min-height: 430px;
      display: flex;
      flex-direction: column;
      background: #07140c;
      border: 1px solid #1d7a38;
      border-radius: 10px;
      box-shadow: 0 0 0 1px rgba(80, 255, 120, 0.15), 0 0 32px rgba(40, 255, 100, 0.18), inset 0 0 40px rgba(0, 0, 0, 0.45);
      overflow: hidden;
      user-select: text;
    }
    .terminal:focus-within {
      box-shadow: 0 0 0 1px #49ff74, 0 0 28px rgba(57, 255, 106, 0.35), inset 0 0 40px rgba(0, 0, 0, 0.45);
    }
    .term-bar {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 12px;
      background: #0c1f12;
      border-bottom: 1px solid #174f28;
      font-family: Consolas, 'Courier New', monospace;
      font-size: 12px;
      color: #8fce78;
    }
    .dots { display: flex; gap: 5px; }
    .dots i {
      width: 9px; height: 9px; border-radius: 50%; display: block;
      background: #2a5a32;
    }
    .dots i:nth-child(1) { background: #ff5f57; }
    .dots i:nth-child(2) { background: #febc2e; }
    .dots i:nth-child(3) { background: #28c840; }
    .term-title { flex: 1; }
    .term-live {
      color: #ff5a5a;
      letter-spacing: 1px;
      animation: blink 1.2s steps(1) infinite;
    }
    .term-screen {
      position: relative;
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background:
        radial-gradient(ellipse at center, transparent 45%, rgba(0, 0, 0, 0.42) 100%),
        repeating-linear-gradient(to bottom, rgba(120, 255, 150, 0.035) 0 1px, transparent 1px 3px),
        #04110a;
      min-height: 250px;
    }
    .term-prompt {
      padding: 8px 12px 0;
      font-family: Consolas, 'Courier New', monospace;
      font-size: 12px;
      color: #6dca78;
    }
    .term-prompt .dir { color: #d8ffe4; }
    #code {
      box-sizing: border-box;
      flex: 1;
      width: 100%;
      min-width: 0;
      min-height: 220px;
      margin: 0;
      padding: 8px 12px 12px;
      border: 0;
      resize: none;
      outline: none;
      background: transparent;
      color: #c8ff9a;
      caret-color: #dbffc4;
      font: 15px/1.45 Consolas, 'Courier New', monospace;
      font-variant-ligatures: none;
      tab-size: 2;
      white-space: pre;
      overflow: auto;
      text-shadow: 0 0 6px rgba(120, 255, 110, 0.35);
      user-select: text;
    }
    #code::placeholder { color: rgba(140, 200, 140, 0.35); }
    #code::selection { background: rgba(80, 255, 120, 0.28); }
    .beam {
      position: absolute;
      left: 0; right: 0;
      height: 28%;
      top: 0;
      background: linear-gradient(to bottom, transparent, rgba(140, 255, 170, 0.06), transparent);
      animation: scan 4.8s linear infinite;
      pointer-events: none;
    }
    .term-help, .term-status {
      box-sizing: border-box;
      padding: 7px 12px;
      font-family: Consolas, 'Courier New', monospace;
      font-size: 11px;
      line-height: 1.45;
      letter-spacing: 0.2px;
      color: #7ebf86;
      background: #08160e;
      border-top: 1px solid #143d22;
    }
    .term-help { white-space: normal; }
    .term-status { display: flex; align-items: center; gap: 8px; color: #b6ff8a; }
    .terminal.bad .term-status { color: #ff9a9a; }
    #statusDot {
      width: 8px; height: 8px; border-radius: 50%; flex: none;
      background: #39ff6a;
      box-shadow: 0 0 8px #39ff6a;
    }
    .terminal.bad #statusDot { background: #ff3b3b; box-shadow: 0 0 8px #ff3b3b; }
    .hidden { display: none !important; }
    @keyframes blink { 50% { opacity: 0; } }
    @keyframes scan {
      from { transform: translateY(-30%); }
      to { transform: translateY(320%); }
    }
    @media (max-width: 860px) {
      .menu-card { flex-direction: column; width: min(560px, 94vw); }
      .menu-copy { text-align: left; }
      #overlay { padding: 14px 12px; }
      #overlay h1 { font-size: 30px; margin-bottom: 4px; }
      .terminal { min-height: 360px; }
    }
    @media (prefers-reduced-motion: reduce) {
      .term-live, .beam { animation: none; }
    }
  </style>
</head>
<body>
  <div id="wrap">
    <canvas id="game" width="900" height="520"></canvas>
    <div id="hud">
      <div id="hudScore">SCORE 0 &nbsp;|&nbsp; BEST 0</div>
      <div id="hudMode">MODE —</div>
    </div>
    <button id="codeBtn" class="hidden" type="button">PYTHON</button>
    <div id="overlay">
      <div class="menu-card">
        <section class="menu-copy">
          <div class="lang-switch" role="group">
            <button type="button" id="langRu">RU</button>
            <button type="button" id="langEn">EN</button>
          </div>
          <h1 id="title">SPACE RUNNER</h1>
          <p id="subtitle"></p>
          <p id="scoreLine" class="hidden"></p>
          <div class="modes">
            <span><b>fly</b> <em data-i18n="modeFly"></em></span>
            <span><b>down</b> <em data-i18n="modeDown"></em></span>
            <span><b>turbo</b> <em data-i18n="modeTurbo"></em></span>
            <span><b>shoot</b> <em data-i18n="modeShoot"></em></span>
          </div>
          <p class="note" data-i18n="note"></p>
          <button id="startBtn" type="button"></button>
        </section>
        <section class="terminal" id="terminal">
          <div class="term-bar">
            <span class="dots"><i></i><i></i><i></i></span>
            <span class="term-title">root@ship:~/flight.py</span>
            <span class="term-live">REC</span>
          </div>
          <div class="term-screen">
            <div class="term-prompt"><span>root@ship</span>:<span class="dir">~</span>$ python3 flight.py</div>
            <textarea id="code" spellcheck="false" autocomplete="off" autocorrect="off" autocapitalize="off" wrap="off" aria-label="Python код управления кораблём"></textarea>
            <div class="beam"></div>
          </div>
          <div class="term-help">if / elif / else · == != and or not · "w" "s" "up" "down" "space" "f"</div>
          <div class="term-status"><span id="statusDot"></span><span id="termStatus">…</span></div>
        </section>
      </div>
    </div>
  </div>

<script>
(() => {
  const canvas = document.getElementById('game');
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const hudScore = document.getElementById('hudScore');
  const hudMode = document.getElementById('hudMode');
  const overlay = document.getElementById('overlay');
  const startBtn = document.getElementById('startBtn');
  const codeBtn = document.getElementById('codeBtn');
  const codeEl = document.getElementById('code');
  const terminal = document.getElementById('terminal');
  const termStatus = document.getElementById('termStatus');
  const titleEl = document.getElementById('title');
  const subtitleEl = document.getElementById('subtitle');
  const scoreLine = document.getElementById('scoreLine');

  const CODE_KEY = 'spaceRunnerFlightPy';
  const LANG_KEY = 'spaceRunnerLang';
  const LEGACY_CODE = [
    '# key — имя нажатой клавиши',
    '# mode — команда кораблю',
    '',
    'if key == "w" or key == "up":',
    '  mode = "fly"',
    'elif key == "s" or key == "down":',
    '  mode = "down"',
    'elif key == "space":',
    '  mode = "turbo"',
    'elif key == "f":',
    '  mode = "shoot"'
  ].join('\n');

  const I18N = {
    ru: {
      subtitle: 'Напиши условия на Python — корабль оживёт.',
      subtitle_over: 'Поправь код и взлетай снова.',
      subtitle_pause: 'Код подхватится сразу, как продолжишь полёт.',
      pause: 'ПАУЗА',
      start: 'СТАРТ',
      retry: 'ЕЩЁ РАЗ',
      resume: 'ДАЛЬШЕ',
      score_line: 'Счёт: <b>{s}</b> · Рекорд: <b>{b}</b>',
      modeFly: 'вверх, или up',
      modeDown: 'вниз',
      modeTurbo: 'ускорение',
      modeShoot: 'астероид рушится',
      note: 'Игра запускает код отдельно для каждой зажатой клавиши и смотрит на mode. Раскладка не важна: физическая клавиша W — это всегда "w".',
      aria_code: 'Python код управления кораблём',
      hud_error: 'ОШИБКА',
      saved_short: ' · сохранено',
      saved_ok: 'OK · сохранено в браузере',
      line: 'Строка',
      err_elif: 'elif / else без if',
      err_indent: 'лишний отступ',
      err_syntax: 'синтаксическая ошибка',
      err_block: 'после : нужен блок с отступом',
      err_write: 'напиши if / elif / else или mode = "..."',
      err_only_mode: 'можно записать только mode',
      err_else: 'здесь нужно просто else:',
      err_empty: 'пустое условие',
      err_not_in: 'после not ждал in',
      err_value: 'не хватает значения',
      err_token: 'не понял «{x}»',
      err_string: 'незакрытая строка',
      err_number: 'странное число',
      err_list: 'не закрыт список',
      err_paren: 'не закрыта скобка',
      err_name: 'неизвестное имя {x}',
      err_in: 'после in нужен список',
      err_cmp: 'через < и > сравниваются только числа',
      err_expr: 'не понял выражение',
      err_mode: 'mode должен быть строкой, например "fly"'
    },
    en: {
      subtitle: 'Write Python conditions and the ship comes alive.',
      subtitle_over: 'Fix the code and launch again.',
      subtitle_pause: 'The ship picks up your code as soon as you resume.',
      pause: 'PAUSED',
      start: 'LAUNCH',
      retry: 'RETRY',
      resume: 'RESUME',
      score_line: 'Score: <b>{s}</b> · Best: <b>{b}</b>',
      modeFly: 'climb, up works too',
      modeDown: 'lower',
      modeTurbo: 'boost',
      modeShoot: 'breaks an asteroid',
      note: 'The game runs your code once for each held key and reads mode. Layout does not matter: the physical W key is always "w".',
      aria_code: 'Python code that controls the ship',
      hud_error: 'ERROR',
      saved_short: ' · saved',
      saved_ok: 'OK · saved in this browser',
      line: 'Line',
      err_elif: 'elif / else without if',
      err_indent: 'unexpected indent',
      err_syntax: 'syntax error',
      err_block: 'expected an indented block after :',
      err_write: 'write if / elif / else or mode = "..."',
      err_only_mode: 'only mode can be assigned',
      err_else: 'use a plain else:',
      err_empty: 'empty condition',
      err_not_in: 'expected in after not',
      err_value: 'missing value',
      err_token: 'unexpected "{x}"',
      err_string: 'unterminated string',
      err_number: 'bad number',
      err_list: 'unclosed list',
      err_paren: 'unclosed parenthesis',
      err_name: 'unknown name {x}',
      err_in: 'the right side of in must be a list',
      err_cmp: 'only numbers can be compared with < and >',
      err_expr: 'could not understand the expression',
      err_mode: 'mode must be a string, for example "fly"'
    }
  };

  let lang = 'ru';
  try {
    const savedLang = localStorage.getItem(LANG_KEY);
    if (savedLang === 'en' || savedLang === 'ru') lang = savedLang;
  } catch (err) {}

  function t(key) {
    const pack = I18N[lang] || I18N.ru;
    return pack[key] != null ? pack[key] : (I18N.ru[key] || key);
  }

  function raise(line, code, extra) {
    const err = new Error(code);
    err.student = true;
    err.line = line || 0;
    err.code = code;
    err.extra = extra || '';
    return err;
  }

  function formatError(e) {
    if (!e) return '';
    if (typeof e === 'string') return e;
    let msg = t(e.code || 'err_syntax');
    if (e.extra) msg = msg.split('{x}').join(e.extra);
    if (e.line) return t('line') + ' ' + e.line + ': ' + msg;
    return msg;
  }

  function compileStudent(src) {
    try {
      return { program: parseProgram(src), error: null };
    } catch (e) {
      return { program: null, error: e };
    }
  }

  function runStudent(program, key) {
    const env = { key: key, mode: null };
    execBlock(program, env);
    return env.mode;
  }

  function parseProgram(src) {
    const text = String(src).replace(/^\uFEFF/, '').replace(/\r\n/g, '\n').replace(/\r/g, '\n').replace(/\t/g, '    ');
    const lines = text.split('\n');
    const items = [];
    for (let n = 0; n < lines.length; n++) {
      const stripped = stripComment(lines[n]);
      if (!stripped.trim()) continue;
      const indent = stripped.match(/^ */)[0].length;
      items.push({ indent: indent, text: stripped.trim(), line: n + 1 });
    }
    if (!items.length) return [];
    const base = items[0].indent;
    const parsed = parseBlock(items, 0, base);
    if (parsed.i < items.length) {
      const bad = items[parsed.i];
      if (/^(elif|else)\b/.test(bad.text) && bad.indent === base) {
        throw raise(bad.line, 'err_elif');
      }
      if (bad.indent > base) throw raise(bad.line, 'err_indent');
      throw raise(bad.line, 'err_syntax');
    }
    return parsed.stmts;
  }

  function stripComment(line) {
    let out = '';
    let quote = null;
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (quote) {
        out += c;
        if (c === '\\' && i + 1 < line.length) { out += line[++i]; continue; }
        if (c === quote) quote = null;
      } else if (c === '"' || c === "'") {
        quote = c;
        out += c;
      } else if (c === '#') {
        break;
      } else {
        out += c;
      }
    }
    return out;
  }

  function parseBlock(items, start, indent) {
    const stmts = [];
    let i = start;
    while (i < items.length && items[i].indent === indent) {
      const before = i;
      const it = items[i];
      const header = parseHeader(it.text, it.line);
      if (header && (header.kind === 'elif' || header.kind === 'else')) break;
      if (header && header.kind === 'if') {
        const node = { type: 'if', test: parseExpr(header.expr, it.line), body: [], elifs: [], elseBody: null, line: it.line };
        i++;
        if (i >= items.length || items[i].indent <= indent) {
          throw raise(it.line, 'err_block');
        }
        let parsed = parseBlock(items, i, items[i].indent);
        node.body = parsed.stmts;
        i = parsed.i;
        while (i < items.length && items[i].indent === indent) {
          const nx = items[i];
          const h = parseHeader(nx.text, nx.line);
          if (h && h.kind === 'elif') {
            i++;
            if (i >= items.length || items[i].indent <= indent) {
              throw raise(nx.line, 'err_block');
            }
            parsed = parseBlock(items, i, items[i].indent);
            node.elifs.push({ test: parseExpr(h.expr, nx.line), body: parsed.stmts, line: nx.line });
            i = parsed.i;
          } else if (h && h.kind === 'else') {
            i++;
            if (i >= items.length || items[i].indent <= indent) {
              throw raise(nx.line, 'err_block');
            }
            parsed = parseBlock(items, i, items[i].indent);
            node.elseBody = parsed.stmts;
            i = parsed.i;
            break;
          } else break;
        }
        stmts.push(node);
      } else if (it.text === 'pass') {
        i++;
      } else {
        const assign = /^([A-Za-z_]\w*)\s*=(?!=)\s*(.+)$/.exec(it.text);
        if (!assign) throw raise(it.line, 'err_write');
        if (assign[1] !== 'mode') throw raise(it.line, 'err_only_mode');
        stmts.push({ type: 'assign', expr: parseExpr(assign[2], it.line), line: it.line });
        i++;
      }
      if (i === before) throw raise(it.line, 'err_syntax');
    }
    return { stmts: stmts, i: i };
  }

  function parseHeader(text, line) {
    if (!text.endsWith(':')) return null;
    const head = text.slice(0, -1).trim();
    if (/^else\b/.test(head)) {
      if (head !== 'else') throw raise(line, 'err_else');
      return { kind: 'else' };
    }
    let kind = null;
    let expr = '';
    if (/^elif\b/.test(head)) { kind = 'elif'; expr = head.replace(/^elif\b/, '').trim(); }
    else if (/^if\b/.test(head)) { kind = 'if'; expr = head.replace(/^if\b/, '').trim(); }
    else return null;
    if (!expr) throw raise(line, 'err_empty');
    return { kind: kind, expr: expr };
  }

  function parseExpr(source, line) {
    const src = source;
    let i = 0;
    function fail(code, extra) {
      throw raise(line, code, extra);
    }
    function skip() { while (src[i] === ' ' || src[i] === '\t') i++; }
    function matchWord(word) {
      skip();
      if (src.startsWith(word, i) && !/[A-Za-z0-9_]/.test(src[i + word.length] || '')) {
        i += word.length;
        return true;
      }
      return false;
    }
    function parseOr() {
      let left = parseAnd();
      while (matchWord('or')) left = { type: 'or', left: left, right: parseAnd() };
      return left;
    }
    function parseAnd() {
      let left = parseNot();
      while (matchWord('and')) left = { type: 'and', left: left, right: parseNot() };
      return left;
    }
    function parseNot() {
      skip();
      if (matchWord('not')) return { type: 'not', expr: parseNot() };
      return parseComparison();
    }
    function parseComparison() {
      const left = parsePrimary();
      skip();
      if (matchWord('not')) {
        if (!matchWord('in')) fail('err_not_in');
        return { type: 'notIn', left: left, right: parsePrimary() };
      }
      if (matchWord('in')) return { type: 'in', left: left, right: parsePrimary() };
      const ops = ['==', '!=', '<=', '>=', '<', '>'];
      for (let k = 0; k < ops.length; k++) {
        const op = ops[k];
        if (src.startsWith(op, i)) {
          i += op.length;
          return { type: 'cmp', op: op, left: left, right: parsePrimary() };
        }
      }
      return left;
    }
    function parsePrimary() {
      skip();
      if (i >= src.length) fail('err_value');
      const c = src[i];
      if (c === '"' || c === "'") return parseString();
      if (c === '(' || c === '[') return parseGroup(c);
      if (/[0-9]/.test(c)) return parseNumber();
      if (/[A-Za-z_]/.test(c)) {
        let name = '';
        while (/[A-Za-z0-9_]/.test(src[i] || '')) name += src[i++];
        return { type: 'name', name: name };
      }
      fail('err_token', src.slice(i, i + 12));
    }
    function parseString() {
      const q = src[i++];
      let s = '';
      while (i < src.length && src[i] !== q) {
        if (src[i] === '\\') {
          i++;
          const n = src[i++] || '';
          s += n === 'n' ? '\n' : n === 't' ? '\t' : n;
        } else {
          s += src[i++];
        }
      }
      if (src[i] !== q) fail('err_string');
      i++;
      return { type: 'str', value: s };
    }
    function parseNumber() {
      let num = '';
      while (/[0-9.]/.test(src[i] || '')) num += src[i++];
      if (num === '.' || num.split('.').length > 2) fail('err_number');
      return { type: 'num', value: parseFloat(num) };
    }
    function parseGroup(open) {
      const close = open === '(' ? ')' : ']';
      i++;
      skip();
      if (src[i] === close) { i++; return { type: 'list', items: [] }; }
      const first = parseOr();
      skip();
      if (src[i] === ',') {
        const items = [first];
        while (src[i] === ',') {
          i++;
          skip();
          if (src[i] === close) break;
          items.push(parseOr());
          skip();
        }
        if (src[i] !== close) fail('err_list');
        i++;
        return { type: 'list', items: items };
      }
      if (open === '[') {
        if (src[i] !== ']') fail('err_list');
        i++;
        return { type: 'list', items: [first] };
      }
      if (src[i] !== ')') fail('err_paren');
      i++;
      return first;
    }
    const ast = parseOr();
    skip();
    if (i < src.length) fail('err_token', src.slice(i, i + 12));
    return ast;
  }

  function execBlock(stmts, env) {
    for (let s = 0; s < stmts.length; s++) {
      const node = stmts[s];
      try {
        if (node.type === 'assign') env.mode = evalExpr(node.expr, env);
        else if (node.type === 'if') {
          if (truthy(evalExpr(node.test, env))) execBlock(node.body, env);
          else {
            let taken = false;
            for (let b = 0; b < node.elifs.length; b++) {
              if (truthy(evalExpr(node.elifs[b].test, env))) {
                execBlock(node.elifs[b].body, env);
                taken = true;
                break;
              }
            }
            if (!taken && node.elseBody) execBlock(node.elseBody, env);
          }
        }
      } catch (e) {
        if (e && e.student) {
          if (!e.line) e.line = node.line;
          throw e;
        }
        throw raise(node.line, 'err_syntax');
      }
    }
  }

  function evalExpr(node, env) {
    if (node.type === 'str') return node.value;
    if (node.type === 'num') return node.value;
    if (node.type === 'name') {
      if (node.name === 'True') return true;
      if (node.name === 'False') return false;
      if (node.name === 'None') return null;
      if (Object.prototype.hasOwnProperty.call(env, node.name)) return env[node.name];
      throw raise(0, 'err_name', node.name);
    }
    if (node.type === 'list') return node.items.map(item => evalExpr(item, env));
    if (node.type === 'not') return !truthy(evalExpr(node.expr, env));
    if (node.type === 'or') {
      const left = evalExpr(node.left, env);
      return truthy(left) ? left : evalExpr(node.right, env);
    }
    if (node.type === 'and') {
      const left = evalExpr(node.left, env);
      return truthy(left) ? evalExpr(node.right, env) : left;
    }
    if (node.type === 'in' || node.type === 'notIn') {
      const left = evalExpr(node.left, env);
      const right = evalExpr(node.right, env);
      if (!Array.isArray(right)) throw raise(0, 'err_in');
      const found = right.some(item => pyEq(item, left));
      return node.type === 'in' ? found : !found;
    }
    if (node.type === 'cmp') {
      const left = evalExpr(node.left, env);
      const right = evalExpr(node.right, env);
      if (node.op === '==') return pyEq(left, right);
      if (node.op === '!=') return !pyEq(left, right);
      if (typeof left !== 'number' || typeof right !== 'number') throw raise(0, 'err_cmp');
      if (node.op === '<') return left < right;
      if (node.op === '>') return left > right;
      if (node.op === '<=') return left <= right;
      if (node.op === '>=') return left >= right;
    }
    throw raise(0, 'err_expr');
  }

  function truthy(v) {
    if (v === null || v === false || v === 0 || v === '') return false;
    if (Array.isArray(v) && v.length === 0) return false;
    return true;
  }

  function pyEq(a, b) { return a === b; }

  let program = null;
  let programError = null;
  let lastRuntime = null;
  let shownStatus = '';

  function loadCode() {
    try {
      const saved = localStorage.getItem(CODE_KEY);
      if (saved === null) return '';
      if (saved.replace(/\s+$/, '') === LEGACY_CODE) return '';
      return saved;
    } catch (err) {
      return '';
    }
  }

  function saveCode(text) {
    try { localStorage.setItem(CODE_KEY, text); } catch (err) {}
  }

  function setStatus(ok, text) {
    const sig = (ok ? '1' : '0') + text;
    if (sig === shownStatus) return;
    shownStatus = sig;
    terminal.classList.toggle('bad', !ok);
    termStatus.textContent = text;
  }

  function recompile() {
    saveCode(codeEl.value);
    const compiled = compileStudent(codeEl.value);
    program = compiled.program;
    programError = compiled.error;
    lastRuntime = '';
    if (programError) setStatus(false, formatError(programError) + t('saved_short'));
    else setStatus(true, t('saved_ok'));
  }

  function noteRuntime(err) {
    const text = err ? formatError(err) : '';
    if (text === lastRuntime) return;
    lastRuntime = text;
    if (text) setStatus(false, text + t('saved_short'));
    else if (!programError) setStatus(true, t('saved_ok'));
  }

  function indentUnit() {
    const lines = codeEl.value.split('\n');
    for (let i = 0; i < lines.length; i++) {
      const m = /^( +)\S/.exec(lines[i]);
      if (m) return ' '.repeat(Math.min(m[1].length, 8));
    }
    return '  ';
  }

  function insertText(text) {
    const start = codeEl.selectionStart;
    const end = codeEl.selectionEnd;
    const val = codeEl.value;
    codeEl.value = val.slice(0, start) + text + val.slice(end);
    const pos = start + text.length;
    codeEl.selectionStart = codeEl.selectionEnd = pos;
    recompile();
  }

  codeEl.value = loadCode();
  recompile();
  codeEl.addEventListener('input', recompile);
  codeEl.addEventListener('focus', () => { for (const k in keys) keys[k] = false; });
  codeEl.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      e.stopPropagation();
      insertText(indentUnit());
    } else if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      e.stopPropagation();
      const val = codeEl.value;
      const start = codeEl.selectionStart;
      const lineStart = val.lastIndexOf('\n', start - 1) + 1;
      const current = val.slice(lineStart, start);
      const indent = (current.match(/^ */) || [''])[0];
      const extra = /:\s*$/.test(current) ? indentUnit() : '';
      insertText('\n' + indent + extra);
    }
  });

  // -------------------- State --------------------
  let running = false;
  let paused = false;
  let over = false;
  let overlayTimer = null;

  const ship = { x: 110, y: H / 2, r: 16, vy: 0, tilt: 0 };
  const shipMaxVy = 6.5;

  const stars = [];
  const starLayers = [
    { count: 90,  speed: 0.6, size: 1,   color: 'rgba(120,180,255,0.5)' },
    { count: 60,  speed: 1.6, size: 1.4, color: 'rgba(180,220,255,0.7)' },
    { count: 40,  speed: 3.2, size: 2,   color: 'rgba(255,255,255,0.9)' },
  ];

  const asteroids = [];
  const particles = [];
  const pickups = [];
  const bullets = [];
  const floaters = [];

  let score = 0;
  let best = 0;
  try { best = parseInt(localStorage.getItem('spaceRunnerBest') || '0', 10) || 0; } catch (err) { best = 0; }
  let spawnTimer = 0;
  let spawnInterval = 900;
  let speedBoost = 0;
  let boosting = false;
  let shootCooldown = 0;
  let muzzle = 0;
  let shake = 0;
  let boomFlash = 0;
  let modeLabel = 'MODE —';
  let modeBad = false;
  let menuKind = 'start';

  const keys = {};
  const IGNORE_KEYS = new Set(['shift', 'control', 'alt', 'meta', 'capslock', 'tab', 'escape', 'os']);

  function rand(a, b) { return a + Math.random() * (b - a); }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }

  function normalizeKey(k) {
    if (k === ' ' || k === 'Spacebar') return 'space';
    if (k === 'ArrowUp') return 'up';
    if (k === 'ArrowDown') return 'down';
    if (k === 'ArrowLeft') return 'left';
    if (k === 'ArrowRight') return 'right';
    if (k === 'Enter') return 'enter';
    return String(k).toLowerCase();
  }

  // e.code is the physical key, so a Russian layout still yields "w" for the W key.
  function keyNameFromEvent(e) {
    const code = e.code || '';
    if (code === 'Space') return 'space';
    if (code === 'ArrowUp') return 'up';
    if (code === 'ArrowDown') return 'down';
    if (code === 'ArrowLeft') return 'left';
    if (code === 'ArrowRight') return 'right';
    if (code === 'Enter' || code === 'NumpadEnter') return 'enter';
    let m = /^Key([A-Z])$/.exec(code);
    if (m) return m[1].toLowerCase();
    m = /^Digit([0-9])$/.exec(code);
    if (m) return m[1];
    m = /^Numpad([0-9])$/.exec(code);
    if (m) return m[1];
    return normalizeKey(e.key || '');
  }

  function pressedKeys() {
    const out = new Set();
    for (const k in keys) {
      if (!keys[k]) continue;
      const name = normalizeKey(k);
      if (!IGNORE_KEYS.has(name)) out.add(name);
    }
    return out;
  }

  function initStars() {
    stars.length = 0;
    for (const layer of starLayers) {
      for (let i = 0; i < layer.count; i++) {
        stars.push({ x: Math.random() * W, y: Math.random() * H, layer: layer });
      }
    }
  }

  function resetGame() {
    clearTimeout(overlayTimer);
    overlayTimer = null;
    over = false;
    score = 0;
    spawnTimer = 0;
    spawnInterval = 900;
    asteroids.length = 0;
    particles.length = 0;
    pickups.length = 0;
    bullets.length = 0;
    floaters.length = 0;
    ship.y = H / 2;
    ship.vy = 0;
    ship.tilt = 0;
    boosting = false;
    speedBoost = 0;
    shootCooldown = 0;
    muzzle = 0;
    shake = 0;
    boomFlash = 0;
    modeLabel = 'MODE —';
    for (const k in keys) keys[k] = false;
    updateHUD();
  }

  function updateHUD() {
    if (score > best) {
      best = score;
      try { localStorage.setItem('spaceRunnerBest', best); } catch (err) {}
    }
    hudScore.textContent = 'SCORE ' + Math.floor(score) + '  |  BEST ' + Math.floor(best);
    hudMode.textContent = modeLabel;
    hudMode.classList.toggle('bad', modeBad || modeLabel.indexOf('?') !== -1);
  }

  function makeAsteroid() {
    const r = rand(14, 38);
    const sides = Math.floor(rand(6, 11));
    const pts = [];
    for (let i = 0; i < sides; i++) {
      const a = (Math.PI * 2 * i) / sides;
      pts.push({ a: a, rr: r * rand(0.72, 1.15) });
    }
    return {
      x: W + r + 10,
      y: rand(r, H - r),
      r: r,
      vy: rand(-0.8, 0.8),
      vx: rand(2.2, 4.2) + score * 0.01,
      angle: Math.random() * Math.PI * 2,
      spin: rand(-0.03, 0.03),
      points: pts,
    };
  }

  function makePickup() {
    return {
      x: W + 20,
      y: rand(40, H - 40),
      r: 10,
      vx: rand(2.6, 4.0),
      phase: Math.random() * Math.PI * 2,
    };
  }

  function spawnExhaust() {
    const speed = boosting ? 4 : 2;
    for (let i = 0; i < (boosting ? 3 : 1); i++) {
      particles.push({
        x: ship.x - ship.r * 0.7,
        y: ship.y + rand(-4, 4),
        vx: rand(-speed - 2, -speed),
        vy: rand(-0.6, 0.6),
        life: 1,
        decay: rand(0.02, 0.05),
        color: boosting ? 'hsl(' + rand(15, 40) + ', 100%, ' + rand(60, 80) + '%)'
                        : 'hsl(' + rand(190, 220) + ', 100%, ' + rand(55, 75) + '%)',
        size: rand(1.5, 3.5),
      });
    }
  }

  function explode(x, y, n, hueBase) {
    for (let i = 0; i < n; i++) {
      const a = Math.random() * Math.PI * 2;
      const s = rand(1, 7);
      particles.push({
        x: x, y: y,
        vx: Math.cos(a) * s,
        vy: Math.sin(a) * s,
        life: 1,
        decay: rand(0.015, 0.04),
        color: 'hsl(' + (hueBase + rand(-30, 30)) + ', 100%, ' + rand(50, 80) + '%)',
        size: rand(1.5, 4),
      });
    }
  }

  function shatter(a) {
    explode(a.x, a.y, 26, 24);
    explode(a.x, a.y, 8, 48);
    particles.push({
      x: a.x, y: a.y, vx: 0, vy: 0, life: 1, decay: 0.04,
      color: 'rgba(255, 220, 160, 0.95)', size: 8, ring: true,
    });
    floaters.push({ x: a.x, y: a.y - 10, text: '+10', life: 1, vy: -0.65 });
    score += 10;
    shake = Math.max(shake, 6);
    boomFlash = Math.max(boomFlash, 0.16);
  }

  function fire() {
    bullets.push({ x: ship.x + ship.r + 2, y: ship.y });
    muzzle = 1;
    particles.push({
      x: ship.x + ship.r,
      y: ship.y,
      vx: rand(0.5, 2.4),
      vy: rand(-0.7, 0.7),
      life: 1,
      decay: 0.08,
      color: '#e7ffff',
      size: rand(2, 3.5),
    });
  }

  function segHits(x1, y1, x2, y2, cx, cy, r) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const len2 = dx * dx + dy * dy || 1;
    let t = ((cx - x1) * dx + (cy - y1) * dy) / len2;
    t = clamp(t, 0, 1);
    const px = x1 + dx * t;
    const py = y1 + dy * t;
    return Math.hypot(px - cx, py - cy) < r;
  }

  function die(asteroid) {
    over = true;
    explode(ship.x, ship.y, 60, 200);
    explode(asteroid.x, asteroid.y, 30, 20);
    clearTimeout(overlayTimer);
    overlayTimer = setTimeout(() => { if (over) openMenu('over'); }, 480);
  }

  function readModes(pressed) {
    const modes = new Set();
    if (!program) return { modes: modes, error: programError };
    let error = null;
    pressed.forEach(key => {
      if (error) return;
      try {
        const mode = runStudent(program, key);
        if (typeof mode === 'string' && mode !== '') modes.add(mode);
        else if (mode != null) error = raise(0, 'err_mode');
      } catch (e) {
        error = e && e.student ? e : raise(0, 'err_syntax');
      }
    });
    return { modes: modes, error: error };
  }

  function updateParticles() {
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.vx *= 0.97;
      p.vy *= 0.97;
      p.life -= p.decay;
      if (p.life <= 0) particles.splice(i, 1);
    }
    for (let i = floaters.length - 1; i >= 0; i--) {
      const f = floaters[i];
      f.y += f.vy;
      f.life -= 0.02;
      if (f.life <= 0) floaters.splice(i, 1);
    }
    if (muzzle > 0) muzzle = Math.max(0, muzzle - 0.08);
    if (boomFlash > 0) boomFlash *= 0.82;
  }

  function update(dt) {
    const playing = running && !paused && !over;
    const extra = playing && boosting ? 6 : 0;
    for (const s of stars) {
      s.x -= s.layer.speed + extra;
      if (s.x < 0) { s.x = W; s.y = Math.random() * H; }
    }

    if (!playing) {
      updateParticles();
      return;
    }

    const pressed = pressedKeys();
    const read = readModes(pressed);
    noteRuntime(read.error);

    let wantUp = false, wantDown = false, wantTurbo = false, wantShoot = false;
    let sawFly = false, sawUp = false;
    const unknown = [];
    read.modes.forEach(m => {
      if (m === 'fly') { wantUp = true; sawFly = true; }
      else if (m === 'up') { wantUp = true; sawUp = true; }
      else if (m === 'down') wantDown = true;
      else if (m === 'turbo') wantTurbo = true;
      else if (m === 'shoot') wantShoot = true;
      else unknown.push(m);
    });

    modeBad = !!read.error;
    if (read.error) modeLabel = t('hud_error');
    else {
      const labels = [];
      if (sawFly) labels.push('FLY');
      if (sawUp) labels.push('UP');
      if (wantDown) labels.push('DOWN');
      if (wantTurbo) labels.push('TURBO');
      if (wantShoot) labels.push('SHOOT');
      for (let u = 0; u < unknown.length; u++) labels.push('"' + unknown[u] + '"?');
      if (labels.length) modeLabel = 'MODE ' + labels.join(' · ');
      else if (pressed.size) modeLabel = 'MODE ?  ' + Array.from(pressed).join(' ');
      else modeLabel = 'MODE —';
    }

    let targetVy = 0;
    if (wantUp) targetVy -= shipMaxVy;
    if (wantDown) targetVy += shipMaxVy;
    ship.vy += (targetVy - ship.vy) * 0.25;
    ship.y = clamp(ship.y + ship.vy, ship.r + 4, H - ship.r - 4);
    ship.tilt = ship.vy / shipMaxVy;

    boosting = wantTurbo;
    if (boosting) {
      speedBoost = Math.min(speedBoost + 0.4, 4);
      score += 0.15;
    } else {
      speedBoost *= 0.92;
    }

    if (shootCooldown > 0) shootCooldown -= dt;
    if (wantShoot && shootCooldown <= 0) {
      shootCooldown = 160;
      fire();
    }

    spawnExhaust();
    score += 0.1;

    spawnTimer += dt;
    const effInterval = Math.max(320, spawnInterval - score * 0.7);
    if (spawnTimer > effInterval) {
      spawnTimer = 0;
      asteroids.push(makeAsteroid());
      if (score > 40 && Math.random() < 0.3) asteroids.push(makeAsteroid());
    }
    if (Math.random() < 0.004 && pickups.length < 2) pickups.push(makePickup());

    for (let i = asteroids.length - 1; i >= 0; i--) {
      const a = asteroids[i];
      a.x -= a.vx + speedBoost;
      a.y += a.vy;
      a.angle += a.spin;
      if (a.y < a.r || a.y > H - a.r) a.vy *= -1;
      if (a.x + a.r < 0) asteroids.splice(i, 1);
    }

    for (let i = bullets.length - 1; i >= 0; i--) {
      const b = bullets[i];
      const prev = b.x;
      b.x += 14;
      let hit = false;
      for (let j = asteroids.length - 1; j >= 0; j--) {
        const a = asteroids[j];
        if (segHits(prev, b.y, b.x, b.y, a.x, a.y, a.r + 3)) {
          shatter(a);
          asteroids.splice(j, 1);
          hit = true;
          break;
        }
      }
      if (hit || b.x > W + 30) bullets.splice(i, 1);
    }

    if (!over) {
      for (let i = 0; i < asteroids.length; i++) {
        const a = asteroids[i];
        if (Math.hypot(a.x - ship.x, a.y - ship.y) < a.r + ship.r * 0.8) {
          die(a);
          break;
        }
      }
    }

    for (let i = pickups.length - 1; i >= 0; i--) {
      const p = pickups[i];
      p.x -= p.vx + speedBoost;
      p.phase += 0.1;
      if (p.x + p.r < 0) { pickups.splice(i, 1); continue; }
      if (Math.hypot(p.x - ship.x, p.y - ship.y) < p.r + ship.r) {
        pickups.splice(i, 1);
        score += 15;
        explode(p.x, p.y, 18, 60);
        floaters.push({ x: p.x, y: p.y - 8, text: '+15', life: 1, vy: -0.55 });
      }
    }

    updateParticles();
    updateHUD();
  }

  function drawShip() {
    ctx.save();
    ctx.translate(ship.x, ship.y);
    ctx.rotate(ship.tilt * 0.35);

    const g = ctx.createRadialGradient(0, 0, 2, 0, 0, ship.r * 2.6);
    g.addColorStop(0, 'rgba(120,220,255,0.55)');
    g.addColorStop(1, 'rgba(120,220,255,0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(0, 0, ship.r * 2.6, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.moveTo(ship.r, 0);
    ctx.lineTo(-ship.r * 0.7, -ship.r * 0.75);
    ctx.lineTo(-ship.r * 0.3, 0);
    ctx.lineTo(-ship.r * 0.7, ship.r * 0.75);
    ctx.closePath();
    const sg = ctx.createLinearGradient(-ship.r, 0, ship.r, 0);
    sg.addColorStop(0, '#0a3b6e');
    sg.addColorStop(1, '#7ce7ff');
    ctx.fillStyle = sg;
    ctx.fill();
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = '#aef0ff';
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(ship.r * 0.15, 0, ship.r * 0.28, 0, Math.PI * 2);
    ctx.fillStyle = '#e9fbff';
    ctx.fill();

    if (muzzle > 0) {
      ctx.beginPath();
      ctx.arc(ship.r * 0.95, 0, 3 + muzzle * 4, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(230,255,255,' + (0.35 + muzzle * 0.55) + ')';
      ctx.fill();
    }

    const flame = boosting ? 22 : 12;
    ctx.beginPath();
    ctx.moveTo(-ship.r * 0.6, -4);
    ctx.lineTo(-ship.r * 0.6 - flame, rand(-3, 3));
    ctx.lineTo(-ship.r * 0.6, 4);
    ctx.closePath();
    ctx.fillStyle = boosting ? 'rgba(255,180,60,0.9)' : 'rgba(90,200,255,0.85)';
    ctx.fill();

    ctx.restore();
  }

  function drawAsteroid(a) {
    ctx.save();
    ctx.translate(a.x, a.y);
    ctx.rotate(a.angle);
    const glow = ctx.createRadialGradient(0, 0, a.r * 0.3, 0, 0, a.r * 1.6);
    glow.addColorStop(0, 'rgba(140,90,60,0.25)');
    glow.addColorStop(1, 'rgba(140,90,60,0)');
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(0, 0, a.r * 1.6, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    a.points.forEach((p, i) => {
      const x = Math.cos(p.a) * p.rr;
      const y = Math.sin(p.a) * p.rr;
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    });
    ctx.closePath();
    const grad = ctx.createRadialGradient(-a.r * 0.3, -a.r * 0.3, a.r * 0.1, 0, 0, a.r);
    grad.addColorStop(0, '#8a6b52');
    grad.addColorStop(0.6, '#5a4636');
    grad.addColorStop(1, '#2c2118');
    ctx.fillStyle = grad;
    ctx.fill();
    ctx.strokeStyle = 'rgba(255,190,140,0.35)';
    ctx.lineWidth = 1.2;
    ctx.stroke();

    ctx.fillStyle = 'rgba(0,0,0,0.25)';
    for (let i = 0; i < 3; i++) {
      ctx.beginPath();
      ctx.arc(Math.cos(i * 2.1 + a.angle) * a.r * 0.4, Math.sin(i * 2.1 + a.angle) * a.r * 0.4, a.r * 0.12, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }

  function drawPickup(p) {
    const pulse = 1 + Math.sin(p.phase) * 0.2;
    ctx.save();
    ctx.translate(p.x, p.y);
    const g = ctx.createRadialGradient(0, 0, 1, 0, 0, p.r * 2.2);
    g.addColorStop(0, 'rgba(120,255,180,0.7)');
    g.addColorStop(1, 'rgba(120,255,180,0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(0, 0, p.r * 2.2, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(0, 0, p.r * pulse, 0, Math.PI * 2);
    ctx.fillStyle = '#a9ffd0';
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.restore();
  }

  function drawBullet(b) {
    ctx.save();
    ctx.shadowColor = '#9fffff';
    ctx.shadowBlur = 10;
    const g = ctx.createLinearGradient(b.x - 22, b.y, b.x + 2, b.y);
    g.addColorStop(0, 'rgba(120,255,255,0)');
    g.addColorStop(1, '#f4ffff');
    ctx.strokeStyle = g;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(b.x - 22, b.y);
    ctx.lineTo(b.x + 2, b.y);
    ctx.stroke();
    ctx.restore();
  }

  function draw() {
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    if (shake > 0.4) {
      ctx.translate((Math.random() - 0.5) * shake, (Math.random() - 0.5) * shake);
      shake *= 0.86;
    } else {
      shake = 0;
    }

    const bg = ctx.createLinearGradient(0, 0, 0, H);
    bg.addColorStop(0, '#03020f');
    bg.addColorStop(0.5, '#050a1f');
    bg.addColorStop(1, '#01030c');
    ctx.fillStyle = bg;
    ctx.fillRect(-8, -8, W + 16, H + 16);

    const t = performance.now() * 0.0002;
    for (let i = 0; i < 3; i++) {
      const nx = (Math.sin(t + i * 2) * 0.5 + 0.5) * W;
      const ny = (Math.cos(t * 1.3 + i) * 0.5 + 0.5) * H;
      const ng = ctx.createRadialGradient(nx, ny, 0, nx, ny, 260);
      ng.addColorStop(0, i === 0 ? 'rgba(80,40,160,0.18)' : i === 1 ? 'rgba(20,80,180,0.16)' : 'rgba(160,30,120,0.12)');
      ng.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = ng;
      ctx.fillRect(-8, -8, W + 16, H + 16);
    }

    for (const s of stars) {
      ctx.fillStyle = s.layer.color;
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.layer.size, 0, Math.PI * 2);
      ctx.fill();
    }
    for (const p of pickups) drawPickup(p);
    for (const a of asteroids) drawAsteroid(a);
    for (const b of bullets) drawBullet(b);

    for (const p of particles) {
      ctx.globalAlpha = Math.max(0, p.life);
      if (p.ring) {
        ctx.strokeStyle = p.color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(p.x, p.y, (1 - p.life) * 42 + 6, 0, Math.PI * 2);
        ctx.stroke();
      } else {
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    ctx.globalAlpha = 1;

    ctx.font = 'bold 14px Consolas, monospace';
    ctx.textAlign = 'center';
    for (const f of floaters) {
      ctx.globalAlpha = Math.max(0, f.life);
      ctx.fillStyle = '#e9fff0';
      ctx.fillText(f.text, f.x, f.y);
    }
    ctx.globalAlpha = 1;

    if (!over) drawShip();

    if (boomFlash > 0.01) {
      ctx.fillStyle = 'rgba(255, 236, 210, ' + boomFlash + ')';
      ctx.fillRect(-8, -8, W + 16, H + 16);
    }
  }

  let last = performance.now();
  function loop(now) {
    const dt = Math.max(0, Math.min(now - last, 80));
    last = now;
    update(dt);
    draw();
    requestAnimationFrame(loop);
  }

  window.addEventListener('keydown', (e) => {
    const target = e.target;
    if (target && (target.tagName === 'TEXTAREA' || target.tagName === 'INPUT')) return;
    if (!overlay.classList.contains('hidden')) return;
    const name = keyNameFromEvent(e);
    if (!name || IGNORE_KEYS.has(name)) return;
    keys[name] = true;
    if (name === 'space' || name === 'up' || name === 'down' || name === 'left' || name === 'right') e.preventDefault();
  });
  window.addEventListener('keyup', (e) => {
    const name = keyNameFromEvent(e);
    if (name) keys[name] = false;
  });
  window.addEventListener('blur', () => { for (const k in keys) keys[k] = false; });

  function setMenu(kind) {
    menuKind = kind;
    if (kind === 'over') {
      titleEl.textContent = 'GAME OVER';
      subtitleEl.textContent = t('subtitle_over');
      scoreLine.classList.remove('hidden');
      scoreLine.innerHTML = t('score_line').replace('{s}', Math.floor(score)).replace('{b}', Math.floor(best));
      startBtn.textContent = t('retry');
    } else if (kind === 'pause') {
      titleEl.textContent = t('pause');
      subtitleEl.textContent = t('subtitle_pause');
      scoreLine.classList.add('hidden');
      startBtn.textContent = t('resume');
    } else {
      titleEl.textContent = 'SPACE RUNNER';
      subtitleEl.textContent = t('subtitle');
      scoreLine.classList.add('hidden');
      startBtn.textContent = t('start');
    }
  }

  function applyLang() {
    document.documentElement.lang = lang;
    const nodes = document.querySelectorAll('[data-i18n]');
    for (let i = 0; i < nodes.length; i++) nodes[i].textContent = t(nodes[i].getAttribute('data-i18n'));
    codeEl.setAttribute('aria-label', t('aria_code'));
    document.getElementById('langRu').classList.toggle('on', lang === 'ru');
    document.getElementById('langEn').classList.toggle('on', lang === 'en');
    setMenu(menuKind);
    shownStatus = '';
    lastRuntime = '';
    if (programError) setStatus(false, formatError(programError) + t('saved_short'));
    else setStatus(true, t('saved_ok'));
    if (modeBad) modeLabel = t('hud_error');
    updateHUD();
  }

  function chooseLang(next) {
    lang = next === 'en' ? 'en' : 'ru';
    try { localStorage.setItem(LANG_KEY, lang); } catch (err) {}
    applyLang();
  }

  document.getElementById('langRu').addEventListener('click', () => chooseLang('ru'));
  document.getElementById('langEn').addEventListener('click', () => chooseLang('en'));

  function openMenu(kind) {
    setMenu(kind);
    overlay.classList.remove('hidden');
    codeBtn.classList.add('hidden');
    for (const k in keys) keys[k] = false;
  }

  codeBtn.addEventListener('click', () => {
    if (!running || over) return;
    paused = true;
    openMenu('pause');
  });

  startBtn.addEventListener('click', () => {
    clearTimeout(overlayTimer);
    const retry = over || !running;
    overlay.classList.add('hidden');
    codeBtn.classList.remove('hidden');
    paused = false;
    if (retry) resetGame();
    running = true;
    startBtn.blur();
    codeEl.blur();
    last = performance.now();
  });

  initStars();
  applyLang();
  requestAnimationFrame(loop);
})();
</script>
</body>
</html>
'''

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("File templates/index.html created successfully!")
