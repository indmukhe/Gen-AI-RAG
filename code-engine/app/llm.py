from langchain.embeddings.openai import Embeddings
from sentence_transformers import SentenceTransformer
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.extensions.langchain import (
    WatsonxLLM,
)


class MiniLML6V2EmbeddingFunctionLangchain(Embeddings):
    MODEL = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, texts):
        return MiniLML6V2EmbeddingFunctionLangchain.MODEL.encode(texts).tolist()

    def embed_query(self, query):
        return MiniLML6V2EmbeddingFunctionLangchain.MODEL.encode([query]).tolist()[0]


def get_llm():
    generate_params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: 800,
        GenParams.TEMPERATURE: 0,
        GenParams.RANDOM_SEED: 12345,
    }

    model = Model(
        model_id=ModelTypes.LLAMA_2_70B_CHAT,
        credentials={
            "apikey": "0Rs_ysQb-gXbQO8NPRX9v8ByvHyKhGJLpBDCK5zOc50P",
            "url": "https://us-south.ml.cloud.ibm.com",
        },
        params=generate_params,
        project_id="0353fa90-88c0-44d2-b6e7-ab143db3f01d",
    )

    llm = WatsonxLLM(model=model)
    return llm
