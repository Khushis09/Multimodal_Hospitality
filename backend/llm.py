from langchain_openai import ChatOpenAI

api_key = "OPENROUTER_API_KEY"

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model="openai/gpt-4o-mini"
)

def generate_description(prompt):
    try:
        response = llm.invoke(
            f"Generate a luxury hotel description in a premium tone for: {prompt}"
        )
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"