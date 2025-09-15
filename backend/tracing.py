from arize.otel import register
from openinference.instrumentation.litellm import LiteLLMInstrumentor

# Initialize LiteLLM instrumentation before registering Phoenix
LiteLLMInstrumentor().instrument()

tracer_provider = register(
    space_id = "U3BhY2U6MjgwMTc6bm1JRw==",
    api_key = "ak-d35b92bb-2be4-4d5a-bd91-469beeacaa45-VRtXnkc_mIzp0b62_ZlVnVegM_YUAW0p",
    project_name = "Chailease AI Evals Workshop", # name this to whatever you would like
)

# Get tracer for manual instrumentation
tracer = tracer_provider.get_tracer(__name__)