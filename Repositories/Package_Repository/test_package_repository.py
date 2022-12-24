from unittest import TestCase
from Models.package import Package
from Data_Structures.Hash_Map.hash_map import HashMap
from Repositories.Package_Repository.package_repository import PackageRepository


class TestPackageRepository(TestCase):

    def _get_sample_packages(self):
        p1 = Package(1, "233 S. Wacker Dr", "Chicago", "60606", "12/01/2022", "20", "", "IL")
        p2 = Package(2, "299 S. Main", "Utah", "84111", "12/03/2022", "30", "", "UT")
        p3 = Package(3, "233 S. Wacker Dr", "Chicago", "60606", "12/03/2022", "20", "", "IL")
        p4 = Package(4, "1200 Main St.", "Kansas City", "64105", "12/01/2022", "10", "", "MO")
        p5 = Package(5, "111 E. Wacker Dr", "Chicago", "60601", "12/05/2022", "40", "foo", "IL")
        packages = HashMap(5)
        packages.append_item(p1.id, p1)
        packages.append_item(p2.id, p2)
        packages.append_item(p3.id, p3)
        packages.append_item(p4.id, p4)
        packages.append_item(p5.id, p5)
        return packages

    def test_repository_search_by_id(self):
        packages = self._get_sample_packages()
        repo = PackageRepository(packages)

        p1 = packages.get_item(1)
        r1 = repo.get_package_by_id(1)

        self.assertEqual(p1.id, r1.id)

    def test_repository_search_by_address(self):
        packages = self._get_sample_packages()
        repo = PackageRepository(packages)

        p = [packages.get_item(1), packages.get_item(3)]
        addr = p[0].address
        r = repo.get_packages_by_address(addr)

        self.assertIsNotNone(r)
        self.assertEqual(len(r), 2)
        self.assertEqual(p[0].id, r[0].id)
        self.assertEqual(p[1].id, r[1].id)

    def test_repository_search_by_delivery_deadline(self):
        packages = self._get_sample_packages()
        repo = PackageRepository(packages)

        p = [packages.get_item(1), packages.get_item(4)]
        deadline = p[0].delivery_deadline
        r = repo.get_packages_by_delivery_deadline(deadline)

        self.assertIsNotNone(r)
        self.assertEqual(p[0].id, r[0].id)
        self.assertEqual(p[1].id, r[1].id)

    def test_repository_search_by_city(self):
        packages = self._get_sample_packages()
        repo = PackageRepository(packages)

        p = [packages.get_item(1), packages.get_item(3), packages.get_item(5)]
        city = p[0].city
        r = repo.get_packages_by_city(city)

        self.assertIsNotNone(r)
        self.assertTrue(r[0].id == p[0].id or r[0].id == p[1].id or r[0].id == p[2].id)
        self.assertTrue(r[1].id == p[0].id or r[1].id == p[1].id or r[1].id == p[2].id)
        self.assertTrue(r[2].id == p[0].id or r[2].id == p[1].id or r[2].id == p[2].id)

    def test_repository_search_by_zip(self):
        packages = self._get_sample_packages()
        repo = PackageRepository(packages)

        p = [packages.get_item(1), packages.get_item(3)]
        zip_code = p[0].zip_code
        r = repo.get_packages_by_zip_code(zip_code)

        self.assertIsNotNone(r)
        self.assertEqual(p[0].id, r[0].id)
        self.assertEqual(p[1].id, r[1].id)

    def test_repository_search_by_weight(self):
        packages = self._get_sample_packages()
        repo = PackageRepository(packages)

        p = [packages.get_item(1), packages.get_item(3)]
        weight = p[0].mass_kilo
        r = repo.get_packages_by_weight(weight)

        self.assertIsNotNone(r)
        self.assertEqual(p[0].id, r[0].id)
        self.assertEqual(p[1].id, r[1].id)

    def test_repository_search_by_delivery_status(self):
        packages = self._get_sample_packages()
        repo = PackageRepository(packages)

        status = packages.get_item(1).delivery_status
        r = repo.get_packages_by_delivery_status(status)

        self.assertIsNotNone(r)
        for index in range(packages.map_length):
            index += 1
            pkg = packages.get_item(index)
            is_in_rep = any(p.id == pkg.id for p in r)
            self.assertTrue(is_in_rep)

    def test_repository_search_by_special_notes(self):
        packages = self._get_sample_packages()
        repo = PackageRepository(packages)

        item = packages.get_item(5)
        notes = item.special_notes
        r = repo.get_packages_by_special_notes(notes)

        self.assertIsNotNone(r)
        self.assertEqual(item.id, r[0].id)
