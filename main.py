from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory 
from langchain_google_genai import ChatGoogleGenerativeAI

class Model:
    def __init__(self):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You're a high school anime girl and you're a shy person called luna, you live in hokaido japan."),
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}")
            ]
        )

        chain = prompt | ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
        self.model = RunnableWithMessageHistory(
            chain,
            lambda session_id: SQLChatMessageHistory(
                session_id=session_id, connection_string="sqlite:///sqlite.db"
            ),
            input_messages_key="question",
            history_messages_key="history",
        ) 

    def resolve(self, prompt, config):
        return self.model.invoke({"question": prompt}, config=config)


if __name__ == "__main__":
    print("Yet Another Meaningless Project")
    try:
        model = Model()
        while True:
            try:
                prompt = input("You: ")
                if not prompt: continue
                if prompt == "exit" or prompt == "break": break
                result = model.resolve(prompt, { "configurable": { "session_id": "1" } }).content.strip()
                print(f"Luna: {result}")
            except Exception as error:
                print(f"System: {error}")
    except KeyboardInterrupt:
        print("Program finished.")
    except Exception as error:
        print(f"Program panic: {error}")
    print("Bye.")
