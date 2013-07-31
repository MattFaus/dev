#!/usr/bin/python

import datetime
import os
import zipfile
import re
from cStringIO import StringIO
import sys
import json

class StrOverload:
    def __str__(self):
        return 'Overloaded str()'

    def __repr__(self):
        return 'Overloaded repr()'

def test_str_overload():
    print str(StrOverload)
    o = StrOverload()
    print str(o)
    print repr(StrOverload)
    print repr(o)

class Holder:
    pass

def obj_to_dict(o, other_dict):
    if o.key in other_dict:
        match = True
    else:
        match = False

    return {
        'key': o.key,
        'match': match,
    }

def test_map_params():
    a = Holder()
    a.key = 1

    b = Holder()
    b.key = 2

    superset = [a, b]
    subset = [2]

    print superset, subset

    # Doesn't work! :(
    print map(obj_to_dict(subset), superset)

def test_any_obj():
    a = Holder()
    a.v = False

    l1 = [a]

    print any(l1)

def test_inner_func_scope():

    hi = 'Hello'

    def my_print(what):
        print hi, what, from_who

        if does_not_exist:
            print does_not_exist

    from_who = 'from Matt Faus!'

    my_print('World!')

def test_inner_func_scope_2(func):
    func()

def test_datetime_calcs():

    birthdate = datetime.datetime.now().date()
    birthdate_datetime = datetime.datetime.combine(birthdate, datetime.datetime.now().time())
    creation = datetime.datetime.now() - datetime.timedelta(days=10)
    duration_of_membership = birthdate_datetime - creation
    age_at_creation = birthdate_datetime - duration_of_membership

    print birthdate
    print birthdate_datetime
    print creation
    print duration_of_membership
    print age_at_creation

class PropertyOverload:
    hi = 'Hello, World.'

    @property
    def hi(self):
        return 'Goodbye!'

def test_property_overload():
    obj = PropertyOverload()
    print obj.hi

def build_report_calls():
    from dateutil import rrule
    #http://stackoverflow.com/questions/153584/how-to-iterate-over-a-timespan-after-days-hours-weeks-and-months-in-python
    start = datetime.date(2011, 1, 1)

    # Go 1 month long so we can subtract form the next
    end = datetime.date(2013, 6, 1)

    month_starts = []

    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start, until=end):
        month_starts.append(dt.date())

    format = ("nohup "
     r"../src/report_generator.py -c ../cfg/daily_report.json "
      "\"<day>=CompanyMetricsBackfill-{0}\" "
      "\"<month_first_day>={1}\" \"<month_last_day>={2}\" "
      "\"<month>={0}\" "
      ">> backfill_{0}.txt &")

    for i in range(len(month_starts)-1):
        end_day = month_starts[i+1] - datetime.timedelta(days=1)
        month = str(end_day)[:7]
        #print month_starts[i], end_day, month
        print format.format(month, month_starts[i], end_day)

def test_star_param(*params):
    for p in params:
        print p

def test_double_star_parms(**kwargs):
    print type(kwargs)

class ReferenceTest:

    def _get_sheet_and_row(self, sheet_name):
        """Gets a reference to the sheet and the value of the current row (
        which should be written to).  This function creates the sheet if one
        does not currently exist with the given name.
        """
        sheet_row = getattr(self, sheet_name + '_row', None)

        if sheet_row == None:
            setattr(self, sheet_name + '_row', 1)

            sheet_row = getattr(self, sheet_name + '_row')

        return sheet_row

    def increment_attribute(self, name):
        row = self._get_sheet_and_row(name)
        row += 1

    def increment_attribute_2(self, name):
        # Make sure it's hot-created at least once
        self._get_sheet_and_row(name)

        row = getattr(self, name + '_row')
        setattr(self, name + '_row', row + 1)

def test_attr_reference():
    tester = ReferenceTest()
    tester.increment_attribute('hi')
    tester.increment_attribute('hi')
    tester.increment_attribute('hi')
    tester.increment_attribute('hi')
    print tester.hi_row

    tester.increment_attribute_2('hi')
    tester.increment_attribute_2('hi')
    tester.increment_attribute_2('hi')
    tester.increment_attribute_2('hi')
    print tester.hi_row

# Nope, doesn't work!
# def test_default_value(required, optional=required):
#     print required, optional

def extract_nested_zipfile(path, parent_zip=None):
    """Returns a ZipFile specified by path, even if the path contains
    intermediary ZipFiles.  For example, /root/gparent.zip/parent.zip/child.zip
    will return a ZipFile that represents child.zip
    """

    def extract_inner_zipfile(parent_zip, child_zip_path):
        """Returns a ZipFile specified by child_zip_path that exists inside
        parent_zip.
        """
        memory_zip = StringIO()
        memory_zip.write(parent_zip.open(child_zip_path).read())
        return zipfile.ZipFile(memory_zip)

    if ('.zip' + os.sep) in path:
        (parent_zip_path, child_zip_path) = os.path.relpath(path).split(
            '.zip' + os.sep, 1)
        parent_zip_path += '.zip'

        if not parent_zip:
            # This is the top-level, so read from disk
            parent_zip = zipfile.ZipFile(parent_zip_path)
        else:
            # We're already in a zip, so pull it out and recurse
            parent_zip = extract_inner_zipfile(parent_zip, parent_zip_path)

        return extract_nested_zipfile(child_zip_path, parent_zip)
    else:
        if parent_zip:
            return extract_inner_zipfile(parent_zip, path)
        else:
            return zipfile.ZipFile(path)

class Root(object):

    def wrapper(self, hi):
        self.foo(hi)

    def foo(self, bar):
        raise NotImplementedError()

class Son(Root):

    def __init__(self):
        self.hair = "blue"

    def foo(self, bar):
        print "Son", bar, "hair:", self.hair

class Daughter(Root):

    def __init__(self, eyes):
        self.e = eyes

    def foo(self, bar):
        print "Daughter", bar, "eyes:", self.e

class Government(object):

    def __init__(self, person):
        person.foo('is under arrest!')
        person.wrapper('was accessed via Root')

def test_classes():
    a = Government(Son())

    # Government(Daughter())
    a = Government(Daughter('hazel'))

    # a = Government(Root())

class GenericSerialized(object):

    def __init__(self, arg):
        self.arg = arg

    def serialize(self):
        return {
            'class_path': self.__class__,
            'arg': self.arg,
        }

def test_serializiation():
    r = GenericSerialized({
        'hi': 1,
        'bye': datetime.datetime.now().strftime('%Y-%M'),
        })

    import json
    json = json.dumps(r.serialize())
    print json

def generate_int_list(n):
    print 'RAW_DATA = ['

    for i in xrange(n):
        sys.stdout.write('%i, ' % i)

    print ''
    print ']'


RAW_DATA = [
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999,
]

def test_slice_step():
    # Does it stepping loop around? NO
    for i in xrange(100):
        print RAW_DATA[i::1000]

def measure_pipeline_ids():
    import uuid

    id_list = []
    for i in range(1000001):
        id_list.append(uuid.uuid1().hex)

        if i % 100000 == 0:
            json_str = json.dumps(id_list)
            bytes = len(json_str)
            k_bytes = bytes / 1024
            m_bytes = k_bytes / 1024
            print '%s %iB %iKB %iMB' % (i, bytes, k_bytes, m_bytes)

# 0 36B 0KB 0MB
# 100000 3600036B 3515KB 3MB
# 200000 7200036B 7031KB 6MB
# 300000 10800036B 10546KB 10MB
# 400000 14400036B 14062KB 13MB
# 500000 18000036B 17578KB 17MB
# 600000 21600036B 21093KB 20MB
# 700000 25200036B 24609KB 24MB
# 800000 28800036B 28125KB 27MB
# 900000 32400036B 31640KB 30MB
# 1000000 36000036B 35156KB 34MB

if __name__ == "__main__":

    test_slice_step()

    # generate_int_list(1000)

    # measure_pipeline_ids()

    # test_serializiation()

    # test_double_star_parms()

    # test_classes()

    #extract_nested_zipfile('/genfiles/third_party.zip/third_party/pytz.zip/zoneinfo.zip')
    # print extract_nested_zipfile('/Users/mattfaus/dev/dev-git/wrap1.zip').open('hi.txt').read()
    # print extract_nested_zipfile('/Users/mattfaus/dev/dev-git/wrap2.zip/wrap1.zip').open('hi.txt').read()
    # print extract_nested_zipfile('/Users/mattfaus/dev/dev-git/wrap3.zip/wrap2.zip/wrap1.zip').open('hi.txt').read()

    # test_attr_reference()
    #test_star_param(*['hello', 'world'])
    #test_star_param('hello', 'world')
    #build_report_calls()
    #test_property_overload()
    #test_datetime_calcs()
    #test_inner_func_scope_2(test_inner_func_scope)
    #test_inner_func_scope()
    # test_str_overload();
    #test_map_params()
