include CommonDefs.mak

BIN_DIR = ../Bin

INC_DIRS = \
	. \
	../Common \
	../../Include \
	/usr/include/GL\
        /usr/include/openni2

SRC_FILES = *.cpp

ifeq ("$(OSTYPE)","Darwin")
	CFLAGS += -DMACOS -std=c++11
	LDFLAGS += -framework OpenGL -framework GLUT
else
	CFLAGS += -DUNIX -DGLX_GLXEXT_LEGACY -std=c++11
	USED_LIBS += glut GL
endif

LIB_DIRS += $(OPENNI2_REDIST) ../Bin

USED_LIBS += OpenNI2 NiTE2

EXE_NAME = MyUserViewer

CFLAGS += -Wall

include CommonCppMakefile
