# UTCA

## Overview

UTCA is a versatile framework designed to streamline the integration of your models, as well as those sourced from Hugging Face, into complex programs. With UTCA, you can effortlessly construct intricate pipelines using pre-built components or tailor them to suit your specific requirements. The framework seamlessly supports multimodal data, offering built-in functionality for manipulating such data through a selection of pre-built components.

## Install

``` console
pip install -U utca
```

## Documentation

Please refer to the detailed documentation available [here](https://utca.knowledgator.com/). This comprehensive guide provides everything you need to get started, including installation instructions, and usage examples. For advanced users, the documentation also covers API reference and customization options.

## Quickstart

For this example will be used simple ExecutionSchema with TokenSearcherNER task. This program will extract entities with provided labels and threshold.

To create program follow this steps:

### 1. Install package

``` console
pip install -U utca
```

### 2. Import modules that will be used

``` python
from utca.core import (
    AddData,
    RenameAttribute,
    Flush
)
from utca.implementation.predictors import (
    TokenSearcherPredictor, TokenSearcherPredictorConfig
)
from utca.implementation.tasks import (
    TokenSearcherNER,
    TokenSearcherNERPostprocessor,
)
```

### 3. Initialize components with desired configurations

#### Predictor that will be used by NER task
``` python
predictor = TokenSearcherPredictor(
    TokenSearcherPredictorConfig(
        device="cpu"
    )
)
```

#### NER task

``` python
ner_task = TokenSearcherNER(
    predictor=predictor,
    postprocess=TokenSearcherNERPostprocessor(
        threshold=0.5
    )
)
```

Here, we set up a task using the created predictor and define a postprocess chain with a predefined threshold.

Alternatively, we can create an NER task without describing the configuration or predictor by simply:

``` python
ner_task = TokenSearcherNER()
```

It will create a default task, which differs from the one described above only by the threshold value, which defaults to 0.

To learn more about default parameters, refer to documentation or source code.

### 4. Create ExecutionSchema

``` python
pipeline = (        
    AddData({"labels": ["scientist", "university", "city"]})         
    | ner_task
    | Flush(keys=["labels"])
    | RenameAttribute("output", "entities")
)
```

Here we described pipeline that will:
1. Add "labels" to input data with values ["scientist", "university", "city"]
2. Execute NER task
3. Remove "labels" from results
4. Rename "output" to "entities"

### 5. Run created pipeline

``` python
res = pipeline.run({
    "text": """Dr. Paul Hammond, a renowned neurologist at Johns Hopkins University, has recently published a paper in the prestigious journal "Nature Neuroscience". 
His research focuses on a rare genetic mutation, found in less than 0.01% of the population, that appears to prevent the development of Alzheimer's disease. Collaborating with researchers at the University of California, San Francisco, the team is now working to understand the mechanism by which this mutation confers its protective effect. 
Funded by the National Institutes of Health, their research could potentially open new avenues for Alzheimer's treatment."""
})
```

Here, we run pupline with input __text__.

> **_NOTE:_**  __"text"__ and __"labels"__ keys are expected by TokenSearcherNER task described above. Refer to documentation or source code.

Result should look similar to:

``` python
{
    "text": """Dr. Paul Hammond, a renowned neurologist at Johns Hopkins University, has recently published a paper in the prestigious journal "Nature Neuroscience". 
His research focuses on a rare genetic mutation, found in less than 0.01% of the population, that appears to prevent the development of Alzheimer's disease. Collaborating with researchers at the University of California, San Francisco, the team is now working to understand the mechanism by which this mutation confers its protective effect. 
Funded by the National Institutes of Health, their research could potentially open new avenues for Alzheimer's treatment.""", 
    "entities": [
        {
            "start": 4, 
            "end": 16, 
            "span": "Paul Hammond",
            "score": 0.5637074708938599, 
            "entity": "scientist"
        }, 
        {
            "start": 44, 
            "end": 68, 
            "span": "Johns Hopkins University", 
            "score": 0.8921091556549072, 
            "entity": "university"
        }, 
        {
            "start": 347, 
            "end": 371,
            "span": "University of California",
            "score": 0.7202138900756836, 
            "entity": "university"
        }, 
        {
            "start": 373, 
            "end": 386,
            "span": "San Francisco",
            "score": 0.7660449743270874, 
            "entity": "city"
        }
    ]
}
```

## Concepts

### Components

All logical blocks of programs are represented as components, each of which inherits from the base class Component. This base class encompasses essential methods and attributes required for execution, including:
* __run__:  Execute component. This method should be called when program executed.
* __\_\_or\_\___: Bound components to ExecutionSchema.
* __set_name__: Set indentification name. Usefull for debugging and logging.

For parameters and more details about Component, see documentation or source code.

### Types of components

As mentioned previously, the Component class serves as the foundational base for all components utilized in program creation. Building upon this class, there exist several primary subclasses, each assigned a distinct role. Additionally, there are specialized types of components responsible for defining the actual structure of the program. These subclasses and specialized components play crucial roles in organizing and defining the program's architecture.

#### Schema of core components

![image](./static/classes.drawio.png)

### ExecutionSchema

The ExecutionSchema is essential for organizing the execution flow in a program. 
When you call the __\_\_or\_\___ method of Component, it binds components in the ExecutionSchema to create the execution pipeline. However, if you call __\_\_or\_\___ on the ExecutionSchema directly, a Component is added to the schema. To maintain the ExecutionSchema's context, it's needed to wrap it within another Component, like another ExecutionSchema or an Evaluator.

### Context

The Evaluator manages the execution context of a program. It's either created by default, passed to the run method, or wrapped around a Component.

#### Simplified schema of context and flow

![image](./static/context.drawio.png)

#### Intermidiate data

Intermidiate data is encapsulated in Transformable object and passed via __call__ method of components. It contains methods for accessing data.

Transformable can be passed between contexts.

#### Memory

Evaluator oversees global memory access throughout its context. Memory used for preserving data that can be accessed in context of Evaluator. Memory acces is provided via special components:
* GetMemory
* SetMemory
* DeleteMemory

Data in memory cannot be manipulated; it can only be stored. If you need to manipulate data, you must retrieve it, which adds it to intermediate data (Transformable).
The memory state is bound to the context (Evaluator), and you cannot access the memory of other contexts, even if the accessing context is nested within them.

#### Logging

Additionally, the Evaluator handles logging. Refer to documentation or source code to learn more.

### Scopes

The term "scope" describes how data is organized hierarchically. At the top level is the global scope, which encompasses the entire intermidiate data (i.e. state of Transformable). Nested within this global scope are inner scopes, corresponding to the values associated with specific keys in the dictionary.

All components manipulate the global scope of input data, which refers to the complete Dict passed as input when the run method is called. Additionally, Actions and Executables have the capability to manipulate inner scopes using ActionExecutor and ExecutableExecutor, respectively. These executors are created upon the use method call and retain the context of execution, which includes the following parameters:
* get_key (Optional[str], optional): Specifies which key value of input_data will be utilized (i.e., the scope to be used).
* set_key (Optional[str], optional): Determines which key will be used to set the result value. If set_key is set to None:
    * if the result is of type Dict[str, Any], it updates the root dict.
    * otherwise, it sets the result to the default_key. (i.e., the scope where the data is placed)
* default_key (str, optional): Denotes the default key used for results that are not of type Dict. If the data is not a Dict, a new default scope is created or used.
* replace (ReplacingScope, optional): Specifies the strategy for replacing data within the executor. It defines how and when data should be placed in the scope. Refer to documentation or source code.

# Contribution

## Ways to contribute​
There are many ways to contribute to UTCA. Here are some common ways people contribute:
* Code: Help us write code, fix bugs, or improve our infrastructure.
* Integrations: Help us integrate with your favorite vendors and tools.
* Discussions: Help answer usage questions and discuss issues with users.

## GitHub Issues​

Our issues page is kept up to date with bugs, improvements, and feature requests.

A taxonomy of labels exists to facilitate sorting and discovering issues of interest. Please utilize these labels to organize issues effectively.
When you commence work on an issue, kindly assign it to yourself.
When adding an issue, strive to keep it focused on a single, modular bug, improvement, or feature. If two issues are related or blocking, please link them rather than combining them.

## Getting Help​

Our goal is to have the simplest developer setup possible. Should you experience any difficulty getting setup, please contact us!

We enforce specific formatting and documentation standards throughout the codebase. If you're finding these guidelines challenging or even just annoying to work with, don't hesitate to reach out to a us. Our goal is to ensure that these standards don't hinder the process of integrating high-quality code into the codebase.

## Code

To contribute to this project, please follow the "fork and pull request" workflow. Please do not try to push directly to this repo unless you are a maintainer.

Please follow the checked-in pull request template when opening pull requests. Note related issues and tag relevant maintainers.

It's essential that we maintain great documentation and testing. If you:
* Fix a bug
    * Add a relevant unit or integration test when possible. These live in coressponding __\_\_test\_\___ directory of module where bug occured.
* Make an improvement
    * Update docstrings and if necessary add/update README file in module(s) where improvement was made
    * Update tests when relevant.
* Add a feature
    * Add a demo notebook in programs module.
    * Add tests.

## Extra tips:
* Try to maintain consistent structure of modules, and code;
* Use docstrings to describe functions and objects that you add;
* Use comments to describe fixed issues or complicated parts of code.
* In future releases, additional tools for formatting, linting, and development needs will be incorporated to simplify contribution flow.