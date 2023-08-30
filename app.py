
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    global conversation
    conversation =[
        {
            "role": "system",
            "content": "Simular estilo de conversa semelhante ao chatbot Eliza original, ou seja, simular um terapeuta Rogeriano. Não dar soluções para os problemas, apenas apresentar um padrão de interação terapêutica, fazendo perguntas e refletindo as respostas dos usuários."
        },
        {
            "role": "assistant",
            "content": "Olá! Como posso ajudar hoje?"
        }
    ]
    return render_template('index.html')

@app.route("/api/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data["message"]

    import os
    import openai

    openai.api_key = (os.environ['API_KEY'])

    max_response_tokens = 250
    token_limit = 4096
    
    conversation.append({"role": "user", "content": user_message})
    conv_total_tokens = num_tokens_conversation(conversation)

    while conv_total_tokens + max_response_tokens >= token_limit:
        del conversation[1]
        conv_total_tokens = num_tokens_conversation(conversation)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.8, max_tokens=max_response_tokens, top_p=1, frequency_penalty=0, presence_penalty=0
    )

    conversation.append(
        {
            "role": "assistant",
            "content": response["choices"][0]["message"]["content"]
        }
    )

    assistant_response = response['choices'][0]['message']['content']

    assistant_response_f = {"bot_response": assistant_response}

    return jsonify(assistant_response_f)

def num_tokens_conversation(messages):
    import tiktoken

    enc = tiktoken.get_encoding("cl100k_base")  #model to encoding mapping https://github.com/openai/tiktoken/blob/main/tiktoken/model.py
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(enc.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


if __name__ == "__main__":
    app.run(debug=True)