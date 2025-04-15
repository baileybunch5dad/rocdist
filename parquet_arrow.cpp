#include <arrow/io/file.h>
#include <arrow/ipc/api.h>
#include <arrow/table.h>
#include <parquet/arrow/reader.h>
#include <Python.h>
#include <iostream>

void callPythonWithArrowBuffer(const std::shared_ptr<arrow::Buffer>& buffer) {
    Py_Initialize();

    // Define a Python script to process the Arrow buffer
    const char* script =
        "import pyarrow as pa\n"
        "def process_arrow_buffer(buffer):\n"
        "    reader = pa.ipc.open_stream(buffer)\n"
        "    table = reader.read_all()\n"
        "    print('Received Table:', table)\n";

    PyRun_SimpleString(script);

    // Get Python module and global dictionary
    PyObject* mainModule = PyImport_AddModule("__main__");
    PyObject* globalDict = PyModule_GetDict(mainModule);

    // Get function reference
    PyObject* func = PyDict_GetItemString(globalDict, "process_arrow_buffer");

    if (func && PyCallable_Check(func)) {
        // Convert Arrow buffer to Python bytes
        PyObject* pyBuffer = PyBytes_FromStringAndSize(
            reinterpret_cast<const char*>(buffer->data()), buffer->size());

        // Call Python function with Arrow buffer
        PyObject* result = PyObject_CallFunctionObjArgs(func, pyBuffer, nullptr);

        if (!result) {
            PyErr_Print();
        }

        Py_DECREF(pyBuffer);
    } else {
        std::cerr << "Failed to retrieve Python function." << std::endl;
    }

    Py_Finalize();
}

int main() {
    std::string parquet_file = "example.parquet";

    // Open Parquet file
    std::shared_ptr<arrow::io::ReadableFile> infile;
    arrow::io::ReadableFile::Open(parquet_file, arrow::default_memory_pool(), &infile);

    // Read as Arrow Table
    std::unique_ptr<parquet::arrow::FileReader> reader;
    parquet::arrow::OpenFile(infile, arrow::default_memory_pool(), &reader);

    std::shared_ptr<arrow::Table> table;
    reader->ReadTable(&table);

    // Convert Table to Arrow IPC stream
    std::shared_ptr<arrow::Buffer> buffer;
    arrow::ipc::SerializeTable(*table, arrow::default_memory_pool(), &buffer);

    // Call Python function with Arrow buffer
    callPythonWithArrowBuffer(buffer);

    return 0;
}