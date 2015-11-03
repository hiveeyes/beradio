/* -*- coding: utf-8 -*-
 * (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
 * (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
 */
#include <Arduino.h>
#include <pnew.cpp>
#include <beradio.h>
#include <simulavr.h>

void BERadioMessage::debug(bool enabled) {
    DEBUG = enabled;
    _l("Node id: "); _d(nodeid);
    _l("Profile: "); _d(profile);
}

void BERadioMessage::temperature(std::vector<double> values) {

    // finally store list of parsed items
    d_temperatures = values;

    // debugging
    if (DEBUG) {
        dump("temp", d_temperatures);
    }

}



void dump(std::string prefix, std::vector<double> vec) {

    std::vector<double>::const_iterator it;
    int i = 1;
    for (it = vec.begin(); it != vec.end(); it++) {

        char buffer[10];
        sprintf(buffer, "%s%d: ", prefix.c_str(), i);
        _l(buffer);

        double value = *it;
        _d(value);

        i++;
    }

}
