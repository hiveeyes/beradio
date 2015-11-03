/* -*- coding: utf-8 -*-
 * (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
 * (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
 */
#include <beradio.h>

#define list std::vector<double>

int main() {

    // message object
    BERadioMessage message(999);

    // enable debugging
    message.debug(true);

    // collect some measurements
    list temperature = measure(collect, 21.63, 19.25, 10.92, 13.54);
    list humidity    = measure(collect, 488.0, 572.0);
    list weight      = measure(collect, 106.77);

    // transfer measurements to message
    message.temperature(temperature);
    //message.add("t", temperature);

    // send message
    //message.send();

    return 0;
}
