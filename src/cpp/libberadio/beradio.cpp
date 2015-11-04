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

void BERadioMessage::temperature(FloatList values) {

    // finally store list of parsed items
    d_temperatures = values;

    // debugging
    if (DEBUG) {
        dump_vector("temp", d_temperatures);
    }

}

void BERadioMessage::something(IntegerList values) {

    // finally store list of parsed items
    d_something = values;

    // debugging
    if (DEBUG) {
        dump_vector("something", d_something);
    }

}


template<typename T>
void dump_vector(std::string item_prefix, std::vector<T> vec) {

    typename std::vector<T>::const_iterator it;
    int i = 1;
    for (it = vec.begin(); it != vec.end(); it++) {

        char buffer[100];
        sprintf(buffer, "%s%d: ", item_prefix.c_str(), i);
        _l(buffer);

        T value = *it;
        _d(value);

        i++;
    }

}
