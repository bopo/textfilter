"""Console script for textfilter."""
import os
import sys

import click

from textfilter.textfilter import TextFilter


@click.command()
@click.option('-m', '--method', default=None, help='过滤方法')
@click.option('-k', '--keyword', default=None, help='关键字或者关键字字典路径.')
@click.option('-s', '--source', default='', help='需要过滤的源文本或者文件路径.')
@click.option('-o', '--output', default='', help='过滤后的文件保存路径.')
def main(method, keyword, source, output):
    """Console script for textfilter."""
    # click.echo("Replace this message by putting your code into textfilter.__main__.main")
    # click.echo("See click documentation at https://click.palletsprojects.com/")

    print(method, source, keyword, output)

    if keyword:
        file = keyword if os.path.isfile(keyword) else None
    else:
        file = None

    if os.path.isfile(source):
        with open(source, 'r') as fs:
            source = fs.read()

    f = TextFilter(method=method, file=file)

    if not file:
        f.add(keyword)

    o = f.filter(source, '*')
    print(o)

    if output:
        with open(output, 'w') as fp:
            fp.write(o)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
