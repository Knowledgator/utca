from typing import List, Literal

from utca.core.executable_level_1.schema import Config

class Web2MeaningMediaParameters(Config):
    audios: bool = False
    images: bool = True
    videos: bool = True


class Web2MeaningDateParameters(Config):
    publishedTime: bool = True
    updateTime: bool = True


class Web2MeaningMetadataParameters(Config):
    author: bool = True
    contentType: bool = True
    date: Web2MeaningDateParameters = Web2MeaningDateParameters()
    description: bool = True
    favicon: bool = True
    keywords: bool = True
    title: bool = True


class Web2MeaningNLPParameters(Config):
    customCategories: List[str] = []
    entities: bool = True
    isArticle: bool = True
    isCorporative: bool = False
    websiteTopic: bool = False


class Web2MeaningRequestParameters(Config):
    htmlProcessing: Literal["shallow", "deep"] = "shallow"
    jsRendering: bool = False
    renderingTime: int = 1
    scroll: int = 0


class Web2MeaningTextParameters(Config):
    body: bool = True
    cleanBody: bool = False
    fullText: bool = True
    includeLinks: bool = False
    lang: bool = True


class Web2MeaningParameters(Config):
    domain: bool = True
    html: bool = False
    links: bool = False
    media: Web2MeaningMediaParameters = Web2MeaningMediaParameters()
    metadata: Web2MeaningMetadataParameters = Web2MeaningMetadataParameters()
    nlp: Web2MeaningNLPParameters = Web2MeaningNLPParameters()
    request: Web2MeaningRequestParameters = Web2MeaningRequestParameters()
    text: Web2MeaningTextParameters = Web2MeaningTextParameters()