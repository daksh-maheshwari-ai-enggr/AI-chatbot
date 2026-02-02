from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()

llm=ChatOpenAI(
    model="gpt-4.1-mini"
)

class chatbot(TypedDict):
    msgs:Annotated[list[BaseMessage],add_messages]

def abc(state:chatbot):
        question=state['msgs']
        answer=llm.invoke(question)

        return {'msgs':[answer]}

Checkpointer=InMemorySaver()

graph=StateGraph(chatbot)

graph.add_node('giving_response',abc)

graph.add_edge(START,'giving_response')
graph.add_edge('giving_response',END)

backend=graph.compile(checkpointer=Checkpointer)

# config1 = {"configurable": {"thread_id": "1"}}

#  result = backend.invoke({
#      "msgs": [HumanMessage(content="What is the capital of India?")]
#  },config=config1)['msgs'][-1].content


# while True:
#       user_msg=input("Type here:")
#       print("User: "+user_msg)

#       if user_msg.strip().lower() in ['bye','close','quit','exit']:
#             print("Bye,Have a good day")
#             break
      
#       result=backend.invoke({"msgs":[HumanMessage(content=user_msg)]},config=config1)
#       result1=result['msgs'][-1].content
      
#       print("AI: ",result1)



