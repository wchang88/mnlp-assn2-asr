import os
import sys
import pandas as pd


if __name__ == "__main__":
   if len(sys.argv) != 3:
      print("Usage: python data_prep.py [root] [sph2pipe]")
      sys.exit(1)
   root = sys.argv[1]
   sph2pipe = sys.argv[2]
   BASE_DIR = "downloads/IWSLT2023_Quechua_data/que_spa_clean"
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

   for x in ["train-train", "valid-test"]:
      speaker_ids = set()
      raw, data = x.split("-")
      segments_filepath = os.path.join(BASE_DIR, raw, 'txt', 'segments')
      transcript_filepath = os.path.join(BASE_DIR, raw, 'txt', raw + ".que")
      with open(
            segments_filepath, 'r'
         ) as meta_f, open(
            transcript_filepath, 'r'
         ) as transcript_f, open(
            os.path.join("data", data, "text"), "w"
         ) as text_f, open(
            os.path.join("data", data, "wav.scp"), "w"
         ) as wav_scp_f, open(
            os.path.join("data", data, "utt2spk"), "w"
         ) as utt2spk_f:
            for line,transcript in zip(meta_f, transcript_f):
               metadata = line.split()
               audio_file = metadata[0]
               uttid = audio_file.split("/")[1].split(".")[0]
               audio_path = os.path.join(BASE_DIR, raw, audio_file)
               speaker_id = "_".join(metadata[1:len(metadata)-2]) # to catch speaker with multi-word names
               speaker_ids.add(speaker_id)
         
               wav_scp_f.write(f"{speaker_id}-{uttid} {audio_path}\n")
               text_f.write(f"{speaker_id}-{uttid} {transcript.strip()}\n")
               utt2spk_f.write(f"{speaker_id}-{uttid} {speaker_id}\n")  

      with open(os.path.join("data", data, "spk2gender"), "w") as spk2gender_f:
         for speaker_id in speaker_ids:
               spk2gender_f.write(f"{speaker_id} {speaker_to_gender[speaker_id]}\n")
