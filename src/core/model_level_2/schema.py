from __future__ import annotations
# from src.executable_level_1.schema import InputType

class Prompt:
    def __init__(self, prompt: str) -> None:
        self._prompt = prompt


    @property
    def prompt(self) -> str:
        return self._prompt


class PromptTemplate:
    complex: bool = False

    def validate_dict_template(self, template: Any) -> None:
        if not isinstance(template, dict):
            raise ValueError(f'Expected dict[str, str] or str. Get {type(template)}')


    def __init__(self, template: Union[str, Dict[str, str]]) -> None:
        self.template = template        
        if not isinstance(self.template, str):
            self.validate_dict_template(self.template)
            self.complex = True

    @classmethod
    def from_messages(cls, message: Dict[str, Any]) -> PromptTemplate:
        template = ''
        return PromptTemplate(template)
    

    @classmethod
    def merge_messages(cls, system: str, content: str) -> str:
        return ' '.join((system, content))


    def format(self, **kwargs: Dict[str, Any]) -> BasicPrompt:
        if not self.complex:
            return BasicPrompt(prompt=self.template.format(**kwargs)) # type: ignore
        else:
            system_message = self.template['system'].format(**kawrgs['system']) # type: ignore
            content = self.template['content'].format(**kawrgs['content']) # type: ignore
            return BasicPrompt(
                prompt=self.merge_messages(system_message, content), 
                prompt_len=len(system_message)
            )