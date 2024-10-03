# Check MSVC runtime version

A python script to check the MSVC runtime version of given executable files.

## Table of contents

1. [How to use](#How-to-use])
2. [Requirements](#Requirements)
3. [License](#License)

## How to use

Quick start:
```shell
python main.py <folder/file path to check>
```

The script contains the following arguments:
* **-o**, **--out**: (Optional) The csv file path to write the result. Default as msvc_runtime_result.csv.
* **-m**, **--min**: The minimum MSVC runtime version. If you set it, only the file below this version will be written to the output file. Value must be the marketing year of the MSVC runtime, e.g. 2019, 2017, 2015, etc.

For example, to filter the files which the msvc runtime version below 2017 and write the result to the *result.csv* file:
```shell
python main.py "C:/abc" -o "result.csv" -m 2017
```

## Requirements

This script use Dumpbin to check the MSVC runtime version of the executable files. You need to install the Visual Studio build tools to get the Dumpbin tool. The build tools can be installed from the Visual Studio Installer.

## License
This project is licensed under [MIT](LICENSE) license.