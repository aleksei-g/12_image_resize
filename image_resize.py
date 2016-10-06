import argparse
import sys
import os.path
from PIL import Image


def create_parser():
    parser = argparse.ArgumentParser(description='Скрипт изменяет размер \
                                     изображения.')
    parser.add_argument('file', metavar='ФАЙЛ',
                        help='Файл исходного изображения.')
    parser.add_argument('--output', metavar='ФАЙЛ',
                        help='Файл результирующего изображения.')
    parser.add_argument('--width', metavar='ШИРИНА', type=int,
                        help='Ширина результирующего изображения.')
    parser.add_argument('--height', metavar='ВЫСОТА', type=int,
                        help='Выота результирующего изображения.')
    parser.add_argument('--scale', metavar='МАСШТАБ', type=float,
                        help='Масштаб увеличения результирующего изображения.')
    return parser


def check_filepath(filepath, check_file_exist=True):
    if check_file_exist:
        if not os.path.exists(filepath):
            print('Файл %s не существует!' % filepath)
            return False
    (dir_name, file_name) = os.path.split(os.path.abspath(filepath))
    if os.path.exists(dir_name):
        (root, ext) = os.path.splitext(filepath)
        if ext not in ['.jpg', '.png', '.bmp']:
            print('Неверный файл "%s".' % (filepath),
                  'Изображение должно быть в формате "jpg", "png", "bmp".')
            return False
    else:
        print('Каталог %s не существует!' % dir_name)
        return False
    return True


def check_parameters(namespace):
    error = False
    error = not check_filepath(namespace.file, True)
    if namespace.output:
        error = not check_filepath(namespace.output, False)
    if not namespace.width and not namespace.height and not namespace.scale:
        print('Необходимо передать значение ходя бы для одного из параметров: \
              "--width", "--height" или "--scale".')
        error = True
    if namespace.scale and (namespace.width or namespace.height):
        print('Если указан масштаб, то ширина и высота указаны быть не могут.')
        error = True
    return not error


def calculate_param(path_to_original, path_to_result, width, height, scale):
    img = Image.open(path_to_original)
    if scale:
        width = int((float(img.size[0]) * float(scale)))
        height = int((float(img.size[1]) * float(scale)))
    elif width and not height:
        height = int((float(img.size[1]) * width / float(img.size[0])))
    elif height and not width:
        width = int((float(img.size[0]) * height / float(img.size[1])))
    elif width and height:
        if img.size[0] / img.size[1] != width / height:
            while True:
                answer = input('Пропорции изображения не сохранятся!\n'
                               'Продолжить? [Y,N]: ')
                if answer.lower() == 'y':
                    break
                elif answer.lower() == 'n':
                    return None, None, None
    if not path_to_result:
        (root, ext) = os.path.splitext(namespace.file)
        path_to_result = ''.join((root, '__%sx%s' % (width, height), ext))
    return width, height, path_to_result


def resize_image(path_to_original, path_to_result, width, height):
    img = Image.open(path_to_original)
    resized_img = img.resize((width, height), Image.ANTIALIAS)
    resized_img.save(path_to_result)
    return True


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    if not check_parameters(namespace):
        sys.exit()
    width, heigth, path_to_result = \
        calculate_param(namespace.file, namespace.output, namespace.width,
                        namespace.height, namespace.scale)
    if width and heigth and path_to_result:
        if resize_image(namespace.file, path_to_result, width, heigth):
            print('Изображение сохранено в файл "%s".' % path_to_result)
        else:
            print('Непредвиденное завершение скрипта!')
    else:
        print('Прервано пользователем.')
