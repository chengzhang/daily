"""
sgame_nlp_data 工程的命令行入口

Author: donyzhang
Date: 2024.07.10
"""

# coding = utf8

import click
import os
from typing import Optional
from sgame_nlp_data.utils.logger import get_logger
from sgame_nlp_data.utils.file_util import load_text_line_file, dump_text_line_file
from sgame_nlp_data.cleaner.cleaner import Cleaner

logger = get_logger()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("in_file", type=str, help='待清洗的句子，文本文件，每行一句话')
@click.argument("out_file", type=str, help='清洗后的句子，文本文件，每行一句话')
@click.option("--force_out", is_flag=True, help='如果 out_file 存在，是否强制 overwrite，默认是')
@click.option("--verbose", is_flag=True, help='输出详细的清洗过程')
@click.option("--more_bad_words", type=str, help='指定额外的过滤词, 则它们将与内建的过滤词一起生效')
@click.option("--exclude_bad_words", type=str, help='指定不生效的过滤词, 则从过滤词典中去除这些过滤词。如果与 more_bad_words 有重合，则以 exclude_bad_words 为准')  # noqa E501
def filter_entity(
        in_file: str,
        out_file: str,
        force_out: Optional,
        verbose: Optional,
        more_bad_words: Optional,
        exclude_bad_words: Optional,
):
    """ 输入一批句子，过滤掉包含实体的句子。 """
    if not os.path.exists(in_file):
        logger.error(f'in_file is not a valid path: {in_file}')
        return

    if os.path.exists(out_file):
        if force_out:
            logger.warning(f'out_file is going to be overwrite: {out_file}')
        else:
            logger.error(f'out_file exist, and not force_out: {more_bad_words} remove out_file or set force_out True')
            return
    else:
        out_dir = os.path.dirname(out_file)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

    if more_bad_words and not os.path.exists(more_bad_words):
        logger.error(f'more_bad_words is not a valid path: {more_bad_words}')
        return

    if exclude_bad_words and not os.path.exists(exclude_bad_words):
        logger.error(f'exclude_bad_words is not a valid path: {exclude_bad_words}')
        return

    more_bad_words = load_text_line_file(more_bad_words)
    exclude_bad_words = load_text_line_file(exclude_bad_words)

    cleaner = Cleaner(more_bad_words=more_bad_words, exclude_bad_words=exclude_bad_words)

    in_texts = load_text_line_file(in_file)
    out_texts, bad_text_word_pairs = cleaner.clean_texts(in_texts, verbose=verbose)
    dump_text_line_file(out_texts, out_file)


@cli.command()
def show_clean_bad_words():
    """ 展示所有的 build-in 的脏词 """
    cleaner = Cleaner()
    cleaner.show_bad_words()


if __name__ == '__main__':
    cli()
