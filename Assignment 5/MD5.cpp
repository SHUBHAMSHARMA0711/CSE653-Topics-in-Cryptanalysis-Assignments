#include <bits/stdc++.h>
using namespace std;

class MD5 {
private:
    vector<char>  message; /* Message buffer */
    int A, B, C, D, K[64];
    
    /* Shift amounts for each round's rotation operations */
    int s[64] = {
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    };
    
    void init(string &msg) 
    {
        long long bitLen = msg.size() * 8;
        message.insert(message.end(), msg.begin(), msg.end());
        
        /* STEP 1.1: Append '1' bit */
        message.emplace_back(0x80);

        /* STEP 1.2: Pad with zeros until len mod 512 = 448 bits */
        while((message.size() * 8) % 512 != 448) message.emplace_back(0);
        
        /* STEP 2: Append original message length as 64-bit value (little-endian) */
        for(int i = 0; i < 8; ++i) message.emplace_back((bitLen >> (8 * i)) & 0xFF);
            
        /* Initialize constant table K using sine function,
            also doing static casting to unsigned int to avoid implicit conversion to int*/
        for(int i = 0; i < 64; ++i) K[i] = static_cast<unsigned int>(floor(abs(sin(i + 1)) * pow(2, 32)));
    }

public:
    /* Constructor to initializes state variables with MD5 standard values */
    MD5(string &msg) : A(0x67452301), B(0xefcdab89), C(0x98badcfe), D(0x10325476) // STEP 3
    {
        init(msg);
    }

    string generateHash() 
    {
        stringstream hash;
        
        /* STEP 4: Process message in 512-bit (64-byte) blocks */
        for(size_t mBlock = 0; mBlock < message.size(); mBlock += 64) 
        {
            /* Initialize working variables and 
                    temporary message chunk array */
            unsigned int M[16], a = A, b = B, c = C, d = D, F, g;
            
            /* Converting 64 bytes to 16 32-bit words (little-endian) 
                by getting 4 consecutive bytes and combining them using bitwise OR */
            for(int i = 0; i < 16; ++i)
                M[i] = (static_cast<unsigned char>(message[mBlock + i * 4 + 0]) <<  0)|
                       (static_cast<unsigned char>(message[mBlock + i * 4 + 1]) <<  8)|
                       (static_cast<unsigned char>(message[mBlock + i * 4 + 2]) << 16)|
                       (static_cast<unsigned char>(message[mBlock + i * 4 + 3]) << 24);

            for(int i = 0; i < 64; ++i) 
            {
                if(i < 16) F = (b & c) | (~b & d), g = i;                     // Round 1

                else if(i < 32) F = (d & b) | (~d & c), g = (5 * i + 1) % 16; // Round 2
                
                else if(i < 48) F = b ^ c ^ d, g = (3 * i + 5) % 16;          // Round 3
                
                else F = c ^ (b | ~d), g = (7 * i) % 16;                      // Round 4
            
                /* Core transformation function, and the bitwise AND with 0xFFFFFFFF 
                    ensures the result stays within 32 bits or perfroming modulo 2^32 */
                F = (F + a + K[i] + M[g]) & 0xFFFFFFFF;
                a = d, d = c, c = b;

                /* Performing left circular shift or bit rotation, 
                    F << s[i] is the left shift operation, 
                        while F >> (32 - s[i]) is the right shift operation, 
                        then bitwise ORing them together to combine the two */
                b = (b + ((F << s[i]) | (F >> (32 - s[i])))) & 0xFFFFFFFF;
            }
            
            /* Add result back to state variables (modulo 2^32) for next block */
            A = (A + a) & 0xFFFFFFFF, B = (B + b) & 0xFFFFFFFF, C = (C + c) & 0xFFFFFFFF, D = (D + d) & 0xFFFFFFFF;
        }

        /* STEP 5: Convert state to hex string (little-endian output) */
        for(auto it: {A, B, C, D}) 
        {
            hash << hex << setfill('0') << setw(2) << (it & 0xFF)
               << setw(2) << ((it >>  8) & 0xFF)
               << setw(2) << ((it >> 16) & 0xFF)
               << setw(2) << ((it >> 24) & 0xFF);
        }
        
        return hash.str();
    }
};


int main() 
{
    string msg;
    cout << "\nEnter the Message to hash using MD5: ";
    getline(cin, msg);

    cout << "\nMD5 Hash: " << MD5(msg).generateHash() << "\n" << endl;
    return 0;
}