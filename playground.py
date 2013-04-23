
import datetime

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

# Nope, doesn't work!
# def test_default_value(required, optional=required):
#     print required, optional

if __name__ == "__main__":
    test_property_overload()
    #test_datetime_calcs()
    #test_inner_func_scope_2(test_inner_func_scope)
    #test_inner_func_scope()
    # test_str_overload();
    #test_map_params()