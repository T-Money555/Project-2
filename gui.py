from tkinter import *
import csv

class Gui:

    def __init__(self, window) -> None:
        """
        Initializes the Title, Label and Entry Box for the name variable and attempt
        number variable, and the submit button, including the function call when it is
        pressed and the label for the error message underneath
        """
        self.__submit_pressed = 0
        self.window = window

        self.title_label = Label(text = "Grade Database Editor")
        self.title_label.pack(anchor = 'n')

        self.frame_one = Frame(self.window)
        self.name_label = Label(self.frame_one, text = "Student Name:\t      ")
        self.name_input = Entry(self.frame_one)
        self.name_label.pack(side = 'left', padx = 10, pady = 10)
        self.name_input.pack(side = 'left')
        self.frame_one.pack(anchor = 'w')

        self.frame_two = Frame(self.window)
        self.attempts_label = Label(self.frame_two, text = "No of Attempts (1-4): ")
        self.attempts_input = Entry(self.frame_two)
        self.attempts_label.pack(side = 'left', padx = 10, pady = 10)
        self.attempts_input.pack(side = 'left')
        self.frame_two.pack(anchor = 'w')

        self.submit_label = Label(text = "")
        self.submit_label.pack(side = BOTTOM)
        self.submit_button = Button(self.window, text = "Submit", command=self.submit)
        self.submit_button.pack(pady = 10, side = BOTTOM)

        self.attempts = []

    def submit(self) -> None:
        """
        Carries out 4 main functions of the submit button. 1st it checks the name and number of grades.
        2nd it initializes the text boxes for the same number of grades entered. 3rd it assigns grades
        to a list checks if the grades are valid entries and assigns an average. 4th it puts name,
        grades, and average into a csv. This is a long segment and pulls lots of outside methods together.
        Some methods are repeated because of repetitive processes. This is also where exception handling takes
        place.
        """
        try:
            #Submit number of attempts and name
            name = self.name_input.get()
            name_contains_num = any(char.isdigit() for char in name) #Looked up to ensure names don't contain numbers
            name_in_grades = self.check_names(name)
            if name == "" or (not self.attempts_input.get().isnumeric()) or name_contains_num or name_in_grades:
                raise ValueError
            num_attempts = int(self.attempts_input.get())
            if self.__submit_pressed == 0:
                if num_attempts == 1:
                    self.init_grade1()
                    self.__submit_pressed = 1
                    self.attempts_input.config(state = DISABLED)
                    self.submit_label.config(text = "", fg = "black")
                elif num_attempts == 2:
                    self.init_grade1()
                    self.init_grade2()
                    self.__submit_pressed = 1
                    self.attempts_input.config(state = DISABLED)
                    self.submit_label.config(text = "", fg = "black")
                elif num_attempts == 3:
                    self.init_grade1()
                    self.init_grade2()
                    self.init_grade3()
                    self.__submit_pressed = 1
                    self.attempts_input.config(state = DISABLED)
                    self.submit_label.config(text = "", fg = "black")
                elif num_attempts == 4:
                    self.init_grade1()
                    self.init_grade2()
                    self.init_grade3()
                    self.init_grade4()
                    self.__submit_pressed = 1
                    self.attempts_input.config(state = DISABLED)
                    self.submit_label.config(text = "", fg = "black")
                else:
                    self.__submit_pressed = 0
                    raise ValueError

            #Submit grades
            elif self.__submit_pressed == 1:
                try:
                    self.attempts = self.attempts_list(num_attempts)
                    for a in self.attempts:
                        if 0 > a or a > 100 or type(a) == 'string':
                            raise ValueError
                    ave = self.average(self.attempts)
                    self.store_grades(name, self.attempts, ave)
                    self.error_reset(num_attempts)
                    self.submit_label.config(text = "Grade Updated", fg = 'black')
                    self.reset(num_attempts)

                #Exception handling for grades
                except ValueError:
                    self.submit_label.config(text = "Enter valid numbers", fg = 'red')
                    if num_attempts > 0 and (self.attempts[0] < 0 or self.attempts[0] > 100 ):
                        self.grade1_error.config(text = "       Enter a valid number for Grade 1 (0-100)", fg = 'red')
                    if num_attempts > 1 and (self.attempts[1] < 0 or self.attempts[1] > 100):
                        self.grade2_error.config(text = "       Enter a valid number for Grade 2 (0-100)", fg = 'red')
                    if num_attempts > 2 and (self.attempts[2] < 0 or self.attempts[2] > 100 ):
                        self.grade3_error.config(text = "       Enter a valid number for Grade 3 (0-100)", fg = 'red')
                    if num_attempts > 3 and (self.attempts[3] < 0 or self.attempts[3] > 100):
                        self.grade4_error.config(text = "       Enter a valid number for Grade 4 (0-100)", fg = 'red')

        #Exception handling for the name and attempt submissions
        except ValueError:
            if (self.name_input.get() == "" or self.attempts_input.get() == "" or
                    not self.attempts_input.get().isnumeric()) or name_contains_num:
                self.submit_label.config(text = "Enter correct inputs for name and attempts (1-4)", fg = 'red')
            elif self.attempts_input.get().isnumeric() and (0 > int(self.attempts_input.get()) or int(self.attempts_input.get()) > 4):
                self.submit_label.config(text = "Enter a number (1-4)", fg='red')
            elif name_in_grades:
                self.submit_label.config(text="Name already in grades", fg='red')

    def check_names(self, name):
        with open ('grades.csv', 'r', newline ="\n") as csvfile:
            match_name = csv.reader(csvfile)
            for line in match_name:
                print(line[0])
                if line[0] == name:

                    return True
            return False

    def average(self, attempts) -> float:
        """
        Averages all grades greater than 0
        """
        sum = 0
        count = 0
        for i in attempts:
            if i > 0:
                sum += i
                count += 1
        if sum > 0 and count > 0:
            return float(f'{sum/count:.2f}')
        else:
            return 0

    def store_grades(self, name, attempts, ave) -> None:
        """
        Stores each of the grades in a csv file.
        """
        line = [name] + attempts + [ave]
        with open ('grades.csv', 'a', newline ="\n") as csvfile:
            update_grades = csv.writer(csvfile)
            update_grades.writerow(line)

    def attempts_list(self, num_attempts) -> list:
        """
        Stores each grade in a list and changes all values to integers
        """
        attempts_list = []
        if num_attempts == 1:
            attempts_list = [(self.grade1_input.get()), "0", "0", "0"]
        elif num_attempts == 2:
            attempts_list = [(self.grade1_input.get()), (self.grade2_input.get()), "0", "0"]
        elif num_attempts == 3:
            attempts_list = [(self.grade1_input.get()), (self.grade2_input.get()), (self.grade3_input.get()), "0"]
        elif num_attempts == 4:
            attempts_list = [(self.grade1_input.get()), (self.grade2_input.get()),
                    (self.grade3_input.get()), (self.grade4_input.get())]
        else:
            self.submit_label.config(text = "How did we get here?", fg = 'red')

        for s in range(len(attempts_list)):
            if attempts_list[s].isnumeric():
                attempts_list[s] = int(attempts_list[s])
            else:
                attempts_list[s] = -1

        return attempts_list

    def error_reset(self, num_attempts) -> None:
        """
        Resets all error messages to a blank label
        """
        if num_attempts > 0:
            self.grade1_error.config(text = "")
        if num_attempts > 1:
            self.grade2_error.config(text = "")
        if num_attempts > 2:
            self.grade3_error.config(text = "")
        if num_attempts > 3:
            self.grade4_error.config(text = "")
        self.submit_label.config(text = "")

    def reset(self, num_attempts):
        """
        Resets the grade editor to the starting position
        """
        self.__submit_pressed = 0
        self.error_reset(num_attempts)
        self.attempts_input.config(state=NORMAL)
        self.attempts_input.delete(0, END)
        self.name_input.delete(0, END)
        self.submit_label.config(text = "", fg = "black")
        if num_attempts > 0:
            self.frame_three.pack_forget()
        if num_attempts > 1:
            self.frame_four.pack_forget()
        if num_attempts > 2:
            self.frame_five.pack_forget()
        if num_attempts > 3:
            self.frame_six.pack_forget()

    def init_grade1(self) -> None:
        '''
        Initializes each of the attempt labels and entry boxes
        individually for use in the submit function (Initializes for grade 1)
        '''
        self.frame_three = Frame(self.window)
        self.grade1_label = Label(self.frame_three, text = "\t       Grade 1:")
        self.grade1_input = Entry(self.frame_three)
        self.grade1_error = Label(self.frame_three, text = "")
        self.grade1_label.pack(side = 'left', padx = 10, pady = 10)
        self.grade1_input.pack(side = 'left')
        self.grade1_error.pack(side = 'left')
        self.frame_three.pack(anchor = 'w')

    def init_grade2(self) -> None:
        """
        Initializes for grade 2
        """
        self.frame_four = Frame(self.window)
        self.grade2_label = Label(self.frame_four, text = "\t       Grade 2:")
        self.grade2_input = Entry(self.frame_four)
        self.grade2_error = Label(self.frame_four, text = "")
        self.grade2_label.pack(side = 'left', padx=10, pady=10)
        self.grade2_input.pack(side = 'left')
        self.grade2_error.pack(side = 'left')
        self.frame_four.pack(anchor = 'w')

    def init_grade3(self) -> None:
        """
        Initializes for grade 3
        """
        self.frame_five = Frame(self.window)
        self.grade3_label = Label(self.frame_five, text = "\t       Grade 3:")
        self.grade3_input = Entry(self.frame_five)
        self.grade3_error = Label(self.frame_five, text = "")
        self.grade3_label.pack(side = 'left', padx=10, pady=10)
        self.grade3_input.pack(side = 'left')
        self.grade3_error.pack(side = 'left')
        self.frame_five.pack(anchor = 'w')

    def init_grade4(self) -> None:
        """
        Initializes for grade 4
        """
        self.frame_six = Frame(self.window)
        self.grade4_label = Label(self.frame_six, text = "\t       Grade 4:")
        self.grade4_input = Entry(self.frame_six)
        self.grade4_error = Label(self.frame_six, text = "")
        self.grade4_label.pack(side = 'left', padx=10, pady=10)
        self.grade4_input.pack(side = 'left')
        self.grade4_error.pack(side = 'left')
        self.frame_six.pack(anchor = 'w')