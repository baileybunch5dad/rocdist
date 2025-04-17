// cpp_python_dataframe_bridge.cpp
// This program creates a DataFrame in C++ and streams it to embedded Python

#include <Python.h>
#include <iostream>
#include <vector>
#include <string>

// Define a simple DataFrame-like structure in C++
class DataFrame {
private:
    std::vector<std::string> columnNames;
    std::vector<std::vector<double>> columns;
    size_t rows;

public:
    DataFrame(const std::vector<std::string>& colNames) : columnNames(colNames), rows(0) {
        columns.resize(columnNames.size());
    }

    void addRow(const std::vector<double>& rowData) {
        if (rowData.size() != columnNames.size()) {
            throw std::runtime_error("Row data size doesn't match column count");
        }
        
        for (size_t i = 0; i < rowData.size(); ++i) {
            columns[i].push_back(rowData[i]);
        }
        rows++;
    }

    size_t numRows() const { return rows; }
    size_t numCols() const { return columnNames.size(); }
    
    const std::vector<std::string>& getColumnNames() const { return columnNames; }
    const std::vector<std::vector<double>>& getData() const { return columns; }
};

// Function to convert C++ DataFrame to Python DataFrame
PyObject* dataFrameToPython(const DataFrame& df) {
    // Initialize the Python interpreter if not already done
    if (!Py_IsInitialized()) {
        Py_Initialize();
        // Add the current directory to Python's path
        PyRun_SimpleString("import sys; sys.path.append('.')");
    }
    
    // Import necessary Python modules
    PyObject* pModuleNumpy = PyImport_ImportModule("numpy");
    if (!pModuleNumpy) {
        PyErr_Print();
        throw std::runtime_error("Failed to import numpy");
    }
    
    PyObject* pModulePandas = PyImport_ImportModule("pandas");
    if (!pModulePandas) {
        Py_DECREF(pModuleNumpy);
        PyErr_Print();
        throw std::runtime_error("Failed to import pandas");
    }
    
    // Get pandas.DataFrame constructor
    PyObject* pPandasDict = PyModule_GetDict(pModulePandas);
    PyObject* pDataFrameClass = PyDict_GetItemString(pPandasDict, "DataFrame");
    
    // Create a dictionary to hold the DataFrame data
    PyObject* pDict = PyDict_New();
    
    // Fill the dictionary with column arrays
    const auto& columnNames = df.getColumnNames();
    const auto& data = df.getData();
    
    for (size_t i = 0; i < columnNames.size(); ++i) {
        // Create a NumPy array for each column
        npy_intp dims[] = {static_cast<npy_intp>(df.numRows())};
        PyObject* pArray = PyArray_SimpleNew(1, dims, NPY_DOUBLE);
        double* arrayData = static_cast<double*>(PyArray_DATA(reinterpret_cast<PyArrayObject*>(pArray)));
        
        // Copy data from C++ vector to NumPy array
        for (size_t j = 0; j < df.numRows(); ++j) {
            arrayData[j] = data[i][j];
        }
        
        // Add the column to the dictionary
        PyDict_SetItemString(pDict, columnNames[i].c_str(), pArray);
        Py_DECREF(pArray);
    }
    
    // Create the pandas DataFrame
    PyObject* pArgs = PyTuple_New(0);
    PyObject* pDataFrame = PyObject_Call(pDataFrameClass, pArgs, pDict);
    
    // Clean up
    Py_DECREF(pArgs);
    Py_DECREF(pDict);
    Py_DECREF(pModuleNumpy);
    Py_DECREF(pModulePandas);
    
    if (!pDataFrame) {
        PyErr_Print();
        throw std::runtime_error("Failed to create pandas DataFrame");
    }
    
    return pDataFrame;
}

// Function to process DataFrame in Python
void processPandasDataFrame(PyObject* pDataFrame) {
    PyObject* pMainModule = PyImport_AddModule("__main__");
    PyObject* pMainDict = PyModule_GetDict(pMainModule);
    
    // Add the DataFrame to the main module
    PyDict_SetItemString(pMainDict, "df", pDataFrame);
    
    // Run Python code to process the DataFrame
    std::cout << "Processing DataFrame in Python..." << std::endl;
    PyRun_SimpleString(
        "print('Python received DataFrame:')\n"
        "print(df)\n"
        "print('\\nDataFrame info:')\n"
        "df.info()\n"
        "print('\\nDataFrame statistics:')\n"
        "print(df.describe())\n"
        "\n"
        "# Perform some operations\n"
        "df['calculated'] = df['value1'] * df['value2']\n"
        "print('\\nModified DataFrame:')\n"
        "print(df)\n"
        "\n"
        "# Save the results back\n"
        "result = df['calculated'].sum()\n"
        "print(f'\\nSum of calculated column: {result}')\n"
    );
}

int main() {
    try {
        // Create a C++ DataFrame
        std::vector<std::string> columns = {"value1", "value2", "value3"};
        DataFrame df(columns);
        
        // Add some data
        df.addRow({1.1, 2.2, 3.3});
        df.addRow({4.4, 5.5, 6.6});
        df.addRow({7.7, 8.8, 9.9});
        df.addRow({10.0, 11.1, 12.2});
        df.addRow({13.3, 14.4, 15.5});
        
        std::cout << "Created C++ DataFrame with " << df.numRows() 
                  << " rows and " << df.numCols() << " columns" << std::endl;
        
        // Convert to Python DataFrame
        PyObject* pDataFrame = dataFrameToPython(df);
        
        // Process the DataFrame in Python
        processPandasDataFrame(pDataFrame);
        
        // Clean up
        Py_DECREF(pDataFrame);
        
        // Finalize the Python interpreter
        if (Py_IsInitialized()) {
            Py_Finalize();
        }
        
        std::cout << "DataFrame processing completed successfully" << std::endl;
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        if (Py_IsInitialized()) {
            Py_Finalize();
        }
        return 1;
    }
    
    return 0;
}