# --- Required Configurations ---
API_TOKEN = "your_actual_cpk_token_here" # Your Chutes.ai API Token

# --- Server Behavior Configurations ---
CHUTES_API_URL = "https://llm.chutes.ai/v1/chat/completions"
MODEL_NAME = "deepseek-ai/DeepSeek-V3-0324" # Set your model here
SERVER_PORT = 11435
DEFAULT_SYSTEM_PROMPT = """ Ex)You are a helpful assistant """ #Default system prompt, or None if not desired
MAX_HISTORY_MESSAGES = -1 # Max conversation messages to keep, set -1 for unlimited
DEBUG_MODE = False

# --- LLM Generation Parameter Defaults ---
# These values are used if the client does not provide them.
# Set to None to omit the parameter from the backend user request, letting the backend user LLM use its own default.

# Sampling parameters
TEMPERATURE = 0.7
TOP_P = None
MIN_P = None
TOP_K = None
SEED = None

# Response control
MAX_TOKENS = 1024
MIN_TOKENS = None
STOP_SEQUENCES = None
STOP_TOKEN_IDS = None

# Penalty parameters
PRESENCE_PENALTY = None
FREQUENCY_PENALTY = None
REPETITION_PENALTY = None
LENGTH_PENALTY = None

# Other parameters
LOGIT_BIAS = None                       # dict[str|int, float]: Modifies likelihood of specified tokens
LOGPROBS = None                         # bool: Whether to return log probabilities, API default typically False
TOP_LOGPROBS = None                     # int: Number of top logprobs if logprobs is true
PROMPT_LOGPROBS = None                  # int: Number of prompt logprobs

# Boolean flags for token processing
IGNORE_EOS = None                       # bool: API default typically False
SKIP_SPECIAL_TOKENS = None              # bool: API default often True
INCLUDE_STOP_STR_IN_OUTPUT = None       # bool: API default typically False
SPACES_BETWEEN_SPECIAL_TOKENS = None    # bool: API default often True

# Response format, Example: {"type": "json_object"}
RESPONSE_FORMAT = None