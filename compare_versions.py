from functools import total_ordering
from itertools import zip_longest
import re


@total_ordering
class Version:
    def __init__(self, version: str):
        self.version: str = version.strip().lower()
        self.version_dots_only: str = self.version.replace('-', '.')
        self.version_listed: list = self.version_dots_only.split('.')

    @staticmethod
    def get_versions_zipped(first_list, second_list) -> list:
        versions_zipped = list(zip_longest(first_list, second_list, fillvalue='0'))
        return versions_zipped

    @staticmethod
    def separate_int_from_string(version_part: str) -> tuple:
        v_num = 0
        v_str = ''

        if re.search('[a-z]', version_part):
            v_str = re.findall('[a-z]+', version_part)[0]
        if re.search('[0-9]', version_part):
            v_num = re.findall('[0-9]+', version_part)[0]

        return int(v_num), v_str

    def __eq__(self, other):
        versions_zipped = self.get_versions_zipped(self.version_listed, other.version_listed)

        is_equal = True

        for this_v, other_v in versions_zipped:
            if not this_v == other_v:
                is_equal = False
                break

        return is_equal

    def __lt__(self, other):
        versions_zipped = self.get_versions_zipped(self.version_listed, other.version_listed)

        self_is_less = True

        for this_v, other_v in versions_zipped:

            '''This block gives 0th version particle priority 
            against any str version particle'''
            if this_v == '0' and other_v.islower():
                self_is_less = False
                break
            elif this_v.islower() and other_v == '0':
                break

            this_v_num, this_v_str = self.separate_int_from_string(this_v)
            other_v_num, other_v_str = other.separate_int_from_string(other_v)

            '''This block gives numeric version particle priority 
            over str version particle and covers the case where particle 
            is a mix of numbers and letters'''
            if this_v_num > other_v_num:
                self_is_less = False
                break
            elif this_v_num < other_v_num:
                break
            elif this_v_str > other_v_str:
                self_is_less = False
                break
            elif this_v_str < other_v_str:
                break

        return self_is_less


def main():
    to_test = [
        ('1b.alfa.1', '10.beta.2'),
        ("alfa.1", "beta.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
        ('1.b.0', '1.0.0'),
        ("rc", "0"),
        ('1', '1.1.0'),
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
    ]

    for version_1, version_2 in to_test:
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"


if __name__ == "__main__":
    main()
