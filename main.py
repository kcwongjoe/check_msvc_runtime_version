
import os
import pathlib
import argparse

from tqdm import tqdm

from msvc_runtime_getter import MSVCRuntimeGetter


if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='Check all the VC runtime version in a folder')
    parser.add_argument(
        'folder_path', type=str,
        help='The path to the folder to check, it can be a exe or dll file as well.')
    parser.add_argument(
        '-o','--out', action='store', type=str, nargs=1,
        default='msvc_runtime_result.csv', help='The csv file path to write the result.')
    parser.add_argument(
        '-m','--min', action='store', type=str, nargs=1, default=None,
        help='The minimum MSVC runtime version. If you set it, only the file below this version will be written to the output file. Value must be the marketing year\
            of the MSVC runtime, e.g. 2019, 2017, 2015, etc.')
    args = parser.parse_args()

    checking_folder_path = args.folder_path
    output_result_file_path = args.out[0]
    minimum_vc_version = args.min[0] if args.min is not None else None

    # Get all exe and dll files in the folder
    if os.path.isfile(checking_folder_path):
        all_exe_file_paths = [checking_folder_path]
    else:
        all_exe_file_paths = list(pathlib.Path(checking_folder_path).rglob('*.[eE][xX][eE]')) + list(pathlib.Path(checking_folder_path).rglob('*.[dD][lL][lL]'))

    # Initialize the MSVC runtime getter
    msvc_runtime_getter = MSVCRuntimeGetter()

    # Get the VC runtime version for each file
    result_msvc_ver = []
    result_file_path = []
    for exe_file_path in tqdm(all_exe_file_paths):
        # Get the VC runtime version
        msvc_runtime_version = msvc_runtime_getter.get_msvc_runtime(exe_file_path)

        if msvc_runtime_version is not None:
            if minimum_vc_version is not None:
                # Only save the file below the minimum version
                if msvc_runtime_version < minimum_vc_version:
                    # Append the result
                    result_msvc_ver.append(msvc_runtime_version)
                    result_file_path.append(exe_file_path)
            else:
                # Append the result
                result_msvc_ver.append(msvc_runtime_version)
                result_file_path.append(exe_file_path)


    # Write the result to a file
    with open(output_result_file_path, 'w') as f:
        f.write('MSVC version,File path\n')
        for msvc_ver, file_path in zip(result_msvc_ver, result_file_path):
            f.write(f'{msvc_ver},{file_path}\n')
