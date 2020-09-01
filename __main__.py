from argparse import ArgumentParser, FileType
from csv import DictReader, Error
from json import load, dump, JSONDecodeError
from colors import COLORS


def parse_args():
    UTF_8 = "UTF-8"
    parser = ArgumentParser(prog="PLCC",
                                description="description: Module to configure infoCourseInstance.json for PrairieLearn")

    parser.add_argument("json_path", type=FileType("r+", encoding=UTF_8), metavar="JSON_PATH",
                            help="relative or absolute path to existing infoCourseInstance.json file")

    parser.add_argument("-c", "--csv", type=FileType("r", encoding=UTF_8), dest="csv_path",
                            help="relative or absolute path to roster csv file from Canvas")

    parser.add_argument("--addStudents", type=str, dest="student_emails", nargs="+",
                            help="add student(s) to the class using their email(s)")

    parser.add_argument("--addTAs", type=str, dest="ta_emails", nargs="+",
                            help="add TA(s) to the class using their email(s)")

    parser.add_argument("--addInstructors", type=str, dest="instructor_emails", nargs="+",
                            help="add instructor(s) to the class using their email(s)")

    parser.add_argument("-u", "--unsorted", action="store_true",
                            help="not sort instructors, TAs, and students by email address in alphabetical order when saving")

    namespace = parser.parse_args()
    return parser, namespace
    

def processCSV(json_file, csv_file):
    ...



def main():
    parser, namespace = parse_args()
    try:
        # Parse JSON file
        try:
            obj = load(namespace.json_path)
        except JSONDecodeError as err:
            raise RuntimeError(f"Failed to parse json at: \"{namespace.json_path.name}\" with error: {err}")
        except Exception as err:
            raise RuntimeError(f"Unexpected Error: {err}")
        finally:
            namespace.json_path.close()

        # Parse CSV file if provided
        if namespace.csv_path is not None:
            try:
                reader = DictReader(namespace.csv_path)
            except Error as err:
                raise RuntimeError(f"Failed to parse csv at \"{namespace.csv_path.name}\" with error: {err}")
            except Exception as err:
                raise RuntimeError(f"Unexpected Error: {err}")
            finally:
                namespace.csv_path.close()
    except RuntimeError as err:
        parser.error(f"{COLORS.FAIL}{err}{COLORS.ENDC}")


    # cleaning up
    namespace.json_path.close()
    namespace.csv_path.close()
    print(f"{COLORS.OKGREEN}Task finished with no error{COLORS.ENDC}")



if __name__ == "__main__":
    main()
