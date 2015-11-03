/* -*- coding: utf-8 -*-
 * (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
 * (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
 */
#include <iterator>
#include <vector>
#include <string>
#include <execvf.h>

// give a convenient name to the variadic argument executor macro
#define measure ExecVF

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
        void temperature(int count, ...);

    private:
        bool DEBUG = false;
        int nodeid;
        std::string profile;

        // internal data store
        std::vector<double> d_temperatures;

};
