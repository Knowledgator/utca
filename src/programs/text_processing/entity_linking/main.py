from typing import Dict, Any, cast

# from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.schema import Transformable
from implementation.tasks.text_processing.entity_linking.transformers.transformers_entity_linking import (
    EntityLinkingTask
)

# Sentences for dataset
sentences = [
    "People who test positive for Covid-19 no longer need to routinely stay away from others for at least five days, according to new guidelines from the US Centers for Disease Control and Prevention issued Friday.", 
    "The change ends a strategy from earlier in the pandemic that experts said has been important to controlling the spread of the infection.",
    "Whether it be the latest prized Stanley cup or that 10-year-old plastic spout bottle you don’t go anywhere without, “emotional support water bottles” seem to be stuck to our sides and not going anywhere.",
    "Health officials in Alaska recently reported the first known human death from a virus called Alaskapox.",
    "Blizzard conditions continued to slam Northern California over the weekend with damaging winds and heavy snow dumping on mountain ridges down to the valleys.",
]


if __name__ == "__main__":
    task = EntityLinkingTask(
        labels=["positive", "negative", "neutral"]
    )
    res = cast(Dict[str, Any], task.execute(Transformable({
        "num_beams": 2,
        "texts": sentences,
        "num_return_sequences": 2
    })).extract())
    print(res)