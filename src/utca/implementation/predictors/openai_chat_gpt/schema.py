from typing import Dict, List, Iterable, Optional, Union

from pydantic import ConfigDict
from httpx import Timeout
from openai._types import Body, Headers, Query, NotGiven, NOT_GIVEN
from openai.types.chat.completion_create_params import (
    FunctionCall,
    Function,
    ResponseFormat
)
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_stream_options_param import (
    ChatCompletionStreamOptionsParam
)
from openai.types.chat.chat_completion_tool_choice_option_param import (
    ChatCompletionToolChoiceOptionParam
)

from utca.core.executable_level_1.schema import IOModel, Config

class ChatGPTInput(IOModel):
    messages: Iterable[ChatCompletionMessageParam]


class ChatCompletionOutput(IOModel, ChatCompletion):
    ...


class ChatCompletionStreamOutput(IOModel):
    stream: Iterable[ChatCompletionChunk]


class ChatGPTConfig(Config):
    """
    Args:
        model: ID of the model to use. See the
            [model endpoint compatibility](https://platform.openai.com/docs/models/model-endpoint-compatibility)
            table for details on which models work with the Chat API.

        frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
            existing frequency in the text so far, decreasing the model's likelihood to
            repeat the same line verbatim.

            [See more information about frequency and presence penalties.](https://platform.openai.com/docs/guides/text-generation/parameter-details)

        function_call: Deprecated in favor of `tool_choice`.

            Controls which (if any) function is called by the model. `none` means the model
            will not call a function and instead generates a message. `auto` means the model
            can pick between generating a message or calling a function. Specifying a
            particular function via `{"name": "my_function"}` forces the model to call that
            function.

            `none` is the default when no functions are present. `auto` is the default if
            functions are present.

        functions: Deprecated in favor of `tools`.

            A list of functions the model may generate JSON inputs for.

        logit_bias: Modify the likelihood of specified tokens appearing in the completion.

            Accepts a JSON object that maps tokens (specified by their token ID in the
            tokenizer) to an associated bias value from -100 to 100. Mathematically, the
            bias is added to the logits generated by the model prior to sampling. The exact
            effect will vary per model, but values between -1 and 1 should decrease or
            increase likelihood of selection; values like -100 or 100 should result in a ban
            or exclusive selection of the relevant token.

        logprobs: Whether to return log probabilities of the output tokens or not. If true,
            returns the log probabilities of each output token returned in the `content` of
            `message`.

        max_tokens: The maximum number of [tokens](/tokenizer) that can be generated in the chat
            completion.

            The total length of input tokens and generated tokens is limited by the model's
            context length.
            [Example Python code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken)
            for counting tokens.

        n: How many chat completion choices to generate for each input message. Note that
            you will be charged based on the number of generated tokens across all of the
            choices. Keep `n` as `1` to minimize costs.

        presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
            whether they appear in the text so far, increasing the model's likelihood to
            talk about new topics.

            [See more information about frequency and presence penalties.](https://platform.openai.com/docs/guides/text-generation/parameter-details)

        response_format: An object specifying the format that the model must output. Compatible with
            [GPT-4 Turbo](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) and
            all GPT-3.5 Turbo models newer than `gpt-3.5-turbo-1106`.

            Setting to `{ "type": "json_object" }` enables JSON mode, which guarantees the
            message the model generates is valid JSON.

            **Important:** when using JSON mode, you **must** also instruct the model to
            produce JSON yourself via a system or user message. Without this, the model may
            generate an unending stream of whitespace until the generation reaches the token
            limit, resulting in a long-running and seemingly "stuck" request. Also note that
            the message content may be partially cut off if `finish_reason="length"`, which
            indicates the generation exceeded `max_tokens` or the conversation exceeded the
            max context length.

        seed: This feature is in Beta. If specified, our system will make a best effort to
            sample deterministically, such that repeated requests with the same `seed` and
            parameters should return the same result. Determinism is not guaranteed, and you
            should refer to the `system_fingerprint` response parameter to monitor changes
            in the backend.

        stop: Up to 4 sequences where the API will stop generating further tokens.

        stream: If set, partial message deltas will be sent, like in ChatGPT. Tokens will be
            sent as data-only
            [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
            as they become available, with the stream terminated by a `data: [DONE]`
            message.
            [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions).

        stream_options: Options for streaming response. Only set this when you set `stream: true`.

        temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
            make the output more random, while lower values like 0.2 will make it more
            focused and deterministic.

            We generally recommend altering this or `top_p` but not both.

        tool_choice: Controls which (if any) tool is called by the model. `none` means the model will
            not call any tool and instead generates a message. `auto` means the model can
            pick between generating a message or calling one or more tools. `required` means
            the model must call one or more tools. Specifying a particular tool via
            `{"type": "function", "function": {"name": "my_function"}}` forces the model to
            call that tool.

            `none` is the default when no tools are present. `auto` is the default if tools
            are present.

        tools: A list of tools the model may call. Currently, only functions are supported as a
            tool. Use this to provide a list of functions the model may generate JSON inputs
            for. A max of 128 functions are supported.

        top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
            return at each token position, each with an associated log probability.
            `logprobs` must be set to `true` if this parameter is used.

        top_p: An alternative to sampling with temperature, called nucleus sampling, where the
            model considers the results of the tokens with top_p probability mass. So 0.1
            means only the tokens comprising the top 10% probability mass are considered.

            We generally recommend altering this or `temperature` but not both.

        user: A unique identifier representing your end-user, which can help OpenAI to monitor
            and detect abuse.
            [Learn more](https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids).

        extra_headers: Send extra headers

        extra_query: Add additional query parameters to the request

        extra_body: Add additional JSON properties to the request

        timeout: Override the client-level default timeout for this request, in seconds
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    model: str
    frequency_penalty: Optional[Union[float, NotGiven]] = NOT_GIVEN
    function_call: Union[FunctionCall, NotGiven] = NOT_GIVEN
    functions: Union[Iterable[Function], NotGiven] = NOT_GIVEN
    logit_bias: Optional[Union[Dict[str, int], NotGiven]] = NOT_GIVEN
    logprobs: Optional[Union[bool, NotGiven]] = NOT_GIVEN
    max_tokens: Optional[Union[int, NotGiven]] = NOT_GIVEN
    n: Optional[Union[int, NotGiven]] = NOT_GIVEN
    presence_penalty: Optional[Union[float, NotGiven]] = NOT_GIVEN
    response_format: Union[ResponseFormat, NotGiven] = NOT_GIVEN
    seed: Optional[Union[int, NotGiven]] = NOT_GIVEN
    stop: Optional[Union[str, List[str], NotGiven]] = NOT_GIVEN
    stream: Optional[Union[NotGiven, bool]] = NOT_GIVEN
    stream_options: Optional[Union[ChatCompletionStreamOptionsParam, NotGiven]] = NOT_GIVEN
    temperature: Optional[Union[float, NotGiven]] = NOT_GIVEN
    tool_choice: Union[ChatCompletionToolChoiceOptionParam, NotGiven] = NOT_GIVEN
    tools: Union[Iterable[ChatCompletionToolParam], NotGiven] = NOT_GIVEN
    top_logprobs: Optional[Union[int, NotGiven]] = NOT_GIVEN
    top_p: Optional[Union[float, NotGiven]] = NOT_GIVEN
    user: Optional[Union[str, NotGiven]] = NOT_GIVEN
    extra_headers: Optional[Headers] = None
    extra_query: Optional[Query] = None
    extra_body: Optional[Body] = None
    timeout: Optional[Union[float, Timeout, NotGiven]] = NOT_GIVEN