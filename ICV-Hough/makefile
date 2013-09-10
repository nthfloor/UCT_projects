JFLAGS = -d -g
JC = javac
SRC_DIR=src/
BIN_DIR=bin/

.SUFFIXES: .java .class
# .java.class:
# 	$(JC) $(JFLAGS) $(BIN_DIR) $(SRC_DIR)$*.java

defualt:
	javac -d bin/ src/*.java
	@echo "Project compiled."

clean:
	$(RM) bin/*.class
	@echo "Project cleaned."

run:
	cd bin/; java runner

run_jar:
	java -jar ICV-hough-runnable.jar

crun:
	make clean; make; make run
