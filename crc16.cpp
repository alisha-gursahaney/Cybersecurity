#include <boost/crc.hpp>
using namespace std;
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <stdio.h>
#include <boost/crc.hpp>

uint16_t GetCrc16(const string& my_string) {
    boost::crc_16_type result;
    result.process_bytes(my_string.data(), my_string.length());
    return result.checksum();
	}
	// return type is crc_16_type


int main(int argc, char **argv) {
    string filename = argv[1];
    string crc = argv[2];

    string input_text;
    ifstream file;
    file.open(filename);
    // if (file.is_open()) {
    // 	string line;
    // 	while(getline(file,line)) {
    // 		input_text = line;
    // 	}
    // }
   if(file) {
      ostringstream ss;
      ss << file.rdbuf(); // reading data
      input_text = ss.str();
   }
   	// cout << input_text;


    int crc_check = stoi(crc, 0, 16);

 	string message = "Hello World!";

 	// 4 ASCII character salt 


 	for(int i = 32; i<128; i++) {
		for(int j = 32; j<128; j++) {
			for(int k = 32; k<128; k++) {
				for(int l = 32; l<128; l++) {
					// fix how to iterate through all characters
					string salt = "";
					// error no viable conversion
					salt.push_back(char(i));
					salt.push_back(char(j));
					salt.push_back(char(k));
					salt.push_back(char(l));
					// cast types
					// cout << salt << endl;
					// error invalid operands to binary expression unsigned int to string
					string total = input_text + message + salt;
					if (GetCrc16(total) == crc_check) {
						ofstream outfile("output.txt");
						// string total_text = text.str() + message + salt;
 						outfile << total;
 						// file.close();
 						break;
 						}
					}
				}
			}
		}	

  	return 0;
}