import aiohttp
import asyncio
import json
from aiohttp import web
from datetime import datetime, timezone
import hashlib
from typing import List, Dict, Any, Optional, Union

# Load Configuration from config.py
try:
    import config
except ImportError:
    raise SystemExit("[Fatal Error] `config.py` not found. Please create it with your configurations, especially API_TOKEN.")

def get_config_value(param_name: str, default_value: Any = None) -> Any:
    return getattr(config, param_name, default_value)

API_TOKEN: str = get_config_value("API_TOKEN")
if not API_TOKEN or not isinstance(API_TOKEN, str):
    raise SystemExit("[Fatal Error] API_TOKEN is not defined, empty, or invalid in `config.py`.")
API_URL: str = get_config_value("CHUTES_API_URL")
MODEL_NAME: str = get_config_value("MODEL_NAME")
SERVER_PORT: int = get_config_value("SERVER_PORT")
SYSTEM_PROMPT: Optional[str] = get_config_value("DEFAULT_SYSTEM_PROMPT")
MAX_HISTORY_MESSAGES: int = get_config_value("MAX_HISTORY_MESSAGES")
DEBUG_MODE: bool = get_config_value("DEBUG_MODE")
TEMPERATURE: Optional[float] = get_config_value("TEMPERATURE")
TOP_P: Optional[float] = get_config_value("TOP_P")
MAX_TOKENS: Optional[int] = get_config_value("MAX_TOKENS")
SEED: Optional[int] = get_config_value("SEED")
STOP_SEQUENCES: Optional[Union[str, List[str]]] = get_config_value("STOP_SEQUENCES")
PRESENCE_PENALTY: Optional[float] = get_config_value("PRESENCE_PENALTY")
FREQUENCY_PENALTY: Optional[float] = get_config_value("FREQUENCY_PENALTY")
REPETITION_PENALTY: Optional[float] = get_config_value("REPETITION_PENALTY")
LENGTH_PENALTY: Optional[float] = get_config_value("LENGTH_PENALTY")
MIN_P: Optional[float] = get_config_value("MIN_P")
TOP_K: Optional[int] = get_config_value("TOP_K")
MIN_TOKENS: Optional[int] = get_config_value("MIN_TOKENS")
LOGIT_BIAS: Optional[Dict[Union[str, int], float]] = get_config_value("LOGIT_BIAS")
STOP_TOKEN_IDS: Optional[List[int]] = get_config_value("STOP_TOKEN_IDS")
RESPONSE_FORMAT: Optional[Dict[str, str]] = get_config_value("RESPONSE_FORMAT")
LOGPROBS: Optional[bool] = get_config_value("LOGPROBS")
TOP_LOGPROBS: Optional[int] = get_config_value("TOP_LOGPROBS")
PROMPT_LOGPROBS: Optional[int] = get_config_value("PROMPT_LOGPROBS")
IGNORE_EOS: Optional[bool] = get_config_value("IGNORE_EOS")
SKIP_SPECIAL_TOKENS: Optional[bool] = get_config_value("SKIP_SPECIAL_TOKENS")
INCLUDE_STOP_STR_IN_OUTPUT: Optional[bool] = get_config_value("INCLUDE_STOP_STR_IN_OUTPUT")
SPACES_BETWEEN_SPECIAL_TOKENS: Optional[bool] = get_config_value("SPACES_BETWEEN_SPECIAL_TOKENS")

SPECIFIC_SYSTEM_PROMPT_TO_IGNORE = " Ex)You are a helpful assistant "
if SYSTEM_PROMPT == SPECIFIC_SYSTEM_PROMPT_TO_IGNORE:
    if DEBUG_MODE:
        print(f"[DEBUG] System prompt matched '{SPECIFIC_SYSTEM_PROMPT_TO_IGNORE}', treating as None.")
    SYSTEM_PROMPT = None

# Global Constants and Derived Settings
_ADVERTISED_MODEL_DEFINITIONS_IN_SCRIPT: List[Dict[str, Any]] = [
    {
        "name": f"{MODEL_NAME}:latest",
        "model": f"{MODEL_NAME}:latest",
    }
]

PROXY_ADVERTISED_MODELS: List[Dict[str, Any]] = []
for model_def_script in _ADVERTISED_MODEL_DEFINITIONS_IN_SCRIPT:
    model_name_tag = model_def_script.get("name", f"{MODEL_NAME}:latest")
    PROXY_ADVERTISED_MODELS.append({
        "name": model_name_tag,
        "model": model_def_script.get("model", model_name_tag),
        "modified_at": model_def_script.get("modified_at", datetime.now(timezone.utc).isoformat()),
        "size": model_def_script.get("size", 0),
        "digest": model_def_script.get("digest", hashlib.sha256(model_name_tag.encode()).hexdigest()[:16]),
        "details": model_def_script.get("details", { "family": "general", "parameter_size": "N/A", "quantization_level": "N/A" })
    })

PROXY_VERSION: str = "0.2.2-chutesai-proxy"


LLM_SSE_EVENT_PREFIX: str = "data: "
LLM_SSE_DONE_PAYLOAD: str = "[DONE]"

# Helper Functions
def _build_backend_llm_request_body(
        chutes_ai_model_name: str,
        processed_messages: List[Dict[str, str]],
        client_options: Dict[str, Any],
        client_request_data: Dict[str, Any]
) -> Dict[str, Any]:
    backend_llm_body: Dict[str, Any] = {
        "model": chutes_ai_model_name, "messages": processed_messages, "stream": True,
    }
    server_llm_params: Dict[str, Any] = {
        "max_tokens": MAX_TOKENS, "temperature": TEMPERATURE, "top_p": TOP_P, "seed": SEED,
        "stop": STOP_SEQUENCES, "presence_penalty": PRESENCE_PENALTY,
        "frequency_penalty": FREQUENCY_PENALTY, "repetition_penalty": REPETITION_PENALTY,
        "length_penalty": LENGTH_PENALTY, "min_p": MIN_P, "top_k": TOP_K,
        "min_tokens": MIN_TOKENS, "logit_bias": LOGIT_BIAS, "stop_token_ids": STOP_TOKEN_IDS,
        "logprobs": LOGPROBS, "top_logprobs": TOP_LOGPROBS, "prompt_logprobs": PROMPT_LOGPROBS,
        "ignore_eos": IGNORE_EOS, "skip_special_tokens": SKIP_SPECIAL_TOKENS,
        "include_stop_str_in_output": INCLUDE_STOP_STR_IN_OUTPUT,
        "spaces_between_special_tokens": SPACES_BETWEEN_SPECIAL_TOKENS,
    }
    if RESPONSE_FORMAT is not None:
        backend_llm_body["response_format"] = RESPONSE_FORMAT

    for key, value in server_llm_params.items():
        if value is not None: backend_llm_body[key] = value

    param_map_from_client: Dict[str, str] = {
        "temperature": "temperature", "top_p": "top_p", "top_k": "top_k", "seed": "seed",
        "stop": "stop", "num_predict": "max_tokens",
        "presence_penalty": "presence_penalty", "frequency_penalty": "frequency_penalty",
        "repeat_penalty": "repetition_penalty", "logit_bias": "logit_bias", "min_p": "min_p",
    }
    used_client_options_for_log: Dict[str, Any] = {}
    ignored_client_options_for_log: Dict[str, Any] = {}

    for client_key, client_value in client_options.items():
        if client_value is None:
            backend_key_to_remove = param_map_from_client.get(client_key, client_key)
            if backend_key_to_remove in backend_llm_body: del backend_llm_body[backend_key_to_remove]
            used_client_options_for_log[client_key] = "None (omitted/nullified by client)"
            continue
        backend_key = param_map_from_client.get(client_key)
        if backend_key:
            backend_llm_body[backend_key] = client_value; used_client_options_for_log[client_key] = client_value
        elif client_key in server_llm_params or client_key == "response_format": # Allow direct override of any server param
            backend_llm_body[client_key] = client_value; used_client_options_for_log[client_key] = client_value
        else: ignored_client_options_for_log[client_key] = client_value

    client_format_option = client_request_data.get("format")
    if client_format_option is not None:
        if isinstance(client_format_option, str) and client_format_option.lower() == "json":
            backend_llm_body["response_format"] = {"type": "json_object"}
            used_client_options_for_log["format='json'"] = backend_llm_body["response_format"]
        elif isinstance(client_format_option, dict) and "type" in client_format_option: # For OpenAI-like schema support
            backend_llm_body["response_format"] = client_format_option
            used_client_options_for_log["format=JSONSchemaObject"] = client_format_option
        else:
            ignored_client_options_for_log["format"] = client_format_option
            if "response_format" in backend_llm_body and client_format_option is not None:
                del backend_llm_body["response_format"]
    elif "response_format" not in backend_llm_body and RESPONSE_FORMAT is not None:
        backend_llm_body["response_format"] = RESPONSE_FORMAT


    final_body = {k: v for k, v in backend_llm_body.items() if v is not None}
    if DEBUG_MODE:
        print(f"[DEBUG] Server-configured LLM params (before client override): { {k:v for k,v in server_llm_params.items() if v is not None} }")
        if RESPONSE_FORMAT: print(f"[DEBUG] Server-configured RESPONSE_FORMAT: {RESPONSE_FORMAT}")
        if used_client_options_for_log: print(f"[DEBUG] Applied/Mapped client parameters: {used_client_options_for_log}")
        if ignored_client_options_for_log: print(f"[DEBUG] Ignored client parameters (not mappable/supported by backend): {ignored_client_options_for_log}")
        tool_related_keys = ["tools", "tool_choice", "functions", "function_call"]
        client_sent_tool_params = any(key in client_request_data or key in client_options for key in tool_related_keys)
        if client_sent_tool_params: print("[DEBUG] Client sent tool/function calling parameters. This proxy currently ignores them as backend support is unconfirmed via schema.")
    return final_body

async def _transform_and_stream_llm_response(
        llm_backend_response: aiohttp.ClientResponse, client_web_response: web.StreamResponse,
        client_model_requested: str, stream_to_client: bool
) -> tuple[str, Dict[str, Any]]:
    content_parts: List[str] = []; last_backend_payload: Dict[str, Any] = {}
    async for line_bytes in llm_backend_response.content:
        line = line_bytes.decode("utf-8").strip()
        if not line.startswith(LLM_SSE_EVENT_PREFIX): continue
        data_json_str = line[len(LLM_SSE_EVENT_PREFIX):].strip()
        if data_json_str == LLM_SSE_DONE_PAYLOAD: break
        if not data_json_str: continue
        try:
            backend_payload = json.loads(data_json_str); last_backend_payload = backend_payload
            choices = backend_payload.get("choices")
            if not (choices and isinstance(choices, list) and choices): continue
            delta = choices[0].get("delta", {}); content_token = delta.get("content")
            if content_token is not None:
                content_parts.append(content_token)
                if stream_to_client:
                    ollama_stream_chunk = { "model": backend_payload.get("model", client_model_requested),
                                            "created_at": datetime.now(timezone.utc).isoformat(),
                                            "message": {"role": delta.get("role", "assistant"), "content": content_token},
                                            "done": False }
                    await client_web_response.write(json.dumps(ollama_stream_chunk).encode('utf-8') + b'\n')
                    await asyncio.sleep(0.001)
            if choices[0].get("finish_reason") is not None: break
        except json.JSONDecodeError: print(f"[Error] Ollama Proxy: Failed to parse JSON chunk from backend: {data_json_str}")
        except Exception as e_chunk_proc: print(f"[Error] Ollama Proxy: Error processing backend chunk: {e_chunk_proc}, data: '{data_json_str}'")
    return "".join(content_parts), last_backend_payload

# Ollama-compatible API Handlers
async def handle_ollama_tags(request: web.Request) -> web.Response:
    """ /api/tags - Returns a list of models available through this proxy."""
    return web.json_response({"models": PROXY_ADVERTISED_MODELS})

async def handle_ollama_version(request: web.Request) -> web.Response:
    """ /api/version - Returns a version for this proxy server."""
    return web.json_response({"version": PROXY_VERSION})

async def ollama_chat_handler(request: web.Request) -> web.Union[web.StreamResponse, web.Response]:
    try: client_request_data: Dict[str, Any] = await request.json()
    except json.JSONDecodeError: return web.json_response({"error": "Invalid JSON body. Please send a valid JSON."}, status=400)
    client_model_from_request: str = client_request_data.get("model", MODEL_NAME)
    client_messages: List[Dict[str, str]] = client_request_data.get("messages", [])
    stream_to_client: bool = client_request_data.get("stream", True)
    client_options: Dict[str, Any] = client_request_data.get("options", {})
    if not client_messages: return web.json_response({"error": "'messages' field is required in the request body."}, status=400)
    chutes_ai_model_name: str = client_model_from_request
    if ":" in chutes_ai_model_name and chutes_ai_model_name.endswith(":latest"): chutes_ai_model_name = chutes_ai_model_name[:-len(":latest")]
    backend_llm_messages: List[Dict[str, str]] = []
    has_system_message_from_client = any(msg.get("role") == "system" for msg in client_messages)

    if SYSTEM_PROMPT and SYSTEM_PROMPT.strip() and not has_system_message_from_client:
        backend_llm_messages.append({"role": "system", "content": SYSTEM_PROMPT})
    backend_llm_messages.extend(client_messages)


    if MAX_HISTORY_MESSAGES != -1 and len(backend_llm_messages) > MAX_HISTORY_MESSAGES:
        if DEBUG_MODE:
            print(f"[DEBUG] Trimming message history from {len(backend_llm_messages)} to {MAX_HISTORY_MESSAGES} messages.")
        if backend_llm_messages[0]["role"] == "system" and \
                SYSTEM_PROMPT and SYSTEM_PROMPT.strip() and \
                backend_llm_messages[0]["content"] == SYSTEM_PROMPT and \
                len(backend_llm_messages) > 1:

            num_to_keep_after_system = MAX_HISTORY_MESSAGES - 1
            if num_to_keep_after_system < 0: num_to_keep_after_system = 0
            actual_messages_to_trim_from = backend_llm_messages[1:]
            backend_llm_messages = [backend_llm_messages[0]] + actual_messages_to_trim_from[-num_to_keep_after_system:]
        else:
            backend_llm_messages = backend_llm_messages[-MAX_HISTORY_MESSAGES:]
    elif MAX_HISTORY_MESSAGES == -1 and DEBUG_MODE:
        print(f"[DEBUG] MAX_HISTORY_MESSAGES is -1. Sending all {len(backend_llm_messages)} messages.")


    backend_llm_body_final = _build_backend_llm_request_body(chutes_ai_model_name, backend_llm_messages, client_options, client_request_data)
    if DEBUG_MODE:
        print("\n[DEBUG] Final request body to backend LLM (Chutes.ai):")
        print(json.dumps(backend_llm_body_final, indent=2, ensure_ascii=False)); print("-" * 40)
    response_headers = {'Cache-Control': 'no-cache', 'Connection': 'keep-alive'}
    if stream_to_client: response_headers['Content-Type'] = 'application/x-ndjson'
    else: response_headers['Content-Type'] = 'application/json'
    client_web_response = web.StreamResponse(status=200, reason='OK', headers=response_headers)
    await client_web_response.prepare(request)
    try:
        async with request.app['aiohttp_session'].post(API_URL, json=backend_llm_body_final, headers={'Authorization': f'Bearer {API_TOKEN}'}) as llm_backend_response:
            if llm_backend_response.status != 200:
                error_text = await llm_backend_response.text()
                print(f"[Error] Backend LLM API Error - Status: {llm_backend_response.status}, Response: {error_text}")
                ollama_error_obj = {"model": client_model_from_request, "created_at": datetime.now(timezone.utc).isoformat(),
                                    "message": {"role": "assistant", "content": ""}, "done": True,
                                    "error": f"Backend LLM Error (Status {llm_backend_response.status}): {error_text[:200]}"}
                await client_web_response.write(json.dumps(ollama_error_obj).encode('utf-8') + (b'\n' if stream_to_client else b''))
                return client_web_response
            full_assistant_content, last_backend_payload = await _transform_and_stream_llm_response(llm_backend_response, client_web_response, client_model_from_request, stream_to_client)
            ollama_final_obj: Dict[str, Any] = {"model": client_model_from_request, "created_at": datetime.now(timezone.utc).isoformat(),
                                                "message": {"role": "assistant", "content": "" if stream_to_client else full_assistant_content},
                                                "done": True }
            usage_info = last_backend_payload.get("usage")
            if isinstance(usage_info, dict):
                if usage_info.get("prompt_tokens") is not None: ollama_final_obj["prompt_eval_count"] = usage_info.get("prompt_tokens")
                if usage_info.get("completion_tokens") is not None: ollama_final_obj["eval_count"] = usage_info.get("completion_tokens")
                if usage_info.get("total_tokens") is not None: ollama_final_obj["total_tokens_backend"] = usage_info.get("total_tokens")

            if stream_to_client:
                await client_web_response.write(json.dumps(ollama_final_obj).encode('utf-8') + b'\n')
            else:
                ollama_final_obj["message"]["content"] = full_assistant_content
                await client_web_response.write(json.dumps(ollama_final_obj).encode('utf-8'))
    except Exception as e_handler:
        error_message = f"Unhandled server error: {str(e_handler)}"; print(f"[Error] Ollama Proxy Handler: {error_message}")
        ollama_error_obj = {"model": client_model_from_request, "created_at": datetime.now(timezone.utc).isoformat(),
                            "message": {"role": "assistant", "content": ""}, "done": True, "error": error_message[:200]}
        try:
            if client_web_response.prepared and not client_web_response.task.done():
                await client_web_response.write(json.dumps(ollama_error_obj).encode('utf-8') + (b'\n' if stream_to_client else b''))
        except Exception as write_e: print(f"[Error] Failed to write final error to client: {write_e}")
    finally:
        if client_web_response.prepared and not client_web_response.task.done():
            try: await client_web_response.write_eof()
            except Exception: pass
    return client_web_response

# Application Setup and Main Execution
async def init_app() -> web.Application:
    """Initializes the aiohttp web application."""
    app = web.Application()
    session_headers = {"Content-Type": "application/json"}
    app['aiohttp_session'] = aiohttp.ClientSession(headers=session_headers)
    app.router.add_post("/api/chat", ollama_chat_handler)
    app.router.add_get("/api/tags", handle_ollama_tags)
    app.router.add_get("/api/version", handle_ollama_version)
    return app

async def main():
    """Main function to start the server."""
    if not API_TOKEN:
        print("[Fatal Error] API_TOKEN is not configured correctly in `config.py` or is invalid."); return

    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", SERVER_PORT)

    print("=======================================================================")
    print(f"Ollama-compatible API Server STARTED (Version: {PROXY_VERSION})")
    print(f"Listening on: http://localhost:{SERVER_PORT}")
    print(f"Endpoints: POST /api/chat, GET /api/tags, GET /api/version")
    print(f"Default Model (if not specified by client): {MODEL_NAME}")
    print(f"")
    if SYSTEM_PROMPT and SYSTEM_PROMPT.strip() and DEBUG_MODE:
        sys_prompt_display = SYSTEM_PROMPT[:70] + ('...' if len(SYSTEM_PROMPT) > 70 else '')
        print(f"Default System Prompt (prepended if client sends none): \"{sys_prompt_display}\"")
    elif not (SYSTEM_PROMPT and SYSTEM_PROMPT.strip()) and DEBUG_MODE:
        print(f"Default System Prompt: Not set or ignored (was '{SPECIFIC_SYSTEM_PROMPT_TO_IGNORE}').")

    if MAX_HISTORY_MESSAGES == -1:
        print("History Trimming: Disabled (MAX_HISTORY_MESSAGES = -1). All messages will be sent.")
    else:
        history_info = f"Remembering last approx. {MAX_HISTORY_MESSAGES} messages (incl. system prompt if active)."
        print(history_info)

    if DEBUG_MODE:
        print("DEBUG MODE IS ON. API request bodies and other debug info will be printed.")

    print(f"")
    print("Press Ctrl+C to stop the server.")
    print("=======================================================================")

    try:
        await site.start()
        while True: await asyncio.sleep(3600)
    except KeyboardInterrupt: print("\nShutting down server...")
    except OSError as e:
        print(f"\n[Error] Could not start server (e.g., port {SERVER_PORT} already in use?): {e}")
    finally:
        if 'aiohttp_session' in app and app['aiohttp_session'] and not app['aiohttp_session'].closed:
            await app['aiohttp_session'].close()
        if 'runner' in locals() and runner: await runner.cleanup()
        print("Server shut down successfully.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt: print("\nApplication terminated by user. ")
    except SystemExit as e:
        if str(e): print(e)
        print("Application exiting due to a fatal error.")