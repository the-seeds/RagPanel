import os
import gradio as gr
from ...save_env import save_to_env


def create_splitter_tab():
    with gr.Blocks() as demo:
        with gr.Row():
            path = gr.Textbox(info="path of your splitter (from hugging face or local), use tiktoken if empty",
                              value=os.getenv('HF_TOKENIZER_PATH', "01-ai/Yi-6B-Chat"),
                              label="splitter path",
                              scale=3)
            path.change(save_to_env, [gr.State("HF_TOKENIZER_PATH"), path])
            chunk_size = gr.Number(info="the max size of each document chunk",
                                   value=os.getenv('DEFAULT_CHUNK_SIZE', "300"),
                                   label="chunk size",
                                   step=50, 
                                   scale=2)
            chunk_size.change(save_to_env, [gr.State("DEFAULT_CHUNK_SIZE"), chunk_size])
            chunk_overlap = gr.Number(info="the size of overlap between document chunks",
                                      value=os.getenv('DEFAULT_CHUNK_OVERLAP', "30"),
                                      label="chunk overlap",
                                      step=10, 
                                      scale=2)
            chunk_overlap.change(save_to_env, [gr.State("DEFAULT_CHUNK_OVERLAP"), chunk_overlap])

    return demo
    