#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PsyCLIENT MVP 本地服务
用法: python3 server.py [端口]   默认 8000
依赖: 仅 Python 3 标准库。.env 放在本目录或上一级目录。
"""
import json, os, sys, time, urllib.request
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(HERE, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# ---------- 配置 ----------
def load_env():
    """环境变量优先（线上部署），其次 .env 文件（本地开发）。"""
    env = {}
    for d in (HERE, os.path.dirname(HERE)):
        p = os.path.join(d, '.env')
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        k, v = line.split('=', 1)
                        env[k.strip()] = v.strip()
            break
    for k in ('API_KEY', 'BASE_URL', 'MODEL', 'MODEL_GEN', 'ACCESS_CODE', 'LOG_DIR'):
        if os.environ.get(k):
            env[k] = os.environ[k]
    env.setdefault('BASE_URL', 'https://open.bigmodel.cn/api/paas/v4')
    env.setdefault('MODEL', 'glm-4.6')
    env.setdefault('MODEL_GEN', env['MODEL'])
    if not env.get('API_KEY'):
        raise SystemExit('缺少 API_KEY：设为环境变量，或放进 app/ 或其上一级目录的 .env')
    return env

ENV = load_env()
ACCESS_CODE = (ENV.get('ACCESS_CODE') or '').strip()   # 非空则全站需要口令

if ENV.get('LOG_DIR'):
    LOG_DIR = ENV['LOG_DIR']
    os.makedirs(LOG_DIR, exist_ok=True)

def _load_items(fn):
    p = os.path.join(HERE, fn)
    if not os.path.exists(p):
        return {}
    with open(p, encoding='utf-8') as f:
        return {it['id']: it for it in json.load(f)}

ITEMS_BY_LANG = {'zh': _load_items('items.json'), 'en': _load_items('items_en.json')}
ITEMS = ITEMS_BY_LANG['zh']   # 兼容旧引用

from prompt import (SKILL_DEFS, CRITERIA, system_prompt, user_prompt, postprocess,  # noqa: E402  提示词单一来源
                    example_system_prompt, example_user_prompt, example_allowed)
from prompt_en import (SKILL_DEFS_EN, CRITERIA_EN, system_prompt_en, user_prompt_en,  # noqa: E402
                       example_system_prompt_en, example_user_prompt_en)
import convo      # noqa: E402  对话练习模式（中文）
import convo_en   # noqa: E402  对话练习模式（英文）

# ---------- 语言分流 ----------
def L(lang):
    """按语言返回该语言的全部资源。未知语言退回中文。"""
    if lang == 'en':
        return dict(lang='en', items=ITEMS_BY_LANG['en'], defs=SKILL_DEFS_EN, crit=CRITERIA_EN,
                    sys=system_prompt_en, usr=user_prompt_en,
                    ex_sys=example_system_prompt_en, ex_usr=example_user_prompt_en,
                    conv_cases=convo_en.CONV_CASES_EN, sca_cases=convo_en.SCA_CASES_EN,
                    client_sys=convo_en.client_system_prompt_en, client_usr=convo_en.client_user_prompt_en,
                    sum_sys=convo_en.summary_system_prompt_en, sum_usr=convo_en.summary_user_prompt_en,
                    pol_sys=convo_en.polish_system_prompt_en, pol_usr=convo_en.polish_user_prompt_en)
    return dict(lang='zh', items=ITEMS_BY_LANG['zh'], defs=SKILL_DEFS, crit=CRITERIA,
                sys=system_prompt, usr=user_prompt,
                ex_sys=example_system_prompt, ex_usr=example_user_prompt,
                conv_cases=convo.CONV_CASES, sca_cases=convo.SCA_CASES,
                client_sys=convo.client_system_prompt, client_usr=convo.client_user_prompt,
                sum_sys=convo.summary_system_prompt, sum_usr=convo.summary_user_prompt,
                pol_sys=convo.polish_system_prompt, pol_usr=convo.polish_user_prompt)

def norm_lang(v):
    return 'en' if (v or '').lower().startswith('en') else 'zh'
import uuid, threading  # noqa: E402
from concurrent.futures import ThreadPoolExecutor  # noqa: E402

SESSIONS = {}            # session_id -> dict(case, skill, history, states, done)
SESS_LOCK = threading.Lock()

def call_llm(sys_p, usr_p, retry=1, model=None):
    m = model or ENV['MODEL']
    payload = {'model': m, 'temperature': 0,
        'messages': [{'role': 'system', 'content': sys_p}, {'role': 'user', 'content': usr_p}]}
    if m.startswith(('glm-4.5', 'glm-4.6', 'glm-z')):
        payload['thinking'] = {'type': 'disabled'}  # 关思考链换速度
    body = json.dumps(payload).encode()
    req = urllib.request.Request(ENV['BASE_URL'].rstrip('/') + '/chat/completions', data=body,
        headers={'Authorization': 'Bearer ' + ENV['API_KEY'], 'Content-Type': 'application/json'})
    last = None
    for a in range(retry + 1):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                d = json.loads(r.read().decode())
            txt = d['choices'][0]['message']['content'].strip()
            if txt.startswith('```'):
                txt = txt.split('```')[1]
                if txt.startswith('json'):
                    txt = txt[4:]
            i, j = txt.find('{'), txt.rfind('}')
            return json.loads(txt[i:j + 1]), None
        except Exception as e:
            last = str(e)[:200]
            if a < retry:
                time.sleep(1.5)
    return None, last

def log_line(rec):
    p = os.path.join(LOG_DIR, 'log_%s.jsonl' % time.strftime('%Y%m%d'))
    with open(p, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')

ANN_PATH = os.path.join(LOG_DIR, 'annotations.jsonl')

# ---------- 跨会话学习目标（Larsson et al. 2025 的 learning goal 环节） ----------
GOALS_PATH = os.path.join(LOG_DIR, 'goals.jsonl')

def latest_goal(user):
    """该学员最近一次复盘存档的学习目标；无则 None。"""
    if not user or not os.path.exists(GOALS_PATH):
        return None
    goal = None
    with open(GOALS_PATH, encoding='utf-8') as f:
        for line in f:
            try:
                g = json.loads(line)
                if g.get('user') == user:
                    goal = g
            except Exception:
                pass
    return goal

def save_goal(user, direction, session, skill):
    if not (user and direction):
        return
    rec = dict(ts=time.strftime('%Y-%m-%d %H:%M:%S'), user=user,
               goal=direction, session=session, skill=skill)
    with open(GOALS_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')

def review_data():
    """全部作答日志 + 已有标注（按 key = 日期文件名:行号 关联）。"""
    ALL_ITEMS = dict(ITEMS_BY_LANG['zh'])
    ALL_ITEMS.update(ITEMS_BY_LANG['en'])   # 英文题 id 与中文相同，取该条日志记录的语言
    entries = []
    for fn in sorted(os.listdir(LOG_DIR)):
        if not (fn.startswith('log_') and fn.endswith('.jsonl')):
            continue
        with open(os.path.join(LOG_DIR, fn), encoding='utf-8') as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if not r.get('feedback'):
                    continue  # 调用失败的不进复盘
                it = ITEMS_BY_LANG.get(r.get('lang') or 'zh', {}).get(r.get('item')) or ALL_ITEMS.get(r.get('item'), {})
                entries.append(dict(
                    key=f'{fn}:{i}', ts=r.get('ts'), user=r.get('user'), item=r.get('item'), skill=r.get('skill'),
                    lang=r.get('lang') or 'zh',
                    attempt=r.get('attempt'), self_rating=r.get('self_rating'),
                    response=r.get('response'), secs=r.get('secs'), feedback=r['feedback'],
                    utterance=it.get('utterance', ''), background=it.get('background', ''),
                    surface=it.get('surface', ''), emotions=it.get('emotions', ''),
                    meaning=it.get('meaning', '')))
    ann = {}
    if os.path.exists(ANN_PATH):
        with open(ANN_PATH, encoding='utf-8') as f:
            for line in f:
                try:
                    a = json.loads(line)
                    ann[a['key']] = a  # 后写覆盖先写：允许改判
                except Exception:
                    pass
    return {'entries': entries, 'annotations': ann,
            'skills': {k: v[0] for k, v in SKILL_DEFS.items()}}


# ---------- 对话练习 ----------
def conv_log(rec):
    p = os.path.join(LOG_DIR, 'conv_%s.jsonl' % time.strftime('%Y%m%d'))
    with open(p, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')

def gen_client_turn(case, history, lang='zh'):
    """生成来访者话轮：先定状态再说话。返回完整状态 dict 或 (None, err)。"""
    r = L(lang)
    out, err = call_llm(r['client_sys'](case), r['client_usr'](case, history),
                        model=ENV.get('MODEL_GEN'))
    if out is None:
        return None, err
    if not out.get('utterance'):
        return None, 'no utterance'
    return out, None

def conv_start(skill, user=None, lang='zh'):
    r = L(lang)
    case = r['conv_cases'][skill]
    sid = uuid.uuid4().hex[:12]
    op = case['opening']
    state = dict(surface=op['surface'], emotions=op['emotions'], meaning=op['meaning'],
                 reaction='open', understood=5, utterance=op['utterance'])
    with SESS_LOCK:
        SESSIONS[sid] = dict(skill=skill, case_id=case['id'], user=user, lang=lang,
                             history=[dict(role='client', text=op['utterance'])],
                             states=[state], done=False, ts=time.strftime('%Y-%m-%d %H:%M:%S'))
    return dict(session_id=sid, client_text=op['utterance'],
                background=case['background'], turn=1,
                min_turns=convo.MIN_TURNS, max_turns=convo.MAX_TURNS)

def conv_reply(sid, resp_text):
    with SESS_LOCK:
        sess = SESSIONS.get(sid)
    if sess is None or sess['done'] or sess.get('mode') == 'sca':
        return None, '会话不存在或已结束'
    entry = dict(role='counselor', text=resp_text)
    pu = None
    for ev in reversed(sess.get('polish_events') or []):
        sug = ev.get('suggestion') or ''
        if not sug:
            continue
        if resp_text == sug:
            pu = 'exact'; break
        if sug in resp_text or resp_text in sug:
            pu = 'edited'; break
    if pu:
        entry['polish_used'] = pu
    sess['history'].append(entry)
    n_student = sum(1 for h in sess['history'] if h['role'] == 'counselor')
    if n_student >= convo.MAX_TURNS:
        return dict(client_text=None, ended=True, turn=n_student), None
    lang = sess.get('lang', 'zh')
    case = L(lang)['conv_cases'][sess['skill']]
    state, err = gen_client_turn(case, sess['history'], lang)
    if state is None:
        sess['history'].pop()
        return None, err
    sess['history'].append(dict(role='client', text=state['utterance']))
    sess['states'].append(state)
    return dict(client_text=state['utterance'], ended=False, turn=n_student,
                can_end=n_student >= convo.MIN_TURNS), None

def conv_end(sid):
    with SESS_LOCK:
        sess = SESSIONS.get(sid)
    if sess is None:
        return None, '会话不存在'
    if sess.get('mode') == 'sca':
        return None, '评估会谈无复盘'
    sess['done'] = True
    skill = sess['skill']
    lang = sess.get('lang', 'zh')
    res = L(lang)
    case = res['conv_cases'][skill]
    # 组装 (来访者话轮+状态, 学员回应) 对
    pairs = []
    hist = sess['history']
    for i, h in enumerate(hist):
        if h['role'] == 'counselor':
            ci = i - 1  # 上一条必为 client
            st = sess['states'][sum(1 for x in hist[:i] if x['role'] == 'client') - 1]
            ctx = '\n'.join(('来访者：' if x['role'] == 'client' else '咨询师：') + x['text']
                             for x in hist[max(0, ci - 2):ci])
            pairs.append(dict(idx=len(pairs), client=hist[ci]['text'], response=h['text'],
                              polish=h.get('polish_used'), state=st, context=ctx or '（会谈开始）'))
    # 并行评分（复用 v3.2 评价器）
    def _eval(p):
        item = dict(skill=skill, background=case['background'], context=p['context'],
                    utterance=p['client'], surface=p['state']['surface'],
                    emotions=p['state']['emotions'], meaning=p['state']['meaning'])
        out, err = call_llm(res['sys'](skill), res['usr'](item, p['response']))
        out = postprocess(out)
        return dict(idx=p['idx'], feedback=out, error=err,
                    verdict=(out or {}).get('verdict', 'ERR'))
    with ThreadPoolExecutor(max_workers=6) as ex:
        evals = sorted(ex.map(_eval, pairs), key=lambda e: e['idx'])
    key_idx = convo.pick_key_moments(
        [dict(idx=e['idx'], verdict=e['verdict']) for e in evals if e['feedback']], k=3)
    # 会谈小结（非处方）
    name = res['defs'][skill][0]
    sm, _ = call_llm(res['sum_sys'](name), res['sum_usr'](
        [dict(client=p['client'], response=p['response'], verdict=evals[p['idx']]['verdict'])
         for p in pairs]), model=ENV.get('MODEL_GEN'))
    moments = []
    for i in key_idx:
        p, e = pairs[i], evals[i]
        moments.append(dict(idx=i, client=p['client'], response=p['response'],
                            surface=p['state']['surface'], emotions=p['state']['emotions'],
                            meaning=p['state']['meaning'], feedback=e['feedback']))
    verdicts = [e['verdict'] for e in evals]
    understood = [st.get('understood') for st in sess['states']]
    transcript = [dict(client=p['client'], response=p['response'],
                       verdict=evals[p['idx']]['verdict'], polish=p.get('polish'))
                  for p in pairs]
    # 学习目标：先取旧目标（供前端问进展），再把本次改进方向存为新目标
    user = sess.get('user')
    prev = latest_goal(user)
    if sm and sm.get('direction'):
        save_goal(user, sm['direction'], sid, skill)
    result = dict(turns=len(pairs), verdicts=verdicts, understood_curve=understood,
                  moments=moments, summary=sm or {}, transcript=transcript,
                  prev_goal=(prev['goal'] if prev else None))
    conv_log(dict(type='session', ts=sess['ts'], user=sess.get('user'), lang=lang, session=sid, skill=skill, case=case['id'],
                  history=hist, states=sess['states'], evals=evals,
                  summary=sm, key_moments=key_idx,
                  polish_events=sess.get('polish_events', [])))
    return result, None

# ---------- SCA 标准化评估会谈 ----------
def sca_log(rec):
    p = os.path.join(LOG_DIR, 'sca_%s.jsonl' % time.strftime('%Y%m%d'))
    with open(p, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')

def sca_start(form, user=None, lang='zh'):
    case = L(lang)['sca_cases'][form]
    sid = uuid.uuid4().hex[:12]
    op = case['opening']
    state = dict(surface=op['surface'], emotions=op['emotions'], meaning=op['meaning'],
                 reaction='open', understood=5, utterance=op['utterance'])
    with SESS_LOCK:
        SESSIONS[sid] = dict(mode='sca', form=form, case_id=case['id'], user=user, lang=lang,
                             history=[dict(role='client', text=op['utterance'])],
                             states=[state], done=False, ts=time.strftime('%Y-%m-%d %H:%M:%S'))
    sca_log(dict(type='start', ts=SESSIONS[sid]['ts'], session=sid, form=form, user=user, lang=lang))
    return dict(session_id=sid, client_text=op['utterance'],
                background=case['background'], total=convo.SCA_TURNS)

def sca_reply(sid, resp_text):
    with SESS_LOCK:
        sess = SESSIONS.get(sid)
    if sess is None or sess.get('mode') != 'sca' or sess['done']:
        return None, '评估会话不存在或已结束'
    sess['history'].append(dict(role='counselor', text=resp_text))
    n_student = sum(1 for h in sess['history'] if h['role'] == 'counselor')
    # 逐轮落盘：评估数据不可丢
    sca_log(dict(type='turn', session=sid, n=n_student, response=resp_text,
                 ts=time.strftime('%H:%M:%S')))
    if n_student >= convo.SCA_TURNS:
        sess['done'] = True
        sca_log(dict(type='session', ts=sess['ts'], session=sid, form=sess['form'],
                     user=sess.get('user'), lang=sess.get('lang', 'zh'),
                     history=sess['history'], states=sess['states']))
        return dict(client_text=None, ended=True, turn=n_student), None
    lang = sess.get('lang', 'zh')
    case = L(lang)['sca_cases'][sess['form']]
    state, err = gen_client_turn(case, sess['history'], lang)
    if state is None:
        sess['history'].pop()
        return None, err
    sess['history'].append(dict(role='client', text=state['utterance']))
    sess['states'].append(state)
    return dict(client_text=state['utterance'], ended=False, turn=n_student), None

# ---------- HTTP ----------
class H(BaseHTTPRequestHandler):
    def _send(self, code, data, ctype='application/json'):
        raw = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', ctype + '; charset=utf-8')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *a):  # 安静一点
        pass

    def _authed(self):
        """口令校验：ACCESS_CODE 为空时始终放行。"""
        if not ACCESS_CODE:
            return True
        c = self.headers.get('X-Access-Code') or ''
        if c.strip() == ACCESS_CODE:
            return True
        from urllib.parse import urlparse, parse_qs
        q = parse_qs(urlparse(self.path).query)
        return (q.get('code') or [''])[0].strip() == ACCESS_CODE

    def do_GET(self):
        base = self.path.split('?')[0]
        if base in ('/', '/index.html'):
            with open(os.path.join(HERE, 'index.html'), 'rb') as f:
                self._send(200, f.read(), 'text/html')
        elif base == '/review':
            with open(os.path.join(HERE, 'review.html'), 'rb') as f:
                self._send(200, f.read(), 'text/html')
        elif base == '/api/health':
            self._send(200, {'ok': True, 'need_code': bool(ACCESS_CODE)})
        elif base == '/api/items':
            if not self._authed():
                return self._send(401, {'error': 'access code required'})
            from urllib.parse import urlparse, parse_qs
            q = parse_qs(urlparse(self.path).query)
            r = L(norm_lang((q.get('lang') or ['zh'])[0]))
            # 学员可见字段——绝不下发标注
            vis = [{k: it.get(k) for k in ('id', 'skill', 'background', 'context', 'utterance', 'level', 'affect')}
                   for it in r['items'].values()]
            self._send(200, {'items': vis, 'skills': {k: v[0] for k, v in r['defs'].items()},
                             'criteria': r['crit']})
        elif base == '/api/review_data':
            if not self._authed():
                return self._send(401, {'error': 'access code required'})
            self._send(200, review_data())
        elif base == '/api/goal':
            from urllib.parse import urlparse, parse_qs
            q = parse_qs(urlparse(self.path).query)
            user = (q.get('user') or [''])[0].strip()
            g = latest_goal(user)
            self._send(200, {'goal': (g['goal'] if g else None),
                             'ts': (g['ts'] if g else None),
                             'skill': (g['skill'] if g else None)})
        else:
            self._send(404, {'error': 'not found'})

    def do_POST(self):
        if not self._authed():
            return self._send(401, {'error': 'access code required'})
        if self.path == '/api/sca_start':
            try:
                n = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(n).decode())
                form = body.get('form')
                lang = norm_lang(body.get('lang'))
                if form not in L(lang)['sca_cases']:
                    return self._send(400, {'error': '卷别无效（A/B）/ invalid form'})
                return self._send(200, sca_start(form, (body.get('user') or '').strip() or None, lang))
            except Exception as e:
                return self._send(500, {'error': str(e)[:200]})
        if self.path == '/api/sca_reply':
            try:
                n = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(n).decode())
                resp = (body.get('response') or '').strip()
                if not resp:
                    return self._send(400, {'error': '回应为空'})
                out, err = sca_reply(body['session_id'], resp)
                if out is None:
                    return self._send(502, {'error': '来访者生成失败，请重试', 'detail': err})
                return self._send(200, out)
            except Exception as e:
                return self._send(500, {'error': str(e)[:200]})
        if self.path == '/api/conv_start':
            try:
                n = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(n).decode())
                return self._send(200, conv_start(body['skill'], (body.get('user') or '').strip() or None,
                                                  norm_lang(body.get('lang'))))
            except Exception as e:
                return self._send(500, {'error': str(e)[:200]})
        if self.path == '/api/conv_reply':
            try:
                n = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(n).decode())
                resp = (body.get('response') or '').strip()
                if not resp:
                    return self._send(400, {'error': '回应为空'})
                out, err = conv_reply(body['session_id'], resp)
                if out is None:
                    return self._send(502, {'error': '来访者生成失败，请重试', 'detail': err})
                return self._send(200, out)
            except Exception as e:
                return self._send(500, {'error': str(e)[:200]})
        if self.path == '/api/conv_polish':
            try:
                n = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(n).decode())
                with SESS_LOCK:
                    sess = SESSIONS.get(body['session_id'])
                if sess is None or sess['done']:
                    return self._send(400, {'error': '会话不存在或已结束'})
                if sess.get('mode') == 'sca':
                    return self._send(400, {'error': '评估会谈不提供润色'})
                draft = (body.get('draft') or '').strip()
                if not draft:
                    return self._send(400, {'error': '草稿为空'})
                pr = L(sess.get('lang', 'zh'))
                name = pr['defs'][sess['skill']][0]
                out, err = call_llm(pr['pol_sys'](name),
                                    pr['pol_usr'](sess['history'], draft), retry=2)
                if out is None or not out.get('suggestion'):
                    conv_log(dict(type='polish_error', session=body['session_id'],
                                  skill=sess['skill'], draft=draft, detail=err,
                                  raw=(out if isinstance(out, dict) else None),
                                  ts=time.strftime('%H:%M:%S')))
                    return self._send(502, {'error': '润色失败，请重试', 'detail': err})
                ev = dict(ts=time.strftime('%H:%M:%S'), draft=draft,
                          suggestion=out.get('suggestion', ''), unchanged=bool(out.get('unchanged')))
                sess.setdefault('polish_events', []).append(ev)
                conv_log(dict(type='polish', session=body['session_id'], user=sess.get('user'), skill=sess['skill'], **ev))
                return self._send(200, out)
            except Exception as e:
                return self._send(500, {'error': str(e)[:200]})
        if self.path == '/api/conv_end':
            try:
                n = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(n).decode())
                out, err = conv_end(body['session_id'])
                if out is None:
                    return self._send(400, {'error': err})
                return self._send(200, out)
            except Exception as e:
                return self._send(500, {'error': str(e)[:200]})
        if self.path == '/api/example':
            # 示范式反馈：学员主动索取，只在作答之后；使用记录进日志供依赖分析
            try:
                n = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(n).decode())
                lang = norm_lang(body.get('lang'))
                r = L(lang)
                item = r['items'][body['item_id']]
                verdict = body.get('verdict')
                if not example_allowed(item['skill'], verdict):
                    return self._send(403, {'error': 'example not available for this module'})
                t0 = time.time()
                out, err = call_llm(r['ex_sys'](item['skill']), r['ex_usr'](item), retry=1)
                secs = round(time.time() - t0, 1)
                log_line(dict(ts=time.strftime('%Y-%m-%d %H:%M:%S'), type='example_shown',
                              user=(body.get('user') or '').strip() or None, lang=lang,
                              item=item['id'], skill=item['skill'],
                              attempt=body.get('attempt'), verdict_at_request=verdict,
                              example=(out or {}).get('example'), secs=secs, error=err))
                if out is None or not out.get('example'):
                    return self._send(502, {'error': '示范生成失败，请重试 / example failed, please retry',
                                            'detail': err})
                return self._send(200, out)
            except Exception as e:
                return self._send(500, {'error': str(e)[:200]})
        if self.path == '/api/annotate':
            try:
                n = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(n).decode())
                rec = dict(ts=time.strftime('%Y-%m-%d %H:%M:%S'), key=body['key'],
                           user=(body.get('user') or '').strip() or None,
                           agree=body['agree'], expert_verdict=body.get('expert_verdict'),
                           note=(body.get('note') or '').strip())
                with open(ANN_PATH, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                return self._send(200, {'ok': True})
            except Exception as e:
                return self._send(500, {'error': str(e)[:200]})
        if self.path != '/api/feedback':
            return self._send(404, {'error': 'not found'})
        try:
            n = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(n).decode())
            lang = norm_lang(body.get('lang'))
            r = L(lang)
            item = r['items'][body['item_id']]
            resp = (body.get('response') or '').strip()
            if not resp:
                return self._send(400, {'error': '回应为空 / empty response'})
            t0 = time.time()
            out, err = call_llm(r['sys'](item['skill']), r['usr'](item, resp))
            out = postprocess(out)
            secs = round(time.time() - t0, 1)
            rec = dict(ts=time.strftime('%Y-%m-%d %H:%M:%S'), user=(body.get('user') or '').strip() or None,
                       lang=lang, item=item['id'], skill=item['skill'],
                       attempt=body.get('attempt', 1), self_rating=body.get('self_rating'),
                       response=resp, secs=secs, feedback=out, error=err)
            log_line(rec)
            if out is None:
                return self._send(502, {'error': '反馈生成失败，请重试 / feedback failed, please retry', 'detail': err})
            self._send(200, {'feedback': out, 'secs': secs})
        except Exception as e:
            self._send(500, {'error': str(e)[:200]})

if __name__ == '__main__':
    # 端口：命令行参数 > PORT 环境变量（Render/Railway 等平台注入）> 8000
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('PORT', 8000))
    # 监听地址：线上需 0.0.0.0，本地默认只听回环
    host = os.environ.get('HOST') or ('0.0.0.0' if os.environ.get('PORT') else '127.0.0.1')
    where = f'http://localhost:{port}' if host == '127.0.0.1' else f'{host}:{port}'
    print(f'REFLECT MVP · {where}  (model: {ENV["MODEL"]}, '
          f'access code: {"on" if ACCESS_CODE else "off"}, Ctrl+C to quit)')
    ThreadingHTTPServer((host, port), H).serve_forever()
