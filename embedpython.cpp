#include <Python.h>
#include <iostream>
#include <vector>
#include <thread>
#include <chrono>

int main() {
    std::cout << "C++ to embedded Python DynamicDist" << std::endl;

    Py_Initialize();
    if (!Py_IsInitialized()) {
        std::cerr << "Failed to initialize Python interpreter" << std::endl;
        return 1;
    }

    // make sure the embedded Python runs
    PyRun_SimpleString("import sys");
    // // add the current directory
    PyRun_SimpleString("sys.path.append('.')");
    // PyRun_SimpleString("print(sys.path)");
    PyRun_SimpleString("from DynamicDist import DynamicDist");

    // Import NumPy module to validate site-packages on path
    PyObject* numpyModule = PyImport_ImportModule("numpy");

    if (!numpyModule) {
        std::cerr << "Failed to import NumPy!" << std::endl;
        Py_Finalize();
        return -1;
    }

    PyObject* mainModule = PyImport_AddModule("__main__");
    if ( !mainModule ) {
        std::cerr << "Could not get Python __main__ " << std::endl;
        return 1;
    }
    PyObject* globalDict = PyModule_GetDict(mainModule);
    if ( ! globalDict ) {
        std::cerr << "Could not get Python __main__  module attributes" << std::endl;
        return 1;
    }

    std::cout << "dd = DynamicDist()" << std::endl;
    // import the file (module) for the class to load
    PyObject* dynamicDistModule = PyImport_ImportModule("DynamicDist");
    if (!dynamicDistModule) {
        PyErr_Print();
        std::cerr << "Failed to import module 'DynamicDist'" << std::endl;
        return 1;
    }

    PyObject* dynamicDistDict = PyModule_GetDict(dynamicDistModule);
    if ( ! dynamicDistDict ) {
        PyErr_Print();
        std::cerr << "Loaded module but cannot load dictionary for 'DynamicDist'" << std::endl;
        return 1;
    }

    // load the DynamicDist class within the module
    PyObject* dynamicDistClass = PyDict_GetItemString(dynamicDistDict, "DynamicDist");
    if ( ! dynamicDistClass ) {
        PyErr_Print();
        std::cerr << "Loaded module and dictionary but failed to load class 'DynamicDist'" << std::endl;
        return 1;
    }

    // Create an instance of the DynamicDist object given the class  
    PyObject* dynamicDistInstance = PyObject_CallObject(dynamicDistClass, nullptr);
    if ( ! dynamicDistInstance ) {
        PyErr_Print();
        std::cerr << "Could not create an instance of the loaded class 'DynamicDist'" << std::endl;
        return 1;
    }

    // Get the DynamicDist.add() function handle
    PyObject* dynamicDist_addFunction = PyObject_GetAttrString(dynamicDistInstance, "add");
    if (!dynamicDist_addFunction || !PyCallable_Check(dynamicDist_addFunction)) {
        PyErr_Print();
        std::cerr << "Failed to find function 'add' within 'DynamicDist'" << std::endl;
        return 1;
    }

    // Get the DynamicDist.add_many() function handle
    PyObject* dynamicDist_add_manyFunction = PyObject_GetAttrString(dynamicDistInstance, "add_many");
    if (!dynamicDist_add_manyFunction || !PyCallable_Check(dynamicDist_add_manyFunction)) {
        PyErr_Print();
        std::cerr << "Failed to find function 'add_many' within 'DynamicDist'" << std::endl;
        return 1;
    }

    // Create a PyTuple with one double element
    double myDouble = 3.14;
    PyObject* tuple = PyTuple_Pack(1, PyFloat_FromDouble(myDouble));

    std::cout << "dd.add(3.14)" << std::endl;
    // finally,  call the add() function
    PyObject_CallObject(dynamicDist_addFunction, tuple);


    // Create a Python list to represent the array of doubles
    int n = 1000;
    PyObject* pythonList = PyList_New(n); // 
    for(int i=0; i<n; i++) {
        PyList_SetItem(pythonList, i, PyFloat_FromDouble(i * 1.1));
    }
    std::cout << "dd.add_many([ ";
    for(int i=0;i<5;i++) {
        PyObject *po = PyList_GetItem(pythonList, i);
        std::cout << PyFloat_AsDouble(po) << " ";
    }
    std::cout << "... ";
    for(int i=n-5;i<n;i++) {
        PyObject *po = PyList_GetItem(pythonList, i);
        std::cout << PyFloat_AsDouble(po) << " ";
    }
    std::cout << "])" << std::endl;
    // Call the Python function with the Python list as an argument
    PyObject_CallFunctionObjArgs(dynamicDist_add_manyFunction, pythonList, nullptr);
    Py_DECREF(pythonList);

    // time 1 million calls of 5k elements
    n = 5000; 
    int nCalls = 1000000;
    std::cout << "listSize=" << n << ", nCalls=" << nCalls << ":dd.add_many()" << std::endl;
    pythonList = PyList_New(n); // 
    for(int i=0; i<n; i++) {
        PyList_SetItem(pythonList, i, PyFloat_FromDouble(i * 1.1));
    }
    std::cout << "dd.add_many([ ";
    for(int i=0;i<5;i++) {
        PyObject *po = PyList_GetItem(pythonList, i);
        std::cout << PyFloat_AsDouble(po) << " ";
    }
    std::cout << "... ";
    for(int i=n-5;i<n;i++) {
        PyObject *po = PyList_GetItem(pythonList, i);
        std::cout << PyFloat_AsDouble(po) << " ";
    }
    std::cout << "])" << std::endl;

    // Call the Python function 1 million times with the 5k Python list as an argument
    for(int i=0;i<nCalls;i++)
        PyObject_CallFunctionObjArgs(dynamicDist_add_manyFunction, pythonList, nullptr);

    // Get the DynamicDist.histogram() function handle
    PyObject* dynamicDist_histogramFunction = PyObject_GetAttrString(dynamicDistInstance, "histogram");
    if (!dynamicDist_histogramFunction || !PyCallable_Check(dynamicDist_histogramFunction)) {
        PyErr_Print();
        std::cerr << "Failed to find function 'histogram' within 'DynamicDist'" << std::endl;
        return 1;
    }

    std::cout << "h,b = dd.histogram(n_bins=10)" << std::endl;
    // now get the histogram

    // Call the function with no keyword arguments
    // PyObject* result = PyObject_CallObject(dynamicDist_histogramFunction, nullptr);
    // Call the function with no keyword arguments
    PyObject* kwargs = PyDict_New();
    PyDict_SetItemString(kwargs, "n_bins", PyLong_FromLong(10)); // Named argument: n_bins=10
    PyObject* result = PyObject_Call(dynamicDist_histogramFunction, PyTuple_New(0), kwargs);
    if (result && PyTuple_Check(result)) {
            // Extract the two arrays from the returned tuple
            PyObject* array1 = PyTuple_GetItem(result, 0);
            PyObject* array2 = PyTuple_GetItem(result, 1);

            // Print the arrays
            std::cout << "h=[ ";
            PyObject* iter1 = PyObject_GetIter(array1);
            PyObject* item1;
            while ((item1 = PyIter_Next(iter1)) != nullptr) {
                std::cout << PyLong_AsLong(item1) << " ";
                Py_DECREF(item1);
            }
            Py_DECREF(iter1);
            std::cout << "]" << std::endl;

            std::cout << "b=[ ";
            PyObject* iter2 = PyObject_GetIter(array2);
            PyObject* item2;
            while ((item2 = PyIter_Next(iter2)) != nullptr) {
                std::cout << PyFloat_AsDouble(item2) << " ";
                Py_DECREF(item2);
            }
            Py_DECREF(iter2);
            std::cout << "]" << std::endl;

            Py_DECREF(array1);
            Py_DECREF(array2);
            Py_DECREF(result);
            Py_DECREF(kwargs);
    } else {
        std::cerr << "Failed to call 'histogram' method and retrieve results." << std::endl;
        PyErr_Print();
        return 1;
    }


    // Finalize the Python interpreter
    Py_Finalize();

    return 0;
}



