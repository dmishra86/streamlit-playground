import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain import FewShotPromptTemplate
from langchain.prompts.example_selector import LengthBasedExampleSelector
from dotenv import load_dotenv

load_dotenv()

def getLLMResponse(query, age_option, tasktype_option):
    llm = OpenAI(temperature=0.9)

    if age_option=="Kid":
        examples = [
            {
                "query":"what is a mobile?",
                "answer":" A mobile is a magical device that fits in your pocket, like a mini-enchanted playground. It has games, videos, and..."
            },{
                "query":"WHat are your dreams?",
                "answer": "My dreams are like colourful adventures, where I become a super hero and save the day. I dream of giggles, ice cream..."
            },{
                "query":"What are your ambitions?",
                "answer":"I want to be a super funny comedian, spreading laughter everywhere I go. I also want to be a master cookie baker."
            },{
                "query":"What happens when you get sick?",
                "answer":"When I get sick, It's like a sneaky monster visits. I feel tired, sniffy, and need lots of cuddles"
            },{
                "query":"How much do you love your dad?",
                "answer":"Oh, I love my data to the moon and the back, with sprinkles and unicorns on top! He is my super hero, my partner is silly"
            },{
                "query":"Tell me about your friend",
                "answer":"My friend is like sunshine rainbow! WE laugh play and have magical parties together. They alwasy listen, share"
            },{
                "query":"What math means to you?",
                "answer":"Math is like puzzle game, full of numbers and shapes. It helps me count my toys, build towers, and share treats"
            },{
                "query":"What is your fear?",
                "answer":"SOme time I am scared of thunderstorm and monters under my bed. But with my teddy bear by my side and lots of cud"
            }
        ]
    elif age_option=="Adult":
        examples = [
            {
                "query":"what is a mobile?",
                "answer":" A mobile, also known as a mobile phone or cell phone, is a portable electronic device used for communication. It allows you to make phone calls, send text messages, access the internet, and use various applications for tasks such as navigation, social media, and email. "
            },{
                "query":"WHat are your dreams?",
                "answer": "My dreams are to make a meaningful impact, continuously learn, and experience life's adventures to the fullest."
            },{
                "query":"What are your ambitions?",
                "answer":"My ambitions are to excel in my career, foster meaningful relationships, and contribute positively to my community."
            },{
                "query":"What happens when you get sick?",
                "answer":"When you get sick, your body's immune system works to fight off the infection, often resulting in symptoms like fever, fatigue, and inflammation. "
            },{
                "query":"How much do you love your dad?",
                "answer":"I love my dad immensely; his support, wisdom, and unconditional love have profoundly shaped who I am today."
            },{
                "query":"Tell me about your friend",
                "answer":"My friend is a remarkable person, always ready to lend a helping hand and share a good laugh. They have a unique ability to bring out the best in people, and their loyalty and kindness make them someone I truly cherish."
            },{
                "query":"What math means to you?",
                "answer":"To me, math is a language of logic and precision that helps explain the patterns and structures of the world. It's a tool for solving problems, making decisions, and understanding the universe on a deeper level."
            },{
                "query":"What is your fear?",
                "answer":"My fear is the possibility of not reaching my full potential or missing out on meaningful opportunities to make a positive impact."
            }
        ]
    elif age_option=="Senior citizen":
        examples = [
            {
                "query":"what is a mobile?",
                "answer":" A mobile phone is a handheld device that allows us to stay connected with loved ones, access information, and enjoy various forms of entertainment no matter where we are."
            },{
                "query":"WHat are your dreams?",
                "answer": "My dreams now are to see my family happy and healthy, to enjoy the simple pleasures of life, and to leave a positive legacy for future generations."
            },{
                "query":"What are your ambitions?",
                "answer":"My ambitions are to share my wisdom and experiences with others, to stay active and engaged in my community, and to cherish every moment with my loved ones."
            },{
                "query":"What happens when you get sick?",
                "answer":"When I get sick, I focus on rest and recovery, seek medical advice if needed, and take care of my health through proper nutrition and medication."
            },{
                "query":"How much do you love your dad?",
                "answer":"I loved my dad deeply; his guidance and love shaped my life profoundly, and I carry his lessons and memories with me every day."
            },{
                "query":"Tell me about your friend",
                "answer":"My friend is a steadfast companion, someone who has shared countless memories and stood by me through thick and thin. Their friendship is a precious part of my life."
            },{
                "query":"What math means to you?",
                "answer":"Math is the foundation of so many aspects of life, from managing finances to understanding the world around us. It has always been a reliable and logical companion."
            },{
                "query":"What is your fear?",
                "answer":"My fear is that I might not have enough time to do all the things I still want to accomplish and to be there for the people I love when they need me."
            }
        ]

    example_template = """
    Question:{query}
    Response:{answer}
    """

    example_prompt = PromptTemplate(
        input_variables=["query","answer"],
        template = example_template
    )

    prefix="""You are a {template_age_option}, and {template_tasktype_option}:
    Here are some examples:
    """

    suffix = """
    Question: {template_userInput}
    Response: """

    example_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=example_prompt,
        max_length=200
    )

    new_prompt_template = FewShotPromptTemplate(
        example_selector=example_selector, # use example selector instead of examples
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["template_userInput","template_age_option","template_tasktype_option"],
        example_separator="\n\n"
    )

    query = form_input
    print(new_prompt_template.format(template_userInput=query, template_age_option=age_option, template_tasktype_option=tasktype_option ))
    response = llm(new_prompt_template.format(template_userInput=query, template_age_option=age_option, template_tasktype_option=tasktype_option ))
    print(response)
    return response

st.set_page_config(page_title="Example Selector Demo APP",
                   page_icon=':Robot:',
                   layout='centered',
                   initial_sidebar_state='collapsed')
st.header("Let's do something specific. Specify what you want to do...")

form_input = st.text_area("Enter text:", height=250)
tasktype_option = st.selectbox(
    'Select the task to be performed.',
    ('Generate sales copy', 'Generate a tweet', 'Generate a product description'), key=1
)

age_option = st.selectbox(
    'Select the age group:',
    ('Kid','Adult','Senior citizen'), key=2
)

number_of_words = st.slider('Words limit', 1,200,25)

submit = st.button("Generate")


if submit:
    st.write(getLLMResponse(form_input, age_option, tasktype_option))

