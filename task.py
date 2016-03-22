# coding:utf-8
import os

import click
from django.conf import settings

current_dir = os.path.abspath(os.path.dirname(__file__))


@click.command()
@click.option('--apk_path', default='default-6.apk', help=u'APK文件名')
@click.option('--userid', default='25327219', help=u'用户ID')
def task_gen_user_apk(apk_path, userid):
    """
    生成指定用户分享包
    :param apk_path:APK的文件名，相对路径不是绝对路径
    :param userid:用户ID，
    :return:
    """
    import os

    apk_path, source_apk_path = os.path.join(current_dir, apk_path), apk_path
    if not os.path.join(apk_path):
        print('apk_path:{0} not exists'.format(apk_path))
        return

    dir_path, apk_fullname = os.path.split(apk_path)
    apk_name, extension = apk_fullname.split('.')

    new_apk_fullname = '{0}_{1}.{2}'.format(apk_name, userid, extension)
    new_apk_path = os.path.join(dir_path, new_apk_fullname)

    empty_path_abs = os.path.join(dir_path, 'empty')
    # 准备一个空文件empty,如果没有则创建
    if not os.path.exists(empty_path_abs):
        fp = open(empty_path_abs, 'w')
        # fp.write('show me the money')
        fp.close()

    # 先复制
    import shutil
    shutil.copy(apk_path, new_apk_path)

    import zipfile
    zipped = zipfile.ZipFile(new_apk_path, 'a', zipfile.ZIP_DEFLATED)
    # 由于apk限定只能修改此目录内的文件，否则会报无效apk包
    # 不知道绝路径路径会不会有问题
    insert_path = 'META-INF/uic_{0}'.format(userid)  # 相对路径

    # insert_path = '{1}/META-INF/uic_{0}'.format(userid, dir_path) 绝对不行，只能相对路径
    zipped.write(empty_path_abs, insert_path)
    zipped.close()

    print('Success')


if __name__ == '__main__':
    task_gen_user_apk()
