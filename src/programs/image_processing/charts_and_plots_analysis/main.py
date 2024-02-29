from core.executable_level_1.interpreter import Evaluator
from core.executable_level_1.actions import (
    AddData
)
from implementation.tasks.image_processing.charts_and_plots_analysis.transformers.transformers_charts_and_plots_analysis import (
    ChartsAndPlotsAnalysis
)
from implementation.datasources.image.actions import ImageRead

task = ChartsAndPlotsAnalysis()

if __name__ == "__main__":
    pipeline = (
        ImageRead()
        | AddData({"text": "Generate underlying data table of the figure below:"})
        | task
    )

    print(Evaluator(pipeline).run_program({
        "path_to_file": "programs/image_processing/charts_and_plots_analysis/test.png"
    }))