# Demo 01: Azure OpenAI Function calling
# Executa acest demo cu comanda: streamlit run 01-demo-functions.py

import json
import time
import os
import random
from openai import AzureOpenAI
import streamlit as st
from dotenv import load_dotenv

st.set_page_config(page_title="Playing with OpenAI functions")
st.title("How to use OpenAI functions")
"""
This bot is enabled with web search using OpenAI Function Calls. It uses status panel prototype for rendering function call and response.
The user can decide via checkbox in sidebar whether to run functions automatically or inspect/edit and approve function calls before running.
"""
check_functions = st.sidebar.checkbox(
    "Edit and approve function calls before running?", value=False
)

# Configuration

load_dotenv(override=True)  # take environment variables from .env file
AZURE_OPENAI_API_ENDPOINT = os.getenv("AZURE_OPENAI_API_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")

client = AzureOpenAI(
    # https://learn.microsoft.com/azure/ai-services/openai/reference#rest-api-versioning
    api_version="2024-06-01",
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_API_ENDPOINT,
    azure_deployment=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "order_status",
            "description": "Get the status for an order based on its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The id of the order to get the status for",
                    },
                },
                "required": ["order_id"],
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "loan_simulation",
            "description": "Simulate a personal loan. Return monthly payments and total amount paid based on amount borrowed, duration in months, and annual interest rate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount_borrowed": {
                        "type": "integer",
                        "description": "The amount borrowed",
                    },
                    "duration_in_months": {
                        "type": "integer",
                        "description": "The loan duration in months, default value is 12",
                    }
                },
                "required": ["amount_borrowed"],
            },
        }
    }
]

def order_status(order_id):
    time.sleep(1) # Simulate a delay

    # Simulate a random order status
    return random.choice(["shipped", "delivered", "in transit", "delayed"])

def loan_simulation(amount_borrowed, duration_in_months, annual_interest_rate):
    # Convert annual interest rate to monthly and in decimal form
    monthly_interest_rate = (annual_interest_rate / 100) / 12

    # Calculate monthly payment
    if monthly_interest_rate > 0:
        monthly_payment = (amount_borrowed * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -duration_in_months)
    else:
        monthly_payment = amount_borrowed / duration_in_months

    # Calculate total amount paid
    total_amount_paid = monthly_payment * duration_in_months

    return f'monthly payment is {monthly_payment}, total amount you pay is {total_amount_paid}'

# This is callback function used further down for user to explicitly approve function call
def save_fn_call():
    tool_calls = st.session_state.tool_calls
    st.session_state.messages.append(
        {
            "role": "assistant",
            "tool_calls": tool_calls,
        }
    )

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Cum te pot ajuta azi?"}]

# Display session_state messages for reference / debugging
# st.json(st.session_state.messages, expanded=False)

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "system":
        pass
    elif msg["role"] == "user":
        st.chat_message(msg["role"]).write(msg["content"])
    elif msg["role"] == "assistant":
        if i == 0 or st.session_state.messages[i - 1]["role"] != "function":
            last_asst = st.chat_message("assistant")
            with last_asst:
                status_space = st.container()
        with last_asst:
            if content := msg.get("content", ""):
                st.write(content)
            elif tool_calls := msg.get("tool_calls", {}):
                fn = tool_calls[0].function
                last_fn = fn.name
                last_status = status_space.status(f"Executing `{last_fn}`")
                last_status.code(fn.arguments, language="json")
    elif msg["role"] == "tool":
        if msg["name"] != last_fn:
            st.error("Unexpected function response")
            st.stop()
        last_status.update(state="complete")
        last_status.write(msg["content"])

# Do we have a function ready to execute?
new_function_response = False
if tool_calls := st.session_state.messages[-1].get("tool_calls", {}):
    tool_call_id = tool_calls[0].id
    fn = tool_calls[0].function
    func_name = fn.name
    if func_name == "loan_simulation":
        amount_borrowed = json.loads(fn.arguments).get("amount_borrowed", "")
        duration_in_months = json.loads(fn.arguments).get("duration_in_months", 12)
        results = loan_simulation(amount_borrowed, duration_in_months, 6)
        last_status.write(results)
        st.session_state.messages.append(
            {"role": "tool", "tool_call_id": tool_call_id, "name": func_name, "content": results}
        )
        last_status.update(state="complete")
    elif func_name == "order_status":
        order_id = json.loads(fn.arguments).get("order_id", "")
        results = order_status(order_id)
        last_status.write(results)
        st.session_state.messages.append(
            {"role": "tool", "tool_call_id": tool_call_id, "name": func_name, "content": results}
        )
        last_status.update(state="complete")
    else:
        st.error("Unexpected function name")
        st.stop()
    new_function_response = True

if prompt:  # last was a new user message, we need a new asst chat bubble
    last_asst = st.chat_message("assistant")

if prompt or new_function_response:
    with last_asst:
        response = ""
        status_space = st.container()
        resp_container = st.empty()
        func_name = ""
        response1 = client.chat.completions.create(
            model=AZURE_OPENAI_CHAT_DEPLOYMENT_NAME,
            messages=st.session_state.messages,
            tools=tools,
            tool_choice="auto",
            stream=False,
        )
        response_message = response1.choices[0].message
        tool_calls = response_message.tool_calls
        if content := response_message.content:
            response += content
            resp_container.markdown(response)
        if tool_calls:
            fn = tool_calls[0].function
            print(fn)
            if fn.name:
                func_name = fn.name
                func_args = ""
                status = status_space.status(
                    f"Executing `{func_name}`", expanded=check_functions
                )
                args_container = status.empty()
            if arg_delta := fn.arguments:
                func_args += arg_delta
                args_container.code(func_args, language="json")

        if func_name:
            st.session_state.pending_call = func_name
            st.session_state.pending_args = func_args
            st.session_state.tool_calls = tool_calls
            if check_functions:
                with args_container.form("args"):
                    st.text_area(
                        "Function arguments",
                        label_visibility="collapsed",
                        key="pending_args",
                    )
                    st.form_submit_button("Execute function", on_click=save_fn_call)
            else:
                # Persist pending call and rerun for auto-function run
                save_fn_call()
                st.experimental_rerun()
        elif response:
            st.session_state.messages.append({"role": "assistant", "content": response})

