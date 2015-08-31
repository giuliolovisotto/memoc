
#include <vector>
#include <stdlib.h>
#include <iostream>
#include <algorithm>
#include <cstdio>
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <math.h>
#include <ctime>


typedef std::pair<int, int> swap;

void saveSolution(const double& time, const double& objVal, const std::vector<int>& path){
  std::ofstream results;
  results.open ("results.csv");
  results << time << "," << objVal << std::endl;
  results.close();
}

void printarr1(const std::vector<int>& path){
	for (int i=0; i<path.size(); i++){
		std::cout<<path[i]<<", ";
	}
	std::cout << std::endl;
}
void printarr2(const std::vector<swap>& swaps){
	for (int i=0; i<swaps.size(); i++){
		std::cout<<"(" << swaps[i].first<<"," <<swaps[i].second<<"), ";
	}
	std::cout << std::endl;
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

double evalSolution(const std::vector<int>& cycle, std::vector<double>* matrix, int nodes){
	if (cycle.size() != nodes) {
		std::cout << "something went wrong" << std::endl;
	}
	double objfunval = 0;
	for (int i=0; i<cycle.size()-1; i++){
		objfunval += (*matrix)[nodes*cycle[i]+cycle[i+1]];
	}
	objfunval += (*matrix)[nodes*cycle[cycle.size()-1]+cycle[0]];
	return objfunval;
}

std::vector<int> applySwaps(const std::vector<int>& start, const std::vector<swap>& swaps){
	std::vector<int> end = start;
	int tmp = 0;
	for (int i=0; i<swaps.size(); i++){
		tmp = end[swaps[i].first];
		end[swaps[i].first] = end[swaps[i].second];
		end[swaps[i].second] = tmp;
	}
	return end;
}

std::vector<swap> diff(const std::vector<int>& pos1, const std::vector<int>& pos2){
	// this is explained in 2.4 The Construction of Basic Swap Sequence
	// we want to move from pos2 to pos1
	std::vector<swap> basicSS(0);
	std::vector<int> current (pos1.size());
	//std::cout << pos1.size() << std::endl;
	current = pos2;
	for (int i=0; i<current.size(); i++){
		if (current[i] != pos1[i]){ // if they are different we must swap
			// find the index of pos1[i] in current
			int indexInCurrent = distance(current.begin(), std::find(current.begin(), current.end(), pos1[i]));
			// add the swap to the sequence
			basicSS.push_back(swap(i, indexInCurrent));
			// actually swap it in current to go on
			int tmp = current[i];
			current[i] = current[indexInCurrent];
			current[indexInCurrent] = tmp;
		}
	}
	return basicSS;
	
}

std::vector<swap> toBasicSequence(const std::vector<swap>& swaps, int length){
	//create reference solution
	std::vector<int> ref(length);
	for(int i=0; i<ref.size(); i++){
		ref[i] = i;
	}
	std::vector<int> afterSwaps = applySwaps(ref, swaps);
	return diff(afterSwaps, ref);
}

std::vector<int> shiftToFirst(const std::vector<int>& sol){
	std::vector<int> shifted = sol;
	for (int i=0; i<shifted.size(); i++){
		if (shifted[0] != 0){
			int tmp = shifted[0];
			for (int j=0; j<shifted.size()-1; j++){
				shifted[j] = shifted[j+1];
			}
			shifted[shifted.size()-1] = tmp;
		}
	}
	return shifted;
}

int main (int argc, char const *argv[])
{
	if (argc < 2){
		std::cout << "Usage:\n./pso <filename> <pop_size>" << std::endl;
		return 0;
	}
	
	int pop_size = 2000;
	const std::string filename = argv[1];
	if (argc > 2) pop_size = int(atoi(argv[2]));
	int iterations = 1000;
	if (argc > 3) iterations = int(atoi(argv[3]));
	double alpha = 0.75;
	if (argc > 4) alpha = double(atof(argv[4]));
	double beta = 0.1;
	if (argc > 5) alpha = double(atof(argv[5]));
	
	srand((unsigned)time(NULL));
	std::vector<double>* objCost = readObjFunArray(filename.c_str());
	const int n_vars = (int)(sqrt(objCost->size()));
	
	std::clock_t start;
	start = std::clock();
	// create X
	std::vector<std::vector<int> > X(pop_size, std::vector<int>(n_vars));
	// these vector will store V
	std::vector<std::vector<swap> > V(pop_size, std::vector<swap>(0));
	// these vectors will store best individual positions
	std::vector<std::vector<int> > P(pop_size, std::vector<int>(n_vars));
	// this vector will store global best position
	std::vector<int> Pg(n_vars);
	// this  will store global best obj function value
	double fevalsPg = 0;
	// this vector will store current obj function values 
	std::vector<double> fevals(pop_size);
	// this vector will store individual best obj function values
	std::vector<double> fevalsP(pop_size);
	int n_swaps = 0;
	int first = 0;
	int second = 0;

	// generate random V == swap sequences
	// also generate random initial positions
	for (int i=0; i<pop_size; i++){
		for (int j=0; j<n_vars; j++){
			X[i][j] = j;  // fill X with nodes from 0 to n_vars-1
		}
		std::random_shuffle (X[i].begin(), X[i].end());  // shuffle
		P[i] = X[i];  // deep copy
		//for (int j=0; j<n_vars; j++){std::cout << X[i][j] << " ";}
		//std::cout << std::endl;
		n_swaps = rand() % (n_vars) + 1;
		for (int j=0; j<n_swaps; j++){
			first = rand() % n_vars;
			second = rand() % n_vars;
			V[i].push_back(swap (first, second));
			//std::cout << V[i][j].first << " " <<  V[i][j].second << std::endl;
		}
		//std::cout << V[i].size() << std::endl;
	}
	
	//evaluate global best
	for (int i=0; i<pop_size; i++){
		fevals[i] = evalSolution(X[i], objCost, n_vars);
		fevalsP[i] = evalSolution(X[i], objCost, n_vars);
		//std::cout << evals[i] << std::endl;
	}
	
	int globBestIndex = distance(fevals.begin(), min_element(fevals.begin(), fevals.end()));
	// std::cout << globBestIndex << std::endl;
	// save global best position and value
	Pg = X[globBestIndex];
	fevalsPg = fevals[globBestIndex];
	//start pso

	bool terminate = false;
	/*
	std::vector<int> pp1 = {1,2,3,4,5,6,7,8};
	std::vector<int> pp2 = {3,2,1,6,8,5,7,4};
	std::vector<swap> pp3 = diff(pp1, pp2);
	printarr1(pp1);
	printarr1(pp2);
	printarr2(pp3);*/
	
	for (int k=0; k<iterations && !terminate; k++){
	    for (int i=0; i<pop_size; i++){
			//3.1 calculate difference between P_i and X_i
			// A = P_i - X_i, where A is a basic sequence.
			std::vector<swap> A = diff(P[i], applySwaps(X[i], V[i]));
			std::vector<swap> B = diff(Pg, applySwaps(X[i], V[i]));
			
			// now lets compute A*alpha and B*beta
			for (int j=A.size()-1; j>=0; j--){
				double p1 = ((double)rand()/(double)RAND_MAX);
				if (p1>alpha){
					A.erase(A.begin() + j);
				}
			}
			for (int j=B.size()-1; j>=0; j--){
				double p2 = ((double)rand()/(double)RAND_MAX);
				if (p2>beta){
					B.erase(B.begin() + j);
				}
			}
			std::vector<swap> newV = V[i];
			// concatenate all the swaps in a single sequence
			newV.insert(newV.end(), A.begin(), A.end());
			newV.insert(newV.end(), B.begin(), B.end());
			// transform the swap sequence in Basic sequence form
			V[i] = toBasicSequence(newV, n_vars);
			// update position with formula X_i = X_i + V_i
			// X[i] = applySwaps(X[i], newV);
			
			// V[i].clear();
			
			// update fevals
			fevals[i] = evalSolution(applySwaps(X[i], V[i]), objCost, n_vars);
			// possibly update P
			if (fevals[i] < fevalsP[i]){
				fevalsP[i] = fevals[i];
				P[i] = applySwaps(X[i], V[i]);
			}
		}
		// possibly update Pg
		globBestIndex = distance(fevals.begin(), min_element(fevals.begin(), fevals.end()));
		Pg = applySwaps(X[globBestIndex], V[globBestIndex]);
		
		if (fevals[globBestIndex] < fevalsPg){
			fevalsPg = fevals[globBestIndex];
			Pg = applySwaps(X[globBestIndex], V[globBestIndex]);
		}
	}
	double elapsedtime = (std::clock() - start) / (double)(CLOCKS_PER_SEC);
	//std::cout << "Time: " << elapsedtime << std::endl;
	std::cout << "best: " << fevalsPg << std::endl;
	saveSolution(elapsedtime, fevalsPg, std::vector<int>(0));
	//printarr1(shiftToFirst(Pg));
}
