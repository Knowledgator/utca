from typing import Any, Dict

from utca.implementation.tasks import (
    TransformersFunctionCall
)

text = """We introduce Mistral 7B, a 7–billion-parameter language model engineered for
superior performance and efficiency. Mistral 7B outperforms the best open 13B
model (Llama 2) across all evaluated benchmarks, and the best released 34B
model (Llama 1) in reasoning, mathematics, and code generation. Our model
leverages grouped-query attention (GQA) for faster inference, coupled with sliding
window attention (SWA) to effectively handle sequences of arbitrary length with a
reduced inference cost. We also provide a model fine-tuned to follow instructions,
Mistral 7B – Instruct, that surpasses Llama 2 13B – chat model both on human and
automated benchmarks. Our models are released under the Apache 2.0 license.
Code: https://github.com/mistralai/mistral-src
Webpage: https://mistral.ai/news/announcing-mistral-7b/"""

schema: Dict[str, Any] = {
    "Model": {
        "Name": "",
        "Number of parameters": "",
        "Number of token": "",
        "Architecture": []
    },
    "Usage": {
        "Use case": [],
        "Licence": ""
    }
}

if __name__ == "__main__":
    res = TransformersFunctionCall().run({
        "text": text,
        "output_schema": schema,
    })["output"]
    print(res)