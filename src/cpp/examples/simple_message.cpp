/* -*- coding: utf-8 -*-
 * (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
 * (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
 */
#include <beradio.h>

int main() {

    // message object
    BERadioMessage message(999);

    // enable debugging
    message.debug(true);

    // transfer measurements to message
    measure(message.temperature, 21.63, 19.25, 10.92, 13.54);

    // send message
    //message.send();

    return 0;
}
