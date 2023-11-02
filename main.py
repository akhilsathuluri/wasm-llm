# create a simple streamlit app that has a chatbox and a button to send the message

import streamlit as st
import pywasm
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from wasmtime import *

# st.title("Welcome to auto-web")

# create a sidebar to input a text field
with st.sidebar:
    st.write("Enter your message below:")
    message = st.text_input("Message", "Type here...")
    if st.button("Send"):
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
@st.cache_resource
def load_models():
    # This function will only be run the first time it's called
    tokenizer = AutoTokenizer.from_pretrained("./models/codegen25-7b-instruct", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("./models/codegen25-7b-instruct")
    return tokenizer, model

tokenizer, model = load_models()

# Use this to load a feature compiled in wasm
def add_button_online(st):
    st.write("This is an online button")
    if st.button("Click me", "online"):
      print("received prompt .... ")
      # read the input message
      comment = message
      st.write("received prompt....")

      # inputs = tokenizer("#include <iostream> \n using namespace std;\n int hello(){//print hello world\n", return_tensors="pt")

      # pad the prompt
      prefix = "#include <stdio.h> \n int hello(){//"
      suffix = "return 0;}"
      # prompt = prefix + comment + "\n" + "<|endoftext|>" + "<sep>" + "<mask_1>" + suffix 
      prompt = prefix + comment + "\n" 
      st.write(prompt)

      inputs = tokenizer(prompt, return_tensors="pt")
      # input_ids = tokenizer(prompt, return_tensors="pt").input_ids
      sample = model.generate(**inputs, max_length=128)
      # sample = model.generate(input_ids, max_length=128)
      print(tokenizer.decode(sample[0]))
      output = tokenizer.decode(sample[0])

      print("printing the code onto drive .....")
      #print output to a file
      with open('file.c', 'w') as f:
        f.write(output.split("###")[0])
      
      print("compiling the code ....")
      # compile the file
      os.system("""emcc -Os -s STANDALONE_WASM -s EXPORTED_FUNCTIONS="['_hello']" --no-entry file.c -o file.wasm""")

      print("executing the code ....")
      # runtime = pywasm.load("./file.wasm")
      # r = runtime.exec('hello')
      engine = Engine()
      store = Store(engine)
      module = Module.from_file(engine, "./file.wasm")
      linker = Linker(engine)
      linker.define_wasi()
      wasi = WasiConfig()
      wasi.inherit_stdout()
      store.set_wasi(wasi)
      instance = linker.instantiate(store, module)
      exports = instance.exports(store)
      
      exports["hello"](store)

      # st.write(r)
      st.write("Executed, check terminal!")

add_button_online(st)
