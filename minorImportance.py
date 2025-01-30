"""
Author: Raymond Xu
Date: January 24, 2025
"""

def minor_importance(course_data,minor_data,college,minor,course_code):
    if minor == "AI":
        return importance_AI(course_data,minor_data,course_code)

def importance_AI(course_data,minor_data,course_code):
    score = 0
    tags = {}

    if course_code in minor_data["Machine Learning"]["included"]:
        score += 8
        tags["AI ML"] = "This can be counted as a Machine Learning course for AI minor."

    for reasoning_group in minor_data["Reasoning"]:
        if course_code in reasoning_group:
            score += 8
            tags["AI Reasoning"] = "This can be counted as an AI Reasoning course for AI minor."

    for interaction_group in minor_data["Human-AI Interaction"]:
        if course_code in interaction_group:
            score += 8
            tags["AI Interaction"] = "This can be counted as a Human-AI Interaction course for AI minor."

    if course_code in minor_data["Ethics, Governance & Policy"]["included"]:
        score += 8
        tags["AI Ethics"] = "This can be counted as an Ethics, Governance & Policy course for AI minor."

    if course_code in minor_data["Electives"]["included"]:
        score += 8
        tags["AI Electives"] = "This can be counted as a Elective course for AI minor."

    return score,tags
