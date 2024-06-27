import argparse

from eulerian_task import EulerianTask

## オイラー回路の生成とオイラールートの生成プログラム。
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='オイラールート生成')
    parser.add_argument('-s', '--start', default='', help='始点')
    parser.add_argument('-g', '--goal', default='', help='終点')
    parser.add_argument('--show_edge', action='store_true', help='ルートを構成するエッジの表示')
    parser.add_argument('-l', '--listfile', help='データファイルを記述したファイル')
    parser.add_argument('FILE', nargs='*', help='データファイル (-lオプション使用時は無視)')
    args = parser.parse_args()

    task = EulerianTask()
    if args.listfile is not None:
        task.run_from_list(args.listfile, args.start, args.goal, args.show_edge)
    else:
        task.run(args.FILE, args.start, args.goal, args.show_edge)
