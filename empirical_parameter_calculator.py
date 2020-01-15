"""empirical parameter calculator, includes calculation functions for 14 values:
'Enthalpy(kJ/mol)', 'std_enthalpy(kJ/mol)', 'average_atomic_radius', 'Delta(%)', 'Omega', 'Entropy(J/K*mol)', 'Tm(K)',
'std_Tm (%)', 'X', 'std_X(%)', 'VEC', 'std_VEC', 'Density(g/com^3)', 'Price(USD/kg)'
written by Will Nash and Zhipeng Li
version 2.1.1"""

import itertools
import numpy as np
import matminer.utils.data as mm_data

# the market price for most chemical elements, these data are retrieved from
# http://www.leonland.de/elements_by_price/en/list
price_dic = {
    "Ag": 462, "Al": 1.91, "Au": 38189, "B": 2386, "Be": 831.6, "Bi": 10.34, "C": 24, "Ca": 5.93, "Cd": 1.98, "Ce": 7,
    "Co": 59.5, "Cr": 7.64, "Cu": 5.9, "Dy": 350, "Er": 95, "Fe": 0.08, "Gd": 55, "Ge": 1833, "Hf": 1414, "Ho": 1400,
    "In": 341.6, "Ir": 31186, "La": 7, "Li": 115.7, "Lu": 6269, "Mg": 2.26, "Mn": 2.06, "Mo": 16, "Nb": 42, "Nd": 60,
    "Ni": 9.19, "Os": 12860, "P": 300, "Pb": 2.29, "Pd": 34401, "Pr": 85, "Pt": 26492, "Re": 1635, "Rh": 76840,
    "Ru": 14720, "Sb": 7.05, "Sc": 15000, "Si": 1.91, "Sm": 14.35, "Sn": 20, "Sr": 5.4, "Ta": 238, "Tb": 550,
    "Ti": 3.77, "Tm": 6200, "V": 22.6, "W": 25.52, "Y": 35, "Yb": 1600, "Zn": 2.83, "Zr": 23.14, "H": 23.64,
    "He": 40.39, "N": 2.77, "O": 0.64, "F": 1900, "Ne": 629.9, "Na": 3.04, "S": 0.1, "Cl": 1.5, "Ar": 2.56, "K": 13.02,
    "Ga": 278.2, "As": 1.74, "Se": 30.37, "Br": 4.4, "Kr": 1.4, "Rb": 14720, "Te": 55.68, "I": 28.00,
    "Xe": 9.2, "Cs": 73400, "Ba": 550, "Eu": 258, "Hg": 38.44, "Tl": 7400, "Th": 176, "U": 57.76,
}


class EmpiricalParams(object):
    """functions for returning the empirical parameters of alloy compositions where element list is a list of pymatgen
    Elements that are in the alloy, and mol_ratio is their respective mole ratios """

    def __init__(self, element_list, mol_ratio=None):
        self.element_list = element_list
        if mol_ratio is None:  # assume that mol_ratio is evenly distributed amongst elements
            mol_ratio = [1 / len(element_list)] * len(element_list)
        self.mol_ratio = np.divide(mol_ratio, np.sum(mol_ratio))
        self.a = self.mean_atomic_radius()
        self.delta = self.atomic_size_difference()
        self.Tm = self.average_melting_point()
        self.mix_entropy = self.entropy_mixing()
        self.mix_enthalpy = self.enthalpy_mixing()
        self.omega = self.calc_omega()
        self.x = self.mean_electronegativity()
        self.std_x = self.std_electronegativity()
        self.vec = self.average_vec()
        self.density = self.calc_density()
        self.price = self.calc_price()

        # self.k = self.mean_bulk_modulus()
        # self.std_k = self.std_bulk_modulus()
        self.std_enthalpy = self.std_enthalpy_mixing()
        self.std_Tm = self.std_melting_point()
        self.vec_std = self.std_vec()

    def mean_atomic_radius(self):
        """function to return the mean atomic size radius (a) of the alloy"""
        radii = []
        for i in range(len(self.element_list)):
            radii.append(self.element_list[i].atomic_radius)
        avg_radii = np.dot(radii, self.mol_ratio)
        return avg_radii

    def atomic_size_difference(self):
        """function to return the atomic size difference (delta) of the alloy"""
        delta = 0
        radii = []
        for i in range(len(self.element_list)):
            radii.append(self.element_list[i].atomic_radius)

        for j in range(len(self.element_list)):
            delta += self.mol_ratio[j] * np.square((1 - np.divide(radii[j], self.a)))

        return np.sqrt(delta)

    def average_melting_point(self):
        """function to return the average melting point (Tm) of the alloy"""
        Tm = 0
        for i in range(len(self.element_list)):
            Tm += self.mol_ratio[i] * self.element_list[i].melting_point
        return Tm

    def std_melting_point(self):
        """function to return the standard deviation (in percentage) of melting points (sigma_t) of the alloy"""
        sigma_t = 0
        T = []
        for i in range(len(self.element_list)):
            T.append(self.element_list[i].melting_point)

        for j in range(len(self.element_list)):
            sigma_t += self.mol_ratio[j] * np.square((1 - np.divide(T[j], self.Tm)))
        return np.sqrt(sigma_t)

    def entropy_mixing(self):
        """function to return entropy of mixing for alloy elements based on Boltzmann's hypothesis"""
        entropy = 0
        for i in range(len(self.mol_ratio)):
            if self.mol_ratio[i] > 0:
                entropy += self.mol_ratio[i] * np.log(self.mol_ratio[i])
        return -8.31446261815324 * entropy

    def enthalpy_mixing(self):
        """function to return the sum enthalpy of mixing of an alloy system based on binary mixtures and the molar
        ratio """
        enthalpies = []
        mol_coefficients = []

        for pair in itertools.combinations(self.element_list, 2):
            enthalpies.append(mm_data.MixingEnthalpy().get_mixing_enthalpy(*pair))

        for molies in itertools.combinations(self.mol_ratio, 2):
            mol_coefficients.append(4 * np.product(molies))

        enthalpy = np.dot(enthalpies, mol_coefficients)
        return enthalpy

    def std_enthalpy_mixing(self):
        """function to return the standard deviation of enthalpy of mixing (sigma_h) of the alloy"""
        sigma_h = 0
        H = np.zeros((len(self.element_list), len(self.element_list)))
        for i in range(len(self.element_list)):
            for j in range(len(self.element_list)):
                if i != j:
                    H[i][j] = mm_data.MixingEnthalpy().get_mixing_enthalpy(self.element_list[i], self.element_list[j])

        for i in range(len(self.element_list)):
            for j in range(len(self.element_list)):
                if i != j:
                    sigma_h += self.mol_ratio[i] * self.mol_ratio[j] * np.square(H[i][j] - self.enthalpy_mixing())
        sigma_h = sigma_h / 2
        return np.sqrt(sigma_h)

    def calc_omega(self):
        """function to return the omega value of the alloy"""
        if np.abs(self.mix_enthalpy) < 1e-6:
            self.mix_enthalpy = 1e-6
        return self.Tm * self.mix_entropy / (np.abs(self.mix_enthalpy) * 1000)

    def mean_electronegativity(self):
        """function to return the mean electronegativity (x) of the alloy"""
        x_list = []
        for i in range(len(self.element_list)):
            x_list.append(self.element_list[i].X)
        x_avg = np.dot(x_list, self.mol_ratio)
        return x_avg

    def std_electronegativity(self):
        """function to return the standard deviation (in percentage) of electronegativity (sigma_x) of the alloy"""
        sigma_x = 0
        x_list = []
        for i in range(len(self.element_list)):
            x_list.append(self.element_list[i].X)

        for j in range(len(self.element_list)):
            sigma_x += self.mol_ratio[j] * np.square(x_list[j] - self.x)
        return np.sqrt(sigma_x) / self.x

    def num_ve(self, element):
        """function to return the number of valence electron of the element"""
        e_structure = element.full_electronic_structure
        outer = element.full_electronic_structure[-1][0]
        num_e = 0
        for t in e_structure:
            if t[0] == outer - 1 and t[1] == 'd':
                num_e += t[2]
            if t[0] == outer:
                num_e += t[2]
        return num_e

    def average_vec(self):
        """function to return the average of valence electron concentration (vec) of the alloy"""
        vec = 0
        for i in range(len(self.element_list)):
            vec += self.mol_ratio[i] * self.num_ve(self.element_list[i])
        return vec

    def std_vec(self):
        """function to return the standard deviation of valence electron concentration (sigma_vec) of the alloy"""
        sigma_vec = 0
        vec_list = []
        for i in range(len(self.element_list)):
            vec_list.append(self.num_ve(self.element_list[i]))

        for j in range(len(self.element_list)):
            sigma_vec += self.mol_ratio[j] * np.square(vec_list[j] - self.vec)
        return np.sqrt(sigma_vec)

    def mean_bulk_modulus(self):
        """function to return the average of bulk modulus (k) of the alloy"""
        k = 0
        for i in range(len(self.element_list)):
            if self.element_list[i].bulk_modulus is None:
                print(self.element_list[i])
            else:
                k += self.mol_ratio[i] * self.element_list[i].bulk_modulus
        return k

    def std_bulk_modulus(self):
        """function to return the standard deviation of bulk modulus (k) of the alloy"""
        sigma_k = 0
        k_list = []
        for i in range(len(self.element_list)):
            k_list.append(self.element_list[i].bulk_modulus)

        for j in range(len(self.element_list)):
            if self.element_list[i].bulk_modulus is None:
                print(self.element_list[i])
            else:
                sigma_k += self.mol_ratio[j] * np.square(k_list[j] - self.k)
        return np.sqrt(sigma_k)

    def calc_density(self):
        """function to return the density (g/cm^3) of the alloy"""
        mass = 0
        volume = 0
        for i in range(len(self.element_list)):
            mass += float(self.element_list[i].atomic_mass) * self.mol_ratio[i]
            volume += self.mol_ratio[i] * self.element_list[i].molar_volume
        return mass / volume

    def calc_price(self):
        """function to return the price (USD/kg) of the alloy"""
        total_mass = 0
        total_price = 0
        for i in range(len(self.element_list)):
            if not str(self.element_list[i]) in price_dic:
                return 'unknown'
            mass = float(self.element_list[i].atomic_mass) * self.mol_ratio[i]
            total_mass += mass
            total_price += mass * price_dic[str(self.element_list[i])]
        return format(total_price / total_mass, '.2f')
