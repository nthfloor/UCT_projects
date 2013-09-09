//interface class used for the model-view-controller design of the program
//used to minimise lag on the GUI by sending signals to GUI class indicating when ready to refresh window
//Nathan Floor
//FLRNAT001

public interface RefreshData {	
	public void updateProcess();
	public void updateLoadAvg();
	public void updateMemory();
	public void updateUptime();
	public void updateCPUUsage(CPUusageChecker usage);
}
