import argparse

from eulerian_task import EulerianTask

# オイラールート生成プログラム。
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='オイラールート生成')
    parser.add_argument('-s', '--start', default='', help='始点')
    parser.add_argument('-g', '--goal', default='', help='終点')
    parser.add_argument('FILE', nargs='*', help='データファイル')
    args = parser.parse_args()

    task = EulerianTask()
    task.gen_eulerian_route(args.FILE, args.start, args.goal)
