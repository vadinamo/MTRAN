class Car {
    public:
        string name;
        int year;
        float engine_capacity;
}

void sort_by_year(var arr[], int size, int pick) {
    switch (pick)
    {
    case 1:
        bool correct = false;
        while (!correct) {
            correct = true;
            for(int i = 0; i < (size - 1); i++) {
                var a = arr[i].year;
                var b = arr[i + 1].year;
                if(a > b) {
                    var buff = arr[i];
                    arr[i] = arr[i + 1];
                    arr[i + 1] = buff;
                    correct = false;
                }
            }
        }
        break;
    case 2:
        bool correct = false;
        while (!correct) {
            correct = true;
            for(int i = 0; i < (size - 1); i++) {
                var a = arr[i].year;
                var b = arr[i + 1].year;
                if(a < b) {
                    var buff = arr[i];
                    arr[i] = arr[i + 1];
                    arr[i + 1] = buff;
                    correct = false;
                }
            }
        }
        break;
    }

    for (int i = 0; i < size; i++) {
        var a = arr[i].year;
        cout << a << " ";
    }
    cout << endl;
}

void sort_by_engine_capacity(var arr[], int size, int pick) {
    switch (pick)
    {
    case 1:
        bool correct = false;
        while (!correct) {
            correct = true;
            for(int i = 0; i < (size - 1); i++) {
                var a = arr[i].engine_capacity;
                var b = arr[i + 1].engine_capacity;
                if(a > b) {
                    var buff = arr[i];
                    arr[i] = arr[i + 1];
                    arr[i + 1] = buff;
                    correct = false;
                }
            }
        }
        break;
    case 2:
        bool correct = false;
        while (!correct) {
            correct = true;
            for(int i = 0; i < (size - 1); i++) {
                var a = arr[i].engine_capacity;
                var b = arr[i + 1].engine_capacity;
                if(a < b) {
                    var buff = arr[i];
                    arr[i] = arr[i + 1];
                    arr[i + 1] = buff;
                    correct = false;
                }
            }
        }
        break;
    }

    for (int i = 0; i < size; i++) {
        var a = arr[i].engine_capacity;
        cout << a << " ";
    }
    cout << endl;
}

int main() {
    Car car0 = Car("3", 3, 3.3);
    Car car1 = Car("2", 2, 2.2);
    Car car2 = Car("1", 1, 1.1);
    Car car3 = Car("4", 4, 4.4);
    Car car4 = Car("5", 5, 5.5);
    var arr[5] {car0, car1, car2, car3, car4};


    int pick1 = 0, pick2 = 0;
    while (true)
    {
        cin >> pick1;
        switch (pick1)
        {
            case 1:
                cin >> pick2;
                sort_by_year(arr, 4, pick2);
                break;
            case 2:
                cin >> pick2;
                sort_by_engine_capacity(arr, 4, pick2);
                break;
        }
    }
    

    return 0;
}