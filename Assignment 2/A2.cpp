#include <set>
#include <vector>
#include <random>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <algorithm>
#include <unordered_map>

using namespace std;

#define NUM_ROUND 10

const vector<int> Sbox = {
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16};


/* <------ Part 1: Implementation of the Toy Cipher (TC) ------> */

// Add Roundkey (AR)
vector<int> AR(const vector<int> &in_state, const vector<int> &rkey)
{
    vector<int> out_state(in_state.size());

    for(int i = 0; i < in_state.size(); ++i) out_state[i] = in_state[i] ^ rkey[i];
    
    return out_state;
}

// S-Box Layer (SB)
vector<int> SB(const vector<int> &in_state)
{
    vector<int> out_state(in_state.size());

    for(int i = 0; i < in_state.size(); ++i) out_state[i] = Sbox[in_state[i]];
    
    return out_state;
}

// Linear Mixing (LM)
vector<int> LM(const vector<int> &in_state)
{
    vector<int> out_state(in_state.size());
    int all_xor = in_state[0] ^ in_state[1] ^ in_state[2] ^ in_state[3];

    for(int i = 0; i < in_state.size(); ++i) out_state[i] = all_xor ^ in_state[i];
    
    return out_state;
}

// Single Encryption Round
vector<int> Enc_Round(const vector<int> &in_state, const vector<int> &rkey)
{
    auto state = AR(in_state, rkey); // Add Roundkey
    state = SB(state);               // Apply S-box layer
    state = LM(state);               // Apply Linear Mixing

    return state;
}

// TC1 Encryption
vector<int> TC1_Enc(vector<int> PT, const vector<int> &key)
{
    for(int i = 0; i < NUM_ROUND; ++i) PT = Enc_Round(PT, key);
    
    return PT;
}


/* <------ Part 2: Exhaustive Search for the Key ------> */

// Exhaustive Search
vector<int> exhaustiveSearch(const vector<int> &plaintext, const vector<int> &ciphertext)
{
    /* Brute force Search for the Key */

    for(int i = 0; i < 256; ++i)
    {
        for(int j = 0; j < 256; ++j)
        {
            for(int k = 0; k < 256; ++k)
            {
                auto key = {0x00, i, j, k};

                if(TC1_Enc(plaintext, key) == ciphertext) return key;
            }
        }
    }
    
    return {-1}; // Key not found
}


/* <------ Part 3: TMTO Attack for Key Recovery ------> */

// Helper function to convert a vector<int> to a string
string vectorToString(const vector<int> &vec)
{
    string result;

    for(auto it : vec) result += to_string(it) + ",";
    
    return result;
}

// Helper function to convert a string back to a vector<int>
vector<int> stringToVector(const string &str)
{
    vector<int> result;
    int pos = 0, prev = 0;

    while((pos = str.find(',', prev)) != string::npos)
    {
        result.emplace_back(stoi(str.substr(prev, pos - prev)));
        prev = pos + 1;
    }

    return result;
}

// Generate Random Key
vector<int> randomKeyGenerator(set<vector<int>> &keys)
{
    /* Generate a random key that is not already present in the set. */

    random_device rd;  // Obtain a random number from hardware
    mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
    uniform_int_distribution<> dis(0, 255);

    while(true)
    {
        vector<int> key = {dis(gen), dis(gen), dis(gen), dis(gen)};

        // Check if the key is already present in the set
        if(keys.find(key) == keys.end())
        {
            keys.insert(key);

            return key;
        }
    }
}

// Offline Phase
unordered_map<string, vector<int>> generateTable(const vector<int> &p, int m, int t)
{
    /* Generate the precomputation table for the TMTO attack. */

    set<vector<int>> keys; // Set to store the unique keys
    unordered_map<string, vector<int>> table;

    ifstream f("table.txt");

    // Read the table from the file(table.txt) if it exists
    if(f.is_open())
    {
        string line;

        while(getline(f, line))
        {
            int pos = line.find(' ');
            string key = line.substr(0, pos);
            string value = line.substr(pos + 1);

            table[key] = stringToVector(value);
        }

        f.close();
        cout << "Table Read Successfully from File!\n";

        return table;
    }

    cout << "Generating Table with " << m << " chains of length " << t << "...\n\n";

    ofstream file("table.txt", ios::app);

    /* Generated the table by computing the chains.
        Stored the endpoint and starting point in the table.*/

    for(int i = 0; i < m; ++i)
    {
        vector<int> SP = randomKeyGenerator(keys);
        vector<int> K = SP;

        for(int j = 0; j < t - 1; ++j) K = TC1_Enc(p, K); // Compute the chain
        
        table[vectorToString(K)] = SP; // Storing the starting point and endpoint in the table

        // Writing the table to the file
        file << vectorToString(K) << " " << vectorToString(SP) << "\n";
    }

    file.close();
    cout << "Table Generated Successfully!\n";

    return table;
}

// Online Phase
vector<int> searchKey(const vector<int> &P, const vector<int> &C, unordered_map<string, vector<int>> &table, int t)
{
    /* Search for the Key in Precomputed Table */

    cout << "\n\nSearching for the Key...\n\n\n";

    vector<int> Y = TC1_Enc(P, C); // Compute the first value of Y

    for(int i = 0; i < t; ++i)
    {
        /* Check if Current Value of Y is in the Table */
        if(table.find(vectorToString(Y)) != table.end())
        {
            vector<int> K = table[vectorToString(Y)];
            vector<int> prev_key = K;
            
            /* Reconstructing the Chain using the Starting Point */
            for(int j = 0; j < t; ++j)
            {
                if(K == C) return prev_key; // If we find the ciphertext in the chain
                
                prev_key = K;
                K = TC1_Enc(P, K); // Update K by encrypting it
            }
        }

        Y = TC1_Enc(P, Y); // Update Y by encrypting it
    }

    return {-1}; // Key not found
}

void printVector(const vector<int> &vec)
{
    /* Function to print a vector<int> */
    
    for(auto it : vec) cout << it << " ";
}


int main()
{
    /*<------ Part 1: Implementation of the Toy Cipher (TC) ------>*/

    vector<int> PT  = {0x12, 0x34, 0x56, 0x78}; // Provided plaintext
    vector<int> key = {0x9A, 0xBC, 0xDE, 0xF0}; // Provided key

    cout << "\n" << string(20, '-') << "Part 1: Toy Cipher (TC) Encryption" << string(20, '-') << "\n\n";

    cout << "Plaintext:  ";
    printVector(PT);

    cout << "\nKey:        ";
    printVector(key);

    cout << "\nCiphertext: ";
    printVector(TC1_Enc(PT, key));
        
    cout << "\n";


    /*<------ Part 2: Exhaustive Search for the Key ------>*/

    cout << "\n\n\n" << string(20, '-') << "Part 2: Exhaustive Search for the Key" << string(20, '-') << "\n\n";

    // Test Case 1
    vector<int> plaintext = {0, 0, 0, 0}, ciphertext = {180, 31, 145, 240};
    key = exhaustiveSearch(plaintext, ciphertext);

    cout << "Test Case 1:\n\n";
    cout << "Plaintext:  ";
    printVector(plaintext);

    cout << "\nCiphertext: ";
    printVector(ciphertext);

    cout << "\nKey:        ";
    printVector(key);

    cout << "\n\n\n";

    // Test Case 2
    plaintext = {1, 2, 3, 4}, ciphertext = {228, 99, 105, 79};
    key = exhaustiveSearch(plaintext, ciphertext);

    cout << "Test Case 2:\n\n";
    cout << "Plaintext:  ";
    printVector(plaintext);

    cout << "\nCiphertext: ";
    printVector(ciphertext);

    cout << "\nKey:        ";
    printVector(key);

    cout << "\n";


    /*<------ Part 3: TMTO Attack for Key Recovery ------>*/

    int t = pow(2, 16); // Chain length
    int m = pow(2, 16); // Number of chains
    plaintext = {18, 52, 86, 120}, ciphertext = {86, 116, 35, 75};

    cout << "\n\n\n" << string(20, '-') << "Part 3: TMTO Attack for Key Recovery" << string(20, '-') << "\n\n";
    
    auto table = generateTable(plaintext, m, t);
    key = searchKey(plaintext, ciphertext, table, t);

    cout << "Plaintext:  ";
    printVector(plaintext);

    cout << "\nCiphertext: ";
    printVector(ciphertext);

    cout << "\nKey:        ";
    printVector(key);

    cout << "\n\n";

    if(key[0] == -1) cout << "Key not found!\n\n";

    return 0;
}