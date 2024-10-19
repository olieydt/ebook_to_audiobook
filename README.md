# Ebook to basic audiobook

Convert an english epub to an "audiobook", basically it is read in a non robotic manner. Each chapter is converted to a single .mp3 file in the output folder provided. The voice is the best I could easily find, i.e. `tts_models/en/ljspeech/tacotron2-DDC_ph` of the `coqui-tts` project.

### Installation guide
1. Install conda at [Conda](https://docs.anaconda.com/miniconda/)
2. Install ffmpeg and make it available on $PATH, ex: `brew install ffmpeg`
3. `conda create --name ebook_to_audiobook --file requirements.txt`
4. `conda activate ebook_to_audiobook`
5. `python main.py -h`


### Example usage
`python main.py -i "myfavbook.epub" -o "/home/user/myfavdirectory"`