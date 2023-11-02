import os
import sys
import pandas as pd


def prep_gn(BASE_DIR, x):
    speaker_to_gender = dict()
    df = pd.read_csv(os.path.join(BASE_DIR, f"{x}.tsv"), sep='\t')
    df['gender'] = df['gender'].fillna('male')
    df.sort_values(by=['client_id', 'path'], inplace=True)
    # all_audio_list = glob.glob(
    #     os.path.join(root, "clips", "*.mp3")
    # )

    with open(os.path.join("data", x, "text"), "w") as text_f, open(
        os.path.join("data", x, "wav.scp"), "w"
    ) as wav_scp_f, open(
        os.path.join("data", x, "utt2spk"), "w"
    ) as utt2spk_f:
        for idx, row in df.iterrows():
            speaker = row['client_id']
            uttid = row['path'].split(".")[0]
            # wav_path = row['path'].replace(".mp3", ".wav")
            audio_path = os.path.join(BASE_DIR, "clips", row['path'])
            gender = row['gender'][0].lower()
            transcript = row['sentence']
            # f"{speaker}-{uttid} {sph2pipe} -f sph -p -c 1 {audio_path} |\n"
            wav_scp_f.write(
                f"{speaker}-{uttid} {audio_path}\n"
            )
            text_f.write(f"{speaker}-{uttid} {transcript}\n")
            utt2spk_f.write(f"{speaker}-{uttid} {speaker}\n")
            speaker_to_gender[speaker] = gender
    with open(
        os.path.join("data", x, "spk2gender"), "w"
    ) as spk2gender_f:
        for speaker, gender in speaker_to_gender.items():
            spk2gender_f.write(f"{speaker} {gender}\n")

def prep_es(BASE_DIR):
    speaker_to_gender = dict()
    txt_file = os.path.join(BASE_DIR, "line_index.tsv")
    df = pd.read_csv(txt_file, sep="\t", header=None)
    x = "train"
    with open(os.path.join("data", x, "text"), "a") as text_f, open(
        os.path.join("data", x, "wav.scp"), "a"
    ) as wav_scp_f, open(
        os.path.join("data", x, "utt2spk"), "a"
    ) as utt2spk_f:
        for idx, row in df.iterrows():
            file_id = row[0]
            speaker = file_id.split("_")[1]
            uttid = file_id
            audio_path = os.path.join(BASE_DIR, file_id + ".wav")
            gender = 'm'
            transcript = row[1]
            wav_scp_f.write(
                f"{speaker}-{uttid} {audio_path}\n"
            )
            text_f.write(f"{speaker}-{uttid} {transcript}\n")
            utt2spk_f.write(f"{speaker}-{uttid} {speaker}\n")
            speaker_to_gender[speaker] = gender
    with open(
        os.path.join("data", x, "spk2gender"), "a"
    ) as spk2gender_f:
        for speaker, gender in speaker_to_gender.items():
            spk2gender_f.write(f"{speaker} {gender}\n")



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python data_prep.py [root] [sph2pipe]")
        sys.exit(1)
    root = sys.argv[1]
    sph2pipe = sys.argv[2]
    BASE_DIR = "../../guarani/asr1/downloads/cv-corpus-15.0-2023-09-08/gn"
    AUX_DIR = "downloads/arg_span"

    for x in ["train", "dev", "test"]:
        prep_gn(BASE_DIR, x)
        if x == "train":
            prep_es(AUX_DIR)
        
        
        
        