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
@click.argument("out_file", type=str)  # final doc text file
@click.option("--overwrite", is_flag=True, help='如果 out_file 文件存在，是否直接覆盖它，默认：覆盖')
@click.option("--verbose", is_flag=True, help='输出详细的清洗过程')
@click.option("--internal_file", type=str, help='internal output text file')
def ai_daily(
        in_file: str,
        out_file: str,
        overwrite: Optional,
        verbose: Optional,
        internal_file: Optional,
):
    """ ai-related news daily
    example: python bin/command.py ai-daily tests/daily/entry/ai_daily/test_ai_daily_entiry.input_example.txt tmp/test_ai_daily_entiry.output.txt  # noqa: E501
    """

    if not os.path.exists(in_file):
        logger.error(f'in_file is not a valid path: {in_file}')
        return

    """ out file """
    if os.path.exists(out_file):
        if overwrite:
            logger.warning(f'out_file is going to be overwrite: {out_file}')
        else:
            logger.error(f'out_file exist, and not overwrite!')
            return
    else:
        out_dir = os.path.dirname(out_file)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

    """ internal file """
    if internal_file:
        if os.path.exists(internal_file):
            if overwrite:
                logger.warning(f'internal_file is going to be overwrite: {internal_file}')
            else:
                logger.error(f'internal_file exist, and not overwrite!')
                return
        else:
            out_dir = os.path.dirname(internal_file)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

    in_urls = load_text_line_file(in_file)
    ai_daily_entry = AiDailyEntry(in_urls)
    daily_result = ai_daily_entry.report()

    dump_text_line_file([daily_result.text], out_file)
    if internal_file:
        dump_text_line_file(daily_result.logs, internal_file)


@cli.command()
def say_hi():
    """ say hi """
    print('hi my friend')


if __name__ == '__main__':
    cli()
