# utils/token_counter.py

def get_token_stats(usage: dict) -> str:
    input_tokens = usage.get("prompt_tokens", 0)
    output_tokens = usage.get("completion_tokens", 0)
    total = input_tokens + output_tokens
    return f"In: {input_tokens} | Out: {output_tokens} | Total: {total}"
