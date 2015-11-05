/* -*- coding: utf-8 -*-
 * (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
 * (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
 */
#include <beradio.h>

int main() {

    // message object with nodeid=999
    BERadioMessage message(999);

    // enable debugging
    message.debug(true);

    // collect some measurements
    FloatList temperature = collect(21.63, 19.25, 10.92, 13.54);
    FloatList humidity    = collect(488.0, 572.0);
    FloatList weight      = collect(106.77);

    // transfer measurements to message
    message.temperature(temperature);
    //message.add("t", temperature);

    std::string payload = message.encode();
    _l("payload: ");
    _d(payload);

    IntegerList something = collect(1, 2, 3);
    message.something(something);
    // send message
    //message.send();

    return 0;
}
