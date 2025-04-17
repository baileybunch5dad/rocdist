#include <Python.h>
#include <vector>
#include <iostream>
#include <random>
#include <string>

// Function to convert a C++ vector of doubles to a Python pickle binary blob
PyObject* doubleArrayToPickleBlob(const std::vector<double>& doubleArray) {
    // Initialize the Python interpreter if not already initialized
    if (!Py_IsInitialized()) {
        Py_Initialize();
    }

    // Import necessary Python modules
    PyObject* pickleModule = PyImport_ImportModule("pickle");
    PyObject* numpyModule = PyImport_ImportModule("numpy");
    
    if (!pickleModule || !numpyModule) {
        std::cerr << "Failed to import Python modules" << std::endl;
        if (PyErr_Occurred()) PyErr_Print();
        return nullptr;
    }

    // Convert C++ vector to Python list
    PyObject* pyList = PyList_New(doubleArray.size());
    for (size_t i = 0; i < doubleArray.size(); i++) {
        PyObject* pyDouble = PyFloat_FromDouble(doubleArray[i]);
        PyList_SetItem(pyList, i, pyDouble); // PyList_SetItem steals the reference
    }

    // Convert list to numpy array
    PyObject* arrayFunc = PyObject_GetAttrString(numpyModule, "array");
    PyObject* args = PyTuple_Pack(1, pyList);
    PyObject* npArray = PyObject_CallObject(arrayFunc, args);
    Py_DECREF(args);
    Py_DECREF(arrayFunc);
    Py_DECREF(pyList);

    // Get pickle dumps function to convert to binary blob
    PyObject* dumpsFunc = PyObject_GetAttrString(pickleModule, "dumps");
    args = PyTuple_Pack(1, npArray);
    
    // Create the pickle binary blob
    PyObject* pickleBlob = PyObject_CallObject(dumpsFunc, args);
    
    // Clean up
    Py_DECREF(args);
    Py_DECREF(dumpsFunc);
    Py_DECREF(npArray);
    Py_DECREF(pickleModule);
    Py_DECREF(numpyModule);
    
    return pickleBlob; // Return the binary blob (caller must DECREF when done)
}


int main() {
    const int arraySize = 1000;
    std::cout << "Creating a vector of " << arraySize << " random doubles" << std::endl;
    std::vector<double> doubleArray(arraySize);
    
    // Fill the vector with random double values
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(-1000.0, 1000.0);
    
    for (int i = 0; i < arraySize; i++) {
        doubleArray[i] = dis(gen);
    }

    std::cout << "Initialize Python interpreter" << std::endl;
    Py_Initialize();
    
    std::cout << "Convert to pickle blob" << std::endl;
    PyObject* pickleBlob = doubleArrayToPickleBlob(doubleArray);
    
    if (pickleBlob) {
        std::cout << "Successfully created pickle blob" << std::endl;
    }
    std::cout << "Finalize the Python interpreter" << std::endl;
    Py_Finalize();
    
    return 0;

}

#if 0
// Function to process the pickle blob using embedded Python
void processPickleBlobInPython(PyObject* pickleBlob) {
    // Import necessary modules
    PyObject* pickleModule = PyImport_ImportModule("pickle");
    PyObject* numpyModule = PyImport_ImportModule("numpy");
    
    if (!pickleModule || !numpyModule) {
        std::cerr << "Failed to import Python modules for processing" << std::endl;
        if (PyErr_Occurred()) PyErr_Print();
        return;
    }

    // Get pickle.loads function
    PyObject* loadsFunc = PyObject_GetAttrString(pickleModule, "loads");
    PyObject* args = PyTuple_Pack(1, pickleBlob);
    
    // Load the array from the pickle blob
    PyObject* npArray = PyObject_CallObject(loadsFunc, args);
    Py_DECREF(args);
    Py_DECREF(loadsFunc);
    
    if (!npArray) {
        std::cerr << "Failed to unpickle data" << std::endl;
        if (PyErr_Occurred()) PyErr_Print();
    } else {
        // Get array shape and other information
        PyObject* shapeAttr = PyObject_GetAttrString(npArray, "shape");
        std::cout << "Successfully unpickled array with shape: ";
        PyObject_Print(shapeAttr, stdout, 0);
        std::cout << std::endl;
        Py_DECREF(shapeAttr);
        
        // Calculate and print mean
        PyObject* meanFunc = PyObject_GetAttrString(numpyModule, "mean");
        args = PyTuple_Pack(1, npArray);
        PyObject* meanResult = PyObject_CallObject(meanFunc, args);
        std::cout << "Array mean: ";
        PyObject_Print(meanResult, stdout, 0);
        std::cout << std::endl;
        Py_DECREF(args);
        Py_DECREF(meanFunc);
        Py_DECREF(meanResult);
        
        // Calculate and print standard deviation
        PyObject* stdFunc = PyObject_GetAttrString(numpyModule, "std");
        args = PyTuple_Pack(1, npArray);
        PyObject* stdResult = PyObject_CallObject(stdFunc, args);
        std::cout << "Array std dev: ";
        PyObject_Print(stdResult, stdout, 0);
        std::cout << std::endl;
        Py_DECREF(args);
        Py_DECREF(stdFunc);
        Py_DECREF(stdResult);
        
        // Example of accessing first few elements
        std::cout << "First few elements: ";
        for (int i = 0; i < std::min(5, (int)PyObject_Length(npArray)); i++) {
            PyObject* item = PySequence_GetItem(npArray, i);
            PyObject_Print(item, stdout, 0);
            std::cout << " ";
            Py_DECREF(item);
        }
        std::cout << std::endl;
        
        Py_DECREF(npArray);
    }
    
    Py_DECREF(pickleModule);
    Py_DECREF(numpyModule);
}

// Alternative function to pass the pickle blob to Python code via PyRun_String
void usePickleBlobWithPyCode(PyObject* pickleBlob) {
    // Create a Python dictionary to hold our variables
    PyObject* globals = PyDict_New();
    PyObject* locals = PyDict_New();
    
    // Add the pickle blob to the dictionary
    PyDict_SetItemString(globals, "pickle_blob", pickleBlob);
    
    // Import modules in the dictionary
    PyRun_String("import pickle\nimport numpy as np", Py_file_input, globals, locals);
    
    // Create and run Python code to process the blob
    const char* pythonCode = R"(
# Unpickle the data
data_array = pickle.loads(pickle_blob)

# Process the data
print(f"Loaded array with {len(data_array)} elements")
print(f"First 5 elements: {data_array[:5]}")
print(f"Array mean: {np.mean(data_array)}")
print(f"Array std: {np.std(data_array)}")

# You can do more processing here
# For example, transform the data
processed_data = data_array * 2 + 10
print(f"After transformation, first 5: {processed_data[:5]}")

# Now we can return processed data to C++ if needed
result = processed_data
    )";
    
    // Execute the Python code
    PyObject* result = PyRun_String(pythonCode, Py_file_input, globals, locals);
    
    if (!result) {
        std::cerr << "Error executing Python code" << std::endl;
        if (PyErr_Occurred()) PyErr_Print();
    } else {
        Py_DECREF(result);
        
        // Get the result back from Python (if we want to)
        PyObject* processed = PyDict_GetItemString(locals, "result");
        if (processed) {
            std::cout << "Successfully retrieved processed data from Python" << std::endl;
            // Here you could convert the processed data back to C++ if needed
        }
    }
    
    Py_DECREF(globals);
    Py_DECREF(locals);
}

int main() {
    // Initialize Python interpreter
    Py_Initialize();
    
    // Create a vector of doubles
    const int arraySize = 1000;
    std::vector<double> doubleArray(arraySize);
    
    // Fill the vector with random double values
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_real_distribution<> dis(-1000.0, 1000.0);
    
    for (int i = 0; i < arraySize; i++) {
        doubleArray[i] = dis(gen);
    }
    
    // Print a few values to verify
    std::cout << "Generated array of " << doubleArray.size() << " doubles" << std::endl;
    std::cout << "First 5 values: ";
    for (int i = 0; i < std::min(5, arraySize); i++) {
        std::cout << doubleArray[i] << " ";
    }
    std::cout << std::endl;
    
    // Convert to pickle blob
    PyObject* pickleBlob = doubleArrayToPickleBlob(doubleArray);
    
    if (pickleBlob) {
        std::cout << "Successfully created pickle blob" << std::endl;
        
        // Option 1: Process the blob using C++ wrapper functions
        processPickleBlobInPython(pickleBlob);
        
        std::cout << "\n--- Using Python code directly ---\n" << std::endl;
        
        // Option 2: Process the blob using Python code
        usePickleBlobWithPyCode(pickleBlob);
        
        // Clean up
        Py_DECREF(pickleBlob);
    } else {
        std::cerr << "Failed to create pickle blob" << std::endl;
    }
    
    // Finalize the Python interpreter
    Py_Finalize();
    
    return 0;
}

#endif