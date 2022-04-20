import unittest
from hypothesis import given
from Mutable import UnrolledLinkedList
import hypothesis.strategies as st


class TestMutable(unittest.TestCase):

    def test_add(self):
        lst = UnrolledLinkedList()
        lst.add([])
        self.assertEqual(lst.to_list(), [[]])
        lst.add('a')
        self.assertEqual(lst.to_list(), [[], 'a'])

    def test_set(self):
        lst = UnrolledLinkedList()
        lst.set(0, 'a')
        self.assertEqual(lst.to_list(), ['a'])
        lst.set(1, 'b')
        self.assertEqual(lst.to_list(), ['a', 'b'])

    def test_remove(self):
        lst = UnrolledLinkedList()
        lst.set(0, 'a')
        lst.set(1, 'b')
        lst.set(2, 'c')
        lst.remove(2)
        self.assertEqual(lst.to_list(), ['a', 'b'])
        lst.remove(1)
        self.assertEqual(lst.to_list(), ['a'])
        lst.remove(0)
        self.assertEqual(lst.to_list(), [])

    def test_size(self):
        lst = UnrolledLinkedList()
        self.assertEqual(lst.size(), 0)
        lst.set(0, 'a')
        self.assertEqual(lst.size(), 1)
        lst.set(1, 'b')
        self.assertEqual(lst.size(), 2)

    def test_is_member(self):
        x = ['a', 'b', 'c']
        lst = UnrolledLinkedList()
        lst.from_list(x)
        index = lst.is_member('b')
        self.assertEqual(index, 1)

    def test_reverse(self):
        lst = UnrolledLinkedList()
        x = ['a', 'b', 'c']
        lst.from_list(x)
        self.assertEqual(lst.reverse().to_list(), ['c', 'b', 'a'])

    def test_from_list(self):
        # Each test has to be initialized again
        # Otherwise the result of the last time is still exis
        lst = UnrolledLinkedList()
        lst.from_list([])
        self.assertEqual(lst.to_list(), [])
        lst = UnrolledLinkedList()
        lst.from_list(['a'])
        self.assertEqual(lst.to_list(), ['a'])
        lst = UnrolledLinkedList()
        lst.from_list(['a', 'b'])
        self.assertEqual(lst.to_list(), ['a', 'b'])

    def test_to_list(self):
        lst = UnrolledLinkedList()
        self.assertEqual(UnrolledLinkedList().to_list(), [])
        lst.set(0, 'a')
        self.assertEqual(lst.to_list(), ['a'])
        lst.set(1, 'b')
        self.assertEqual(lst.to_list(), ['a', 'b'])

    def test_filter(self):
        x = [1, 2, 3, 4, 5]
        lst = UnrolledLinkedList()
        lst.from_list(x)
        lst.filter(lambda e: e % 2 == 0)
        self.assertEqual([2, 4], lst.to_list())

    # def test_filter(self):
    #     x = [1, 2, 3, 4]
    #     lst = UnrolledLinkedList()
    #     lst.from_list(x)
    #     lst.filter()
    #     self.assertEqual([2, 4], lst.to_list())

    def test_get(self):
        lst = UnrolledLinkedList()
        lst.set(0, 'a')
        lst.set(1, 'b')
        self.assertEqual(lst.get(0), 'a')
        self.assertEqual(lst.get(1), 'b')

    def test_map(self):
        lst = UnrolledLinkedList()
        lst.map(str)
        self.assertEqual(lst.to_list(), [])

        lst = UnrolledLinkedList()
        lst.from_list([1, 2, 3])
        lst.map(str)
        self.assertEqual(lst.to_list(), ["1", "2", "3"])

        lst = UnrolledLinkedList()
        lst.from_list([1, 2, 3])
        lst.map(lambda x: x + 1)
        self.assertEqual(lst.to_list(), [2, 3, 4])

    def test_reduce(self):
        # sum of empty list
        lst = UnrolledLinkedList()
        self.assertEqual(lst.reduce(lambda st, e: st + e, 0), 0)

        # sum of list
        lst = UnrolledLinkedList()
        lst.from_list([1, 2, 3])
        self.assertEqual(lst.reduce(lambda st, e: st + e, 0), 6)
        # size
        test_data = [
            [],
            ['a'],
            ['a', 'b']
        ]
        for e in test_data:
            lst = UnrolledLinkedList()
            lst.from_list(e)
            self.assertEqual(lst.reduce(lambda st, _: st + 1, 0), lst.size())

    def test_iter(self):
        x = [1, 2, 3]
        lst = UnrolledLinkedList()
        lst.from_list(x)
        tmp = []
        for e in lst.head.next.elements:
            if e is not None:
                tmp.append(e)
        self.assertEqual(x, tmp)
        self.assertEqual(lst.to_list(), tmp)
        i = iter(UnrolledLinkedList())
        self.assertRaises(StopIteration, lambda: next(i))

        lst = UnrolledLinkedList()
        lst1 = UnrolledLinkedList()
        x = [1, 2, 3, 4, 5]
        lst.from_list(x)
        lst1.from_list(x)
        i1 = iter(lst)
        i2 = iter(lst1)
        next(i1)  # -> 1
        next(i1)  # -> 2
        next(i2)  # -> 1
        next(i2)  # -> 2
        next(i1)  # -> 3

    def test_empty(self):
        lst = UnrolledLinkedList()
        self.assertEqual(lst.empty(), [])

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        lst = UnrolledLinkedList()
        lst.from_list(a)
        b = lst.to_list()
        self.assertEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        lst = UnrolledLinkedList()
        lst.from_list(a)
        self.assertEqual(lst.size(), len(a))

    @given(a=st.lists(st.integers()),
           b=st.lists(st.integers()),
           c=st.lists(st.integers()))
    def test_monoid_properties(self, a, b, c):
        lst1 = UnrolledLinkedList()
        lst1.from_list(a)
        lst2 = UnrolledLinkedList()
        lst2.from_list(b)
        lst3 = UnrolledLinkedList()
        lst3.from_list(c)

        # Associativity
        # concat a b and a * b
        lst, ans1 = lst1.concat(lst1.to_list(), lst2.to_list())
        # (a * b) * c
        lst, ans1 = lst1.concat(lst.to_list(), lst3.to_list())
        # print(ans)

        # concat b c and b * c
        lst, ans2 = lst1.concat(lst2.to_list(), lst3.to_list())
        # a * (b * c)
        lst, ans2 = lst1.concat(lst.to_list(), lst3.to_list())
        self.assertEqual(ans1, ans2)

        # Identity element
        # a * e
        lst, ans3 = lst1.concat(lst1.to_list(), lst2.empty())
        # a * e
        lst, ans4 = lst1.concat(lst2.empty(), lst1.to_list())
        self.assertEqual(ans3, ans4)


if __name__ == '__main__':
    unittest.main()
