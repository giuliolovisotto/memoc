/**
 * @file lpbase.cpp
 * @brief basic use of newcols and addrow
 * to solve the model
 *  max 2 x1 + 3 x2 + w
 *    x1 + x2 <= 5 z									
 *    x2 + 9 y1 + 9 y2 + 8w = 2
 *    8 y1 >= -1									
 *    -4 y1 + 7z + 5w <= 9				
 *    x1,x2 >=0
 *    y1 <=0
 *    z in {0,1}
 *    w in Z+					
 */

#include <cstdio>
#include <iostream>
#include <vector>
#include <string>
#include "cpxmacro.h"
#include <sstream>
#include <fstream>
#include <math.h>



using namespace std;

void saveSolution(const double& time, const double& objVal, const std::vector<int>& path){
  std::ofstream results;
  results.open ("results.csv");
  results << time << "," << objVal << std::endl;
  results.close();
}


std::vector<double>* readObjFunArray(std::string filename)
{
    std::ifstream  data(filename.c_str());

    std::string line;
    std::vector<double>* coeffs = new std::vector<double>();
    while(std::getline(data,line))
    {
        std::stringstream  lineStream(line);
        std::string        cell;
        while(std::getline(lineStream,cell,','))
        {
            // You have a cell!!!!
            coeffs->push_back(atof(cell.c_str()));
        }
    }
    return coeffs;
 }

// error status and messagge buffer
int status;
char errmsg[BUF_SIZE];

int findIndex(char type, int i, int j, int nodes){
	if (type == 'y') {
	    return (nodes*i)+j;
	}
	else{
	    return (nodes*nodes)+(nodes*i)+j;
	}
	
}

int main (int argc, char const *argv[])
{
	if (argc < 2){
		std::cout << "Usage:\n./cplex <filename>" << std::endl;
		return 0;
	}
	const std::string filename = argv[1];
    try
    {
        ///////////////////////// init
        DECL_ENV( env );
        DECL_PROB( env, lp );

        std::vector<double>* objCost = readObjFunArray(filename.c_str());
        
        // number of variables
        const int ccnt=objCost->size()*2;
        // number of nodes
        const int N = int(sqrt(objCost->size()));
        
        //char xtype[ccnt];
        std::vector<char> xtype;
        //double lb[ccnt];
        std::vector<double> lb;
        //double ub[ccnt];
        std::vector<double> ub ;
        for (int i=0; i<ccnt;i++){
            lb.push_back(0.0);
            if (i < ccnt/2){
                xtype.push_back('B');  // queste sono le y_ij 
                ub.push_back(1.0);
            }
            else{
                xtype.push_back('I');  // queste sono le x_ij 
                ub.push_back(CPX_INFBOUND);
                objCost->push_back(0.0);  // aggiungiamo zeri sui coefficienti della f obiettivo per gli x_ij
            }
        }
        
        char ** xname = NULL;
             
        CHECKED_CPX_CALL(CPXnewcols, env, lp, ccnt, &(*objCost)[0], &lb[0], &ub[0], &xtype[0], xname);
        
        
        char ** newcolnames = NULL;
        char ** rownames = NULL;
        std::vector<int> rmatind(0);
        std::vector<double> rmatval(0);
        // facciamo un ciclo per ogni tipo di vincolo del problema
        // 1. Vincolo per nodo iniziale
        int nzcnt = N;
        double rhs = N;
        char sense = 'E';
        int rmatbeg = 0;
        rmatind.clear();
        rmatval.clear();
        for (int j=0; j<N; j++){
            rmatind.push_back(findIndex('x', 0, j, N));
            rmatval.push_back(1.0);
        }
        CHECKED_CPX_CALL( CPXaddrows, env, lp, 0, 1, nzcnt, &rhs, &sense, &rmatbeg, &rmatind[0], &rmatval[0], newcolnames , rownames );
        
        // 2. Vincolo sottraz sommatorie
        // ci sono N archi entranti in k dove andra' 1
        // ci sono N archi uscenti da k dove andra' -1
        for (int k=1; k<N; k++){
			nzcnt = N*2;
			rhs = 1;
			sense = 'E';
			rmatbeg = 0;
			rmatind.clear();
			rmatval.clear();
			
			for (int i=0; i<N; i++){
			    rmatind.push_back(findIndex('x', i, k, N));
			    rmatval.push_back(1.0);
			    rmatind.push_back(findIndex('x', k, i, N));
			    rmatval.push_back(-1.0);
			}
			CHECKED_CPX_CALL( CPXaddrows, env, lp, 0, 1, nzcnt, &rhs, &sense, &rmatbeg, &rmatind[0], &rmatval[0], newcolnames , rownames );
		}

        // 3. Vincolo su y_ij
        for (int i=0; i<N; i++){
			nzcnt = N;
			rhs = 1;
			sense = 'E';
			rmatbeg = 0;
			rmatind.clear();
			rmatval.clear();
			for (int j=0; j<N; j++){
				rmatind.push_back(findIndex('y', i, j, N));
				rmatval.push_back(1.0);
			}
			CHECKED_CPX_CALL( CPXaddrows, env, lp, 0, 1, nzcnt, &rhs, &sense, &rmatbeg, &rmatind[0], &rmatval[0], newcolnames , rownames );
		}
		// 4. Vincolo su y_ji
        for (int j=0; j<N; j++){
			nzcnt = N;
			rhs = 1;
			sense = 'E';
			rmatbeg = 0;
			rmatind.clear();
			rmatval.clear();
			for (int i=0; i<N; i++){
				rmatind.push_back(findIndex('y', i, j, N));
				rmatval.push_back(1.0);
			}
			CHECKED_CPX_CALL( CPXaddrows, env, lp, 0, 1, nzcnt, &rhs, &sense, &rmatbeg, &rmatind[0], &rmatval[0], newcolnames , rownames );
		}

		// 5. Vincolo su minore uguale
		for (int i=0; i<N; i++){
			for (int j=0; j<N; j++){
				nzcnt = 2;
				rhs = 0;
				sense = 'L';
				rmatbeg = 0;
				rmatind.clear();
				rmatval.clear();
				rmatind.push_back(findIndex('y', i, j, N));
				rmatval.push_back(-N);
				rmatind.push_back(findIndex('x', i, j, N));
				rmatval.push_back(1.0);
				CHECKED_CPX_CALL( CPXaddrows, env, lp, 0, 1, nzcnt, &rhs, &sense, &rmatbeg, &rmatind[0], &rmatval[0], newcolnames , rownames );
			}		
		}
		
		std::vector<int> selfloops(ccnt);
		for (int i=0; i<N; i++){
			selfloops[i*N+i] = 1;
			selfloops[N*N + i*N+i] = 1;
		}
		CHECKED_CPX_CALL( CPXdelsetcols, env, lp, &selfloops[0]);
		
		double start, end;
		CHECKED_CPX_CALL(CPXgettime, env, &start);
		CHECKED_CPX_CALL(CPXmipopt, env, lp);
		CHECKED_CPX_CALL(CPXgettime, env, &end);
		double time = end -start;
        ///////////////////////// print (debug)
        //CHECKED_CPX_CALL( CPXwriteprob, env, lp, "primo.lp", NULL );
        
        ///////////////////////// print
        //Valore della funzione obbiettivo per la soluzione ottima
        double objval;
        
        // get the objective function value into objval
        CHECKED_CPX_CALL( CPXgetobjval, env, lp, &objval );
        
        //std::cout << "Objval: " << objval << std::endl;
        // get the number of variables (columns) into n (simple routine, no need for return status);
        int n = CPXgetnumcols(env, lp);
        
        /////// get the value of the variables using
        //
        //    status = CPXgetx (env, lp, varVals, fromIdx, toIdx);
        //
        
        // we prepare a vector to get n values from index 0 to index n-1
        std::vector<double> varVals;
        varVals.resize(n);
        //int fromIdx = 0;
        //int toIdx = n - 1;
        
        // Questa funzione legge il valore delle variabili nell' intervallo specificato.
        // get the value of the variables from index fromIdx to index toIdx into an array having (toIdx - fromIdx + 1) available positions
        //CHECKED_CPX_CALL(CPXgetx, env, lp, &varVals[0], fromIdx, toIdx);
        
        saveSolution(time, objval, std::vector<int>(0));
        
        //for ( int i = 0 ; i < n ; ++i ) {
            /// to get variable name, use the RATHER TRICKY "CPXgetcolname"
            /// status = CPXgetcolname (env, lp, cur_colname, cur_colnamestore, cur_storespace, &surplus, 0, cur_numcols-1);
            //std::cout << "var in position " << i << " : " << varVals[i] << std::endl;
        //}
        
        // write the solution to a text file
        //CHECKED_CPX_CALL( CPXsolwrite, env, lp, "primo.sol" );
        

        // free
        CPXfreeprob(env, &lp);
        CPXcloseCPLEX(&env);
    }
    catch(std::exception& e)
    {
        std::cout << ">>>EXCEPTION: " << e.what() << std::endl;
    }
    return 0;
}
