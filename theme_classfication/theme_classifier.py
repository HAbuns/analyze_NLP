import torch
from transformers import pipeline
from nltk.tokenize import sent_tokenize
import nltk
import numpy as np
import pandas as pd
import os
import sys
import pathlib

folder_path = pathlib.Path(__file__).parent.resolve()
utils_path = os.path.join(folder_path, '../')
if utils_path not in sys.path:
    sys.path.append(utils_path)

from utils import load_subtitles_dataset
nltk.download('punkt')
nltk.download('punkt_tab')

class ThemeClassifier():
    def __init__(self, theme_list):
        self.model_name = 'facebook/bart-large-mnli'
        self.device = 0 if torch.cuda.is_available() else 'cpu'
        self.theme_list = theme_list
        self.theme_classifier = self.load_model(self.device)
    def load_model(self, device):
        theme_classifiser = pipeline(
            'zero-shot-classification',
            model=model_name,
            device=device
            )
        return theme_classifiser
    def get_theme_inference(self, script):
        script_sentences = sent_tokenize(script)

        # batch sentences
        sentence_batch_size = 20
        script_batches = []
        for index in range(0, len(script_sentences),sentence_batch_size):
            sent = " ".join(script_sentences[index:index+sentence_batch_size])
            script_batches.append(sent)

        # Run model
        theme_output = self.theme_classifiser(
            script_batches,
            self.theme_list,
            multi_label=True
        )

        # Wrangle output
        themes = {}
        for output in theme_output:
            for label, score in zip(output['labels'], output['scores']):
                if label not in themes:
                    themes[label] = []
                themes[label].append(score)

        themes = {key: np.mean(np.array(value)) for key, value in themes.items()}
        return themes
    def get_themes(self, dsetpath, savepath = None):
        
        #save output if exists
        if savepath is not None and os.path.exists(savepath):
            df = df.read_csv(save_path)
            return df
        #load dataset
        df = load_subtitles_dataset(dsetpath)
        
        #run inference
        output_themes = df['script'].apply(self.get_theme_inference)
        
        themes_df = pd.DataFrame(output_themes.tolist())
        df[themes_df.columns] = themes_df
        
        #save
        if save_path:
            df.to_csv(save_path, index=False)
        return df