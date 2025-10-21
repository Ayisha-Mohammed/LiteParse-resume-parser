# ---------------- FIXTURES --------------

import pytest


@pytest.fixture
def full_resume():
    return """
    Name John Doe
    Phone: +91 9876543210
    Email: john.doe@example.com

    Education
    B.Tech in Computer Science 2020
    M.Tech in AI 2022

    Skills
    Python, Java, SQL, AWS

    Projects
    Resume Parser
    Chatbot
    """


# @pytest.fixture
# def tricky_resume():
#     return """
#     JOHN DOE
#     Contact: 9876543210 | Email: john.doe@example.com

#     M.Tech in Artificial Intelligence 2022
#     B.Tech in Computer Science 2020

#     Skills include Python, java, sql, aws
#     Projects
#     Resume Parser
#     """


@pytest.fixture
def skills_list():
    return ["Python", "Java", "SQL", "AWS"]
