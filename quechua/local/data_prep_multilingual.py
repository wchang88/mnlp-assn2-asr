import os
import sys
import pandas as pd
import random


if __name__ == "__main__":
   if len(sys.argv) != 3:
      print("Usage: python data_prep.py [root] [sph2pipe]")
      sys.exit(1)
   root = sys.argv[1]
   sph2pipe = sys.argv[2]
   BASE_DIR = "../../quechua/asr1/downloads/IWSLT2023_Quechua_data/que_spa_clean" # TODO: change for final submission
   ES_PE_F = "downloads/es_pe_f"
   ES_PE_M = "downloads/es_pe_m"
   # dev->test, part of train->dev
   speaker_to_gender = {
      'JUAN_JOSE': 'm', 
      'ANA': 'f', 
      'ANTONIO': 'm', 
      'TOMAS': 'm', 
      'MANUEL': 'm', 
      'CHRISTOPHER': 'm', 
      'ENRIQUE': 'm', 
      'IRMA': 'f', 
      'JULIA': 'f', 
      'ALFREDO': 'm', 
      'RICHARD': 'm', 
      'SIMON': 'm', 
      'FERNANDA': 'f', 
      'CELIA': 'f', 
      'RENZO': 'm', 
      'JACOBO': 'm', 
      'FRANCO': 'm', 
      'MARCOS': 'm', 
      'IVAN': 'm', 
      'ESTEBAN': 'm', 
      'JAIME': 'm', 
      'MARIO': 'm', 
      'JESUS': 'm', 
      'CAMILO': 'm', 
      'LUZ': 'm', 
      'RUTH': 'f', 
      'RUBEN': 'm', 
      'SANTI': 'm', 
      'INES': 'f', 
      'NICO': 'm', 
      'JULIO': 'm', 
      'NURIA': 'f', 
      'ALBERTO': 'm', 
      'LUIS': 'm', 
      'MAURICIO': 'm', 
      'PEDRO': 'm', 
      'MIGUEL': 'm', 
      'RICARDO': 'm', 
      'JOSEF': 'm'
   }

   for x in ["train-dev_train", "valid-test"]:
      # speaker_ids = set()
      raw, data = x.split("-")
      segments_filepath = os.path.join(BASE_DIR, raw, 'txt', 'segments')
      transcript_filepath = os.path.join(BASE_DIR, raw, 'txt', raw + ".que")

      tgts = data.split("_")
      if len(tgts) == 2:
         splits = [125] # take the first 125 as dev out of train
      else:
         splits = [0]
      
      with open(
            segments_filepath, 'r'
         ) as meta_f, open(
            transcript_filepath, 'r'
         ) as transcript_f:
            meta_lines = meta_f.readlines()
            transcript_lines = transcript_f.readlines()

            alignments = list(zip(meta_lines, transcript_lines))
            random.shuffle(alignments)
            if len(tgts) == 2:
               splits = [(0,125), (125,len(meta_lines))]
            else:
               splits = [(0,len(meta_lines))]

            for tgt,split_idx in zip(tgts,splits):
               subset = alignments[split_idx[0]:split_idx[1]]
               speaker_ids = set()
               with open(
                     os.path.join("data", tgt, "text"), "w"
                  ) as text_f, open(
                     os.path.join("data", tgt, "wav.scp"), "w"
                  ) as wav_scp_f, open(
                     os.path.join("data", tgt, "utt2spk"), "w"
                  ) as utt2spk_f:
                     for line,transcript in subset:
                        metadata = line.split()
                        audio_file = metadata[0]
                        uttid = audio_file.split("/")[1].split(".")[0]
                        audio_path = os.path.join(BASE_DIR, raw, audio_file)
                        speaker_id = "_".join(metadata[1:len(metadata)-2]) # to catch speaker with multi-word names
                        speaker_ids.add(speaker_id)
                  
                        wav_scp_f.write(f"{speaker_id}-{uttid} {audio_path}\n")
                        text_f.write(f"{speaker_id}-{uttid} {transcript.strip()}\n")
                        utt2spk_f.write(f"{speaker_id}-{uttid} {speaker_id}\n")  

               with open(os.path.join("data", tgt, "spk2gender"), "w") as spk2gender_f:
                  for speaker_id in speaker_ids:
                        spk2gender_f.write(f"{speaker_id} {speaker_to_gender[speaker_id]}\n")

   for ES_PE in [ES_PE_F, ES_PE_M]:
      speaker_to_gender = dict()
      txt_file = os.path.join(ES_PE, "line_index.tsv")
      df = pd.read_csv(txt_file, sep="\t", header=None)
      x = "train"
      with open(os.path.join("data", x, "text"), "a") as text_f, open(
         os.path.join("data", x, "wav.scp"), "a"
      ) as wav_scp_f, open(
         os.path.join("data", x, "utt2spk"), "a"
      ) as utt2spk_f:
         for idx, row in df.sample(frac=0.1, random_state=3846).iterrows():
               file_id = row[0]
               speaker = "_".join(file_id.split("_")[:1])
               uttid = file_id
               audio_path = os.path.join(ES_PE, file_id + ".wav")
               gender = ES_PE.split("_")[-1].lower()
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
