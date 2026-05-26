from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class AssessmentQuestion:
    id: str
    category: str
    question: str
    rating_type: str  # 'severity' | 'alcohol' | 'drug' | 'personality' | 'stress' | 'yesno'
    sub_questions: List[str] = field(default_factory=list)
    is_screening: bool = False
    clinician_note: Optional[str] = None

@dataclass
class AssessmentCategory:
    id: str
    name: str
    icon: str
    questions: List[AssessmentQuestion]
    screening_question_ids: List[str]

SEVERITY_RATINGS = [
    {"value": 0, "label": "None",     "description": "No evidence of presence of symptom"},
    {"value": 1, "label": "Mild",     "description": "Symptom present and mildly distressing or disabling"},
    {"value": 2, "label": "Moderate", "description": "Symptom present and moderately distressing or disabling"},
    {"value": 3, "label": "Severe",   "description": "Symptom present and severely distressing or disabling"},
]

ALCOHOL_RATINGS = [
    {"value": 0, "label": "None",      "description": "Doesn't drink or drinks only socially occasionally"},
    {"value": 1, "label": "Social",    "description": "Regular social drinking"},
    {"value": 2, "label": "Harmful",   "description": "Clear evidence of drinking with harmful effects"},
    {"value": 3, "label": "Dependent", "description": "Significant drink problem with dependence"},
]

DRUG_RATINGS = [
    {"value": 0, "label": "None",      "description": "No evidence of any drug misuse"},
    {"value": 1, "label": "Occasional","description": "Occasional use of illicit drugs"},
    {"value": 2, "label": "Frequent",  "description": "Frequent use of illicit drugs"},
    {"value": 3, "label": "Dependent", "description": "Significant use with dependence and complications"},
]

STRESS_RATINGS = [
    {"value": 0, "label": "None",     "description": "No stress"},
    {"value": 1, "label": "Mild",     "description": "Mild degree of stress"},
    {"value": 2, "label": "Moderate", "description": "Moderate degree of stress"},
    {"value": 3, "label": "Severe",   "description": "Severe degree of stress"},
]

ASSESSMENT_CATEGORIES: List[AssessmentCategory] = [
    # 1. WORRIES
    AssessmentCategory(
        id='worries', name='Worries', icon='😟',
        screening_question_ids=['worries_main'],
        questions=[
            AssessmentQuestion(
                id='worries_main', category='Worries',
                question="Do you tend to worry a lot?",
                sub_questions=[
                    "What kind of things do you worry about?",
                    "What about money or family problems, your own health or someone else's health?",
                ],
                rating_type='severity', is_screening=True,
            ),
        ]
    ),
    # 2. ANXIETY
    AssessmentCategory(
        id='anxiety', name='Anxiety', icon='😰',
        screening_question_ids=['anxiety_screen'],
        questions=[
            AssessmentQuestion(
                id='anxiety_screen', category='Anxiety',
                question="Do you get frightened or nervous for no apparent reason?",
                rating_type='severity', is_screening=True,
            ),
            AssessmentQuestion(
                id='anxiety_panic', category='Anxiety — Panic',
                question="Do you get sudden episodes of intense fear or panic attacks?",
                sub_questions=[
                    "Do you get palpitations?",
                    "Sweating?",
                    "Trembling or shaking?",
                    "Restless feelings in the stomach?",
                ],
                rating_type='severity',
            ),
        ]
    ),
    # 3. CONCENTRATION
    AssessmentCategory(
        id='concentration', name='Concentration', icon='🧠',
        screening_question_ids=['concentration_main'],
        questions=[
            AssessmentQuestion(
                id='concentration_main', category='Concentration',
                question="How is your concentration?",
                sub_questions=[
                    "Can you concentrate on talking to someone, or listening to the radio, watching TV, or reading?",
                ],
                rating_type='severity', is_screening=True,
            ),
        ]
    ),
    # 4. DEPRESSION
    AssessmentCategory(
        id='depression', name='Depression', icon='😔',
        screening_question_ids=['depressed_mood', 'loss_of_interest'],
        questions=[
            AssessmentQuestion(
                id='depressed_mood', category='Depressed Mood',
                question="Have you been sad or depressed recently?",
                sub_questions=[
                    "Have you cried at all or felt like crying?",
                    "Is the depression there most of the time or just a few hours?",
                ],
                rating_type='severity', is_screening=True,
            ),
            AssessmentQuestion(
                id='loss_of_interest', category='Loss of Interest',
                question="Have you lost interest in things you used to enjoy?",
                sub_questions=["What have you enjoyed doing recently?"],
                rating_type='severity', is_screening=True,
            ),
            AssessmentQuestion(
                id='sleep', category='Sleep',
                question="Have you had trouble sleeping recently?",
                sub_questions=[
                    "Do you have difficulties falling asleep?",
                    "Do you wake up early in the morning and cannot get back to sleep?",
                    "Have you been sleeping more than usual?",
                ],
                rating_type='severity',
            ),
            AssessmentQuestion(
                id='appetite', category='Appetite',
                question="What has your appetite been like?",
                sub_questions=[
                    "Do you enjoy your food?",
                    "Have you been eating more or less than usual?",
                ],
                rating_type='severity',
            ),
            AssessmentQuestion(
                id='suicidal_ideation', category='Suicidal Ideation',
                question="Have you had thoughts of harming yourself or ending your life?",
                sub_questions=[
                    "Have you felt that life is not worth living?",
                    "Have you made any plans or attempts?",
                ],
                rating_type='severity',
                clinician_note=(
                    "IMPORTANT: This is a critical safety question. Rate carefully. "
                    "Any score ≥1 requires immediate clinical action."
                ),
            ),
        ]
    ),
    # 5. EATING DISORDERS
    AssessmentCategory(
        id='eating', name='Eating Disorders', icon='🍽️',
        screening_question_ids=['eating_concern'],
        questions=[
            AssessmentQuestion(
                id='eating_concern', category='Eating Concern',
                question="Are you unduly concerned about eating fattening food?",
                sub_questions=[
                    "Differentiate between normal/general concern and excessive, distressing concern.",
                ],
                rating_type='severity', is_screening=True,
                clinician_note="Rate only excessive concern, not healthy interest in diet.",
            ),
            AssessmentQuestion(
                id='body_image', category='Body Image',
                question="Do you believe yourself to be fat when others say you are too thin?",
                rating_type='severity',
            ),
        ]
    ),
    # 6. HEALTH ANXIETY
    AssessmentCategory(
        id='health_anxiety', name='Health Anxiety', icon='🏥',
        screening_question_ids=['hypochondriasis'],
        questions=[
            AssessmentQuestion(
                id='hypochondriasis', category='Health Anxiety',
                question="Do you worry a lot about your health or having a serious illness?",
                sub_questions=[
                    "Is there anything about your body which bothers or upsets you?",
                    "Are you in pain?",
                    "Is any part of your body not working properly?",
                ],
                rating_type='severity', is_screening=True,
            ),
        ]
    ),
    # 7. OCD
    AssessmentCategory(
        id='ocd', name='Obsessive Compulsive', icon='🔄',
        screening_question_ids=['obsessions'],
        questions=[
            AssessmentQuestion(
                id='obsessions', category='Obsessions / Compulsions',
                question="Do you have to check things over and over again, or repeat actions?",
                sub_questions=[
                    "For example, whether you have turned off taps, gas, lights, or locked your door?",
                    "Do you wash your hands repeatedly?",
                    "Do unwanted, distressing thoughts come into your head and won't go away?",
                ],
                rating_type='severity', is_screening=True,
            ),
        ]
    ),
    # 8. PHOBIAS
    AssessmentCategory(
        id='phobia', name='Phobias', icon='😱',
        screening_question_ids=['phobia_screen'],
        questions=[
            AssessmentQuestion(
                id='phobia_screen', category='Phobias',
                question="Do you have fears that you know are unreasonable but cannot control?",
                sub_questions=[
                    "Like being afraid of crowds, going out alone, or using public transport?",
                    "Do you have any other specific fears — animals, heights, blood?",
                ],
                rating_type='severity', is_screening=True,
            ),
        ]
    ),
    # 9. MANIA
    AssessmentCategory(
        id='mania', name='Manic Behaviour', icon='⚡',
        screening_question_ids=['mania_energy'],
        questions=[
            AssessmentQuestion(
                id='mania_energy', category='Mania — Energy',
                question="Has there been a period recently when you felt unusually energetic or needed less sleep?",
                rating_type='severity', is_screening=True,
            ),
            AssessmentQuestion(
                id='mania_mood', category='Mania — Elevated Mood',
                question="Have you been feeling very happy or elated recently for no apparent reason?",
                sub_questions=[
                    "Observe for: disinhibited social behaviour, grandiose beliefs, excessive talking, racing thoughts.",
                ],
                rating_type='severity',
                clinician_note="Observe carefully for disinhibition, pressure of speech, and grandiosity during the interview.",
            ),
        ]
    ),
    # 10. PSYCHOSIS
    AssessmentCategory(
        id='psychosis', name='Psychosis', icon='🌀',
        screening_question_ids=['thought_disorder'],
        questions=[
            AssessmentQuestion(
                id='thought_disorder', category='Thought Disorder',
                question="Can you think clearly? Do your thoughts get muddled or mixed up?",
                sub_questions=[
                    "Observe for disorganised, tangential, or illogical thinking during the interview.",
                ],
                rating_type='severity', is_screening=True,
                clinician_note="Observe the patient's speech and thought process throughout the interview.",
            ),
            AssessmentQuestion(
                id='delusions', category='Delusions',
                question=(
                    "Do you believe that people are talking about you, laughing at you, "
                    "or that TV/radio refers specifically to you?"
                ),
                sub_questions=[
                    "Do you have any unusual ideas or beliefs that others find hard to understand?",
                    "For example, do you feel people are going to harm you?",
                ],
                rating_type='severity',
            ),
            AssessmentQuestion(
                id='auditory_hallucinations', category='Auditory Hallucinations',
                question="Do you hear things that other people cannot hear — like voices when no one is about?",
                sub_questions=["What do the voices say?", "How often does this happen?"],
                rating_type='severity',
            ),
            AssessmentQuestion(
                id='visual_hallucinations', category='Visual Hallucinations',
                question="Do you see things or visions that are invisible to other people?",
                sub_questions=["How often does this happen?"],
                rating_type='severity',
            ),
        ]
    ),
    # 11. DISORIENTATION
    AssessmentCategory(
        id='disorientation', name='Disorientation', icon='🧭',
        screening_question_ids=['time_orientation'],
        questions=[
            AssessmentQuestion(
                id='time_orientation', category='Time Orientation',
                question="Some people when unwell lose track of time. Can you tell me today's date?",
                sub_questions=[
                    "What day of the week is it?",
                    "What month is it?",
                    "What year is it?",
                    "Where are we right now?",
                ],
                rating_type='severity', is_screening=True,
                clinician_note="Ask date, day, month, year, and place. Rate based on number of errors.",
            ),
        ]
    ),
    # 12. MEMORY
    AssessmentCategory(
        id='memory', name='Memory', icon='💭',
        screening_question_ids=['memory_main'],
        questions=[
            AssessmentQuestion(
                id='memory_main', category='Memory',
                question="Have you had any difficulties with your memory?",
                sub_questions=[
                    "Is that a problem for you in daily life?",
                    "Do you forget recent events more than past ones?",
                ],
                rating_type='severity', is_screening=True,
            ),
        ]
    ),
    # 13. ALCOHOL
    AssessmentCategory(
        id='alcohol', name='Alcohol Use', icon='🍷',
        screening_question_ids=['alcohol_main'],
        questions=[
            AssessmentQuestion(
                id='alcohol_main', category='Alcohol',
                question="May I ask about your drinking habits? How much alcohol do you drink?",
                sub_questions=[
                    "Do you have a strong urge or craving to drink every day?",
                    "Can you stop after one or two drinks?",
                    "Has the amount you drink increased over time?",
                    "Have you experienced shaking, sweating, or anxiety when not drinking?",
                ],
                rating_type='alcohol', is_screening=True,
            ),
        ]
    ),
    # 14. DRUGS
    AssessmentCategory(
        id='drugs', name='Drug Use', icon='💊',
        screening_question_ids=['drugs_main'],
        questions=[
            AssessmentQuestion(
                id='drugs_main', category='Drugs',
                question="Do you take any drugs not prescribed by your doctor?",
                sub_questions=[
                    "What kind of drugs?",
                    "How much and how often do you take them?",
                    "Do you suffer withdrawal symptoms if you stop?",
                ],
                rating_type='drug', is_screening=True,
            ),
        ]
    ),
    # 15. PERSONALITY
    AssessmentCategory(
        id='personality', name='Personality', icon='🎭',
        screening_question_ids=['personality_main'],
        questions=[
            AssessmentQuestion(
                id='personality_main', category='Personality',
                question=(
                    "Have you had long-standing problems in the way you behave towards others, "
                    "causing difficulties?"
                ),
                sub_questions=[
                    "Problems in relationships, at work, or with the law?",
                    "Has that been going on since you were young?",
                    "Has it continued throughout your life?",
                ],
                rating_type='severity', is_screening=True,
                clinician_note=(
                    "This should reflect enduring patterns from early adulthood, not just recent behaviour."
                ),
            ),
        ]
    ),
    # 16. STRESSORS
    AssessmentCategory(
        id='stress', name='Stressors', icon='😓',
        screening_question_ids=['stress_main'],
        questions=[
            AssessmentQuestion(
                id='stress_main', category='Stressors',
                question=(
                    "Have you experienced any significant stress or traumatic events "
                    "around the time your problems started?"
                ),
                sub_questions=[
                    "Has anyone close to you died?",
                    "Break-up of a relationship?",
                    "Serious accident or illness?",
                    "Any other stressful life event?",
                ],
                rating_type='stress', is_screening=True,
            ),
        ]
    ),
]


def get_ratings_for_type(rating_type: str) -> list:
    if rating_type == 'alcohol':
        return ALCOHOL_RATINGS
    if rating_type == 'drug':
        return DRUG_RATINGS
    if rating_type == 'stress':
        return STRESS_RATINGS
    return SEVERITY_RATINGS


def get_all_questions():
    return [q for cat in ASSESSMENT_CATEGORIES for q in cat.questions]
