from argparse import ArgumentParser, FileType

def parse_args():
    UTF_8 = "UTF-8"
    parser = ArgumentParser(prog="PLCC",
                                description="description: Module to configure infoCourseInstance.json for PrairieLearn")

    parser.add_argument("dest", type=FileType("rw", encoding=UTF_8), metavar="JSON_PATH",
                            help="relative or absolute path to existing infoCourseInstance.json file")

    parser.add_argument("-c", "--csv", type=FileType("r", encoding=UTF_8),
                            metavar="PATH", dest="csv_path",
                            help="relative or absolute path to roster csv file from Canvas")

    parser.add_argument("--addStudent", type=str, metavar="STUDENT_EMAIL", dest="student_email",
                            help="add a student to the class using their email")

    parser.add_argument("--addTA", type=str, metavar="TA_EMAIL", dest="ta_email",
                            help="add a TA to the class using their email")

    parser.add_argument("--addInstructor", type=str, metavar="INSTRUCTOR_EMAIL", dest="instructor_email",
                            help="add a instructor to the class using their email")

    namespace = parser.parse_args()
    return parser, namespace
    


def main():
    parser, namespace = parse_args()


if __name__ == "__main__":
    main()
