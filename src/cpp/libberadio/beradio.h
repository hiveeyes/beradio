/* -*- coding: utf-8 -*-
 * (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
 * (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
 */
#include <execvf.h>
#include <varargs.h>
#include <iterator>
#include <vector>
#include <string>
#include <simulavr.h>

// give convenient name to the variadic argument executor macro,
// which drives the varargs template to convert a variable list
// of arguments into a vector containing all items
#define collect(...) varargs(VA_LENGTH(__VA_ARGS__), __VA_ARGS__)

// shortcuts for standard vectors containing items of various types
#define FloatList std::vector<double>
#define IntegerList std::vector<int>

// generic dump vector utility
template<typename T>
void dump_vector(std::string prefix, std::vector<T> vec);

class BERadioMessage {

    public:

        // constructor
        BERadioMessage(int nodeid, std::string profile="h1") {
            this->nodeid  = nodeid;
            this->profile = profile;
        };

        // enable/disable debugging
        void debug(bool enabled);

        // measure multiple temperatures
        void temperature(FloatList values);
        void something(IntegerList values);

        std::string encode();

    private:
        bool DEBUG = false;
        int nodeid;
        std::string profile;

        // internal data store
        FloatList d_temperatures;
        IntegerList d_something;

};
