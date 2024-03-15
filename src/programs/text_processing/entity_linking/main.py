from typing import Any, Dict, List

from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.eval import ForEach, ExecutionSchema
from core.executable_level_1.actions import ExecuteFunction
from implementation.tasks.text_processing.entity_linking.transformers.transformers_entity_linking import (
    EntityLinkingTask
)
from implementation.tasks.text_processing.text_classification.comprehend_it.comprehend_it import (
    ComprehendIt
)

# Sentences for dataset
sentences = [
    "People who test positive for Covid-19 no longer need to routinely stay away from others for at least five days, according to new guidelines from the US Centers for Disease Control and Prevention issued Friday.", 
    "The change ends a strategy from earlier in the pandemic that experts said has been important to controlling the spread of the infection.",
    "Whether it be the latest prized Stanley cup or that 10-year-old plastic spout bottle you don’t go anywhere without, “emotional support water bottles” seem to be stuck to our sides and not going anywhere.",
    "Health officials in Alaska recently reported the first known human death from a virus called Alaskapox.",
    "Blizzard conditions continued to slam Northern California over the weekend with damaging winds and heavy snow dumping on mountain ridges down to the valleys.",
]

def prepare_to_rescore(input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {
            "text": sentence,
            "labels": [l[0] for l in labels]
        } for sentence, labels in zip(sentences, input_data["classification_output"])
    ]

if __name__ == "__main__":
    pipeline = (
        EntityLinkingTask(
            labels=["positive", "negative", "neutral"]
        )
        | ExecuteFunction(prepare_to_rescore).use(set_key="inputs")
        | ForEach(ExecutionSchema(ComprehendIt()), get_key="inputs")
    )

    res = Evaluator(pipeline).run_program({
        "num_beams": 2,
        "texts": sentences,
        "num_return_sequences": 2
    })
    print(res)