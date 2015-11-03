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

void BERadioMessage::temperature(int count, ...) {

    // buffer for collecting variadic arguments
    std::vector<double> values;

    // initialize reading of variadic arguments
    va_list arguments;
    va_start(arguments, count);

    // read "double" items from argument list
    for (int i = 0; i < count; i++) {

        // pop item from argument list
        double value = va_arg(arguments, double);

        // store into buffer
        values.push_back(value);

        // debugging
        if (DEBUG) {
            _l("temperature value: ");
            _d(value);
        }

    }

    // clean up from reading arguments
    va_end(arguments);

    // finally store list of parsed items
    d_temperatures = values;

}
