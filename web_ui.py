import gradio as gr
from dotenv import load_dotenv


load_dotenv()


from src import Engine
import pandas as pd
from subprocess import Popen

load_dotenv()

def info_fn():
    gr.Info("file uploaded")


def delete_docs(ids: list, docs: pd.DataFrame):
    for doc_id in ids:
        engine.delete_by_id(doc_id)

    docs = docs[~docs["id"].isin(ids)]
    return docs

def launch(filepath, action):
    if filepath and action:
        command = f"python ./api_demo/launch.py --config {filepath} --action {action}"
        Popen(command, shell=True)

        gr.Info("Success")
        

if __name__ == '__main__':
    engine = Engine()

    with gr.Blocks() as demo:
        result_state = gr.State()

        # TODO:增加新建接口，可以输入名字新建数据库，可调用engine.new_store
        # TODO:增加删除接口，可以根据名字删除某个数据库，可调用engine.rm_store
        # TODO:调用engine.change_to来同步选择
        dropdown = gr.Dropdown(
            choices=engine.store_names,
            label="Select database",
            allow_custom_value=True
        )
        with gr.Tab("Launch"):
            with gr.Row(equal_height=False):
                config_file = gr.File(
                    file_count="single",
                    file_types=[".yml", "yaml"],
                    label="Config file"
                )

                action = gr.Radio(["build", "launch", "dump"], label="Parameter", info="action")
            launch_btn = gr.Button("Launch")
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
                slider = gr.Slider(1, 10, step=1, label="top_k")

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


        insert_btn.click(engine.insert, file, None).success(info_fn, None, None)

        search_btn.click(engine.search, [search_box, slider], result_state)

        replace_btn.click(engine.replace, [replace_content, file], None)
        
        launch_btn.click(launch, [config_file, action], None)
         
    demo.launch()
          