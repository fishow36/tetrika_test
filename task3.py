from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import os

def intersect(pupil, tutor):
    p = 0
    t = 0
    intersections = []
    while True:
        if p > len(pupil) - 2 or t > len(tutor) - 2:
            break
        if pupil[p + 1] <= tutor[t]:
            p += 2
        elif tutor[t + 1] <= pupil[p]:
            t += 2
        else:
            intersections.append(max(pupil[p], tutor[t]))
            intersections.append(min(pupil[p + 1], tutor[t + 1]))
            if pupil[p + 1] == tutor[t + 1]:
                p += 2
                t += 2
            elif pupil[p + 1] < tutor[t + 1]:
                p += 2
            else:
                t += 2
    return intersections

def clean_intervals(intrv_list):
    clean = []
    low = intrv_list[0]
    high = intrv_list[1]
    for i in range(2, len(intrv_list) - 1, 2):
        if intrv_list[i] <= high:
            high = max(high, intrv_list[i + 1])
        else:
            clean.append(low)
            clean.append(high)
            low = intrv_list[i]
            high = intrv_list[i + 1]
    clean.append(low)
    clean.append(high)
    return (clean)

def appearance(intervals):
    p = clean_intervals(intervals['pupil'])
    t = clean_intervals(intervals['tutor'])
    p_t_intersect = intersect(p, t)
    total_intersect = intersect(p_t_intersect, intervals['lesson'])
    total = 0
    for i in range(0, len(total_intersect) - 1, 2):
        total += (total_intersect[i + 1] - total_intersect[i])
    return total

app = Flask(__name__)
api = Api(app)

lesson_args_parse = reqparse.RequestParser()

lesson_args_parse.add_argument('lesson', type=int, action="append")
lesson_args_parse.add_argument('pupil', type=int, action="append")
lesson_args_parse.add_argument('tutor', type=int, action="append")

class Appearance(Resource):
    def post(self):
        args = lesson_args_parse.parse_args()
        print(args)
        return({"answer": appearance(args)})

api.add_resource(Appearance, "/")

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 4444)),debug=False)