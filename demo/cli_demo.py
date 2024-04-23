import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


model_name_or_path = "model/zhanghuiATchina/zhangxiaobai_shishen2_full"

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map='auto')
model = model.eval()

system_prompt = """我是食神周星星的唯一传人张小白，我什么菜都会做，包括黑暗料理，您可以问我什么菜怎么做---比如酸菜鱼怎么做?，我会告诉你具体的做法。"""

messages = [(system_prompt, '')]

print("=============Welcome to InternLM chatbot, type 'exit' to exit.=============")

while True:
    input_text = input("User  >>> ")
    input_text = input_text.replace(' ', '')
    if input_text == "exit":
        break
    response, history = model.chat(tokenizer, input_text, history=messages)
    messages.append((input_text, response))
    print(f"robot >>> {response}")