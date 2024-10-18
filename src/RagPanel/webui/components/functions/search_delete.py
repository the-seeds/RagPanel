import gradio as gr
import pandas as pd

def create_search_delete_tab(engine, search_result_state):
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                threshold_slider = gr.Slider(minimum=0,
                                             maximum=2,
                                             value=1, 
                                             step=0.02,
                                             label="threshold",
                                             info="results with Euclidean distance greater than the threshold will be filtered")
                top_k_slider = gr.Slider(minimum=1, 
                                         maximum=32,
                                         value=5,
                                         step=1,
                                         label="top_k",
                                         info="top k document chunks with the smallest Euclidean distance will be retrieved")
            search_box = gr.Textbox(label="query",
                                    lines=10,
                                    scale=3)

        with gr.Row():
            search_btn = gr.Button("search file")
            delete_btn = gr.Button("delete")

        search_btn.click(engine.search,
                         [search_box, threshold_slider, top_k_slider],
                         search_result_state)

    @gr.render(inputs=search_result_state, triggers=[search_result_state.change])
    def show_search_results(docs: pd.DataFrame):
        if any(docs):
            with gr.Row():
                checkbox = gr.Checkboxgroup(choices=docs["id"].tolist(), 
                                            label="select file to delete")
                gr.DataFrame(value=docs)
                delete_btn.click(engine.delete,
                                 [checkbox, search_result_state],
                                 search_result_state)
        else:
            gr.Warning("No matching docs")
    return demo