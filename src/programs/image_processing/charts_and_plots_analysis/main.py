from transformers import ( # type: ignore
    Pix2StructProcessor, Pix2StructForConditionalGeneration
)
from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.actions import (
    AddData
)
from implementation.predictors.transformers.transformers_model import (
    TransformersGenerativeModel,
    TransformersGenerativeModelConfig
)
from implementation.tasks.charts_and_plots_analysis.transformers_charts_and_plots_analysis import (
    ChartsAndPlotsAnalysis
)
from implementation.tasks.charts_and_plots_analysis.actions import (
    ChartsAndPlotsAnalysisPreprocessor,
    ChartsAndPlotsAnalysisPreprocessorConfig,
    ChartsAndPlotsAnalysisPostprocessor,
    ChartsAndPlotsAnalysisPostprocessorConfig
)
from implementation.datasources.image.actions import ImageRead

model_name = "google/deplot"

model = Pix2StructForConditionalGeneration.from_pretrained(model_name) # type: ignore
processor = Pix2StructProcessor.from_pretrained(model_name) # type: ignore

task = ChartsAndPlotsAnalysis(
    predictor=TransformersGenerativeModel(
        TransformersGenerativeModelConfig(
            model=model,
            max_new_tokens=1024
        )
    ),
    preprocess=[
        ChartsAndPlotsAnalysisPreprocessor(
            ChartsAndPlotsAnalysisPreprocessorConfig(
                processor=processor # type: ignore
            )
        )
    ],
    postprocess=[
        ChartsAndPlotsAnalysisPostprocessor(
            ChartsAndPlotsAnalysisPostprocessorConfig(
                processor=processor # type: ignore
            )
        )
    ]
)

if __name__ == "__main__":
    pipeline = (
        ImageRead()
        | AddData({"text": "Generate underlying data table of the figure below:"})
        | task
    )

    print(Evaluator(pipeline).run_program({
        "path_to_file": "programs/program11/test.png"
    }))