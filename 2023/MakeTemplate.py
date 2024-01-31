import os
import sys


def create_files(day: str) -> None:
    '''
    Copy the files from the DayXX directory into the DayDD directory, where DD
    is the two digit representation of the supplied `day` argument. The DayDD
    directory is created if necessary and the script aborts if this directory
    already exists (so as not to unintentionally overwrite files). Any instance
    of `XX` is replaced with `DD` in the copied files.
    '''
    ss = 'XX'
    src = f'./Day{ss}'
    dd = f'{day:02}'
    dest = f'./Day{dd}'

    if os.path.exists(dest):
        print('Destination folder already exists. Aborting.')
        return None

    os.makedirs(dest)
    for f in os.listdir(src):
        s = f'{src}/{f}'
        d = f'{dest}/{f.replace(ss, dd)}'

        with open(s, 'r') as file:
            data = file.read().replace(ss, dd)

        with open(d, 'w') as file:
            file.write(data)


def main():
    '''
    Can be run from the command line where the day number is supplied as the
    first command line argument. If no command line arguments are passed, the
    user will be prompted to enter the day number.
    '''
    if len(sys.argv) > 1:
        day = sys.argv[1]
    else:
        day = input('Enter day number: ')
    create_files(day)


if __name__ == '__main__':
    main()
