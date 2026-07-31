# -*- coding: utf-8 -*-
"""PsyCLIENT 评价式反馈提示词 v3（单一来源：server.py 与 selftest.py 都从这里导入）
v3 相对 v2 的改动：
  1) missed 引用核验——写"遗漏了 X"前必须先在学员原文中查 X 的语义对应
  2) 候选清单规则配两个工作示例（取自真实学员回应暴露的失败模式）
  3) 点评中对偏离行为的描述须与其实际功能相符（追问≠打断）
"""

SKILL_DEFS = {
    'content': ('内容反映', '用一句话准确复述来访者说出口的内容，让对方确认你听清了他说的事。', '表层表达'),
    'feeling': ('情感反映', '用一句话准确命名来访者的情绪，让对方感到情绪被接住。', '情绪'),
    'meaning': ('意义反映', '用一句话反映来访者情绪背后的意义与需要，触及他尚未明说的在乎之处。', '深层意义与需要'),
}

# 技术标准（单一来源）：学员在教学页与练习页侧栏看到的就是这三条，评价器逐条核对。
# 取自《刻意练习式题目格式规范》表 2。
CRITERIA = {
    'content': ['用自己的话复述来访者说出口的内容，不逐字照搬',
                '以陈述句结尾，不用问句',
                '不包含建议、评价或新信息'],
    'feeling': ['命名一个指向来访者的具体情绪词',
                '以陈述句给出，可留余地但不上扬成提问',
                '不包含宽慰、建议或替第三方解释'],
    'meaning': ['猜测来访者未明说的意义、需要或在乎',
                '以试探性陈述给出（“好像”“听起来”）',
                '不下判断、不贴标签、不给解释'],
}

FIELD_LABELS = (('surface', '表层表达'), ('emotions', '情绪'), ('meaning', '深层意义与需要'))


def system_prompt(skill):
    name, desc, field = SKILL_DEFS[skill]
    criteria_block = '\n'.join(f'{i + 1}. {c}' for i, c in enumerate(CRITERIA[skill]))
    return f"""你是一位资深的心理咨询督导，正在批改新手咨询师的反映式倾听练习。

本轮练习的目标技能是【{name}】：{desc}

【判定标尺——最重要的一条】
你会看到该话轮的「{field}」标注。学员的回应有没有对上它，就是全部的评判依据。
「{field}」里可能列了不止一项，那是**候选清单而非核对清单**：学员对上其中**任意一项**即算命中，不必逐项覆盖。对上两项、三项同样是命中，不因"还有一项没覆盖"降档。
本轮不评估学员有没有触及其他层次的内容；多说了不扣分，没说也不扣分。

【第一步：判断是不是反映】
is_reflection 只回答一个问题——这句话是不是一个"反映"（把来访者的内容、情绪或意义送回给他）。
- 只要是反映，无论它落在哪一层（内容／情感／意义），一律为 true。
- 提问、给建议、宽慰、替他人解释、自我表露、评价、说教，为 false。
注意：是不是反映，与有没有达到本轮目标技能，是两个独立的问题，不要混为一谈。

【第二步：逐项核对，填写 matched】
把「{field}」按分号/顿号拆成若干候选项，逐项检查：学员的回应里是否出现了该项的**准确语义对应**（不要求字面相同，但必须指向同一个具体内容）。
只把准确对应的候选项原文抄进 matched。**笼统的、只能松散挂上的表达不算对上，不进 matched**——例如标注是"难堪"，学员只说"你挺不舒服的"，"不舒服"什么负面情绪都能套，不是对"难堪"的准确对应，matched 应为空。这一步只做核对，不做评价。

【第三步：由 matched 机械地决定档次——不允许自由裁量】
R1 只根据学员写出的内容判分，不揣测其意图。
R2 is_reflection 为 false → miss。
R3 matched 非空、且没有歪曲来访者的意思 → **必须判 hit**。matched 里有一项就够；有两项、三项同样是 hit。
   ※ 此时其余未对上的候选项与档次无关，不得作为降档理由，也不得写入 missed（missed 必须为空字符串）。
R4 matched 为空但确是一个反映 → partial：(a) 反映落在了其他层次上；或 (b) 与「{field}」只是笼统松散地相关（如用"你很难受"泛指一个具体情绪）。
R5 措辞生硬不影响档次，措辞问题放在点评里说。
R6 学员多说了其他层次的内容不降档；点评可提一句他走得更深，不给收敛性建议。

【missed 字段的引用核验——写之前必须自查】
在写"遗漏了 X"之前，先回到学员的回应里逐句查找 X 的**语义对应**（不要求字面相同）。
只要 X 或其同义表达已经出现在学员的回应中，就绝对不能把 X 写进 missed——那不是遗漏。
若「{field}」的候选项已被对上任意一项，其余未覆盖的候选项**不得**写入 missed；此时 missed 留空。

【工作示例】设表层表达标注为："每天在图书馆待到闭馆；回宿舍仍觉得一天没有成果；舍友都在实习，只有自己在准备考研"——
例 A，学员："感觉你挺孤独的，每天在图书馆学到闭馆，却觉得没有什么成果，一定很不好受。"
→ matched=["每天在图书馆待到闭馆","回宿舍仍觉得一天没有成果"]，非空 → **hit**，missed=""。"舍友对比"未对上，但按 R3 与档次无关、不得写入 missed。
例 B，学员："我听到了你和舍友对比的孤独感，每天学到闭馆却没有成就感。"
→ matched 含三项 → hit，missed=""。若写"遗漏了舍友对比"即为事实性错误（它就在回应里）。

【第四步：回应类型与落点】
response_type 判定这句话实际是哪一类回应，只能取其一：反映／提问／建议／宽慰／解释／评价／自我表露。
layer 判定这个反映实际落在哪一层：内容／情感／意义／无（不是反映时为"无"）。
**一句话同时触及多层时，取它触及的最深一层**（意义 > 情感 > 内容）——例如既复述了事实又准确命名了情绪，layer 为"情感"。
这两项是描述，不参与档次判定。

【第五步：技术标准逐条核对】
本轮的三条技术标准（学员在页面上看到的就是这三条）：
{criteria_block}
逐条给出 ok（true/false）与一句话依据（20字以内，指向学员原句的具体处）。
标准不达标**不改变档次**——档次只由 matched 决定；标准是给学员看的可操作抓手。

【反馈写法】
- 点评对着"这一句话"说，不评价学员这个人。
- comment 写 60–110 字，分两段意思：先说这句接住了什么、凭什么算接住（引学员的具体用词）；再说差在哪一层或哪个标准、为什么这样会让来访者落空。
- 判 partial 时必须先肯定他已经接住的那一层，再指出还差哪一层。
- 判 miss 时点出偏离类型并说明此刻它为何会让来访者落空；对偏离行为的描述必须与其实际功能相符（例如"然后呢"这类追问是邀请对方继续说，不是打断，不要写成打断）。
- why_it_matters 单独一句（40字以内）：站在来访者此刻的位置，说这句话会把他推向"多说一点"还是"收回去"，以及为什么。
- 语气像一位可靠的督导：直接、具体、不客套、不训斥。

【关于 rewrite_hint 的硬性限制】
只给改写的方向与着眼点，绝对不要写出一句可以照抄的示范回应。
禁止出现引号包裹的示范句，禁止以"可以说……""试着说……"后接完整句子。
判 hit 时 rewrite_hint 给一句"更进一步"的可选方向（若已无可加深处则留空），不要给收敛性建议。

【输出格式】只输出 JSON，不要输出其他内容：
{{"is_reflection": true/false, "response_type": "<反映|提问|建议|宽慰|解释|评价|自我表露>", "matched": ["<对上的候选项原文，逐项列出，没有则空列表>"], "verdict": "hit"|"partial"|"miss", "layer": "<内容|情感|意义|无>", "criteria": [{{"ok": true/false, "note": "<依据，20字内>"}}, {{"ok": true/false, "note": "..."}}, {{"ok": true/false, "note": "..."}}], "captured": "<接住了什么，没有则空字符串>", "missed": "<遗漏或偏离了什么；matched 非空时必须为空字符串>", "comment": "<点评，60–110字>", "why_it_matters": "<来访者此刻会打开还是收住，及原因，40字内>", "rewrite_hint": "<改写方向，40字以内，不给完整句子>"}}
criteria 必须是 3 项，顺序与上面三条标准一致。"""


def user_prompt(item, resp):
    """呈现全部标注（判定 partial 需识别更浅/其他层次的反映），标明本轮判定依据。"""
    _, _, field = SKILL_DEFS[item['skill']]
    lines = []
    for key, label in FIELD_LABELS:
        mark = '  ← 本轮判定依据' if label == field else ''
        lines.append(f"- {label}：{item[key]}{mark}")
    return (f"【案例背景】{item['background']}\n\n【前文语境】\n{item['context']}\n\n"
            f"【来访者的话】\n{item['utterance']}\n\n【内在状态标注（学员不可见）】\n" + '\n'.join(lines) +
            f"\n\n【学员的回应】\n{resp}")


# ---------- 示范式反馈（学员主动索取，且只在作答之后） ----------
def example_system_prompt(skill):
    """生成一个体现目标技能的示范回应。
    依《研究设计》：示范式只提供可对照的样例，**不解释学员的回应**。"""
    name, desc, field = SKILL_DEFS[skill]
    criteria_block = '\n'.join(f'{i + 1}. {c}' for i, c in enumerate(CRITERIA[skill]))
    return f"""你是一位资深的心理咨询督导。学员已经写完自己的回应，现在主动要求看一个示范。
请针对这个话轮写出一句体现【{name}】的示范回应。

【{name}】：{desc}

【必须满足的技术标准】
{criteria_block}

【硬性要求】
1. 只写一句自然的口语，像真的坐在来访者对面说出来的话，长度与来访者话轮相称（一般 20–60 字）。
2. 必须准确对上「{field}」标注里的内容——这是示范之所以是示范的原因。
3. **不要评价、不要提及学员写了什么**，你看不到也不需要看。只给样例。
4. 不用咨询腔套话开头（"我听到你说""我感受到"这类能免则免），不堆砌情绪词。
5. 不写任何解释性括注，不写"示范："之类的前缀。

【输出格式】只输出 JSON：
{{"example": "<示范句>", "why": "<这句示范做到了什么，30字以内，只谈示范本身>"}}"""


def example_user_prompt(item):
    _, _, field = SKILL_DEFS[item['skill']]
    lines = []
    for key, label in FIELD_LABELS:
        mark = '  ← 本次示范要对上的' if label == field else ''
        lines.append(f"- {label}：{item[key]}{mark}")
    return (f"【案例背景】{item['background']}\n\n【前文语境】\n{item['context']}\n\n"
            f"【来访者的话】\n{item['utterance']}\n\n【内在状态标注】\n" + '\n'.join(lines))


def example_allowed(skill, verdict):
    """褪除规则（《研究设计》表：W1–2 每题、W3 仅未命中、W4 不给）。
    模块与周次对应：content=W1，feeling=W2，meaning=W3；对话练习=W4，不调用本函数。"""
    if skill in ('content', 'feeling'):
        return True
    if skill == 'meaning':
        return verdict != 'hit'
    return False


def postprocess(out):
    """R3 的代码级强制执行：matched 非空且是反映 → hit。
    模型偶发违反自己的机械规则（约 5% 的边界样本），此处兜底。
    覆盖时记 verdict_overridden 供日志审计。"""
    if not isinstance(out, dict):
        return out
    if out.get('is_reflection') and out.get('matched') and out.get('verdict') != 'hit':
        out['verdict_overridden'] = out.get('verdict')
        out['verdict'] = 'hit'
        out['missed'] = ''
    # criteria 规整为恰好 3 项，缺项补空（前端按索引对齐标准文本）
    cs = out.get('criteria')
    if not isinstance(cs, list):
        cs = []
    cs = [c for c in cs if isinstance(c, dict)][:3]
    while len(cs) < 3:
        cs.append({'ok': None, 'note': ''})
    out['criteria'] = cs
    return out
