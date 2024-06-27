import argparse

from eulerian_task import EulerianTask

# (準)オイラーグラフ生成プログラム。
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='(準)オイラーグラフ生成')
    parser.add_argument('-s', '--start', default='', help='始点')
    parser.add_argument('-g', '--goal', default='', help='終点')
    parser.add_argument('-l', '--listfile', help='データファイルを記述したファイル')
    parser.add_argument('FILE', nargs='*', help='データファイル (-lオプション使用時は無視)')
    args = parser.parse_args()

    task = EulerianTask()
    if args.listfile is not None:
        task.gen_eulerian_graph_from_list(args.listfile, args.start, args.goal)
    else:
        task.gen_eulerian_graph(args.FILE, args.start, args.goal)
