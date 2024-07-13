from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.tools import DuckDuckGoSearchRun


def generate_script(prompt, video_length, creativity, api_key):
    title_template = PromptTemplate(
        input_variables=["subject"],
        template="Please come with a title for a Youtube video on the {subject}."
    )

    script_template = PromptTemplate(
        input_variables=["title","DuckDuckGo_Search","duration"],
        template="Create a script for a youtube video based on this title for me. TITLE: {title} of duration: {duration} minutes using this search data {DuckDuckGo_Search}"
    )

    llm = OpenAI(temperature=creativity, openai_api_key=api_key)

    title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True)
    script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True)

    search = DuckDuckGoSearchRun()
    title = title_chain.run(prompt)
    search_result = search.run(prompt)
    script = script_chain.run(title=title, DuckDuckGo_Search=search_result, duration=video_length)

    return search_result, title, script
