import pickle


if __name__ == '__main__':
    with open('model.pkl') as file:
        model = pickle.load(file)
