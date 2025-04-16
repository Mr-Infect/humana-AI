import time
from llama_cpp import Llama
from model.prompt_builder import build_prompt

MODEL_PATH = "models/local-gpt-model/mistral.gguf"
_llm = None

def load_model():
    global _llm
    if _llm is None:
        _llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=4096,
            n_gpu_layers=-1,
            n_threads=12,
            n_batch=512,
            use_mlock=True,
            use_mmap=True,
            verbose=False
        )
    return _llm

def run_inference(prompt: str) -> dict:
    llm = load_model()
    full_prompt = build_prompt(prompt)
    start = time.time()
    result = llm(full_prompt, max_tokens=512, stop=["</s>"])
    end = time.time()
    return {
        "response": result["choices"][0]["text"].strip(),
        "tokens": result["usage"],
        "latency": round(end - start, 2)
    }
