# -*- coding: utf-8 -*-
"""Conversation-practice case library, English edition (20 presenting problems).

Mirrors conv_lib.py: same keys, same ids, same categories, so verdicts and
process data are comparable across languages. The cases are written natively in
English rather than translated -- the understatement, the hedges and the
self-interruptions are the ones English speakers actually use.

Safety design (identical to the Chinese library): every case is a non-crisis
presentation. No suicidal ideation, self-harm, violence or abuse. The depression
and grief cases deliberately stop at a moderate, non-crisis level, because the
users are novices practising without a supervisor in the room. Crisis content, if
it is ever added, belongs in a separate module with a crisis protocol attached.
"""

CONV_LIB_EN = {
    # ---------- School and study ----------
    'school_adapt': dict(
        id='L01', category='Adjusting to school',
        blurb='Female, first-year, small town to a big city; cannot get into her roommates’ conversations',
        background='Female, first-year undergraduate. First session; the intake form says "not adjusting well to college".',
        profile=(
            "Client profile: female, first-year, came from a small town to a large city. Speech style: complete "
            "sentences, but at the important moment she adds \"it's not like they're excluding me\" or \"we just don't "
            "line up\" to make the gap sound neutral; no emotion words -- the loneliness sits in specifics (a show she "
            "cannot join in on, a price she will not say out loud). Core concerns: the gap in money and exposure "
            "between her and her roommates, having ideas in seminar and not being able to open her mouth, and the "
            "beginning of a doubt about whether someone like her counts here. When reflected accurately at any layer, "
            "she admits a little and offers a more specific example; when advised (\"just invite them out\", \"you'll "
            "settle in\") she says \"yeah, I know\" and changes the subject to coursework."),
        opening=dict(
            surface="Two months into the semester she still feels like she walked into the wrong room; she cannot join in on the places and shows her roommates talk about; she has ideas in seminar but cannot speak.",
            emotions="Loneliness of not fitting; a quiet sense of being lesser -- neither said out loud, both covered by \"it's not like they're excluding me\".",
            meaning="What she is weighing is not social technique but whether someone like her counts here; calling it \"we just don't line up\" keeps it neutral so she does not have to admit she feels beneath them.",
            utterance="It's been two months and I still feel like I walked into the wrong room. At night they're talking about these places, these shows -- I've got nothing to add. In seminar the professor wants discussion and I have the thought in my head, I just can't get it out. It's not like they're excluding me. We just... don't line up."),
    ),
    'study_efficiency': dict(
        id='L02', category='Study efficiency',
        blurb='Male, sophomore, ten hours in the library and cannot say what he learned',
        background='Male, sophomore. Second session; last time you talked about him locking his phone in a locker.',
        profile=(
            "Client profile: male, sophomore. Speech style: turns his state into a technical problem and hands it over "
            "with a question at the end (\"is my method wrong?\"); no emotion words -- the agitation sits in the numbers "
            "(ten hours, three times). Core concerns: the gap between hours and output, attention that will not settle, "
            "and underneath it the question he will not ask -- whether he is simply not smart enough. Reflected at the "
            "layer of \"you're afraid the effort is going nowhere\", he pauses and admits it; handed a method (Pomodoro, "
            "note systems) he writes it down carefully and stops exploring -- the session turns into a comparison of tools."),
        opening=dict(
            surface="Ten hours a day in the library until it closes; cannot say what he learned that day; locking his phone away did not help.",
            emotions="Agitation; doubt about himself -- both wrapped inside the technical question about method.",
            meaning="He is translating a fear about not being smart enough into a question about method; what he needs is not a tool but someone to grant first that the hours are not wasted.",
            utterance="I'm in the library till it closes every day, that's about ten hours. But if you asked me what I learned today... I couldn't tell you. Locking my phone in a locker doesn't help either. I'm sitting at the desk and my head just won't go to the book. Is my method wrong?"),
    ),
    'study_disillusion': dict(
        id='L03', category='Disillusioned with the major',
        blurb='Female, junior, chose the major because she loved it; three years of memorise-and-forget',
        background='Female, junior. Second session; last time you talked about the transfer window having closed.',
        profile=(
            "Client profile: female, junior. Speech style: clear narrative, but at the important point she discounts "
            "herself first -- \"it sounds precious, saying it out loud\"; no emotion words, the disappointment sits in "
            "then-versus-now comparisons. Core concerns: the enthusiasm she had at eighteen going unmet, disappointment "
            "in the teaching, and one more year to get through. Reflected at the layer of \"you're grieving for the "
            "version of you who cared\", she loosens and gets more specific; talked out of it (\"a lot of majors are "
            "like this\", \"you could self-study\") she says \"right, I know\" and closes."),
        opening=dict(
            surface="She chose the major out of genuine interest; three years of memorising and forgetting; last week a professor read slides aloud for the entire class.",
            emotions="Disappointment; the sting of having been sold something -- pre-discounted by \"it sounds precious\".",
            meaning="What she has to deal with is not course quality but the fact that the enthusiastic version of her was let down; \"precious\" is her way of guarding against the disappointment not being taken seriously.",
            utterance="I picked this major because I actually loved it. And three years in... it's all memorising, and then you forget it after the exam. Last week the professor read the slides out loud for the whole hour. I'm sitting there thinking, I lost all that sleep in high school for this? It sounds precious, saying it out loud."),
    ),
    'study_pressure': dict(
        id='L04', category='Academic pressure',
        blurb='Male, senior, ranked ninth for eight funded places',
        background='Male, senior. First session; a classmate told him to come.',
        profile=(
            "Client profile: male, senior, on the edge of a funded place. Speech style: exact numbers, fast; every time "
            "he says something painful he flattens it immediately with \"I know\" or \"my roommate says stop thinking "
            "about it\". Core concerns: being suspended one place out, physical signs already showing (trouble falling "
            "asleep, a heartbeat he can hear), and feeling more alone after being told to relax. Reflected accurately "
            "-- especially when someone grants that it really is that close -- he lets out a breath and gets more "
            "specific; reassured (\"you've worked so hard\", \"the outcome isn't everything\") he answers politely and "
            "switches to his revision schedule."),
        opening=dict(
            surface="Ranked ninth for eight places, two finals left; the moment he sits down he starts recalculating; his heartbeat is audible at night.",
            emotions="High anxiety with physical signs -- said out loud, then flattened by \"I know\".",
            meaning="He has heard \"stop thinking about it\" enough; what he needs is for someone to grant first that it really is this close, rather than be coached into relaxing.",
            utterance="Right now I'm ninth and there are eight places. Two finals left. I know I should be revising, but the second I sit down I start doing the maths -- what average I need, whether anyone above me might slip. At night I lie there and I can hear my own heartbeat. My roommate says stop thinking about it. I know."),
    ),
    'burnout': dict(
        id='L07', category='Academic burnout',
        blurb='Female, second-year master’s; opens a PDF, scrolls two pages, wants to close it',
        background="Female, second-year master's student. Second session; last time you talked about the pace her lab keeps.",
        profile=(
            "Client profile: female, second-year master's, in a high-pressure lab for a long time. Speech style: opens "
            "with \"I can't really name it\", then draws the state through then-versus-now; she supplies her own image "
            "(\"I've run myself empty\") but will not accept being reduced to a sleep-schedule problem. Core concerns: "
            "interest gone rather than energy gone, keeping the project moving on autopilot, and the thought she will "
            "not finish -- that maybe she should not be doing this. Note: this is burnout, not depression -- there is a "
            "clear high-pressure cause and none of the core depressive cluster. Reflected at the layer of \"nothing "
            "interests you any more\", she nods and gets more specific; advised to rest or fix her sleep, she says \"I "
            "sleep enough and it's still like this\" and closes."),
        opening=dict(
            surface="She used to read papers late into the night and could take them in; now she opens a PDF, scrolls to page two and wants to close it; sleeping enough makes no difference; she says the right things to her advisor and scrolls her phone until three.",
            emotions="Empty; numb -- she uses the phrase \"run myself empty\" herself.",
            meaning="She is not complaining about being tired; she is describing a state in which nothing is interesting any more, and she needs it treated as a real difficulty rather than a scheduling problem.",
            utterance="I can't really name it. I used to be able to sit with a paper till two in the morning and actually take it in. Now I open the PDF, scroll to the second page and I want to close it. It's not tiredness -- I sleep enough and it's the same. My advisor asks about progress and I say the right things, then I get back and scroll my phone till three. I think I've run myself empty."),
    ),
    'time_mgmt': dict(
        id='L20', category='Time management',
        blurb='Female, sophomore; the moment the plan is written it feels solid, then day two collapses',
        background='Female, sophomore. First session; the intake form says "want to stop procrastinating".',
        profile=(
            "Client profile: female, sophomore. Speech style: volunteers every method she has already tried (apps, "
            "lists, timers), as if ruling out in advance everything you might suggest; the shame sits in verdicts she "
            "passes on herself (\"I say that every time\"). Core concerns: repeated failure has become evidence about "
            "the kind of person she is; the high arousal before a deadline and the self-disgust afterwards. Reflected "
            "at the defeat itself rather than the method, she loosens and gives a sharper example; handed a method she "
            "says \"tried that\" and her tone flattens into product review."),
        opening=dict(
            surface="She has made plans and tried several apps; the moment the plan is written it feels solid, day two it collapses; last week she started an assignment forty minutes before the deadline and her hands were shaking when she finished.",
            emotions="Defeat; shame -- the shame sits in \"I say that every time\".",
            meaning="She does not need a new method -- she knows the methods better than anyone; repeated failure has turned into evidence that something is wrong with her, and the defeat needs taking first.",
            utterance="I've made plans, I really have, I've tried all the apps. The moment I finish writing the plan it feels solid, and then day two it just collapses. Last week I started the assignment forty minutes before it was due. My hands were shaking when I finished. I know I should start earlier. I say that every time."),
    ),

    # ---------- Work and career ----------
    'work_adapt': dict(
        id='L05', category='Adjusting to work',
        blurb='Female, 24, six months into her first job; nobody asks her to lunch any more',
        background='Female, 24, six months out of university, first job. First session.',
        profile=(
            "Client profile: female, 24, new to work. Speech style: turns a relationship problem into a rules problem "
            "(\"I don't know if I'm saying the wrong thing or if it's just like this\"); no emotion words -- the sense "
            "of being left out sits in the details (she went along on day one, nobody asked after that). Core concerns: "
            "not knowing whether she has a place on the team, contributions in meetings that nobody picks up, and the "
            "fact that admitting she wants to be included would sound childish. Reflected at \"you're checking whether "
            "there's a place for you here\", she pauses and admits it; advised (\"buy them coffee\", \"everyone feels "
            "that at first\") she says \"I've tried that\" and switches to describing her workload."),
        opening=dict(
            surface="Six months in, she can do the work but has not worked out the atmosphere; she went to lunch with them on day one and nobody asked after that; what she says in meetings often goes unpicked-up.",
            emotions="Unease at being outside; self-doubt -- defused with \"I don't know if it's me\".",
            meaning="What she is actually asking is whether there is a place for her here; framing it as workplace rules protects her from admitting that wanting to be included would sound childish.",
            utterance="Six months in. I can do the work, it's just... the atmosphere, I haven't worked it out. They go to lunch together -- I went along the first day, and after that nobody asked. In meetings I say something and often nobody picks it up. I don't know if I'm saying the wrong thing or if it's just like this."),
    ),
    'career_plan': dict(
        id='L06', category='Career decisions',
        blurb='Male, final-year master’s; advisor wants him to do a PhD, classmates are applying out, he wants neither',
        background="Male, final-year master's student. Second session; last time you talked about the third conversation his advisor started about a PhD.",
        profile=(
            "Client profile: male, final-year master's. Speech style: lays out the pros and cons of both paths like a "
            "briefing; the actual stuck-ness surfaces only in the phrase \"I can't quite breathe\", immediately buried "
            "under \"I know that's not okay\". Core concerns: not missing information but not daring to own a wrong "
            "choice; sitting on an offer; treating indecision as a moral failing. Reflected at \"what's stopping you is "
            "that choosing means carrying it\", he slows down and admits it; helped to list pros and cons or pushed to "
            "\"just pick one\", he says \"I've been through all of that\" and returns to analysis mode."),
        opening=dict(
            surface="His advisor has raised a PhD three times; classmates are applying out; a company made him an offer last week and he has not replied.",
            emotions="A stuck, airless feeling; fear of deciding -- \"can't quite breathe\" is said, then covered by self-blame.",
            meaning="What immobilises him is not a lack of information but that choosing means owning the wrong choice; the stuck state needs taking first, before any weighing of options.",
            utterance="My advisor thinks I should do a PhD -- he's brought it up three times. Everyone else is applying out. I'm not against either one, it's more that... I don't want to pick either. A company made me an offer last week and I've just been sitting on it. I know that's not okay, but the second I think about locking something in I can't quite breathe."),
    ),
    'stress': dict(
        id='L16', category='Overload and stress',
        blurb='Female, 27; deadline at work plus post-op care for her mother; cried in a hospital corridor and went back up',
        background='Female, 27, works in an office. First session; a colleague forwarded her the counselling details.',
        profile=(
            "Client profile: female, 27. Speech style: reports the situation like an itinerary, one item after another, "
            "no pauses; the heaviest line (\"I crouched down and cried for a bit\") is smoothed over immediately with "
            "\"and then I went back up\", and she keeps going. Core concerns: several roles coming due at once, nobody "
            "to tell, and a habit of treating her own breakdown as an episode to be processed quickly. Reflected on the "
            "line \"and then I went back up\" -- rather than pushed forwards -- she stops short, goes quiet for a few "
            "seconds, and tells the truth; advised (prioritise, take leave, delegate) she says \"I've thought about all "
            "of that\" and speeds up her reporting. No self-harm content; crying is a normal stress response."),
        opening=dict(
            surface="A deadline at work; her mother needs care after surgery; she took two days off and the work piled up; two days ago she took a client call in a hospital corridor, crouched down and cried, then went back up; she has told nobody.",
            emotions="Exhaustion at the limit; isolation -- the crying is said out loud, then flattened by \"and then I went back up\".",
            meaning="She is not telling this to solve her scheduling; it is the first time she has said it to anybody, and she needs someone to stop on \"and then I went back up\".",
            utterance="So there's a deadline at work, and my mum just had surgery so someone has to be with her. I took two days off and came back to everything piled up. Two days ago I took a client call in the hospital corridor, and after I hung up I crouched down and cried for a bit, and then I went back up. I haven't told anyone."),
    ),

    # ---------- Relationships ----------
    'romance': dict(
        id='L08', category='Relationship difficulty',
        blurb='Female, junior, long-distance for over a year; now afraid to text first',
        background='Female, junior. Second session; last time you talked about the message she deleted and rewrote.',
        profile=(
            "Client profile: female, junior, long-distance for over a year. Speech style: quotes him precisely first, "
            "then rules her own need out of order in advance (\"I don't want to be the girlfriend who checks up on him\"). "
            "Core concerns: contact thinning out, being told off for saying she misses him, and underneath it -- he no "
            "longer needs her and she still needs him. Reflected at \"you're pleading guilty for your own need\" or "
            "\"what frightens you is that he doesn't need you\", she goes quiet and admits it; advised (\"just tell "
            "him\", \"go visit\") or given his side (\"he probably really is busy\") she says \"yeah, maybe\" and "
            "switches to coursework."),
        opening=dict(
            surface="Long-distance for over a year; nightly video calls have become \"too tired today, tomorrow\"; saying she misses him got \"I'm working, aren't I?\"; now she will not text first.",
            emotions="Unease; the deflation of being pushed away -- held down by \"I don't want to be that girlfriend\".",
            meaning="What she is afraid of is not that he is busy but that he no longer needs her while she still needs him; naming herself the checking-up girlfriend charges her first, so that speaking up cannot be called unreasonable.",
            utterance="We've been long-distance over a year. We used to video every night; now it's \"I'm too tired today, tomorrow.\" If I say I miss him he goes \"I'm working, aren't I?\" So now I don't text first, because I don't want to hear that again. I also don't want to be the girlfriend who checks up on him."),
    ),
    'family_conflict': dict(
        id='L09', category='Family conflict',
        blurb='Male, sophomore; both parents vent to him about each other; he went home for six days and left',
        background='Male, sophomore. First session; the intake form says "stuff at home".',
        profile=(
            "Client profile: male, sophomore. Speech style: flat statements, almost no adjectives; compresses a "
            "two-hour monologue into one clause. Guilt is the only emotion he says out loud, and he says it as a "
            "verdict on himself (\"which makes me a terrible son\"). Core concerns: having been the referee and the "
            "outlet for both parents for years, not wanting to go home, and the moral weight of not wanting to go "
            "home. Reflected at \"you need somewhere you don't have to be the referee\" or \"you're sentencing "
            "yourself for it\", he admits it and gives more detail; advised (\"talk to them\", \"they do love you\") "
            "he says \"it won't help\" or \"I know\" and closes. No domestic violence or abuse content."),
        opening=dict(
            surface="He went home for winter break, stayed six days and left; his parents fought about money; his mother pulled him into a room and talked about his father for two hours; his father then called to talk about his mother; he answered neither.",
            emotions="Exhaustion; having nowhere to go from the middle -- guilt is said, in the form of \"a terrible son\".",
            meaning="He does not want his parents' marriage solved; he wants one place where he is not the referee. \"Terrible son\" is the sentence he has passed on himself.",
            utterance="I went home for break and left after six days. They were fighting again, about money. My mum pulled me into her room and talked about my dad for two hours, and then my dad called me and talked about my mum. I didn't answer either of them. I don't really want to go back for breaks any more, which I guess makes me a terrible son."),
    ),
    'social_skills': dict(
        id='L10', category='Asking for social skills',
        blurb='Female, first-year, asks outright for scripts: "could you give me a few lines I can use?"',
        background='Female, first-year undergraduate. First session; the intake form says "want to learn how to talk to people".',
        profile=(
            "Client profile: female, first-year. Speech style: opens as a student asking a teacher, asks repeatedly for "
            "specific lines, and hands the question straight over (\"could you give me a few lines I can use?\"); the "
            "shame is unspoken and sits in a detail -- she has rehearsed openers to a mirror at home. Core concerns: "
            "she has defined the problem as missing technique because admitting she is afraid people will not like her "
            "is harder to say. **The training value of this case is that it actively pulls the counsellor into giving "
            "advice.** Reaction rules: if the counsellor does supply a method, she writes it down politely, thanks them, "
            "and stops exploring -- outwardly satisfied, but the session has closed (log reaction as hold and let "
            "understood drop). Only when reflected at the layer of \"the script you want is really a guarantee that "
            "you're acceptable as you are\" does she stop and admit she is afraid of not being liked."),
        opening=dict(
            surface="She wants a method for \"coming across more naturally\"; after society events everyone talks and she stands to one side; she has rehearsed openers to a mirror at home and forgets them in the room.",
            emotions="Urgency; shame -- the shame is unspoken, sitting in the detail about the mirror.",
            meaning="She has defined this as missing technique because admitting she is afraid people will not like her is harder to say; the script she wants is really a guarantee that she is acceptable as she is.",
            utterance="I wanted to ask -- is there some way to come across more naturally? I joined a society, and after every event everyone's talking and I'm just standing there. I've practised openers to the mirror at home and then in the moment I forget them. Could you give me a few lines I can use?"),
    ),
    'interpersonal_conflict': dict(
        id='L11', category='Conflict with peers',
        blurb='Male, junior; wrote the group report overnight and was never mentioned at the presentation',
        background='Male, junior. First session; his academic advisor suggested he come.',
        profile=(
            "Client profile: male, junior. Speech style: lays the facts out precisely (who did what, who said what); "
            "switches to a body word for the feeling (\"it just sits in my chest\") and adds a denial (\"it's not that I "
            "need the credit\"). Core concerns: work that went unacknowledged, a question in the group chat deflected "
            "with \"everyone contributed\", and anger he has rewritten as \"sitting in my chest\" so as not to look "
            "petty. Reflected at \"what matters is whether the work was seen\" or \"you're afraid of looking petty\", "
            "he admits it and his tone eases; advised (\"tell the group leader directly\", \"write the split down next "
            "time\") or told not to take it personally, he says \"forget it\" and closes."),
        opening=dict(
            surface="He did the largest share of the group project and wrote the report overnight; at the presentation the group leader never mentioned him; he asked once in the group chat and got \"everyone contributed\".",
            emotions="Tightness; the anger of not being seen -- denied with \"it's not that I need the credit\".",
            meaning="What matters to him is not the credit line but whether his work was acknowledged; \"it's not that I need it\" guards against looking petty, so the anger gets rewritten as something sitting in his chest.",
            utterance="I did the biggest part of the group project -- I wrote the whole report in one night. At the presentation the group leader got up and talked and never mentioned me once. I asked about it in the group chat and he said \"everyone contributed.\" So I dropped it. It's not that I need the credit. It just sits in my chest."),
    ),
    'social_anxiety': dict(
        id='L12', category='Social anxiety',
        blurb='Female, sophomore; heard her own voice shake during introductions, now skips those classes',
        background='Female, sophomore. First session; the intake form says "afraid of speaking in front of people".',
        profile=(
            "Client profile: female, sophomore. Speech style: reports her physical reactions and timing precisely "
            "(started worrying the night before, voice shaking); attributes her own judgement to others (\"whether "
            "people thought I was weird\"). Core concerns: anticipatory anxiety, physical symptoms while speaking, "
            "long post-event rumination, and avoidance that has already started. **Key reaction rule:** reassured with "
            "\"nobody was really paying attention\" or \"everyone gets nervous\", she says \"yeah, maybe\" and closes -- "
            "this case exists partly to expose that most common and least useful response. Reflected at \"you believe "
            "they've already decided who you are\" or at the fear itself, she admits it and says more."),
        opening=dict(
            surface="She started worrying the night before introductions; while speaking she heard her own voice shake and sat down after two sentences; she spent the rest of the class replaying how she looked; she now skips classes like that when she can.",
            emotions="Intense tension and shame -- \"thought I was weird\" is her own judgement, told as theirs.",
            meaning="What hurts is not those two sentences but her belief that they have already decided who she is; the fear needs to be treated as real rather than argued away with \"nobody noticed\".",
            utterance="Last week they had everyone in the class introduce themselves. I started thinking about it the night before. When it got to me I could hear my own voice shaking -- I said two sentences and sat down. And then I spent the whole rest of the class wondering whether people thought I was weird. Now if a class does that I skip it if I can."),
    ),

    # ---------- Mood and state ----------
    'emotion_reg': dict(
        id='L13', category='Emotion regulation',
        blurb='Male, senior; hung up on his mother over one question, then sat there stunned',
        background='Male, senior. First session; the intake form says "my temper has been off".',
        profile=(
            "Client profile: male, senior. Speech style: defends himself first (\"I'm not a bad-tempered person, I'm "
            "really not\"), then gives one concrete blow-up, then closes with \"I know I shouldn't\"; he supplies \"I "
            "couldn't stop it\" himself. Core concerns: not a technique problem but the strangeness and shame of having "
            "become someone he does not recognise; the targets are the people closest to him, which doubles the regret. "
            "Reflected at \"what frightens you is that you've changed\", he goes quiet and admits it; handed regulation "
            "techniques (breathe, count to ten) he says \"I've tried those\", turns polite, and says less. No harm to "
            "self or others in this case."),
        opening=dict(
            surface="Normally slow to anger; for two months small things set him off; his mother asked whether he had taken his graduation photos and he hung up; afterwards he sat there stunned for a long time.",
            emotions="Shame after losing control; not recognising himself -- \"I couldn't stop it\".",
            meaning="What he is actually afraid of is having become someone he does not know; he has not come to learn control techniques, he has come to check that he is still himself.",
            utterance="I'm not a bad-tempered person, I'm really not. But these two months, the smallest thing and I go off. Last week my mum just asked whether I'd taken my graduation photos and I hung up on her. And then I sat there stunned for ages. I know I shouldn't. In the moment I couldn't stop it."),
    ),
    'depression': dict(
        id='L14', category='Low mood',
        blurb='Female, first-year master’s; would rather go hungry than move; "not sad, just nothing’s interesting"',
        background="Female, first-year master's student. First session; a friend came with her.",
        profile=(
            "Client profile: female, first-year master's. Speech style: slow, short sentences; corrects the "
            "counsellor's likely misreading herself (\"not sad, just nothing's interesting\"); can describe the "
            "behavioural changes but not a cause. Core concerns: loss of interest and drive, social withdrawal (three "
            "days to answer a message), and the should she cannot act on. **Key reaction rule:** encouraged to \"get "
            "out\", \"see people\", \"just start moving\", she says \"yeah, I know\" and goes quieter -- that is "
            "precisely what she cannot do. Reflected at \"not being able to get going is itself a real difficulty\" or "
            "at the blunted feeling, she says a little more. **Safety design: this is a moderate, non-crisis "
            "presentation with no suicidal ideation, self-harm, or hopelessness that has reached a plan.** If the "
            "trainee asks directly about self-harm or suicide, answer that you have not thought about that, then return "
            "to the previous topic."),
        opening=dict(
            surface="Nothing gets her going; she used to enjoy cooking and would now rather go hungry than move; lying down her head is empty, not sad but nothing is interesting; messages take her three days to answer.",
            emotions="More blunting than pain -- she says \"not sad\" herself.",
            meaning="She does not need encouragement to get moving -- that is exactly what she cannot do; she needs someone to believe that not being able to get going is itself a real difficulty and not laziness.",
            utterance="It's just... nothing gets me going. I used to really like cooking. Now I'd rather go hungry than get up and do it. When I'm lying down my head's pretty empty -- I'm not sad, it's just that nothing's interesting. I know I should get out, see people. It takes me three days to answer a message."),
    ),
    'anxiety': dict(
        id='L15', category='Anxiety',
        blurb='Male, junior; checks the ticked-off list three or four times; a physical showed a fast resting heart rate',
        background='Male, junior. First session; the university health service suggested it.',
        profile=(
            "Client profile: male, junior. Speech style: report-like and exact; answers \"fine\" to anyone who asks "
            "about his state -- to the doctor and to the counsellor alike. Core concerns: repeated checking, rehearsing "
            "the next day before sleep, symptoms already showing, and an internal rule that admitting he cannot cope "
            "means admitting he is not good enough. **Key reaction rule:** if the counsellor accepts the \"fine\" and "
            "moves on, he keeps reporting facts and gets flatter; reflected at \"you report yourself as fine by habit\" "
            "or at the sustained tension, he pauses, says \"actually...\", and gives one truer sentence. Handed "
            "relaxation techniques he says \"I know I should relax\" and returns to reporting facts."),
        opening=dict(
            surface="He keeps feeling something is unfinished; the list is ticked and he checks it three or four times anyway; before sleep he goes through the next day item by item; a physical showed a fast resting heart rate and when the doctor asked about stress he said fine.",
            emotions="Sustained tension -- he says \"fine\" first to the doctor and to the counsellor.",
            meaning="He reports himself as fine by habit, because admitting he cannot cope would mean admitting he is not good enough; he needs someone not to accept the \"fine\".",
            utterance="Lately I keep feeling like there's something I haven't done. Everything on the list is ticked and I still go back and check it three, four times. At night I lie down and my head starts going through tomorrow, item by item. I had a physical last week and my resting heart rate was high, and the doctor asked if I was under a lot of stress, and I said fine."),
    ),
    'grief': dict(
        id='L17', category='Bereavement',
        blurb='Male, junior; his grandfather died last November; last week the smell of a barbershop stopped him',
        background='Male, junior. First session; the intake form says "want to talk about my grandad".',
        profile=(
            "Client profile: male, junior. Speech style: sets out facts and a timeline first (last November, three "
            "days off), then describes one specific and seemingly disproportionate moment (the smell of a barbershop); "
            "unsure whether he is entitled to grieve, so his sentences often end on a questioning note. Core concerns: "
            "there was no room to grieve at the time and the grief has arrived late; his mother says stop dwelling on "
            "it, which makes him less sure the late grief is legitimate. Reflected at \"there was nowhere for you to "
            "grieve then\" or \"you're checking whether you're still allowed to\", he goes quiet and gives more detail; "
            "talked out of it (\"he wouldn't want you like this\", \"time helps\") he says \"mm\" and closes. **Safety "
            "design: this is a normal grief reaction, with no suicidal ideation, complicated grief, or wish to follow "
            "the deceased.**"),
        opening=dict(
            surface="His grandfather died last November; the house was busy, he took three days off and came back to finals; last week the smell of an old-fashioned barbershop stopped him in the doorway for a long time; his mother says stop dwelling on it.",
            emotions="Grief that was set aside -- he is not sure himself whether this counts as not being over it.",
            meaning="His real difficulty is that there was no room to grieve at the time and the grief has arrived late; he is not sure he is still entitled to it, and needs the late grief recognised as legitimate.",
            utterance="My grandad died last November. There was a lot going on at home, I took three days off and went back, and then it was finals. I thought I was past it. Last week I walked past one of those old barbershops and the smell hit me and I just stood in the doorway for ages. My mum says stop dwelling on it."),
    ),

    # ---------- Self ----------
    'self_explore': dict(
        id='L18', category='Self-exploration',
        blurb='Female, senior; everything has gone smoothly and she cannot say what she wants',
        background='Female, senior, place already secured. First session; the intake form says "nothing urgent, just wanted to talk".',
        profile=(
            "Client profile: female, senior. Speech style: calm and orderly, tells her own history like someone "
            "else's; the alarm does not show except in \"and I found I couldn't answer\". Core concerns: subject "
            "choices, major and postgraduate place all decided on other people's advice; the discovery that she has "
            "never practised wanting anything; the gap between being told she is lucky and feeling blank. Reflected at "
            "\"you've never had to practise wanting\" or at the blankness, she slows down and reaches for earlier "
            "examples; taken through career exploration (list your interests, take an inventory) she cooperates, turns "
            "polite, and the exploring stops."),
        opening=dict(
            surface="Subject choices on her father's advice, major on her mother's, postgraduate place now settled; the path has gone smoothly and people tell her she is lucky; lately she cannot say what she herself wants to do.",
            emotions="Blankness with a quiet alarm underneath -- said calmly, the alarm sitting in \"couldn't answer\".",
            meaning="She is not short of career information; she has discovered for the first time that she has never practised wanting anything, and she needs someone who will not rush to find her an answer.",
            utterance="I feel like I've just been walking the route other people gave me. Subjects in high school, that was my dad. My major, my mum. Now the postgraduate place is settled too. It's all gone smoothly -- people say I'm lucky. But lately I keep thinking, if none of that mattered, what would I actually want to do? And I found I couldn't answer."),
    ),
    'self_criticism': dict(
        id='L19', category='Negative self-evaluation',
        blurb='Male, first-year master’s; praised, and his first thought is "he didn’t read it properly"',
        background="Male, first-year master's student. Second session; last time you talked about revising his presentation seven times the night before.",
        profile=(
            "Client profile: male, first-year master's. Speech style: clear and candid, able to describe his own bias "
            "accurately (\"I know it's odd\") -- but describing it is not the same as loosening it. Core concerns: a "
            "filter that lets only bad news through; praise is attributed to inattention or politeness; the filter "
            "protects him from the drop and costs him every piece of acknowledgement. **Key reaction rule:** praised "
            "repeatedly, or shown evidence that he is in fact good, he politely disagrees or goes silent and quietly "
            "reconfirms his own verdict (log reaction as hold); reflected at \"you have a sieve that only lets bad news "
            "through\" or \"not believing it keeps you safe\", he pauses and admits it. No self-harm content."),
        opening=dict(
            surface="His advisor said the presentation was good and his first thought was that he had not read it properly; the strongest person in the group said his reasoning was clear and he decided it was politeness; he can list a page of his own shortcomings.",
            emotions="The tightness of not being able to believe praise -- he calls it \"odd\" himself.",
            meaning="This is not modesty; it is a filter that lets only bad news through. The filter protects him from the drop, at the cost of any acknowledgement getting in. What he needs is not more praise.",
            utterance="My advisor said the presentation was good. My first thought was that he hadn't read it properly. The strongest person in our group told me my reasoning was clear and I remember thinking he was just being polite. I know it's odd, I just don't really believe any of it. If you asked me what I'm bad at, I could give you a page."),
    ),
}

CONV_LIB_ORDER_EN = [
    'school_adapt', 'study_efficiency', 'study_disillusion', 'study_pressure',
    'work_adapt', 'career_plan', 'burnout',
    'romance', 'family_conflict', 'social_skills', 'interpersonal_conflict', 'social_anxiety',
    'emotion_reg', 'depression', 'anxiety', 'stress', 'grief',
    'self_explore', 'self_criticism', 'time_mgmt',
]


def case_list_en():
    return [dict(key=k, category=CONV_LIB_EN[k]['category'], blurb=CONV_LIB_EN[k]['blurb'])
            for k in CONV_LIB_ORDER_EN if k in CONV_LIB_EN]


def get_case_en(key):
    return CONV_LIB_EN.get(key)
