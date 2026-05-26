from typing import Dict, List
from data.assessment_questions import ASSESSMENT_CATEGORIES, AssessmentQuestion, AssessmentCategory


def should_skip_question(
    question: AssessmentQuestion,
    category: AssessmentCategory,
    responses: Dict[str, Dict],
) -> bool:
    if question.is_screening:
        return False
    all_answered = all(sid in responses for sid in category.screening_question_ids)
    if not all_answered:
        return False
    return all(responses[sid].get('rating', 1) == 0 for sid in category.screening_question_ids)


def build_active_question_list(responses: Dict[str, Dict]) -> List[Dict]:
    result = []
    for category in ASSESSMENT_CATEGORIES:
        for question in category.questions:
            skipped = should_skip_question(question, category, responses)
            result.append({'category': category, 'question': question, 'skipped': skipped})
    return result


def get_active_questions(responses: Dict[str, Dict]) -> List[Dict]:
    return [item for item in build_active_question_list(responses) if not item['skipped']]


def calculate_symptom_summaries(responses: Dict[str, Dict]) -> List[Dict]:
    summaries = []
    for category in ASSESSMENT_CATEGORIES:
        screening_responses = [
            responses[sid] for sid in category.screening_question_ids if sid in responses
        ]
        all_screening_zero = (
            len(screening_responses) == len(category.screening_question_ids)
            and all(r.get('rating', 1) == 0 for r in screening_responses)
        )
        non_screening_qs = [q for q in category.questions if not q.is_screening]
        any_followup_answered = any(q.id in responses for q in non_screening_qs)
        was_skipped = all_screening_zero and bool(non_screening_qs) and not any_followup_answered

        category_responses = [responses[q.id] for q in category.questions if q.id in responses]

        if not category_responses and not was_skipped:
            continue

        if was_skipped:
            summaries.append({
                'category': category.name,
                'severity': 'No',
                'score': 0,
                'max_score': len(category.questions) * 3,
                'skipped': True,
            })
            continue

        total = sum(r.get('rating', 0) for r in category_responses)
        max_score = len(category_responses) * 3

        if max_score == 0 or total == 0:
            severity = 'No'
        else:
            avg = total / (max_score / 3)
            if avg <= 1:
                severity = 'Mild'
            elif avg <= 2:
                severity = 'Moderate'
            else:
                severity = 'Severe'

        summaries.append({
            'category': category.name,
            'severity': severity,
            'score': total,
            'max_score': max_score,
            'skipped': False,
        })
    return summaries


def get_main_diagnosis(summaries: List[Dict]) -> str:
    active = [s for s in summaries if not s['skipped']]
    severe = [s for s in active if s['severity'] == 'Severe']
    if severe:
        return severe[0]['category']
    moderate = [s for s in active if s['severity'] == 'Moderate']
    if moderate:
        return moderate[0]['category']
    return 'No significant symptoms detected'
