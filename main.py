# create a simple streamlit app that has a chatbox and a button to send the message

import streamlit as st
import pywasm

st.title("Welcome to auto-web")

# create a sidebar to input a text field
with st.sidebar:
    st.write("Enter your message below:")
    message = st.text_input("Message", "Type here...")
    if st.button("Send"):
        # send prompt to create and compile a wasm code

        st.write("Message sent!")

# Use this to have a defined feature
def add_button_offline(st):
    st.write("This is an offline button")
    if st.button("Click me", "offline"):
        st.write("You clicked me!")

add_button_offline(st)

# Use this to load a feature compiled in wasm
# def add_button_online(st):
#     st.write("This is an online button")
#     if st.button("Click me", "online"):
#         runtime = pywasm.load("./examples/fib.wasm")
#         r = runtime.exec('fib', [10])
#         st.write(r)
#         # st.write("You clicked me!")

# add_button_online(st)

# model inference
from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("./models/codegen25-7b-instruct", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("./models/codegen25-7b-instruct")

def format(prefix, suffix):
  return prefix + "<mask_1>" + suffix + "<|endoftext|>" + "<sep>" + "<mask_1>"

prefix = "def hello_world():\n    "
suffix = "    return name"
text = format(prefix, suffix)
input_ids = tokenizer(text, return_tensors="pt").input_ids
generated_ids = model.generate(input_ids, max_length=128)
st.write(tokenizer.decode(generated_ids[0], skip_special_tokens=False)[len(text):])


