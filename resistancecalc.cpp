#include <stdio.h>

extern "C" {
#include <Python.h>
}

static PyObject * resistancecalc_Floyd_Warshall(PyObject *module, PyObject *args)
{
	// get arg
	PyObject * M = PyTuple_GetItem(args, 0);
	int size = PyObject_Size(M);

	// Python -> C
	double ** arr = (double**)malloc(size * sizeof(double*));
	for (int i = 0; i < size; ++i)
	{
		arr[i] = (double*)malloc(size * sizeof(double));
		PyObject * row = PyList_GetItem(M, i);
		for (int j = 0; j < size; ++j)
		{
			PyObject * element = PyList_GetItem(row, j);
			arr[i][j] = PyFloat_AsDouble(element);
		}
	}

	// Floyd-Warshall
	for (int k = 0; k < size; ++k)
	{
		for (int i = 0; i < size; ++i)
		{
			for (int j = 0; j < size; ++j)
			{
				arr[i][j] = 1.0 / ( 1.0 / arr[i][j] + 1.0 / (arr[i][k] + arr[k][j]) );
			}
		}
	}

	// C -> Python
	for (int i = 0; i < size; ++i)
	{
		PyObject * row = PyList_GetItem(M, i);
		for (int j = 0; j < size; ++j)
		{
			PyObject * value = PyFloat_FromDouble(arr[i][j]);
			PyList_SetItem(row, j, value);
		}
	}

	// free memory
	for (int i = 0; i < size; ++i)
	{
		free(arr[i]);
	}
	free(arr);

	Py_INCREF(Py_None);
	return Py_None;
}

PyMODINIT_FUNC PyInit_resistancecalc()
{
	static PyMethodDef ModuleMethods[] = {
		{ "Floyd_Warshall", resistancecalc_Floyd_Warshall, METH_VARARGS,
				"Floyd_Warshall(M):\n\n"

				"Calculates the shortest distances between every two pair "
				"of vertices in a graph, provided that M is a square matrix "
				"of distances between adjacent vertices.\n\n"

				"Return value:\n"
				"   None.\n\n"

				"Arguments:\n"
				"   M: a square matrix containing initial data and storing "
				"the result after execution."
		},
		{ NULL, NULL, 0, NULL }
	};
	static PyModuleDef ModuleDef = {
		PyModuleDef_HEAD_INIT,
		"resistancecalc",
		"Resistance calculation. Hometask #2 module",
		-1, ModuleMethods, 
		NULL, NULL, NULL, NULL
	};
	PyObject * module = PyModule_Create(&ModuleDef);
	return module;
}
