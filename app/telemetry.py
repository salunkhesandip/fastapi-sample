import logging
import os

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry._logs import set_logger_provider

_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "fastapi-sample")
_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")


def _build_resource() -> Resource:
    return Resource.create(
        {
            "service.name": _SERVICE_NAME,
            "service.version": os.getenv("SERVICE_VERSION", "1.0.0"),
            "deployment.environment": os.getenv("DEPLOYMENT_ENV", "local"),
        }
    )


def _setup_traces(resource: Resource) -> None:
    exporter = OTLPSpanExporter(endpoint=f"{_OTLP_ENDPOINT}/v1/traces")
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)


def _setup_metrics(resource: Resource) -> None:
    exporter = OTLPMetricExporter(endpoint=f"{_OTLP_ENDPOINT}/v1/metrics")
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=30_000)
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)


def _setup_logs(resource: Resource) -> None:
    exporter = OTLPLogExporter(endpoint=f"{_OTLP_ENDPOINT}/v1/logs")
    provider = LoggerProvider(resource=resource)
    provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    set_logger_provider(provider)
    LoggingInstrumentor().instrument(set_logging_format=True, log_level=logging.DEBUG)


def setup_telemetry() -> None:
    """Initialise OpenTelemetry traces, metrics, and logs.

    Call this once at application startup before creating the FastAPI instance.
    Configuration is driven by environment variables:
      OTEL_SERVICE_NAME          – service name (default: fastapi-sample)
      OTEL_EXPORTER_OTLP_ENDPOINT – OTLP HTTP base URL (default: http://localhost:4318)
      SERVICE_VERSION            – reported service version (default: 1.0.0)
      DEPLOYMENT_ENV             – environment tag (default: local)
    """
    resource = _build_resource()
    _setup_traces(resource)
    _setup_metrics(resource)
    _setup_logs(resource)
