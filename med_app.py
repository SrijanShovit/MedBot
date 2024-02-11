from pymed import PubMed
from typing import List
from haystack import component
from haystack import Document
from haystack.components.generators import HuggingFaceTGIGenerator
from dotenv import load_dotenv
import os
from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
import gradio as gr
import time
import cProfile


load_dotenv()
os.environ['HUGGINGFACEHUB_API_TOKEN'] = os.getenv('HUGGINGFACEHUB_API_TOKEN')


pubmed = PubMed(
    tool="Haystack2.0Prototype",
    email="dummayemail@gmail.com"
)


def documentize(article):
    return Document(
        content=article.abstract,
        meta = {'title':article.title,
                'keywords':article.keywords                
            }
    )


@component
class PubMedFetcher():

    @component.output_types(articles=List[Document])
    def run(self,queries:list[str]):
        cleaned_queries = queries[0].strip().split('\n')

        articles = []
        try:
            for query in cleaned_queries:
                response = pubmed.query(query,max_results=1)
                documents = [documentize(article) for article in response]
                articles.extend(documents)
        
        except Exception as e:
            print(e)
            print(f"Couldn't fetch articles for queries: {queries}")

        results = {'articles':articles}
        return results


keyword_llm = HuggingFaceTGIGenerator("mistralai/Mistral-7B-Instruct-v0.2")
keyword_llm.warm_up()

llm = HuggingFaceTGIGenerator("mistralai/Mistral-7B-Instruct-v0.2")
llm.warm_up()


keyword_prompt_template = """
Your task is to convert the following question into 3 keywords that can be used to find relevant medical research papers on PubMed.
Here is an examples:
question: "What are the latest treatments for major depressive disorder?"
keywords:
Antidepressive Agents
Depressive Disorder, Major
Treatment-Resistant depression
---
question: {{ question }}
keywords:
"""

prompt_template = """
Answer the question truthfully based on the given documents.
If the documents don't contain an answer, use your existing knowledge base.

q: {{ question }}
Articles:
{% for article in articles %}
  {{article.content}}
  keywords: {{article.meta['keywords']}}
  title: {{article.meta['title']}}
{% endfor %}

"""


keyword_prompt_builder = PromptBuilder(template=prompt_template)

prompt_builder = PromptBuilder(template=prompt_template)

fetcher = PubMedFetcher()

pipe = Pipeline()

pipe.add_component("keyword_prompt_builder",keyword_prompt_builder)
pipe.add_component("keyword_llm",keyword_llm)
pipe.add_component("pubmed_fetcher",fetcher)
pipe.add_component("prompt_builder",prompt_builder)
pipe.add_component("llm",llm)

pipe.connect("keyword_prompt_builder.prompt","keyword_llm.prompt")
pipe.connect("keyword_llm.replies","pubmed_fetcher.queries")

pipe.connect("pubmed_fetcher.articles","prompt_builder.articles")
pipe.connect("prompt_builder.prompt","llm.prompt")



# Initialize an empty cache to store questions and answers
question_answer_cache = {}


def ask(question):
    start_time = time.time()

    if question in question_answer_cache:
        resp = question_answer_cache[question]
    
    else:
        output = pipe.run(
            data = {"keyword_prompt_builder": {"question" : question},
                    "prompt_builder":{"question":question},
                    "llm" : {
                        "generation_kwargs": {"max_new_tokens":500}
                    }})
        
        resp = output['llm']['replies'][0]
        question_answer_cache[question] = resp        
    
    
    end_time = time.time()
    time_taken = end_time - start_time   
    

    print(question,"-------------------------------------")
    
    print(f"Time taken: {time_taken:.6f} seconds")
    print(resp)
    print("-------------------------------------------")

    return resp


# Profile the ask function
cProfile.run("ask('How are mRNA vaccines being used for cancer treatment?')")




# Define Gradio interface
iface = gr.Interface(
    fn=ask,
    inputs=gr.Textbox(
        label="🔍 Ask a question",
        placeholder="💡 Type your question here...",
        lines=3
    ),
    outputs=gr.Textbox(
        label="✨ Answer",
        placeholder="💬 Answer will appear here...",
        lines=10
    ),
    title="📚 Biomedical Literature Q&A with PubMed",
    description="🔬 Ask a question about Biomedical Literature.",
    examples=[
            ["How are mRNA vaccines being used for cancer treatment?"],
            ["Suggest some Case Studies related to Pneumonia."],
            ["Tell me about HIV AIDS."],
            ["Suggest some case studies related to Autoimmune Disorders."],
            ["How to treat a COVID infected Patient?"]
        ],
    theme=gr.themes.Soft(),
    allow_flagging='never'
)

# Update examples list with cached questions
examples_with_cache = list(question_answer_cache.keys())

# Add cached questions to examples in the interface
iface.examples.extend(examples_with_cache)

iface.launch(share=True)

  