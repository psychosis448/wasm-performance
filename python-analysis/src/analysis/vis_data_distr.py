import json
import matplotlib.pyplot as plt

# note: data moved
def validate_data():
    data_kind = 'unsorted'
    with open('../data/' + data_kind + '.json', 'r') as test_data_file:
        data=test_data_file.read()

    test_data = json.loads(data)

    for d in test_data:
        print('Plotting for: ' + d)
        fig, ax = plt.subplots()
        ax.scatter(x=range(0, len(test_data[d])), y=test_data[d], s=1)
        ax.set_title('Data Distribution for Array of length ' + d)
        ax.set_xlabel('index')
        ax.set_ylabel('value')
        plt.savefig('../data/' + data_kind + '_' + d)
