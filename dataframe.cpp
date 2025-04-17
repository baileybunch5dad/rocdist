#include "usinggrpc.pb.h"
#include "usinggrpc.grpc.pb.h"

DataFrame dataframe;

ColumnData column1;
column1.add_double_array(1.1);
column1.add_double_array(2.2);
column1.add_string_array("hello");
column1.add_string_array("world");
(*dataframe.mutable_columns())["Column1"] = column1;

ColumnData column2;
column2.add_double_array(3.3);
column2.add_double_array(4.4);
column2.add_string_array("foo");
column2.add_string_array("bar");
(*dataframe.mutable_columns())["Column2"] = column2;

// Send dataframe using gRPC client logic