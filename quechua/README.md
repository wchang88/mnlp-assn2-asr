This is the directory for Quechua.

## Steps to run Quechua ASR training in ESPnet

### 0. Follow the setup for ESPnet

### 1. Setup the directory for Quechua in ESPnet

#### Run ESPnet's setup script to set up the directory structure

```
cd espnet
egs2/TEMPLATE/asr1/setup.sh egs2/quechua/asr1
cd egs2/quechua/asr1
```

#### Download the data and decompress it

For Quechua, the dataset we used was https://github.com/Llamacha/IWSLT2023_Quechua_data

```
mkdir downloads
# however you get the data into the downloads folder
# however you decompress the downloaded data, if necessary
cd ..
echo "" >> db.sh
echo "QUECHUA=<absolute path to the dataset>" >> db.sh
```

##### For multilingual training, also do the following

For multilingual training, we used both the male and female splits from the Peruvian Spanish dataset from OpenSLR (https://www.openslr.org/73/).

Run

```
cd downloads
mkdir es_pe_f
mkdir es_pe_m
wget <url for the male dataset>
wget <url for the female dataset>
unzip -q <male_speaker_dataset_filename> -d ./es_pe_m
unzip -q <femal_speaker_dataset_filename> -d ./es_pe_f
cd ..
```

### 2. Copy over the configuration files and data preparation files

#### Configuration files

```
mkdir conf
cd conf
# copy over the relevant files
cd ..
```

Copy over the configuration files under `baseline`, `pretrained`, `multilingual` depending on which training you want to do.

#### Data preparation files

```
cd local
# copy over the relevant files
cd ..
```

Copy over the data prep files under `baseline`, `pretrained`, `multilingual` depending on which training you want to do. You may have to open `data.sh` and make appropriate changes for multilingual training.

### 3. Run the scripts

First copy over the relevant `run.sh` files from `baseline`, `pretrained`, `multilingual` depending on which training you want to do. This should be on the outermost level just under the `quechua/asr1/` directory

```
./run.sh
```

You can follow the tutorials in ESPnet for more information on how to run different stages.

If you encounter any issues with permissions, run `chmod +x <file_name>` on the scripts that have permission errors.
