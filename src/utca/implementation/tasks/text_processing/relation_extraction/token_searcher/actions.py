from typing import Any, Dict, List, Set, Generator, Optional, Tuple

from utca.core.executable_level_1.actions import Action
from utca.implementation.predictors.token_searcher.utils import (
    build_entity
)

class TokenSearcherRelationExtractionPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Create prompts with provided text

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "text" (str): Text to process;

            "relations" (List[Relation]): Relations parameters;

            "entities" (List[ClassifiedEntity]): Entities to use;

    Returns:
        Dict[str, Any]: Expected keys:
            "source_entities" (List[ClassifiedEntity]): Source entities to use;

            "relations_labels" (List[str]): Corresponding relations labels;

            "inputs" (List[str]): Model inputs;
            
            "prompt_lengths" (List[int]): Prompt lenghts. Used by postprocessor;
    """

    prompt: str = """
Identify target entity given the following realtion: "{relation}" and the following source entity: "{entity}"

Text:
"""
    def create_prompt(self, span: str, relation: str):
        return self.prompt.format(relation=relation, entity=span)
    

    def get_expected_start_labels(
        self, relations: List[Dict[str, Any]]
    ) -> Dict[str, Optional[Set[str]]]:
        return {
            r["relation"]: (
                {i[0] for i in pf}
                if (pf := r.get("pairs_filter")) 
                else None
            )
            for r in relations
        }

    
    def get_source_entities(
        self, 
        expected_starts: Dict[str, Optional[Set[str]]],
        entities: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        return [
            e
            for starts in expected_starts.values()
            for e in entities
            if not starts or e["entity"] in starts
        ]
    

    def get_prompts(
        self,
        expected_starts: Dict[str, Optional[Set[str]]],
        entities: List[Dict[str, Any]],
    ) -> List[str]:
        return [
            self.create_prompt(e["span"], rel)
            for rel, starts in expected_starts.items()
            for e in entities
            if not starts or e["entity"] in starts
        ]
    

    def get_prompts_lengths(self, prompts: List[str]) -> List[int]:
        return [
            len(p) for p in prompts
        ]
    

    def get_relations(
        self,
        expected_starts: Dict[str, Optional[Set[str]]],
        entities: List[Dict[str, Any]],
    ) -> List[str]:
        return [
            rel
            for rel, starts in expected_starts.items()
            for e in entities
            if not starts or e["entity"] in starts
        ]


    def get_inputs(self, prompts: List[str], text: str) -> List[str]:
        return [
            p + text for p in prompts
        ]


    def prepare_inputs(
        self, 
        text: str, 
        relations: List[Dict[str, Any]],
        entities: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        expected_starts = self.get_expected_start_labels(relations)
        prompts = self.get_prompts(expected_starts, entities)
        return {
            "source_entities": self.get_source_entities(expected_starts, entities),
            "relations_labels": self.get_relations(expected_starts, entities),
            "inputs": self.get_inputs(prompts, text),
            "prompt_lengths": self.get_prompts_lengths(prompts),
        }

    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "text" (str): Text to process;

                "relations" (List[Relation]): Relations parameters;

                "entities" (List[ClassifiedEntity]): Entities to use;

        Returns:
            Dict[str, Any]: Expected keys:
                "source_entities" (List[ClassifiedEntity]): Source entities to use;

                "relations_labels" (List[str]): Corresponding relations labels;

                "inputs" (List[str]): Model inputs;
                
                "prompt_lengths" (List[int]): Prompt lenghts. Used by postprocessor;
        """
        return self.prepare_inputs(
            text = input_data["text"],
            relations = input_data["relations"],
            entities = input_data["entities"]
        )


class TokenSearcherRelationExtractionPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Format output

    Arguments:
        input_data (Dict[str, Any]): Expected keys:
            "text" (str): Processed text;

            "output" (List[List[Dict[str, Any]]]): Model output; 

            "relations" (List[Relation]): Relations parameters;

            "source_entities" (List[ClassifiedEntity]): Used source entities;

            "relations_labels" (List[str]): Corresponding relations labels;
            
            "entities" (List[ClassifiedEntity]): Entities to use;

            "prompt_lengths" (List[int]): Prompt lenghts;
            
    Returns:
        Dict[str, Any]: Expected keys:
            "output" (List[Triplets]): Extracted relations;
    """
    def __init__(
        self, 
        threshold: float=0.,
        name: Optional[str]=None,
    ) -> None:
        """
        Arguments:
            threshold (float): Relations threshold score. Defaults to 0.
            
            name (Optional[str], optional): Name for identification. If equals to None,
                class name will be used. Defaults to None.      
        """
        super().__init__(name)
        self.threshold = threshold


    def get_expected_end_labels(
        self, relations: List[Dict[str, Any]]
    ) -> Dict[str, Optional[Set[str]]]:
        return {
            r["relation"]: (
                {i[1] for i in pf}
                if (pf := r.get("pairs_filter")) 
                else None
            )
            for r in relations
        }


    def get_target_entities(
        self, 
        expected_ends: Dict[str, Optional[Set[str]]],
        entities: List[Dict[str, Any]],
    ) -> Dict[str, Optional[List[Dict[str, Any]]]]:
        return {
            rel: [
                e for e in entities
                if not ends or e["entity"] in ends
            ]
            for rel, ends in expected_ends.items()
        }


    def process_target_entity(
        self, 
        e: Dict[str, Any], 
        targets: Optional[List[Dict[str, Any]]],
        shift: int,
        text: str,
    ) -> Optional[Dict[str, Any]]:
        tmp_target = {
            **build_entity(
                text, e, 0, "other", -shift
            ).__dict__,
            "score": 1
        }
        if not targets:
            return None
        
        for t in targets:
            if t["start"] <= tmp_target["start"] and t["end"] >= tmp_target["end"]:
                return t
        return None


    def validate_labels(
        self, 
        e1: Dict[str, Any],
        e2: Dict[str, Any],
        pairs: Optional[List[Tuple[str, str]]]
    ) -> bool:
        if pairs is None:
            return True
        for p in pairs:
            if (
                p[0] == e1["entity"]
                and p[1] == e2["entity"]
            ):
                return True
        return False


    def validate_distance(
        self, 
        e1: Dict[str, Any],
        e2: Dict[str, Any],
        distance_threshold: int
    ) -> bool:
        if distance_threshold < 0:
            return True
        return (
            abs(e1["end"] - e2["start"]) <= distance_threshold
            or abs(e2["end"] - e1["start"]) <= distance_threshold
        )


    def extract_relations(
        self,
        text: str, 
        relations: List[Dict[str, Any]],
        entities: List[Dict[str, Any]],
        sources: List[Dict[str, Any]],
        relations_labels: List[str],
        targets: List[List[Dict[str, Any]]],
        prompt_lengths: List[int]
    ) -> Generator[Dict[str, Any], None, None]:
        target_entities = self.get_target_entities(
            self.get_expected_end_labels(relations),
            entities,
        )

        relations_by_name = {
            r["relation"]: r for r in relations
        }

        for s, r, ts, pl in zip(sources, relations_labels, targets, prompt_lengths):
            for ti in ts:
                if ((t := self.process_target_entity(
                        ti, target_entities[r], pl, text,
                    )) 
                    and ti["score"] >= self.threshold 
                    and self.validate_labels(s, t, relations_by_name[r]["pairs_filter"])
                    and self.validate_distance(
                        s, t, relations_by_name[r]["distance_threshold"]
                    )
                ):
                    yield {
                        "source": s,
                        "relation": r,
                        "target": t,
                        "score": ti["score"]
                    }
                

    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Arguments:
            input_data (Dict[str, Any]): Expected keys:
                "text" (str): Processed text;

                "output" (List[List[Dict[str, Any]]]): Model output; 

                "relations" (List[Relation]): Relations parameters;

                "source_entities" (List[ClassifiedEntity]): Used source entities;

                "relations_labels" (List[str]): Corresponding relations labels;
                
                "entities" (List[ClassifiedEntity]): Entities to use;

                "prompt_lengths" (List[int]): Prompt lenghts;

        Returns:
            Dict[str, Any]: Expected keys:
                "output" (List[Triplets]): Extracted relations;
        """
        return {
            "output": list(self.extract_relations(
                text = input_data["text"],
                relations = input_data["relations"],
                entities = input_data["entities"],
                sources = input_data["source_entities"],
                relations_labels = input_data["relations_labels"],
                targets = input_data["output"],
                prompt_lengths = input_data["prompt_lengths"],
            ))
        }