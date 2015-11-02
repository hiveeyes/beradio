==================================
Arduino convenient C++ programming
==================================

About
=====
The ATmega328_ has 32 KB ISP flash memory and 2 KB SRAM.

.. _ATmega328: https://en.wikipedia.org/wiki/ATmega328


Tech
====

Variable-Length Argument Lists
------------------------------
- http://c-faq.com/varargs/
- http://en.cppreference.com/w/cpp/utility/variadic
- https://www.eskimo.com/~scs/cclass/int/sx11b.html
- https://stackoverflow.com/questions/1657883/variable-number-of-arguments-in-c
- https://stackoverflow.com/questions/16337459/undefined-number-of-arguments
- http://www.varesano.net/blog/fabio/functions-variable-lenght-arguments-arduino
- http://www.cprogramming.com/tutorial/c/lesson17.html

initializer_list
................
- http://coliru.stacked-crooked.com/a/84c7739d7d7e03cc


Standard Template Library
-------------------------
Our pick
........
- | The Standard Template Library (STL) for AVR with C++ streams
  | Version 1.1.1 (most recent as of 2015-11-01)
  | http://andybrown.me.uk/2011/01/15/the-standard-template-library-stl-for-avr-with-c-streams/
  | https://drive.google.com/uc?export=download&id=0B9Zobp2aWUKzb2xvZ0Y2VGd1RTQ

Other choices
.............
- http://hackaday.com/2012/10/22/giving-the-arduino-deques-vectors-and-streams-with-the-standard-template-library/
- https://github.com/maniacbug/StandardCplusplus
- https://andybrown.me.uk/2011/01/15/the-standard-template-library-stl-for-avr-with-c-streams/
- https://arduino.stackexchange.com/questions/9835/problem-with-declaring-2d-vector-in-arduino
- https://msharov.github.io/ustl/
- http://cxx.uclibc.org/


Using the "Vector" container object
-----------------------------------
- https://github.com/maniacbug/StandardCplusplus/blob/master/vector
- https://github.com/maniacbug/StandardCplusplus/blob/master/vector.cpp
- | Topic: container for Objects like c++ vector?
  | https://stackoverflow.com/questions/9986591/vectors-in-arduino
- http://forum.arduino.cc/index.php/topic,45626.0.html
- | LinkedList for Arduino
  | https://gist.github.com/obedrios/2957439


Memory profiling
----------------
- http://andybrown.me.uk/2011/01/01/debugging-avr-dynamic-memory-allocation/


Simulation
==========
- http://www.nongnu.org/simulavr/
- https://github.com/Traumflug/simulavr
