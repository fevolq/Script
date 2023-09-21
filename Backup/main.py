#!-*- coding:utf-8 -*-
# python3.7
# CreateTime: 2023/9/20 14:00
# FileName:

import asyncio
import getopt
import io
import sys
import zipfile
import os

sys.path.append('.')
from utils import util


class Zip:

    def __init__(self, src_path, output_path=None):
        self.src_path = src_path
        self.target_name = os.path.basename(self.src_path)
        self.target = None  # 目标路径（output_path/target_name.zip）或流数据
        self.is_stream = False  # 是否为流数据

        if output_path:
            self.is_stream = False
            self.target = os.path.join(output_path, f'{self.target_name}.zip')
            util.mkdir(output_path)
        else:
            self.is_stream = True
            self.target = io.BytesIO()

    async def zip_folder(self, zipf, folder):

        def write_file(file_path):
            try:
                zipf.write(file_path, os.path.relpath(file_path, self.src_path))
            except Exception as e:
                print(str(e))

        async def write_folder(root, files):
            for file in files:
                file_path = os.path.join(root, file)
                write_file(file_path)

        tasks = (write_folder(root_, files_) for root_, _, files_ in os.walk(folder))

        await asyncio.gather(*tasks)

    @util.timer
    def run(self, zip_sion=zipfile.ZIP_DEFLATED, zip_level=9):
        with zipfile.ZipFile(self.target, 'w', compression=zip_sion, compresslevel=zip_level) as zipf:
            if os.path.isfile(self.src_path):
                zipf.write(self.src_path, os.path.basename(self.src_path))
            else:
                asyncio.run(self.zip_folder(zipf, self.src_path))

        if self.is_stream is None:
            self.target.seek(0)


class Upload:

    def __init__(self, target, is_stream):
        pass


def main(source, output):
    zip_obj = Zip(source_path, output_zip)
    zip_obj.run()

    Upload(zip_obj.target, zip_obj.is_stream)


if __name__ == '__main__':
    source_path = ''
    output_zip = ''

    opts, _ = getopt.getopt(sys.argv[1:], "s:o:", ["source=", "output="])
    opts = dict(opts)
    if opts.get("-s"):
        source_path = str(opts.get("-s"))
    elif opts.get("--source"):
        source_path = str(opts.get("--source"))
    if opts.get("-o"):
        output_zip = str(opts.get("-o"))
    elif opts.get("--output"):
        output_zip = str(opts.get("--output"))

    assert source_path, 'Missing parameters: source_path'

    main(source_path, output_zip)
