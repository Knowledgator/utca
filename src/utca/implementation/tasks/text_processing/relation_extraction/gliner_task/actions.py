from typing import Any, Dict, List, Set, Optional, Tuple, Generator, cast

from utca.core.executable_level_1.actions import Action

class GLiNERRelationExtractionPreprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Create labels for relation extraction

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "relations" (List[Relation]): Relations parameters;

            "entities" (List[ClassifiedEntity]): Entities to use;

    Returns:
        Dict[str, Any]: Expected keys:
            "labels" (List[str]): Labels model inputs;
    """
    def create_label(self, span: str, relation: str) -> str:
        return f"{span} <> {relation}"
        
    
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
    

    def get_labels(
        self,
        expected_starts: Dict[str, Optional[Set[str]]],
        entities: List[Dict[str, Any]],
    ) -> List[str]:
        return [
            self.create_label(e["span"], rel)
            for rel, starts in expected_starts.items()
            for e in entities
            if not starts or e["entity"] in starts
        ]


    def prepare_inputs(
        self, 
        relations: List[Dict[str, Any]],
        entities: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        expected_starts = self.get_expected_start_labels(relations)
        return {
            "labels": self.get_labels(expected_starts, entities)
        }

    
    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "relations" (List[Relation]): Relations parameters;

                "entities" (List[ClassifiedEntity]): Entities to use;

        Returns:
            Dict[str, Any]: Expected keys:
                "labels" (List[str]): Labels model inputs;
        """
        return self.prepare_inputs(
            relations = input_data["relations"],
            entities = input_data["entities"]
        )


class GLiNERRelationExtractionPostprocessor(Action[Dict[str, Any], Dict[str, Any]]):
    """
    Format output

    Args:
        input_data (Dict[str, Any]): Expected keys:
            "output" (List[List[Dict[str, Any]]]): Model output; 

            "relations" (List[Relation]): Relations parameters;

            "entities" (List[ClassifiedEntity]): Entities to use;

            "chunks_starts" (List[int]): Chunks starts;
    Returns:
        Dict[str, Any]: Expected keys:
            "output" (List[Triplets]): Extracted relations;
    """
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


    def process_target_entity(
        self, 
        e: Dict[str, Any], 
        targets: Optional[List[Dict[str, Any]]],
        shift: int,
    ) -> Optional[Dict[str, Any]]:
        if not targets:
            return None
        
        start = e["start"] - shift
        end = e["end"] - shift
        for t in targets:
            if t["start"] <= start and t["end"] >= end:
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


    def get_source_and_relation(self, label: str) -> Tuple[str, str]:
        return cast(Tuple[str, str], tuple(label.split(" <> ", 1)))


    def get_entities_by_span(
        self, span: str, entities: List[Dict[str, Any]]
    ) -> Generator[Dict[str, Any], None, None]:
        for e in entities:
            if e["span"] == span:
                yield e


    def extract_relations(
        self,
        relations: List[Dict[str, Any]],
        entities: List[Dict[str, Any]],
        targets: List[List[Dict[str, Any]]],
        chunk_starts: List[int],
    ) -> Generator[Dict[str, Any], None, None]:
        relations_by_name = {
            r["relation"]: r for r in relations
        }
        for id, output in enumerate(targets):
            shift = chunk_starts[id]
            for ent in output:
                source_span, r = self.get_source_and_relation(ent['label'])
                ss = self.get_entities_by_span(source_span, entities)
                t = self.process_target_entity(ent, entities, shift)
                if not t:
                    continue
                for s in ss:
                    if (
                        self.validate_labels(s, t, relations_by_name[r]["pairs_filter"])
                        and self.validate_distance(
                            s, t, relations_by_name[r]["distance_threshold"]
                        )
                    ):
                        yield {
                            "source": s,
                            "relation": r,
                            "target": t,
                            "score": ent["score"]
                        }


    def execute(
        self, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Args:
            input_data (Dict[str, Any]): Expected keys:
                "output" (List[List[Dict[str, Any]]]): Model output; 

                "relations" (List[Relation]): Relations parameters;

                "entities" (List[ClassifiedEntity]): Entities to use;

                "chunks_starts" (List[int]): Chunks starts;
        Returns:
            Dict[str, Any]: Expected keys:
                "output" (List[Triplets]): Extracted relations;
        """
        return {
            "output": list(self.extract_relations(
                relations = input_data["relations"],
                entities = input_data["entities"],
                targets = input_data["output"],
                chunk_starts=input_data["chunks_starts"],
            ))
        }