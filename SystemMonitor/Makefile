# Makefile to compile java files when necessary

JAVAC = /usr/bin/javac
SOURCE=Runner.java MainWindow.java RefreshData.java CPUChecker.java MemoryChecker.java Process.java ProcessChecker.java UptimeChecker.java LoadAvgChecker.java CPUusageChecker.java

#default build rule
.SUFFIXES: .java .class

.java.class:
	$(JAVAC) -g -source 1.6 $<

Runner.class: MainWindow.class Runner.java

MainWindow.class: CPUChecker.class CPUusageChecker.class LoadAvgChecker.class ProcessChecker.class MemoryChecker.class RefreshData.class UptimeChecker.class MainWindow.java

ProcessChecker.class: RefreshData.class Process.class ProcessChecker.java

UptimeChecker.class: RefreshData.class UptimeChecker.java

CPUusageChecker.class: RefreshData.class CPUusageChecker.java

LoadAvgChecker.class: RefreshData.class LoadAvgChecker.java

MemoryChecker.class: RefreshData.class MemoryChecker.java

Process.class: Process.java

RefreshData.class: RefreshData.java

CPUChecker.class: CPUChecker.java

#explicit rules

clean:
	@rm -f $(SOURCE:.java=.class)
	@rm *.class

run:
	@java Runner

buildnew:
	@make clean; make; make run
