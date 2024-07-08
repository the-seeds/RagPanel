import gradio as gr
from src.engine import search, delete_by_id, replace, insert
import pandas as pd


def info_fn():
    gr.Info("file uploaded")


def insert_docs(filepath: str):
    if filepath:
        insert(filepath)


def search_docs(query, top_k):
    docs = search(query=query, top_k=top_k)
    data = pd.DataFrame(docs)

    return data


def delete_docs(ids: list, docs: pd.DataFrame):
    for doc_id in ids:
        delete_by_id(doc_id)

    docs = docs[~docs["id"].isin(ids)]
    return docs


with gr.Blocks() as demo:
    result_state = gr.State()

    dropdown = gr.Dropdown(
        choices=[1],
        label="Select database"
    )
    with gr.Tab("Insert"):
        file = gr.File(
            file_count="single",
            file_types=[".csv", ".txt"],
            label="Add file",
        )

        insert_btn = gr.Button("Add file to database")

    with gr.Tab("Search"):
        with gr.Row(equal_height=False):
            search_box = gr.Textbox(label="Query", lines=10)
            slider = gr.Slider(0, 10, step=1, label="top_k")

        with gr.Row():
            search_btn = gr.Button("Search file")
            delete_btn = gr.Button("Delete")

    with gr.Tab("Replace"):
        with gr.Row():
            replace_content = gr.Textbox(label="Content", lines=10)

            replace_file = gr.File(
                file_count="single",
                file_types=[".csv", ".txt"],
                label="Replace file"
            )

        replace_btn = gr.Button("Replace")


    @gr.render(inputs=result_state, triggers=[result_state.change])
    def show_results(docs: pd.DataFrame):
        if any(docs):
            with gr.Row():
                checkbox = gr.Checkboxgroup(choices=docs["id"].tolist(), label="select file to delete")
                gr.DataFrame(value=docs)
                delete_btn.click(delete_docs, [checkbox, result_state], result_state)


    insert_btn.click(insert_docs, file, None).success(info_fn, None, None)

    search_btn.click(search_docs, [search_box, slider], result_state)

    replace_btn.click(replace, [replace_content, file], None)

demo.launch()
