# -*- coding: utf-8 -*-
"""PsyCLIENT MVP 反馈提示词自检
把 3 道样题 x 3 档回应（共 9 条）送入评价式反馈提示词，
比较模型判定与《结构化练习题样例》中标注的档次是否一致。
用法: python3 selftest.py [模型名]
"""
import json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
def load_env():
    env = {}
    with open(os.path.join(HERE, '.env'), encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env

ENV = load_env()
MODEL = sys.argv[1] if len(sys.argv) > 1 else ENV.get('MODEL', 'glm-4.5')

import sys as _sys
_sys.path.insert(0, os.path.join(HERE, 'app'))
from prompt import SKILL_DEFS, system_prompt, user_prompt, postprocess  # 单一来源

# ---- 三道样题（取自《结构化练习题样例_v4》，虚构占位材料）----
ITEMS = [
 dict(id='W1_content', skill='content',
   background='男，大三，正在准备考研。第二次会谈，谈最近的学习状态。',
   context='咨询师：这一周过得怎么样？\n来访者：还是老样子吧，就是有点没劲。',
   utterance='我这学期基本上每天都在图书馆待到闭馆，可回宿舍还是觉得今天什么都没干成。舍友他们都在忙实习，就我一个人在那儿刷题。',
   surface='每天在图书馆待到闭馆；回宿舍仍觉得一天没有成果；舍友都在实习，只有自己在准备考研。',
   emotions='挫败、孤单。',
   meaning='怀疑自己的投入是否换得来结果；在同伴中走了一条不一样的路，无人同行。',
   responses=[
     ('miss','你要不要试试换一种学习方法？效率可能会高一些。'),
     ('hit','你每天都在图书馆学到很晚，但还是觉得没什么收获，而且只有你一个人在准备考研。'),
     ('hit','天天待到闭馆，回去却觉得白过了一天；周围人都在往另一个方向走，只剩你一个人在刷题——这么熬着，会不会有点怀疑这么下去到底行不行。'),
     # ---- 以下为真实学员回应（2026-07-27 日志，Claude 初标、待临床复核）----
     ('miss','hahhahhah'),
     ('miss','嗯嗯然后呢？'),
     ('partial','感觉你一定非常孤独吧，听到你说你提不起劲来'),
     ('hit','感觉你一定非常孤独吧，听到你说你提不起劲来，每天在图书馆学习到闭馆但无成就感一定很不好受。'),
     ('hit','我听到了你和同伴差异带来的孤独感，听到你说你提不起劲来，每天在图书馆学习到闭馆但无成就感一定很不好受。'),
     ('hit','我听到了你和同学对比的孤独感，这种每天在图书馆学习到闭馆但无成就感一定很不好受。'),
     ('hit','我听到了你和舍友对比的孤独感，这种每天在图书馆学习到闭馆但无成就感一定很不好受。'),
   ]),
 dict(id='W2_feeling', skill='feeling',
   background='女，研一，因与导师的关系困扰求助。第三次会谈。',
   context='咨询师：你刚才提到上周组会之后就不太想去实验室了。\n来访者：嗯……是从那天开始的。',
   utterance='上周组会我汇报完，老师当着所有人的面说我这个方向做了半年还没入门。我当时脸都白了，特别难堪。后来这几天在楼道里看到他，我都绕道走。',
   surface='组会上被导师当众评价"半年还没入门"；当时脸色发白；之后在楼道回避导师。',
   emotions='难堪；羞耻与害怕再次被否定。',
   meaning='那句话动摇了她"自己是否适合做研究、是否属于这个实验室"的位置感；她需要有人先承认这件事确实难受。',
   responses=[
     ('miss','老师那样说可能只是想激励你，他应该不是针对你。'),
     ('hit','当着全组人被那样说，你觉得特别难堪，难堪到这几天都绕着他走。'),
     ('hit','那句"还没入门"，好像不只让你难堪，还让你有点怀疑自己到底适不适合待在这儿。'),
     # ---- 真实学员回应 ----
     ('miss','别太往心里去，导师对谁都这样。'),
     ('partial','听起来你挺不舒服的。'),
   ]),
 dict(id='W3_meaning', skill='meaning',
   background='女，大四，面临就业选择与父母期望的冲突。第二次会谈。',
   context='咨询师：offer 的事，你跟家里说了吗？\n来访者：……还没有。',
   utterance='我爸妈一直希望我回老家考编，说女孩子稳定最重要。我拿到了深圳一家公司的 offer，可一直没敢开口。那边后天就要我答复了。',
   surface='父母希望她回老家考编；她已拿到深圳的 offer；一直没告诉父母；后天必须答复。',
   emotions='焦虑、内疚。',
   meaning='这是她第一次公开地按自己的意愿做决定；"没敢开口"意味着她预判说出来会引发冲突；她在意的是能否被父母当作一个可以自己拿主意的成年人。',
   responses=[
     ('miss','要不你先跟他们商量一下，听听他们怎么说？'),
     ('partial','你拿到了深圳的 offer，但还没告诉爸妈，后天就要答复了，心里挺着急的。'),
     ('hit','后天就要答复了，而这件事你还一个人放在心里。它好像不只是一份工作的选择——更像是你要不要第一次照自己的意思来；而你迟迟没开口，好像是因为你已经猜到他们会怎么反应了。'),
   ]),
]

def call(sys_p, usr_p, retry=1):
    payload = {"model": MODEL, "temperature": 0,
        "messages":[{"role":"system","content":sys_p},{"role":"user","content":usr_p}]}
    if MODEL.startswith(('glm-4.5', 'glm-4.6', 'glm-z')):
        payload["thinking"] = {"type": "disabled"}   # 判定任务不需要思考链，关掉换速度
    body = json.dumps(payload).encode()
    req = urllib.request.Request(ENV['BASE_URL'].rstrip('/')+'/chat/completions', data=body,
        headers={'Authorization':'Bearer '+ENV['API_KEY'],'Content-Type':'application/json'})
    for a in range(retry+1):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read().decode())
            txt = d['choices'][0]['message']['content'].strip()
            if txt.startswith('```'):
                txt = txt.split('```')[1]
                if txt.startswith('json'): txt = txt[4:]
            i, j = txt.find('{'), txt.rfind('}')
            return json.loads(txt[i:j+1]), None
        except Exception as e:
            if a == retry: return None, str(e)[:120]
            time.sleep(2)

def flatten():
    """展平成 9 条 (item, expected, response)"""
    out = []
    for item in ITEMS:
        for expected, resp in item['responses']:
            out.append((item, expected, resp))
    return out


def run_range(start, end, model=None, outfile='selftest_result.json'):
    """跑第 start..end-1 条，结果增量写入 outfile。供分段调用。"""
    global MODEL
    if model: MODEL = model
    cases = flatten()[start:end]
    path = os.path.join(HERE, outfile)
    existing = []
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            try: existing = json.load(f)
            except Exception: existing = []
    for item, expected, resp in cases:
        t0 = time.time()
        out, err = call(system_prompt(item['skill']), user_prompt(item, resp), retry=0)
        out = postprocess(out)
        rec = dict(item=item['id'], skill=item['skill'], model=MODEL, expected=expected,
                   response=resp, secs=round(time.time()-t0, 1))
        if out is None:
            rec.update(got='ERR', error=err)
            print(f"✗ [{item['id']}] 调用失败 {err}")
        else:
            got = out.get('verdict', '?')
            rec.update(got=got, is_reflection=out.get('is_reflection'),
                       captured=out.get('captured', ''), missed=out.get('missed', ''),
                       comment=out.get('comment', ''), rewrite_hint=out.get('rewrite_hint', ''))
            print(f"{'✓' if got==expected else '✗'} [{item['id']}] 预期={expected} 判定={got} ({rec['secs']}s)")
        existing = [e for e in existing if not (e.get('item')==rec['item'] and e.get('response')==rec['response'] and e.get('model')==rec['model'])]
        existing.append(rec)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
    return existing


if __name__ == '__main__':
    print(f'模型: {MODEL}\n' + '='*74)
    rows, agree = [], 0
    for item in ITEMS:
        for expected, resp in item['responses']:
            out, err = call(system_prompt(item['skill']), user_prompt(item, resp))
            if out is None:
                print(f"[{item['id']}] 调用失败: {err}"); rows.append((item['id'],expected,'ERR',resp,'')); continue
            got = out.get('verdict','?')
            ok = (got == expected)
            agree += ok
            mark = '✓' if ok else '✗'
            print(f"\n{mark} [{item['id']}] 预期={expected} 判定={got}  is_reflection={out.get('is_reflection')}")
            print(f"   学员：{resp[:44]}...")
            print(f"   接住：{out.get('captured','')[:56]}")
            print(f"   遗漏：{out.get('missed','')[:56]}")
            print(f"   点评：{out.get('comment','')[:90]}")
            print(f"   改写：{out.get('rewrite_hint','')[:60]}")
            rows.append((item['id'],expected,got,resp,out.get('comment','')))
    total = len(rows)
    print('\n'+'='*74)
    print(f'一致 {agree}/{total} = {agree/total:.0%}')
    with open(os.path.join(HERE,'selftest_result.json'),'w',encoding='utf-8') as f:
        json.dump([dict(item=r[0],expected=r[1],got=r[2],response=r[3],comment=r[4]) for r in rows],
                  f, ensure_ascii=False, indent=2)
    print('明细已存 selftest_result.json')
