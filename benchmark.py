from backend.service.chatbot.chill_chatbot import ChillChatBot
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

from pathlib import Path
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity

pdf_path = "backend/data/"
question_path = "benchmark/questions.txt"
answer_path = "benchmark/answers.txt"

def measure_relevance(response, query):
    embeddings = similarity_model.encode([response, query])
    return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

def measure_groundedness(response, source):
    embeddings = similarity_model.encode([response, source])
    return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

def measure_accuracy(response, answer):
    embeddings = similarity_model.encode([response, answer])
    return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

# TODO: rewrite main to measure accuracy using Gemini

def LLM_measure_accuracy(query:str, response: str, answer: str, llm: genai.GenerativeModel):
    prompt = (
        f"I trained a large language model to answer the following question: {query}\n"
        f"I need you to evaluate the given answer against correct answer.\n"
        f"Given answer is: {response}\n"
        f"Correct answer is: {answer}\n"
        f"Please rate the given answer on a scale of 1 to 5, where 1 is completely wrong and 5 is completely correct.\n"
        f"Do not include anything other than the number from 1 to 5 in your response.\n"
        f"ANSWER:"
    )

    reply = llm.generate_content(prompt)

    return reply.candidates[0].content.parts[0].text

if __name__ == "__main__":
    # assert pathlib.Path(".env").exists()
    # load_dotenv()
    # assert os.getenv("GEMINI_API_KEY")

    # genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # model_name = "gemini-1.5-flash"
    # model = genai.GenerativeModel(model_name, generation_config=genai.GenerationConfig(
    #     max_output_tokens=1000,
    #     temperature=0.1,
    # ))

    similarity_model = SentenceTransformer('lang-uk/ukr-paraphrase-multilingual-mpnet-base')
    chatbot = ChillChatBot(list(Path(pdf_path).glob("*.pdf")))
    with open(question_path, "r") as f:
        questions = f.readlines()

    with open(answer_path, "r") as f:
        answers = f.readlines()

    mean_groundness = 0
    mean_relevance = 0
    mean_accuracy = 0

    for question, answer in tqdm(zip(questions, answers), total=len(questions)):
        result = chatbot.RAG_pipeline(question.strip())
        response, retrieved_documents = result["response"], result["retrieved_docs"]
        source_text = "\n\n".join([doc.page_content for doc in retrieved_documents])

        print(f"Query: {question.strip()}")
        print(f"Response: {response}")
        print(f"Actual Answer: {answer.strip()}")
        mean_groundness += measure_groundedness(response, source_text)
        mean_relevance += measure_relevance(response, question.strip())
        mean_accuracy += measure_accuracy(response, answer.strip())


    mean_groundness /= len(questions)
    mean_relevance /= len(questions)
    mean_accuracy /= len(questions)

    print(f"Groundness: {mean_groundness:.4f}, Relevance: {mean_relevance:.4f}, Accuracy: {mean_accuracy:.4f}")
