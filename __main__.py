from argparse import ArgumentParser, FileType
from csv import DictReader, Error
from json import load, dump, JSONDecodeError
from collections import OrderedDict
from colors import Colors
from roles_manager import RolesManager


def _parse_args():
    UTF_8 = "UTF-8"
    parser = ArgumentParser(prog="PLCC",
                                description="description: Module to configure EXISTING infoCourseInstance.json for PrairieLearn")

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

    parser.add_argument("--removeUsers", type=str, dest="rm_user_emails", nargs="+",
                            help="remove users using their email(s)")

    parser.add_argument("--noGroup", action="store_true",
                            help="not group user roles by roles")

    namespace = parser.parse_args()
    return parser, namespace
    

def _load_files(json_fp, csv_fp):
    assert json_fp is not None, "JSON fp is None"
    obj, reader = None, None
    # Parse JSON file
    try:
        obj = load(json_fp)
    except JSONDecodeError as err:
        raise RuntimeError(f"Failed to parse JSON at: \"{json_fp.name}\" with error: {err}")
    except Exception as err:
        raise RuntimeError(f"Unexpected Error: {err}")

    # Parse CSV file if provided
    if csv_fp is not None:
        try:
            reader = DictReader(csv_fp)
        except Error as err:
            raise RuntimeError(f"Failed to parse CSV at \"{csv_fp.name}\" with error: {err}")
        except Exception as err:
            raise RuntimeError(f"Unexpected Error: {err}")
    return obj, reader

def _write_json(obj : dict, json_fp):
    assert obj is not None, "obj is None"
    assert json_fp is not None, "json_fp is None"
    try:
        json_fp.seek(0)
        dump(obj, json_fp, indent=4)
        json_fp.truncate()
    except Exception as err:
        raise RuntimeError(f"Unexpected Error when writing to json file: {err}")


def main():
    parser, ns = _parse_args()
    try:
        # Main Logic
        obj, reader = _load_files(ns.json_path, ns.csv_path)
        mgr = RolesManager(obj)
        mgr.process_csv(reader)
        mgr.process_add_users(ns.student_emails, ns.ta_emails, ns.instructor_emails)
        
        if mgr.is_changed() or not ns.noGroup:
            if not ns.noGroup:
                obj["userRoles"] = OrderedDict(sorted(obj["userRoles"].items(), key=lambda item: item[1]))
            _write_json(obj, ns.json_path)
        print(f"{Colors.OKGREEN}Success!{Colors.ENDC}")
    except RuntimeError as err:
        parser.error(f"{Colors.FAIL}{err}{Colors.ENDC}")
    except AssertionError as err:
        parser.error(f"{Colors.FAIL}Internal Error: {err}{Colors.ENDC}")
    finally:
        # cleaning up
        ns.json_path.close()
        if ns.csv_path is not None:
            ns.csv_path.close()


if __name__ == "__main__":
    main()
