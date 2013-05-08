
import os
import pprint

root_dir = '/Users/mattfaus/dev/dev-git'

def parse_logs(file_paths):
    # print 'Parsing ', file_paths
    # These files are generated with a command line like the following:
    # analytics@ip-10-0-0-108:~/kalogs/2013/04/10$ zgrep "UserData.<put>" *.gz >> 2013.04.10-UserDataPut.txt

    pp = pprint.PrettyPrinter(indent=4)

    for path in file_paths:
        full_path = os.path.join(root_dir, path)
        print 'Parsing', full_path
        the_dict = parse_log(open(full_path, 'r'))
        print_dict(the_dict)

def parse_log(the_file):
    # Example log entries:
    # 00:00:00Z.log.gz:16: api/v1_notifications.py:122 -- UserData.<put>
    # 00:00:00Z.log.gz:92: api/v1_notifications.py:88 -- UserData.<put>
    # 00:00:00Z.log.gz:7: api/v1_user.py:2224 -- UserData.<put>
    # 00:00:00Z.log.gz:27: api/v1_user.py:533 -- UserData.<put>

    # Build a dict that looks like this:
    # {
    #     'discussion/voting.py':
    #     {
    #         # Line number : Count
    #         172: 15000,
    #         185: 25000,
    #     },
    #       ...
    # }
    line_count_dict = {}

    for line in the_file:
        parts = line.split(' ')

        if len(parts) < 2 or ':' not in parts[1]:
            print 'Could not understand', line
            continue

        path_parts = parts[1].split(':')
        path = path_parts[0]
        src_line_num = path_parts[1]

        if not line_count_dict.get(path):
            line_count_dict[path] = {}

        if not line_count_dict[path].get(src_line_num):
            line_count_dict[path][src_line_num] = 0

        line_count_dict[path][src_line_num] += 1

    return line_count_dict


def print_dict(the_dict):
    """Print stuff in CSV format for easy input to Excel."""
    for k in the_dict:
        for l in the_dict[k]:
            print "{0},{1},{2}".format(k, l, the_dict[k][l])

if __name__ == "__main__":
    # Find files that look like 2013.03.10-UserDataPut.txt
    files = [f for f in os.listdir(root_dir) if 'UserData' in f]

    parse_logs(files)
