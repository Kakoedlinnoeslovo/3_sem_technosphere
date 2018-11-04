from flask import Flask
from flask import request
app = Flask(__name__)

import numpy as np
#import commands



def oracle(x):
    x = list(x)
    query = "./Oracle.static " + ' '.join(map(lambda y:str(y), x))
    if query.strip() == 'Function is undefined at this point!' or query.strip() == 'inf':
        return None
    return np.array(x + [float(commands.getoutput(query))])

@app.route('/')
def hello_world():
    query_string = request.query_string

    query_list  = query_string.split()
    print(query_list)


    return query_string

if __name__ == '__main__':
    app.run()
