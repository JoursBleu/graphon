from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable

from graphon.model_runtime.entities.model_entities import AIModelEntity, ModelType
from graphon.model_runtime.protocols.llm_runtime import LLMModelRuntime
from graphon.model_runtime.protocols.moderation_runtime import (
    ModerationModelRuntime,
)
from graphon.model_runtime.protocols.rerank_runtime import RerankModelRuntime
from graphon.model_runtime.protocols.speech_to_text_runtime import (
    SpeechToTextModelRuntime,
)
from graphon.model_runtime.protocols.text_embedding_runtime import (
    TextEmbeddingModelRuntime,
)
from graphon.model_runtime.protocols.tts_runtime import TTSModelRuntime


@runtime_checkable
class ModelRuntime(
    LLMModelRuntime,
    TextEmbeddingModelRuntime,
    RerankModelRuntime,
    SpeechToTextModelRuntime,
    ModerationModelRuntime,
    TTSModelRuntime,
    Protocol,
):
    """Aggregate runtime for adapters that implement every model capability."""

    def fetch_models(
        self,
        *,
        provider: str,
        model_type: ModelType,
        credentials: Mapping[str, Any],
    ) -> list[AIModelEntity]:
        """Fetch a credential-scoped catalog for an opted-in remote provider.

        Hosts call this only when the provider declares ``remote_model_catalog``.
        Adapters without discovery support fail explicitly rather than returning
        an empty catalog. Selection, schema caching, and refresh belong to hosts.
        """
        msg = "Remote model catalog is not supported by this runtime."
        raise NotImplementedError(msg)
