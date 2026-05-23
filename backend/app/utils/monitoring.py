"""
Monitoring and metrics
Implements Prometheus monitoring
"""
import logging
from prometheus_client import Counter, Histogram, Gauge
import time

logger = logging.getLogger(__name__)

# Define metrics
request_count = Counter(
    'rag_api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status_code']
)

request_duration = Histogram(
    'rag_api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

document_count = Gauge(
    'rag_documents_total',
    'Total documents in system'
)

vector_store_size = Gauge(
    'rag_vector_store_size_bytes',
    'Vector store size in bytes'
)

active_tasks = Gauge(
    'rag_agent_tasks_active',
    'Active agent tasks'
)

query_latency = Histogram(
    'rag_query_latency_seconds',
    'Query processing latency'
)

llm_tokens_used = Counter(
    'rag_llm_tokens_used_total',
    'Total LLM tokens used',
    ['model']
)

embedding_calls = Counter(
    'rag_embedding_calls_total',
    'Total embedding API calls'
)


def setup_monitoring() -> None:
    """
    Setup monitoring and metrics collection
    """
    logger.info("Monitoring system initialized")


def record_api_request(method: str, endpoint: str, status_code: int, duration: float) -> None:
    """Record API request metrics"""
    request_count.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code
    ).inc()
    
    request_duration.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)


def record_query(duration: float) -> None:
    """Record query metrics"""
    query_latency.observe(duration)


def record_llm_tokens(model: str, tokens: int) -> None:
    """Record LLM token usage"""
    llm_tokens_used.labels(model=model).inc(tokens)


def record_embedding_call() -> None:
    """Record embedding API call"""
    embedding_calls.inc()
