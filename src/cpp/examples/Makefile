# -*- coding: utf-8 -*-
# (c) 2015 Richard Pobering <einsiedlerkrebs@netfrag.org>
# (c) 2015 Andreas Motl, Elmyra UG <andreas.motl@elmyra.de>
#
# ==========================================
#  Minimal Makefile for producing firmwares
#  and running them in simulavr.
#  See README.rst
# ==========================================


# ------------------------------------------
#    configure which program to compile
#    remark: can be overwritten from
#            command line
# ------------------------------------------
name     := simple_message
more     := ../libberadio/beradio.cpp ../libberadio/simulavr.cpp


# ------------------------------------------
#           configuration options
# ------------------------------------------
#compiler := /opt/local/bin/avr-gcc
compiler := /opt/local/bin/avr-g++
#compiler := /usr/share/arduino/hardware/tools/avr/bin/avr-gcc
cppflags := -ffunction-sections -fdata-sections -g -Os -w -fno-exceptions -std=c++11
# remark: -std=c++11 gives nice iterator convenience, but adds another 1860 bytes
cppflags_avr := -mmcu=atmega328p -DF_CPU=8000000L -DARDUINO=105 #-DSIMULAVR=$(sim)

define INCLUDE
		-I/opt/local/avr/include \
		-I/Applications/Arduino.app/Contents/Resources/Java/hardware/arduino/cores/arduino \
		-I/Applications/Arduino.app/Contents/Resources/Java/hardware/arduino/variants/standard \
		-I/Users/amo/dev/foss/open.nshare.de/beradio/tmp/avr-stl/include \
		-I/Users/amo/dev/foss/open.nshare.de/beradio/tmp/embencode \
		-I../libberadio
endef

simulavr          := /Users/amo/dev/foss/open.nshare.de/simulavr/src/simulavr
simulavr_options  := --verbose --cpufrequency 8000000 --device atmega328
simulavr_hook     := --terminate=exit --writetopipe=0x91,- --writetoabort=0x95 --writetoexit=0x96



# ------------------------------------------
#                compilation
# ------------------------------------------
source   := $(name).cpp
elf      := $(name).elf
hex      := $(name).hex

build: elf hex

hex:
	avr-objcopy -O ihex -R .eeprom $(elf) $(hex)

elf:
	@echo ------------------------------------------
	@echo   Compiling \"$(name)\”
	@echo ------------------------------------------
	$(compiler) $(cppflags) $(cppflags_avr) $(cppflags_more) $(INCLUDE) -o $(elf) $(source) $(more)

clean:
	rm $(elf) $(hex)

clean-all:
	rm *.elf *.hex


# ------------------------------------------
#                simulation
# ------------------------------------------
sim:
	$(MAKE) build cppflags_more=-DSIMULAVR=true
	@echo ------------------------------------------
	@echo   Simulating \"$(name)\"
	@echo ------------------------------------------
	# http://www.nongnu.org/simulavr/intro.html
	$(simulavr) $(simulavr_options) $(simulavr_hook) --file $(elf)


sim-all:
	$(MAKE) sim name=simple_message
