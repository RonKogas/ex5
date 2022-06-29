import json
import os

students_name_key = "student_name"
registered_courses_key = "registered_courses"
course_name_key = "course_name"
lecturers_key = "lecturers"
file_extension = ".json"
tab_spacecs = 4



def get_dict(input_json_path):
    with open(input_json_path,'r') as student_file:
        students_dict=json.load(student_file)
    return students_dict

def names_of_registered_students(input_json_path, course_name):
    """
    This function returns a list of the names of the students who registered for
    the course with the name "course_name".

    :param input_json_path: Path of the students database json file.
    :param course_name: The name of the course.
    :return: List of the names of the students.
    """
    students_dict=get_dict(input_json_path)
    result_list=[]
    for student_id in students_dict:
        student_name = students_dict[student_id][students_name_key]
        student_course_list=students_dict[student_id][registered_courses_key]
        if course_name in student_course_list:
            result_list.append(student_name)
    return result_list


def enrollment_numbers(input_json_path, output_file_path):
    """
    This function writes all the course names and the number of enrolled
    student in ascending order to the output file in the given path.

    :param input_json_path: Path of the students database json file.
    :param output_file_path: Path of the output text file.
    """
    students_dict=get_dict(input_json_path)
    courses_list=[]
    num_dict = {}
    end_line="\n"
    for student_id in students_dict:
        student_course_list=students_dict[student_id][registered_courses_key]
        for course in student_course_list:
            if course not in courses_list:
                courses_list.append(course)
    courses_list=sorted(courses_list)
    with open(output_file_path,'w') as out_file:
            for course in courses_list:
                num_students=len(names_of_registered_students(input_json_path, course))
                out_file.write('"'+course+'" '+str(num_students)+end_line)  


def courses_for_lecturers(json_directory_path, output_json_path):
    """
    This function writes the courses given by each lecturer in json format.

    :param json_directory_path: Path of the semsters_data files.
    :param output_json_path: Path of the output json file.
    """
    json_files = [file for file in os.listdir(json_directory_path) if file.endswith(file_extension)]
    lecturer_courses_dict = {}
    for file in json_files:
        file_path = os.path.join(json_directory_path, file)
        with open(file_path, "r") as curr_file:
            curr_courses_dict = json.load(curr_file)
        for course_id in curr_courses_dict:
            course_name = curr_courses_dict[course_id][course_name_key]
            lecturers_list = curr_courses_dict[course_id][lecturers_key]
            for lecturer in lecturers_list:
                if lecturer not in lecturer_courses_dict:
                    lecturer_courses_dict[lecturer] = [course_name]
                if course_name not in lecturer_courses_dict[lecturer]:
                    lecturer_courses_dict[lecturer].append(course_name)
    with open(output_json_path,'w') as out_file:
            json.dump(lecturer_courses_dict, out_file, indent=tab_spacecs)
