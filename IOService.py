#   4/23/19 15:40
#   Author: Zach Domke
#   Purpose of this code is to import a new roster and replace the internal roster

import os
import csv
from student import Student


# Main import function. Takes in a new roster and replaces the old roster.
# Checks for a new roster in the path "ImportFolder/New Roster.tsv" and replaces "Resources/Internal Roster.tsv".
class IO:
    def importRoster():
        # Locates the new roster or stops running if there is no new roster.
        try:
            newRoster = open("ImportFolder/New Roster.tsv", 'r')
        except FileNotFoundError:
            return

        # Populates the newStudentQ with the list of students from the new roster.
        newStudentQ = []
        IO.readFile(newStudentQ, newRoster, False)

        # Populates the oldStudentQ with the students from the current/existing roster.
        existingRoster = open("Resources/Internal Roster.tsv", 'r')
        oldStudentQ = []
        IO.readFile(oldStudentQ, existingRoster, True)

        # Checks if the queues are different. If they are different, we confirm with the user. If they are the same, we stop.
        if not IO.importWarning(newStudentQ, oldStudentQ):
            return

        # Overwrites the existing internal roster with the new information.
        existingRoster = open("Resources/Internal Roster.tsv", 'w')
        existingRoster.write("<total times called>\t<times of concern>\t<first name>\t<last name>\t<UO ID>\t<email address>\t<phonetic spelling>\t<reveal code>\n")
        IO.writeToFile(newStudentQ, existingRoster, True)
        existingRoster.close()
        # if os.path.exists("ImportFolder/New Roster.tsv"):
        #     os.remove("ImportFolder/New Roster.tsv")
        return

    # Compares 2 lists of students and confirms changes with the user.
    def importWarning(newStudentQ, oldStudentQ):
        # Populates the list of differences and tells whether the student will be added or removed.
        diffStudentQ = []
        for x in newStudentQ:
            isIn = False
            for y in oldStudentQ:
                if x == y:
                    isIn = True
                    x.setCalledOnCount(y.getCalledOnCount())
                    x.setConcernCount(y.getConcernCount())
            if not isIn:
                diffStudentQ.append((x, "added"))
        for x in oldStudentQ:
            isIn = False
            for y in newStudentQ:
                if x == y:
                    isIn = True
            if not isIn:
                diffStudentQ.append((x, "removed"))

        # Stops running if there are no differences. Nothing will change.
        if not diffStudentQ:
            return False

        # Prints out a warning that changes will be made and lists the changes. Will ask the user to cancel or continue.
        print("WARNING: There are differences between Internal Roster and New Roster:")
        for (x, code) in diffStudentQ:
            print(x.getFName() + ' ' + x.getLName() + ' ' + code)

        # Open window showing differences
        # ask if we continue

        continueImport = True #response
        return continueImport

    def readFile(studentQ, input, importCodes):
        # sys.path = currentSys
        reader = csv.reader(input, delimiter='\t')
        for row in reader:
            if row[-1] == 'X' or row[-1] == "True":
                reveal = True
            else:
                reveal = False
            if importCodes:
                tempStudent = Student(row[2], row[3], row[4], row[5], row[6], reveal)
                tempStudent.setCalledOnCount(row[0])
                tempStudent.setConcernCount(row[1])
            else:
                tempStudent = Student(row[0], row[1], row[2], row[3], row[4], reveal)

            studentQ.append(tempStudent)
        input.close()
        del studentQ[0]
        return studentQ

    def writeToFile(studentQ, output, printCodes):
        if printCodes:
            for student in studentQ:
                output.write(str(student.getCalledOnCount()) + '\t')
                output.write(str(student.getConcernCount()) + '\t')
                output.write(student.getFName() + '\t')
                output.write(student.getLName() + '\t')
                output.write(student.getID() + '\t')
                output.write(student.getEmail() + '\t')
                output.write(student.getPSpell() + '\t')
                output.write(str(student.getReveal()) + '\n')
        else:
            for student in newStudentQ:
                output.write(student.getFName() + '\t')
                output.write(student.getLName() + '\t')
                output.write(student.getID() + '\t')
                output.write(student.getEmail() + '\t')
                output.write(student.getPSpell() + '\t')
                output.write(str(student.getReveal()) + '\n')



def main():
    IO.importRoster()

if __name__ == "__main__":
    main()