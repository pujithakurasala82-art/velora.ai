
from collections import defaultdict
from backend.utils import score_pct

INTEREST_QUESTIONS = [
    ("Which activity sounds most interesting?", ["Building a website", "Investigating a security alert", "Analyzing a dataset", "Designing a visual"], [3,4,5,2]),
    ("Which problem would you enjoy solving?", ["Finding why a system failed", "Understanding customer data", "Creating an app", "Planning a business"], [5,4,3,2]),
    ("Which subject area attracts you most?", ["Computer networks", "Mathematics and statistics", "Programming", "Business and management"], [5,4,3,2]),
    ("Which task sounds satisfying?", ["Spotting unusual activity", "Finding patterns in data", "Writing code", "Presenting ideas"], [5,4,3,2]),
    ("Which environment sounds best?", ["Security operations center", "Data/analytics team", "Software team", "Creative studio"], [5,4,3,2]),
    ("What would you rather learn?", ["Ethical security concepts", "Data visualization", "Application development", "UI/UX design"], [5,4,3,2]),
    ("Which challenge appeals to you?", ["Protecting systems", "Predicting trends", "Automating a task", "Improving a user experience"], [5,4,3,2]),
    ("Which tool category interests you?", ["SIEM/security tools", "Spreadsheets/BI tools", "Code editors", "Design tools"], [5,4,3,2]),
    ("Which outcome feels most rewarding?", ["Stopping a threat", "Explaining a data trend", "Launching software", "Creating a polished design"], [5,4,3,2]),
    ("Which career area would you explore first?", ["Cybersecurity", "Data analytics", "Software engineering", "Product/design"], [5,4,3,2]),
]

APTITUDE_QUESTIONS = [
    {"q":"If 20% of 150 students choose a course, how many students is that?","options":["20","25","30","35"],"answer":2,"category":"Quantitative"},
    {"q":"A ratio is 2:3. If the first part is 20, what is the second?","options":["25","30","35","40"],"answer":1,"category":"Quantitative"},
    {"q":"What comes next: 2, 4, 8, 16, ?","options":["20","24","32","36"],"answer":2,"category":"Logical"},
    {"q":"What comes next: 3, 6, 11, 18, ?","options":["25","27","29","31"],"answer":1,"category":"Logical"},
    {"q":"If all A are B and all B are C, which is true?","options":["All C are A","All A are C","No A are C","Some C are not B"],"answer":1,"category":"Logical"},
    {"q":"A project has 4 tasks. Each takes 3 hours. How many task-hours are needed?","options":["7","10","12","16"],"answer":2,"category":"Quantitative"},
    {"q":"A value increases from 80 to 100. What is the percentage increase?","options":["20%","25%","30%","40%"],"answer":1,"category":"Quantitative"},
    {"q":"Which number is the odd one out? 4, 9, 16, 20, 25","options":["4","9","20","25"],"answer":2,"category":"Logical"},
    {"q":"If Monday is day 1, what day is day 10?","options":["Tuesday","Wednesday","Thursday","Friday"],"answer":1,"category":"Analytical"},
    {"q":"A team has 12 members. 1/3 are assigned to testing. How many?","options":["3","4","5","6"],"answer":1,"category":"Quantitative"},
]

WORKSTYLE_QUESTIONS = [
    ("When a difficult task appears, you usually...", ["Break it into smaller parts", "Ask others for ideas", "Try several creative approaches", "Start immediately and adapt"], "Analytical"),
    ("In a team, you naturally...", ["Check details", "Coordinate people", "Generate ideas", "Keep the group moving"], "Teamwork"),
    ("When learning something new, you prefer...", ["Understanding how it works", "Discussing it", "Experimenting", "Following a practical example"], "Curiosity"),
    ("When plans change, you...", ["Analyze the new situation", "Discuss the impact", "Look for a new possibility", "Quickly adjust"], "Adaptability"),
    ("You enjoy work that requires...", ["Precision", "Communication", "Creativity", "Action"], "WorkStyle"),
    ("When solving a problem, you value...", ["Evidence", "Different viewpoints", "Novel solutions", "Speed"], "ProblemSolving"),
    ("A good project outcome means...", ["Correct and reliable work", "Strong collaboration", "An innovative result", "A practical result"], "WorkStyle"),
    ("You are most motivated by...", ["Complex problems", "Helping a team", "Creating something new", "Achieving a clear goal"], "Motivation"),
    ("You prefer instructions that are...", ["Detailed", "Discussable", "Flexible", "Goal-oriented"], "WorkStyle"),
    ("When you make a mistake, you...", ["Find the root cause", "Ask for feedback", "Try a different method", "Fix it and continue"], "Adaptability"),
]

def grade_mcq(questions, answers):
    category = defaultdict(lambda: [0,0])
    correct = 0
    for i, q in enumerate(questions):
        selected = answers.get(str(i))
        category[q["category"]][1] += 1
        if selected == q["answer"]:
            correct += 1
            category[q["category"]][0] += 1
    cats = {k: score_pct(v[0], v[1]) for k,v in category.items()}
    return {"correct": correct, "total": len(questions), "percentage": score_pct(correct, len(questions)), "categories": cats}

def grade_interest(answers):
    # Interest options are scored toward a technology/security/data/design profile.
    buckets = defaultdict(int)
    for i, selected in enumerate(answers):
        if selected is None: continue
        score = INTEREST_QUESTIONS[i][3][selected]
        option = INTEREST_QUESTIONS[i][1][selected].lower()
        if any(x in option for x in ["security","network","threat","siem","protecting"]):
            buckets["Cybersecurity"] += score
        elif any(x in option for x in ["data","analytics","dataset","statistics","trend","bi"]):
            buckets["Data"] += score
        elif any(x in option for x in ["website","app","programming","code","software","automating"]):
            buckets["Software"] += score
        else:
            buckets["Design/Business"] += score
    max_score = len(INTEREST_QUESTIONS) * 5
    return {k: round(v/max_score*100,1) for k,v in buckets.items()}

def grade_workstyle(answers):
    scores = defaultdict(int)
    for i, selected in enumerate(answers):
        if selected is None: continue
        _, _, dimension = WORKSTYLE_QUESTIONS[i]
        scores[dimension] += selected + 1
    max_per_dim = {}
    for _, _, dim in WORKSTYLE_QUESTIONS:
        max_per_dim[dim] = max_per_dim.get(dim, 0) + 4
    return {k: round(v/max_per_dim[k]*100,1) for k,v in scores.items()}
