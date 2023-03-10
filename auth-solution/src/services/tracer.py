from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)
from ..core.config import settings


def configure_tracer() -> None:
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create(
                attributes={
                    "service.name": "auth-service",
                    "service.namespace": "Auth",
                    "service.version": "1.0.0",
                }
            )
        )
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.tracer.TRACER_HOST,
                agent_port=settings.tracer.TRACER_PORT,
            )
        )
    )
    if settings.tracer.CONSOLE_TRACING_ENABLED:
        trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
