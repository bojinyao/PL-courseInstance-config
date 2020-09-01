from argparse import ArgumentParser, FileType
from csv import DictReader, Error
from json import load, dump, JSONDecodeError
from colors import COLORS


def _parse_args():
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
    

def _load_files(json_fp, csv_fp):
    # Parse JSON file
    try:
        obj = load(json_fp)
    except JSONDecodeError as err:
        raise RuntimeError(f"Failed to parse JSON at: \"{json_fp.name}\" with error: {err}")
    except Exception as err:
        raise RuntimeError(f"Unexpected Error: {err}")
    finally:
        json_fp.close()

    # Parse CSV file if provided
    if csv_fp is not None:
        try:
            reader = DictReader(csv_fp)
        except Error as err:
            raise RuntimeError(f"Failed to parse CSV at \"{csv_fp.name}\" with error: {err}")
        except Exception as err:
            raise RuntimeError(f"Unexpected Error: {err}")
        finally:
            csv_fp.close()
    return obj, reader


def process_csv(json_fp, csv_fp):
    ...



def main():
    parser, namespace = _parse_args()
    try:
        obj, reader = _load_files(namespace.json_path, namespace.csv_path)
    except RuntimeError as err:
        parser.error(f"{COLORS.FAIL}{err}{COLORS.ENDC}")


    # cleaning up
    namespace.json_path.close()
    namespace.csv_path.close()
    print(f"{COLORS.OKGREEN}Success!{COLORS.ENDC}")



if __name__ == "__main__":
    main()
