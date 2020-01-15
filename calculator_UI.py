"""This script provides the user interface of the empirical parameter calculator.
written by Zhipeng Li
version 2.1.1"""
import csv
import xlrd
from tkinter import *
from tkinter import filedialog
from pymatgen.core.periodic_table import Element
import empirical_parameter_calculator as calculator


# the maximum number of elements can be included in the individual calculation process
num_elements = 10

root = Tk()
# set the title of the application.
root.title('Empirical Property Calculator')
root.file_path = ''

input_frame = Frame(root, bd=20)
input_frame.place(x=0, y=0)
output_frame = Frame(root)
output_frame.place(x=40, y=120)
input_frame.rowconfigure(3, minsize=10)
output_frame.columnconfigure(1, minsize=150)
output_frame.columnconfigure(3, minsize=150)


def center_window(w, h):
    """set the size and position of the application window."""
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def open_calculation_window():
    """create a window for large scale calculation."""
    window = Toplevel(root)
    # set the title, size, position of the batch calculation window.
    window.title('Batch Calculation')
    w = 450
    h = 250
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2) + 500
    y = (hs / 2) - (h / 2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def open_file_name():
        # create an open file dialogue for selecting source file
        root.file_path = filedialog.askopenfilename(title='Select File to Generate Result',
                                                    filetypes=(("csv files", "*.csv"), ("xlsx files", "*.xlsx")))
        in_entry.insert(0, root.file_path)

    # set the input file selection button
    in_btn = Button(window, text='Select', command=open_file_name)
    in_btn.place(x=350, y=80)

    def output_path_select():
        # create an dialogue for selecting output file path
        root.output_path = filedialog.askdirectory()
        out_entry.insert(0, root.output_path)

    # set the output file path selection button
    out_btn = Button(window, text='Select', command=output_path_select)
    out_btn.place(x=350, y=120)

    def start_calculation():
        # start batch calculation
        generate_empirical_properties()
        window.destroy()

    # set the batch calculation button
    calculate_btn = Button(window, text='Start Calculation', command=start_calculation)
    calculate_btn.place(x=170, y=160)

    # set the labels and entries for the batch calculation window

    in_path = Label(window, text='Input File Path:')
    in_path.place(x=47, y=80)
    in_entry = Entry(window)
    in_entry.place(x=150, y=80)

    out_path = Label(window, text='Output File Path:')
    out_path.place(x=35, y=120)
    out_entry = Entry(window)
    out_entry.place(x=150, y=120)

    window.winfo_toplevel()


def generate_empirical_properties():
    """This is the function that generates all the empirical parameters for the selected source file"""
    out = open(root.output_path + '/batch_calculation_results.csv', 'a', newline='')
    csv_write = csv.writer(out, dialect='excel')
    csv_write.writerow(['Elements', 'Molar_ratios', 'Enthalpy(kJ/mol)', 'std_enthalpy(kJ/mol)', 'Delta(%)', 'Omega', 'Entropy(J/K*mol)', 'Tm(K)',
                        'std_Tm (%)', 'X', 'std_X(%)', 'VEC', 'std_VEC', 'Density(g/com^3)', 'Price(USD/kg)'])
    if root.file_path.split('.')[1] == 'csv':
        with open(root.file_path) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=',')
            for row in read_csv:
                print(row)
                if len(row) > 0 and row[0] != 'Element':
                    alloy = row[0].split(',')
                    ratio = row[1].split(',')

                    alloy_elements = []
                    mol_ratio = []
                    element_str = ""
                    ratio_str = ""
                    for j in range(len(alloy)):
                        if len(alloy[j]) > 0:
                            alloy_elements.append(Element(alloy[j].strip()))
                            mol_ratio.append(float(ratio[j]))
                            element_str += (alloy[j] + '-')
                            ratio_str += (ratio[j] + '-')
                    alloy = calculator.EmpiricalParams(alloy_elements, mol_ratio)
                    csv_write.writerow(
                        [element_str, ratio_str, alloy.mix_enthalpy, alloy.std_enthalpy, 100 * alloy.delta, alloy.omega,
                         alloy.mix_entropy, 100 * alloy.Tm, alloy.std_Tm, alloy.x, 100 * alloy.std_x, alloy.vec,
                         alloy.vec_std, alloy.density, alloy.price])

    if root.file_path.split('.')[1] == 'xlsx':
        wb = xlrd.open_workbook(root.file_path)
        sheet = wb.sheet_by_index(0)
        for i in range(sheet.nrows):
            row = sheet.row_values(i)
            if len(row) > 0 and row[0] != 'Element':
                alloy = row[0].split(',')
                ratio = row[1].split(',')

                alloy_elements = []
                mol_ratio = []
                element_str = ""
                ratio_str = ""
                for j in range(len(alloy)):
                    if len(alloy[j]) > 0:
                        alloy_elements.append(Element(alloy[j].strip()))
                        mol_ratio.append(float(ratio[j]))
                        element_str += (alloy[j] + '-')
                        ratio_str += (ratio[j] + '-')
                alloy = calculator.EmpiricalParams(alloy_elements, mol_ratio)
                csv_write.writerow(
                        [element_str, ratio_str, alloy.mix_enthalpy, alloy.std_enthalpy, 100 * alloy.delta, alloy.omega,
                         alloy.mix_entropy, 100 * alloy.Tm, alloy.std_Tm, alloy.x, 100 * alloy.std_x, alloy.vec,
                         alloy.vec_std, alloy.density, alloy.price])
    out.close()


center_window(520, 500)

# set the menu
menu = Menu(root)
root.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='Batch Calculation', command=open_calculation_window)
subMenu.add_separator()
subMenu.add_command(label='Exit', command=root.destroy)

# set the individual calculation label and input entry
label_1 = Label(input_frame, text='Elements:')
label_2 = Label(input_frame, text='Ratios:')
label_1.grid(row=1, column=0, sticky=E)
label_2.grid(row=2, column=0, sticky=E)

element_entries = []
ratio_entries = []
for i in range(num_elements):
    element_entries.append(Entry(input_frame, width=5))
    ratio_entries.append(Entry(input_frame, width=5))
    element_entries[i].grid(row=1, column=i + 1)
    ratio_entries[i].grid(row=2, column=i + 1)

# set the individual calculation button
calc_btn = Button(input_frame, text='Show Empirical Properties', fg='blue')
calc_btn.grid(row=4, columnspan=20)

# set the labels and entries for all the calculated empirical parameters
entropy_lb = Label(output_frame, text='ΔS:')
enthalpy_lb = Label(output_frame, text='ΔH:')
std_enthalpy_lb = Label(output_frame, text='std H:')
a_lb = Label(output_frame, text='a:')
delta_lb = Label(output_frame, text='δ:')
vec_lb = Label(output_frame, text='VEC:')
std_vec_lb = Label(output_frame, text='ΔVEC:')
omega_lb = Label(output_frame, text='Ω:')
tm_lb = Label(output_frame, text='Tm:')
std_tm_lb = Label(output_frame, text='ΔTm:')
X_lb = Label(output_frame, text='X:')
std_X_lb = Label(output_frame, text='ΔX:')
density_lb = Label(output_frame, text='density:')
price_lb = Label(output_frame, text='price:')

entropy_lb.grid(row=5, column=0, sticky=E)
enthalpy_lb.grid(row=7, column=0, sticky=E)
std_enthalpy_lb.grid(row=7, column=2, sticky=E)
a_lb.grid(row=6, column=0, sticky=E)
delta_lb.grid(row=6, column=2, sticky=E)
vec_lb.grid(row=10, column=0, sticky=E)
std_vec_lb.grid(row=10, column=2, sticky=E)
omega_lb.grid(row=5, column=2, sticky=E)
tm_lb.grid(row=8, column=0, sticky=E)
std_tm_lb.grid(row=8, column=2, sticky=E)
X_lb.grid(row=9, column=0, sticky=E)
std_X_lb.grid(row=9, column=2, sticky=E)
density_lb.grid(row=12, column=0, sticky=E)
price_lb.grid(row=12, column=2, sticky=E)

entropy = Label(output_frame, text='*')
enthalpy = Label(output_frame, text='*')
std_enthalpy = Label(output_frame, text='*')
a = Label(output_frame, text='*')
delta = Label(output_frame, text='*')
vec = Label(output_frame, text='*')
std_vec = Label(output_frame, text='*')
omega = Label(output_frame, text='*')
tm = Label(output_frame, text='*')
std_tm = Label(output_frame, text='*')
X = Label(output_frame, text='*')
std_X = Label(output_frame, text='*')
density = Label(output_frame, text='*')
price = Label(output_frame, text='*')

entropy.grid(row=5, column=1, sticky=W)
enthalpy.grid(row=7, column=1, sticky=W)
std_enthalpy.grid(row=7, column=3, sticky=W)
a.grid(row=6, column=1, sticky=W)
delta.grid(row=6, column=3, sticky=W)
vec.grid(row=10, column=1, sticky=W)
std_vec.grid(row=10, column=3, sticky=W)
omega.grid(row=5, column=3, sticky=W)
tm.grid(row=8, column=1, sticky=W)
std_tm.grid(row=8, column=3, sticky=W)
X.grid(row=9, column=1, sticky=W)
std_X.grid(row=9, column=3, sticky=W)
density.grid(row=12, column=1, sticky=W)
price.grid(row=12, column=3, sticky=W)


def calculate(event):
    """This function calculates the empirical parameters for individual alloy"""
    alloy_elements = []
    mol_ratio = []
    for i in range(num_elements):
        if len(element_entries[i].get().strip()) > 0:
            alloy_elements.append(Element(element_entries[i].get().strip()))
        if len(ratio_entries[i].get().strip()) > 0:
            mol_ratio.append(float(ratio_entries[i].get().strip()))

    if len(alloy_elements) > len(mol_ratio):
        tmp = []
        for i in range(len(mol_ratio)):
            tmp.append(alloy_elements[i])
        alloy_elements = tmp

    if len(alloy_elements) < len(mol_ratio):
        tmp = []
        for i in range(len(alloy_elements)):
            tmp.append(mol_ratio[i])
        mol_ratio = tmp

    alloy = calculator.EmpiricalParams(element_list=alloy_elements, mol_ratio=mol_ratio)

    entropy.config(text='{:.2f} J/(K*mol)'.format(alloy.mix_entropy))
    enthalpy.config(text='{:.2f} kJ/mol'.format(alloy.mix_enthalpy))
    std_enthalpy.config(text='{:.2f} kJ/mol'.format(alloy.std_enthalpy))
    a.config(text='{:.2f} angstrom'.format(alloy.a))
    delta.config(text='{:.2f} %'.format(100 * alloy.delta))
    vec.config(text='{:.2f}'.format(alloy.vec))
    std_vec.config(text='{:.2f}'.format(alloy.vec_std))
    omega.config(text='{:.2f}'.format(alloy.omega))
    tm.config(text='{:.2f} K'.format(alloy.Tm))
    std_tm.config(text='{:.2f} %'.format(100 * alloy.std_Tm))
    X.config(text='{:.2f}'.format(alloy.x))
    std_X.config(text='{:.2f} %'.format(100 * alloy.std_x))
    density.config(text='{:.2f} g/cm^3'.format(alloy.density))
    price.config(text='{} USD/kg'.format(alloy.price))


calc_btn.bind('<Button-1>', calculate)

# run the program
root.mainloop()
