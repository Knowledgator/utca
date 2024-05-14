import pathlib
PATH = pathlib.Path(__file__).parent.resolve()

from utca.core import (
    AddData
)
from utca.implementation.tasks import (
    TransformersChartsAndPlotsAnalysis
)
from utca.implementation.datasources.image import ImageRead

task = TransformersChartsAndPlotsAnalysis()

if __name__ == "__main__":
    pipeline = (
        ImageRead()
        | AddData({"text": "Generate underlying data table of the figure below:"})
        | task
    )

    print(pipeline.run({
        "path_to_file": f"{PATH}/test.png"
    }))