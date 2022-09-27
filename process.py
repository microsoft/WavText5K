import argparse
import logging
import multiprocessing as mp
import os
from datetime import datetime
from pathlib import Path

import glob
import librosa
from zsvision.zs_multiproc import starmap_with_kwargs
import soundfile as sf
import pandas as pd
import wget

def resample_audio(load_folder: Path, save_folder: Path, audio_path: Path, resample_rate):
    """
    Resampling one audio file.
    Inputs:
        load_folder: path of top directory of audio files to be resampled
        save_folder: Location where audio file is downloaded
        audio_path: location where to save the resampled file
        resample_rate: resample rate for the audio files
    """
    relative_path = os.path.relpath(audio_path, load_folder)
    try:
        resampled_audio_path = os.path.join(save_folder, relative_path)
        os.makedirs(os.path.sep.join(os.path.join(save_folder, relative_path).split(os.path.sep)[0:-1]), exist_ok=True)

        audio, _ = librosa.load(audio_path, sr = resample_rate)
        sf.write(resampled_audio_path, audio, resample_rate, 'PCM_24')

    except Exception as e:
        logging.info(f'File {relative_path} could not be resampled because of error {e}')


def resample_audios(load_folder: Path, save_folder: Path, logging,  resample_rate, processes):
    """
    Resampling all audio files residing within the load_folder path.
    Inputs:
        load_folder: Location where audio file to be resampled reside. The folder structure here will be mimiced at save_folder
        save_folder: Location where to save the resampled audio files
        logging: Logging module containing information about the progress of the code
        processes: Number of processes downloading audio content at
            the same time
    """
    audio_paths = glob.glob(os.path.join(load_folder,'**','*.wav'), recursive=True)
    audio_paths = [x for x in audio_paths if not any(ext in os.sep.join(x.split(os.sep)[0:-1]) for ext in ['44800','44100','16000','22050','32000'])]

    kwarg_list = []
    for audio_path in audio_paths:
        kwarg_list.append({
            "load_folder": load_folder,
            "save_folder": save_folder,
            "audio_path": audio_path,
            "resample_rate": resample_rate,
        })

    pool_func = resample_audio
    if processes > 1:
        with mp.Pool(processes=processes) as pool:
            starmap_with_kwargs(pool=pool, func=pool_func, kwargs_iter=kwarg_list)
    else:
        for idx, kwarg in enumerate(kwarg_list):
            pool_func(**kwarg)

def download_audio(save_folder: Path, file_name: Path, link: str):
    """
    download one audio file.
    Inputs:
        save_folder: folder to save audio files
        file_path: location to save the audo file
        link: link to download the audio file
    """
    audio_save_path = os.path.join(save_folder,file_name)

    try:
        wget.download(link, audio_save_path)
    except Exception as e:
        logging.info(f'File {link} could not be downloaded because of error {e}')

def download_audios(csv_path: Path, save_folder: Path, logging, processes):
    """
    Download all audio files listed in fname.csv
    Inputs:
        load_folder: Location where audio file to be resampled reside. The folder structure here will be mimiced at save_folder
        save_folder: Location where to save the resampled audio files
        logging: Logging module containing information about the progress of the code
        processes: Number of processes downloading audio content at
            the same time
    """
    fname = pd.read_csv(csv_path)
    fname = fname.iloc[0:3,:]
    download_links = list(fname['download_link'])
    file_names = list(fname['fname'])

    kwarg_list = []
    for i, link in enumerate(download_links):
        kwarg_list.append({
            "save_folder": save_folder,
            "file_name": file_names[i],
            "link": link,
        })

    pool_func = download_audio
    if processes > 1:
        with mp.Pool(processes=processes) as pool:
            starmap_with_kwargs(pool=pool, func=pool_func, kwargs_iter=kwarg_list)
    else:
        for idx, kwarg in enumerate(kwarg_list):
            pool_func(**kwarg)
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", type=Path, required=True)
    parser.add_argument("--save_folder_path", type=Path, required=True)
    parser.add_argument("--resample_rate", type=int, default=44100, choices=[44100,16000,22050,32000,44100,44800])
    parser.add_argument("--processes", type=int, default=1)

    args = parser.parse_args()

    # Create necessary folders
    os.makedirs(os.path.join(args.save_folder_path, str(args.resample_rate)), exist_ok=True)
    resample_folder_path = os.path.join(args.save_folder_path, str(args.resample_rate))
    os.makedirs(os.path.join(resample_folder_path,'logs'), exist_ok=True)
    os.makedirs(os.path.join(resample_folder_path, 'audios'), exist_ok=True)

    logging.basicConfig(filename=os.path.join(resample_folder_path,'logs',f"{datetime.now().strftime(r'%m%d_%H%M%S')}.log"), level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    logging.info(f'Creating folder {args.save_folder_path}/download')
    download_folder_path = os.path.join(args.save_folder_path, 'download')
    os.makedirs(download_folder_path, exist_ok=True)

    # Download files
    logging.info('Starting to download files')
    download_audios(args.csv_path, download_folder_path, logging, args.processes)

    # Resample files
    logging.info('Starting to resample files')
    resample_save_path = os.path.join(resample_folder_path, 'audios')
    resample_audios(download_folder_path, resample_save_path, logging, args.resample_rate, args.processes)


if __name__ == "__main__":
    main()