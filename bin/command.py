"""
daily 工程的命令行入口

Author: chengzhang
Date: 2024.07.29
"""

# coding = utf8

import click
import os
from typing import Optional
from pybp.pybp.logger.logger_helper import get_logger
from pybp.pybp.file_io.textline_file import load_text_line_file, dump_text_line_file

logger = get_logger()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("in_file", type=str, help='news urls text file, one link per line')
@click.argument("out_file", type=str, help='final doc text file')
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
    """ ai-related news daily """
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
    daily, internal_texts = ai_daily(in_urls)

    dump_text_line_file([daily], out_file)
    dump_text_line_file(internal_texts, internal_file)


@cli.command()
def say_hi():
    """ say hi """
    print('hi my friend')


if __name__ == '__main__':
    cli()
