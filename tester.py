import csv, string_processing, time, solvers
from config import *
from question_class import *

def test_solver(method, q_type, maximum = 45, debug_mode = True):
    #el argumento maximum esta para no saturar las queries diarias de la api de google
    filename = 'ingame_questions_' + q_type + '.csv'
    with open(filename, 'r') as csvfile:
        questions = csv.reader(csvfile, delimiter=';')
        results = []
        questions_asked = 0
        for row in questions:
            body = row[0]
            options = row[1 : 1+N_OPTIONS]
            start_time = time.time()
            cur_question = Question(body, options)
            scores = method(cur_question)
            end_time = time.time()
            if debug_mode:
                print(1+questions_asked, cur_question.body.original)
                print(', '.join([option.original for option in cur_question.options]))
                print(scores)
                print(end_time - start_time)
            best_index = solvers.argmin if (cur_question.question_type == 'O' and cur_question.is_negative) else solvers.argmax
            if 1+best_index(scores) == int(row[-1]): #compara la posición del mayor score con la respuesta correcta
                results.append(1)
                if debug_mode: print('Correcto')
            else:
                results.append(0)
                if debug_mode: print('Error')
            if questions_asked >= maximum:
                break
            questions_asked += 1
        return results

def classify_questions():
    all_questions = 'ingame_questions.csv'
    c_questions = 'ingame_questionss_c.csv'
    o_questions = 'ingame_questions_o.csv'
    d_questions = 'ingame_questions_d.csv'
    with open(all_questions, 'r') as all_file, open(c_questions, 'w', newline='') as c_file, open(o_questions, 'w', newline='') as o_file, open(d_questions, 'w', newline='') as d_file:
        questions_reader = csv.reader(all_file, delimiter=';')
        c_questions_writer = csv.writer(c_file, delimiter=';')
        o_questions_writer = csv.writer(o_file, delimiter=';')
        d_questions_writer = csv.writer(d_file, delimiter=';')
        for row in questions_reader:
            body = row[0]
            options = row[1 : 1+N_OPTIONS]
            q_type = Question(body, row).question_type
            if q_type == 'C':
                c_questions_writer.writerow(row)
            elif q_type == 'O':
                o_questions_writer.writerow(row)
            elif q_type == 'D':
                d_questions_writer.writerow(row)

def average(results):
    return sum(results)/len(results)
