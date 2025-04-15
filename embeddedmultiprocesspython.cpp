#include <Python.h>
#include <iostream>
#include <vector>
#include <thread>
#include <chrono>
#include <fstream>

int main()
{

    std::string pycode = R"KLINGON(
import sys
sys.path.append('.')
)KLINGON";

    // std::cout << pycode << std::endl;

    std::cout << "Initializing Python" << std::endl;
    Py_Initialize();
    if (!Py_IsInitialized())
    {
        std::cerr << "Failed to initialize Python interpreter" << std::endl;
        return 1;
    }

    std::cout << "Running initialization to set path" << std::endl; // << pycode.c_str() << std::endl;
    if(PyRun_SimpleString(pycode.c_str()) != 0) {
        std::cerr << "Non zero return code from Py_RunSimpleString, aborting" << std::endl;
        return 1;
    }

    std::string fname = "multiprocesspython.py";
    std::cout << "Opening file " << fname << std::endl;
    FILE *fp = fopen(fname.c_str(), "r");
    if( ! fp )
    {
        std::cerr << "Error opening " << fname << std::endl;
        return 1;
    }

    std::cout << "Launching as embedded Python" << std::endl;
    PyRun_SimpleFile(fp, fname.c_str());
    fclose(fp);

    std::cout << "Cleaning up resources" << std::endl;
    Py_Finalize();
}