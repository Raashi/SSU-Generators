import sys
import argparse

import utils
import utils.launch_dist as launch_dist
import dist
import stats

import criteria.chi2 as chi2
import criteria.serial as serial
import criteria.intervals as intervals
import criteria.splitting as splitting
import criteria.permutations as permutations
import criteria.run as run
import criteria.conflicts as conflicts

CRITERIAS = [
    chi2.chi2, serial.serial, intervals.intervals, splitting.splitting,
    permutations.permutations, run.run_1, run.run_2, conflicts.conflicts
]


def parse_args():
    args = utils.get_args()
    # Добавление аргументов
    parser = argparse.ArgumentParser()
    parser.add_argument('--f', help='Файл с входной ППСЧ')
    parser.add_argument('--fout', help='Файл с отчётом', default='report.txt')
    # Парсинг
    args_parsed = parser.parse_args(args)
    # Стандартное равномерное распределение
    args_parsed.d = 'st'
    args_parsed.p1 = 0
    args_parsed.p2 = 1
    return args_parsed


def main():
    args = parse_args()

    orig_stdout = sys.stdout
    f = open(args.fout, 'w')
    sys.stdout = f

    # Генерация ПСП и приведение к стандартному равномерному распределению
    prs = launch_dist.read(args)
    prs_st, prs_ideal = dist.transform(args, prs)
    # Первые задания
    stats.stats(prs_st, args)

    old_separator = utils.SEPARATOR
    utils.SEPARATOR = old_separator + '\n' + old_separator

    for crit in CRITERIAS:
        crit(prs_st)  # критерий конфликтов запустим на исходной ПСП
        print(utils.SEPARATOR)

    utils.SEPARATOR = old_separator

    sys.stdout = orig_stdout
    f.close()


if __name__ == '__main__':
    main()
