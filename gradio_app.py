import gradio as gr
from theme_classfication import ThemeClassifier

def get_themes(theme_list, subtitles_path, save_path):
    theme_list = theme_list.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)
    
    # remove dialouge
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    output_df = output_df[theme_list]
    
    output_df = output_df[theme_list].sum().reset_index()
    output_df.columns = ['Theme', 'Score']
    output_chart = gr.BarPlot(
        x = "Theme", 
        y = "Score",
        title = 'series themes',
        tooltip = ['Theme', 'Score'],
        vertical = False,
        width = 500,
        height = 250
        )
    return output_chart
    
def main():
    with gr.Blocks() as iface:
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1> Themes classfication (Zero shot classifiers)</h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                    with gr.Column():
                        theme_list = gr.Textbox(label="themes")
                        subtitles_path = gr.Textbox(label = "subtitles path")
                        save_path = gr.Textbox(label = "save path")
                        get_themes_button = gr.Button("Get themes")
                        get_themes_button.click(get_themes, inputs=[theme_list, subtitles_path, save_path], outputs=[plot])
                    
    iface.launch(share = True)

if __name__ == "__main__":
    main()