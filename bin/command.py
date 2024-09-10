"""
daily 工程的命令行入口

Author: chengzhang
Date: 2024.07.29
"""

# coding = utf8

import click
import os
from typing import Optional
from pybp.logger.app_logger import get_logger
from pybp.file_io.textline_file import load_text_line_file, dump_text_line_file
from daily.entry.ai_daily.ai_daily_entry import AiDailyEntry

logger = get_logger()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("in_file", type=str)  # news urls text file, one link per line
@click.argument("out_dir", type=str)  # 最终的输出目录，包含文本、语音等
@click.option("--overwrite", is_flag=True, help='如果 out_file 文件存在，是否直接覆盖它，默认：覆盖')
@click.option("--verbose", is_flag=True, help='输出详细的清洗过程')
@click.option("--internal_file", type=str, help='internal output text file')
def ai_daily(
        in_file: str,
        out_dir: str,
        overwrite: Optional,
        verbose: Optional,
        internal_dir: Optional,
):
    """ ai-related news daily
    example: python bin/command.py ai-daily tests/daily/entry/ai_daily/test_ai_daily_entiry.input_example.txt tmp/test_ai_daily_entiry.output.txt  # noqa: E501
    """

    if not os.path.exists(in_file):
        logger.error(f'in_file is not a valid path: {in_file}')
        return

    """ out dir """
    if os.path.exists(out_dir):
        if overwrite:
            logger.warning(f'out_dir is going to be overwrite: {out_dir}')
            # TODO: 备份
            os.rmdir(out_dir)
        else:
            logger.error(f'out_file exist, and not overwrite!')
            return
    os.makedirs(out_dir)

    """ internal dir """
    if internal_dir:
        if os.path.exists(internal_dir):
            if overwrite:
                logger.warning(f'internal_dir is going to be overwrite: {internal_dir}')
                os.rmdir(internal_dir)
            else:
                logger.error(f'internal_file exist, and not overwrite!')
                return
        os.makedirs(internal_dir)

    in_urls = load_text_line_file(in_file)
    ai_daily_entry = AiDailyEntry(in_urls)
    daily_result = ai_daily_entry.report()
    ai_daily_entry.dump(daily_result, out_dir, internal_dir)


@cli.command()
def say_hi():
    """ say hi """
    print('hi my friend')


if __name__ == '__main__':
    cli()
