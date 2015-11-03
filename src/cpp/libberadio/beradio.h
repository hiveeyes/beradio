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

// give convenient names to the variadic argument executor macro
#define measure ExecVF

// give a convenient name to the variadic argument executor macro
#define collect varargs

class BERadioMessage {

    public:

        // constructor
        BERadioMessage(int nodeid, std::string profile="h1") {
            this->nodeid = nodeid;
            this->profile = profile;
        };

        // enable/disable debugging
        void debug(bool enabled);

        // measure multiple temperatures
        void temperature(std::vector<double> values);

    private:
        bool DEBUG = false;
        int nodeid;
        std::string profile;

        // internal data store
        std::vector<double> d_temperatures;

};

void dump(std::string prefix, std::vector<double> vec);
