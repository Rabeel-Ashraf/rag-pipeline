import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_primary_llm():
    """Get primary LLM based on DEFAULT_MODEL setting"""
    provider = os.getenv("DEFAULT_MODEL", "openai")
    
    if provider == "deepseek":
        return ChatDeepSeek(
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY"),
            model="deepseek-chat"
        )
    else:
        return ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("MODEL_NAME", "gpt-4-turbo"),
            temperature=0.7
        )

def get_fallback_llm():
    """Get DeepSeek as fallback LLM"""
    try:
        return ChatDeepSeek(
            deepseek_api_key=os.getenv("DEEPSEEK_API_KEY"),
            model="deepseek-chat"
        )
    except Exception as e:
        print(f"DeepSeek fallback unavailable: {e}")
        # Return a basic OpenAI model as last resort
        return ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo",
            temperature=0.7
        )

def call_llm_with_fallback(prompt: str, context: str) -> str:
    """Call LLM with fallback logic"""
    # Create the full prompt
    template = """Answer the question based only on the following context:
    
    {context}
    
    Question: {question}
    
    Answer:"""
    
    prompt_template = ChatPromptTemplate.from_template(template)
    chain = prompt_template | get_primary_llm() | StrOutputParser()
    
    try:
        return chain.invoke({"context": context, "question": prompt})
    except Exception as e:
        print(f"Primary LLM failed: {e}. Trying fallback...")
        fallback_chain = prompt_template | get_fallback_llm() | StrOutputParser()
        return fallback_chain.invoke({"context": context, "question": prompt})
