from langchain_openai import ChatOpenAI

api_key = "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"

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