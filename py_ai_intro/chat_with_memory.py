from quart import Quart, render_template, request, session
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI()
app = Quart(__name__)
app.secret_key = "SECRET_KEY"  # still needed for session handling

@app.route('/', methods=['GET'])
async def index():
    # Render the simplified chat window
    return await render_template('index.html', assistant_reply="")

@app.route('/chat', methods=['POST'])
async def chat():
    try:
        form_data = await request.form
        query = form_data['user_input']

        # Retrieve or initialize chat history (remove old system prompts)
        chat_history = session.get('chat_history', [])
        chat_history = [m for m in chat_history if m["role"] != "system"]

        # Always insert the same system prompt
        system_prompt = "You are a helpful assistant."
        chat_history.insert(0, {"role": "system", "content": system_prompt})

        # Add new user message
        chat_history.append({"role": "user", "content": query})

        # Call OpenAI
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=chat_history
        )

        assistant_response = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": assistant_response})

        # Save updated chat history back to session
        session['chat_history'] = chat_history

        return await render_template('index.html', assistant_reply=assistant_response)

    except Exception as e:
        app.logger.error(f"Error: {e}")
        return await render_template("index.html", assistant_reply="Something went wrong, please try again.")

if __name__ == "__main__":
    app.run(debug=True)
