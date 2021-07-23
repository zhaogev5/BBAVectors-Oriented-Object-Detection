import utils as util
import os
import ImgSplit_multi_process
import SplitOnlyImage_multi_process
import shutil
from multiprocessing import Pool
from DOTA2COCO import DOTA2COCOTest, DOTA2COCOTrain
import argparse

# wordname_15 = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle', 'large-vehicle', 'ship', 'tennis-court',
            #    'basketball-court', 'storage-tank',  'soccer-ball-field', 'roundabout', 'harbor', 'swimming-pool', 'helicopter']

#37
class_name = ['Dry-Cargo-Ship', 'Passenger-Ship', 'Fishing-Boat', 'Engineering-Ship', 'Motorboat', 'A220', 'Boeing737', 'Liquid-Cargo-Ship',
 'Cargo-Truck', 'Small-Car', 'Dump-Truck', 'Van', 'Excavator', 'Intersection', 'other-vehicle', 'A321', 'Tennis-Court', 'Basketball-Court', 
 'other-airplane', 'Boeing787', 'Warship', 'Tugboat', 'other-ship', 'Tractor', 'Bus', 'Roundabout', 'ARJ21', 'Boeing747', 'Football-Field', 
 'Trailer', 'Truck-Tractor', 'Bridge', 'Baseball-Field', 'A330', 'A350', 'Boeing777', 'C919']
print(len(class_name))

# 1732zhang 1500 116 116

def parse_args():
    parser = argparse.ArgumentParser(description='prepare far1m')
    parser.add_argument('--srcpath', default=r'../FAR_dataset/FAR_ori')
    parser.add_argument('--dstpath', default=r'../FAR_dataset/FAR_multi',#r'/home/dingjian/workfs/dota1-split-1024',
                        help='prepare data')
    args = parser.parse_args()

    return args


def single_copy(src_dst_tuple):
    shutil.copyfile(*src_dst_tuple)


def filecopy(srcpath, dstpath, num_process=32):
    pool = Pool(num_process)
    filelist = util.GetFileFromThisRootDir(srcpath)

    name_pairs = []
    for file in filelist:
        basename = os.path.basename(file.strip())
        dstname = os.path.join(dstpath, basename)
        name_tuple = (file, dstname)
        name_pairs.append(name_tuple)

    pool.map(single_copy, name_pairs)


def singel_move(src_dst_tuple):
    shutil.move(*src_dst_tuple)


def filemove(srcpath, dstpath, num_process=32):
    pool = Pool(num_process)
    filelist = util.GetFileFromThisRootDir(srcpath)

    name_pairs = []
    for file in filelist:
        basename = os.path.basename(file.strip())
        dstname = os.path.join(dstpath, basename)
        name_tuple = (file, dstname)
        name_pairs.append(name_tuple)

    pool.map(filemove, name_pairs)


def getnamelist(srcpath, dstfile):
    filelist = util.GetFileFromThisRootDir(srcpath)
    with open(dstfile, 'w') as f_out:
        for file in filelist:
            basename = util.mybasename(file)
            f_out.write(basename + '\n')


def prepare(srcpath, dstpath):
    """
    :param srcpath: train, val, test
          train --> trainval1024, val --> trainval1024, test --> test1024
    :return:
    """
    if not os.path.exists(os.path.join(dstpath, 'test')):
        os.makedirs(os.path.join(dstpath, 'test'))
    # if not os.path.exists(os.path.join(dstpath, 'test800_ms')):
    #     os.makedirs(os.path.join(dstpath, 'test800_ms'))
    if not os.path.exists(os.path.join(dstpath, 'trainval')):
        os.makedirs(os.path.join(dstpath, 'trainval'))
    # if not os.path.exists(os.path.join(dstpath, 'trainval800_ms')):
    #     os.makedirs(os.path.join(dstpath, 'trainval800_ms'))

    # split_train = ImgSplit_multi_process.splitbase(os.path.join(srcpath, 'train'),
    #                                                os.path.join(
    #                                                    dstpath, 'trainval'),
    #                                                gap=500,
    #                                                subsize=800,
    #                                                num_process=16
    #                                                )
    # split_train.splitdata(1)
    # split_val = ImgSplit_multi_process.splitbase(os.path.join(srcpath, 'val'),
    #                                              os.path.join(
    #                                                  dstpath, 'trainval'),
    #                                              gap=500,
    #                                              subsize=800,
    #                                              num_process=16)
    # split_val.splitdata(1)

#SplitOnlyImage_multi_process
    split_test = ImgSplit_multi_process.splitbase(os.path.join(srcpath, 'test'), #, 'images'
                                                        os.path.join(
                                                            dstpath, 'test'), #
                                                        gap=500,
                                                        subsize=800,
                                                        num_process=16)
    split_test.splitdata(1)
    # DOTA2COCOTrain(os.path.join(dstpath, 'trainval'), os.path.join(
    #     dstpath, 'trainval', 'DOTA_trainval.json'), class_name, difficult='2')

    # DOTA2COCOTrain(os.path.join(dstpath, 'test'), os.path.join(
    #     dstpath, 'test', 'DOTA_test.json'), class_name, difficult='2')



if __name__ == '__main__':
    args = parse_args()
    srcpath = args.srcpath
    dstpath = args.dstpath
    prepare(srcpath, dstpath)
