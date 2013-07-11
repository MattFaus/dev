#!/usr/bin/python

import datetime
import os
import zipfile
from cStringIO import StringIO

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


if __name__ == "__main__":
    #extract_nested_zipfile('/genfiles/third_party.zip/third_party/pytz.zip/zoneinfo.zip')
    print extract_nested_zipfile('/Users/mattfaus/dev/dev-git/wrap1.zip').open('hi.txt').read()
    print extract_nested_zipfile('/Users/mattfaus/dev/dev-git/wrap2.zip/wrap1.zip').open('hi.txt').read()
    print extract_nested_zipfile('/Users/mattfaus/dev/dev-git/wrap3.zip/wrap2.zip/wrap1.zip').open('hi.txt').read()

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