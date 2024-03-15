import re

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.eval import Filter
from implementation.conditions.pattern.main import RePattern
from implementation.conditions.semantic.embedding import SemanticCondition

sentences = [
    "I love exploring new restaurants and trying different cuisines when I travel.",
    "The latest smartphone technology is revolutionizing the way we communicate.",
    "Food blogs are great for discovering hidden gems in the culinary world.",
    "Traveling allows me to experience different cultures and cuisines firsthand.",
    "Advancements in medical technology are saving lives every day.",
    "Sampling street food is one of the best parts of traveling to new places.",
    "Virtual reality technology is changing the way we experience entertainment.",
    "Trying out new gadgets is always exciting for tech enthusiasts.",
    "Exploring food markets is a highlight of any travel experience.",
    "The intersection of technology and healthcare is rapidly evolving.",
]

keywords = [
    "food", "travel", "technology"
]

if __name__ == "__main__":
    re_pattern = RePattern(
        pattern=re.compile("|".join(keywords), re.IGNORECASE),
        key="text"
    )
    pipeline = (
        Filter(re_pattern.search, get_key="texts") 
        | Filter(SemanticCondition(
            distance=1,
            targets=["Positive experience"],
            subject_key="text"
        ), get_key="texts")
    )
    
    print(Evaluator(pipeline).run_program({"texts": [
        {"text": s} for s in sentences
    ]}))