# WavText5K
This repository contains WavText5K crawl from [Audio Retrieval with WavText5K and CLAP Training](link). The repository provides .csv containing metadata like descriptions, titles, tags and python script to download and resample the audio files. 

## Setup
- The setup assumes [Anaconda](https://www.anaconda.com) is installed
- Open the anaconda terminal and follow the below commands. The symbol `{..}` indicates user input. 
```shell
> git clone https://github.com/microsoft/WavText5K.git
> cd WavText5K
> conda create -n wavtext python=3.8
> conda activate wavtext
> pip install -r requirements.txt
> python process.py --csv_path WavText5K.csv --save_folder_path WavText5K --resample_rate {sampling rate} --processes {no. of process}
```

## Citation


## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
