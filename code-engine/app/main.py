import copy
from fastapi import FastAPI, APIRouter
from langchain.vectorstores import FAISS
from .llm import MiniLML6V2EmbeddingFunctionLangchain, get_llm
from .utils import GenerateRequest, GenerateResponse, openapi
from .prompt import QUESTION_TEMPLATE, TELL_ME_MORE_TEMPLATE
import re

llm = get_llm()
app = FastAPI()
router = APIRouter()

db = FAISS.load_local("db", MiniLML6V2EmbeddingFunctionLangchain())

app.add_api_route("/openapi", endpoint=openapi)


@app.get("/")
def hello():
    return {"generated_text": "Hello"}




def build_prompt(messages):
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
    BOS, EOS = "<s>", "</s>"
    DEFAULT_SYSTEM_PROMPT = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content."
    if not messages:
        return None
    messages_ = copy.deepcopy(messages)
    messages_ = [x["a"] if "a" in x else x["u"] for x in messages_]
    messages_[0] = "".join([B_SYS, DEFAULT_SYSTEM_PROMPT, E_SYS, messages_[0]])
    messages_list = []
    for i, x in enumerate(messages_):
        if i % 2 == 0:
            messages_list.append(f"{BOS}{B_INST} {x.strip()} {E_INST}")
        else:
            messages_list.append(f" {x.strip()} {EOS}")
    prompt = "".join(messages_list)
    # prompt = prompt + "\n"
    return prompt


@app.post("/api/generate")
def generate(request: GenerateRequest) -> GenerateResponse:
    if request.history:
        print(request.history)
    k_docs = request.k_docs
    messages = request.history

    question = messages[-1]["u"].strip()
    if "tell me more" in question:
        search_results = db.similarity_search(messages[-3]["u"].strip(), k=1)
        context = "\n\n".join([f"Context Document {e+1}:\n"+x.page_content for e, x in enumerate(search_results)])
        messages[-1]["u"] = TELL_ME_MORE_TEMPLATE.replace(
            "{{context}}", context
        ).replace("{{question}}", messages[-3]["u"])
    else:
        search_results = db.similarity_search(question, k=k_docs)
        context = "\n\n".join([f"Context Document {e+1}:\n"+x.page_content for e, x in enumerate(search_results)])
        messages[-1]["u"] = QUESTION_TEMPLATE.replace("{{context}}", context).replace(
            "{{question}}", question
        )
    prompt = build_prompt(messages)
    # if not prompt:
    #     return {
    #         "generated_text": "I'm afraid I don't understand. Please rephrase your question."
    #     }
    generated_text = llm(prompt).strip().replace("•", "*").replace("```", "")
    generated_text = re.sub("Context Document \d", "documentation", generated_text)
    generated_text = re.sub("Context Documents \d-\d", "documentation", generated_text)
    # if "I do not know" or "not sure" not in generated_text:
    #     source = "\n\n<br><hr>Source:<br><ul><li>" + "</li><li>".join(
    #         dict.fromkeys([x.metadata["filename"] for x in search_results[:1]])
    #     ) + "</li></ul>"
    #     generated_text = generated_text + source
    print({"prompt": prompt, "generated_text": generated_text})
    return {"generated_text": generated_text}
