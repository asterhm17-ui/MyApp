from kivy.lang import Builder
from kivymd.app import MDApp

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


TextInput(
    multiline=False,
    input_type='text',  # or 'number' if needed
    input_filter=None   # or 'int', 'float'
        )
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'dock')  # Options: 'system', 'dock', 'multi', 'none'

class PayrollApp(MDApp):
    def build(self):
        return Builder.load_file("payroll.kv")

    def get_tax_brackets(self, month, year):
        if (month >= 11 and year >= 2017):
            return [
                (0, 2000, 0, 0),
                (2001, 4000, 0.15, 300),
                (4001, 7000, 0.20, 500),
                (7001, 10000, 0.25, 850),
                (10001, 14000, 0.30, 1350),
                (14001, float('inf'), 0.35, 2050)
            ]
        elif (year == 2017 and month < 11) or (2008 < year < 2017):
            return [
                (0, 600, 0, 0),
                (601, 1650, 0.10, 60),
                (1651, 3200, 0.15, 142.50),
                (3201, 5250, 0.20, 302.50),
                (5251, 7800, 0.25, 565),
                (7801, 10900, 0.30, 955),
                (10901, float('inf'), 0.35, 1500)
            ]
        else:
            return []

    def calculate(self):
        try:
            salary = float(self.root.ids.salary.text)
            other_income = float(self.root.ids.other_income.text)
            month = int(self.root.ids.month.text)
            year = int(self.root.ids.year.text)
            pension = salary * 0.07 if self.root.ids.pension_yes.active else 0
            total_income = salary + other_income

            brackets = self.get_tax_brackets(month, year)
            tax = 0
            for lower, upper, rate, deduction in brackets:
                if lower <= total_income <= upper:
                    tax = total_income * rate - deduction
                    break

            net_pay = total_income - pension - tax

            self.root.ids.pension_val.text = f"{pension:.2f}"
            self.root.ids.tax_val.text = f"{tax:.2f}"
            self.root.ids.netpay_val.text = f"{net_pay:.2f}"

        except ValueError:
            self.root.ids.netpay_val.text = "Invalid input!"

    def reset(self):
        for field in ['name', 'salary', 'other_income', 'month', 'year']:
            self.root.ids[field].text = ""
        self.root.ids.pension_yes.active = True
        self.root.ids.pension_val.text = ""
        self.root.ids.tax_val.text = ""
        self.root.ids.netpay_val.text = ""


if __name__ == "__main__":
    PayrollApp().run()

