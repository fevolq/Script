#!-*- coding:utf-8 -*-
# python3.7
# CreateTime: 2023/9/20 14:00
# FileName: 文件备份

import asyncio
import getopt
import io
import sys
import zipfile
import os
from typing import Union

from aligo import Aligo

sys.path.append('.')
import conf
from utils import util, send_msg, log_util

logger = log_util.get_logger('backup', 'INFO')


class Zip:

    def __init__(self, src_path: str, output_path: str = None, name: str = None):
        """

        :param src_path: 源文件（夹）路径
        :param output_path: 输出路径（无 则输出流数据）
        :param name: 输出名称（无后缀）
        """
        self.src_path = src_path
        self.target_name = name or os.path.basename(self.src_path)
        self.target: Union[str, io.BytesIO] = ''  # 目标路径（output_path/target_name.zip）或流数据
        self.is_stream = False  # 是否为流数据

        if output_path:
            output_path = os.path.realpath(output_path)
            util.mkdir(output_path)
            self.is_stream = False
            self.target = os.path.join(output_path, f'{self.target_name}.zip')
        else:
            self.is_stream = True
            self.target = io.BytesIO()

    async def zip_folder(self, zipf, folder):

        def write_file(file_path):
            try:
                zipf.write(file_path, os.path.relpath(file_path, self.src_path))
            except Exception as e:
                logger.error(str(e))

        async def write_folder(root, files):
            for file in files:
                file_path = os.path.join(root, file)
                write_file(file_path)

        tasks = (write_folder(root_, files_) for root_, _, files_ in os.walk(folder))

        await asyncio.gather(*tasks)

    def run(self, zip_sion=zipfile.ZIP_DEFLATED, zip_level=9):
        with zipfile.ZipFile(self.target, 'w', compression=zip_sion, compresslevel=zip_level) as zipf:
            if os.path.isfile(self.src_path):
                zipf.write(self.src_path, os.path.basename(self.src_path))
            else:
                asyncio.run(self.zip_folder(zipf, self.src_path))

        if self.is_stream is None:
            self.target.seek(0)
        logger.info('打包完成')


class Upload:
    PORT = conf.AliLoginPort

    def __init__(self):
        self.ali = Aligo(port=self.PORT)

    def upload(self, remote_folder: str, target, name, is_stream=False, mode='auto_rename'):
        """

        :param remote_folder: 存储路径
        :param target: 存储文件的路径（或 流数据）
        :param name: 文件名称
        :param is_stream: 是否流数据
        :param mode: 存储模式（auto_name、rename、...）
        :return:
        """
        current_date = util.now_time(fmt='%Y-%m-%d')
        new_remote_folder = f'{remote_folder}/{current_date}'

        exist = self.ali.get_folder_by_path(new_remote_folder)
        if exist is None:
            remote = self.ali.get_folder_by_path(remote_folder)
            self.ali.create_folder(current_date, remote.file_id)

        new_remote = self.ali.get_folder_by_path(new_remote_folder)
        result = self.ali.upload_file(target, parent_file_id=new_remote.file_id, name=name, check_name_mode=mode)
        # print(f'{current_date} {name} ' + '上传成功' if result else '上传失败')
        logger.info(f'{current_date} {name} ' + '上传成功' if result else '上传失败')


def main(source, output, name, path):
    @util.catch_error(raise_error=False, callback=send_msg.feishu_robot_msg, args=(conf.FeiShuErrorRobot,),
                      kwargs={'title': '文件备份', 'content': f'异常文件：{source}'})
    def run():
        zip_obj = Zip(source, output, name=name)
        zip_obj.run()

        Upload().upload(path, zip_obj.target, f'{zip_obj.target_name}.zip', is_stream=zip_obj.is_stream, )

        if not zip_obj.is_stream:
            os.remove(zip_obj.target)

    run()


if __name__ == '__main__':
    source_path = ''  # 源文件（夹）路径
    output_zip = os.path.join(os.path.abspath(__file__), '../data')  # 输出路径（完成后删除，空则使用流数据）
    output_name = None  # 输出名称（默认基于source_path）

    ali_folder_path = '/备份/Volume'  # 阿里云盘的保存路径

    opts, _ = getopt.getopt(sys.argv[1:], "s:o:n:p:", ["source=", "output=", "name=", "path="])
    opts = dict(opts)
    if opts.get("-s"):
        source_path = str(opts.get("-s"))
    elif opts.get("--source"):
        source_path = str(opts.get("--source"))
    if opts.get("-o"):
        output_zip = str(opts.get("-o"))
    elif opts.get("--output"):
        output_zip = str(opts.get("--output"))
    if opts.get("-n"):
        output_name = str(opts.get("-n"))
    elif opts.get("--name"):
        output_name = str(opts.get("--name"))
    if opts.get("-p"):
        ali_folder_path = str(opts.get("-p"))
    elif opts.get("--path"):
        ali_folder_path = str(opts.get("--path"))

    assert source_path, 'Missing parameters: source_path'

    main(source_path, output_zip, output_name, ali_folder_path)
