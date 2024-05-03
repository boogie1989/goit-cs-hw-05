import os
import shutil
import asyncio
import argparse
import logging


logging.basicConfig(level=logging.ERROR)


async def read_folder(source_folder, output_folder):
    """Asynchronously read and process files from the source folder."""
    for root, _, files in os.walk(source_folder):
        tasks = [copy_file(root, file, output_folder) for file in files]
        await asyncio.gather(*tasks)


async def copy_file(root, file, output_folder):
    """Copy a file to a new directory based on its file extension."""
    file_extension = os.path.splitext(file)[1]
    source_path = os.path.join(root, file)
    output_path = os.path.join(output_folder, file_extension.lstrip('.'))
    os.makedirs(output_path, exist_ok=True)

    try:
        shutil.copy(source_path, os.path.join(output_path, file))
        print(f"File {file} copied to {output_path}")
    except Exception as e:
        logging.error(f"Error copying file {file} to {output_path}: {e}")


async def main():
    parser = argparse.ArgumentParser(
        description="Sort files based on their extensions")
    parser.add_argument("input", help="Input folder path")
    parser.add_argument("output", help="Output folder path")
    args = parser.parse_args()

    source_folder = args.input
    output_folder = args.output

    os.makedirs(output_folder, exist_ok=True)

    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())
