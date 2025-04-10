# Yasser Hifny (yhifny@yahoo.com)
import sys
import json
import wave
from phonetiser.phonetise_Arabic import phonetise
import string 

def remove_digits(text):
    """
    Removes all digits from the given text.

    Parameters:
        text (str): The input text.

    Returns:
        str: The text without digits.
    """
    return ''.join(char for char in text if not char.isdigit())

def remove_punctuation(text):
    """
    Remove "?", "!", and "." from the input text.
    
    Args:
        text (str): The input text.
        
    Returns:
        str: The text with specified punctuation removed.
    """
    return text.translate(str.maketrans('', '', string.punctuation))

#from a-elrawy github
def get_wav_duration(filepath):
    try:
        with wave.open(filepath, 'r') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            return round(duration, 2)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def create_manifest(csv_filename, dataset_path):
    manifest_file = f'{csv_filename}.json'

    with open(csv_filename, 'r', encoding='utf-8') as csv_file:
        with open(manifest_file, 'w') as json_file:
            line = csv_file.readline().strip()  # Read only the first line
            if not line:
                print("CSV file is empty.")
                return
            
            fields = line.split(',')
            file_id = fields[0]
            print("file id hereeeeeeeeeeeeeeeeeeee",file_id)
            text = " ".join(fields[1:])
            
            audio_path = f"{dataset_path}/{file_id.strip()}.wav"
            #print(remove_punctuation(text))
            
            transcription = "<sil> " + " ".join(phonetise(text)[1]).replace("sil", "<sil>")
            transcription = remove_digits(transcription)
            print("transcript: ",transcription)
            duration = get_wav_duration(audio_path)
            
            if duration is not None:
                manifest_data = {
                    "audio_filepath": audio_path,
                    "text": transcription,
                    "duration": duration,
                    "utf8_text": text
                }

                json.dump(manifest_data, json_file)
                json_file.write('\n')

csv_filename = sys.argv[1]
dataset_path = sys.argv[2]
create_manifest(csv_filename, dataset_path)