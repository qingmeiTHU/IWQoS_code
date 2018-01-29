/* Copyright 2018, rqm, Inc. */
#include "stdafx.h"
#include "gurobi_c++.h"
using namespace std;

int T = 900;

int oracle() {
	try {
		GRBEnv env = GRBEnv();
		GRBModel model = GRBModel(env);
		GRBVar * send = model.addVars(T*T, GRB_BINARY);
		GRBVar * drop = model.addVars(T*T, GRB_BINARY);
		GRBVar * buffer = model.addVars(T*T, GRB_BINARY);

		// constraints

		//object

		//optimize
	}
	catch (GRBException e) {
		cout << "Error code = " << e.getErrorCode() << endl;
		cout << e.getMessage() << endl;
	}
	catch (...) {
		cout << "Exception during optimization" << endl;
	}
	cout << "wrnmmp" << endl;
	return 0;
}